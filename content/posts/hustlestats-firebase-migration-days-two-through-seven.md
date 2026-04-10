+++
title = 'HustleStats Firebase Migration Days 2-7: Schema, Auth Swap, Data Port, and the Cost Cliff'
slug = 'hustlestats-firebase-migration-days-two-through-seven'
date = 2025-11-11T10:00:00-06:00
draft = false
tags = ["firebase", "firestore", "authentication", "migration", "typescript", "hustlestats"]
categories = ["Development Journey"]
description = "Six days of Firebase migration in four commits: Firestore subcollection hierarchy, Firebase Auth replacing NextAuth, a 58-user data port with lazy password migration, and monthly costs dropping from $20-30 to $0-10."
+++

Six days. Four commits. The entire HustleStats backend moved from PostgreSQL + NextAuth to Firebase.

## Day 2: Firestore Schema

The Firestore subcollection hierarchy follows the access pattern:

```
users/{uid}
  └── players/{pid}
        └── games/{gid}
```

Every query starts with a user. Players belong to a user. Games belong to a player. The hierarchy means security rules can enforce ownership at every level without extra lookups. A read to `users/abc/players/xyz/games/123` already proves the caller owns the path.

TypeScript types mirror the hierarchy. Each collection has a create type (what goes in), a document type (what comes out with Firestore metadata), and a CRUD service that wraps the Firestore SDK with typed inputs and outputs.

```typescript
interface Player {
  id: string;
  name: string;
  position: string;
  jerseyNumber: number;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}

// CRUD service wraps Firestore SDK
async function createPlayer(uid: string, data: CreatePlayerInput): Promise<Player> {
  const ref = doc(collection(db, `users/${uid}/players`));
  const player = { ...data, id: ref.id, createdAt: serverTimestamp(), updatedAt: serverTimestamp() };
  await setDoc(ref, player);
  return player;
}
```

Three services total: users, players, games. Each service handles its own subcollection path. No raw Firestore calls anywhere else in the app.

## Day 3: Auth Swap

NextAuth was ripped out entirely. Firebase Auth replaced it with four functions and one hook:

- `signUp` — email/password creation, writes user doc to Firestore
- `signIn` — email/password, returns Firebase user
- `signOut` — clears auth state
- `resetPassword` — sends Firebase reset email
- `useAuth` — React hook that subscribes to `onAuthStateChanged`

The `useAuth` hook is the only auth surface the rest of the app touches. Components check `user` for authenticated state. No more NextAuth session callbacks, no JWT rotation logic, no adapter configuration. Firebase handles token refresh internally.

```typescript
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    return onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      setLoading(false);
    });
  }, []);

  return { user, loading };
}
```

Every NextAuth import was deleted. Every `getServerSession` call was replaced. The entire auth surface reduced from ~400 lines to ~120.

## Day 4: Data Migration

58 users needed to move from PostgreSQL to Firestore. The migration script:

1. Reads all users from PostgreSQL
2. Creates Firebase Auth accounts with the same email
3. Writes user documents to `users/{uid}` with all profile data
4. Migrates player and game records into subcollections

The password problem: PostgreSQL stored bcrypt hashes. Firebase Auth uses scrypt internally. These hash algorithms are incompatible — you cannot import a bcrypt hash into Firebase Auth's scrypt-based system.

The solution was lazy password migration. Every migrated user gets a temporary random password. On first login attempt, the app catches the auth failure, prompts a password reset, and Firebase Auth handles the new password with its own hashing. Users reset once and never deal with it again.

58 users migrated. Zero data loss. The PostgreSQL database was kept read-only for 30 days as a safety net before deletion.

Workspace cleanup: removed all Prisma files, deleted the `prisma/` directory, uninstalled `@prisma/client` and `prisma` packages, removed the PostgreSQL connection string from environment variables.

## Days 5-7: Production Readiness

Password reset flow: Firebase's `sendPasswordResetEmail` sends a branded email with a reset link. The link redirects back to a custom `/reset-password` page that calls `confirmPasswordReset`. No custom email infrastructure needed.

Login page: rebuilt with Firebase Auth error handling. Firebase returns specific error codes (`auth/user-not-found`, `auth/wrong-password`, `auth/too-many-requests`) that map directly to user-facing messages.

Deployment guides: documented the Firebase project setup, service account creation, environment variables, and Firestore security rules deployment. Rollback procedures in case the migration needed to be reversed — switch `NEXT_PUBLIC_AUTH_PROVIDER` back to `nextauth`, restore PostgreSQL connection string, redeploy.

## The Cost Cliff

The old stack: Vercel Pro ($20/mo) + Neon PostgreSQL ($0-10/mo depending on usage) = $20-30/month.

The new stack: Firebase Spark plan (free tier) covers all current usage. Firestore free tier: 50K reads, 20K writes, 20K deletes per day. Firebase Auth free tier: 10K authentications per month. HustleStats has 58 users. The free tier covers 100x the current load.

Estimated monthly cost after migration: **$0-10/month**, with the $10 ceiling only if usage grows 10x.

The migration wasn't motivated by cost. It was motivated by removing the PostgreSQL operational burden and simplifying the auth stack. The cost reduction was a side effect of moving to a serverless database with a generous free tier.

---

**Related Posts:**

- [HustleStats Production Auth Debugging: NextAuth, PrismaAdapter, and the Cascade](/posts/hustlestats-production-auth-debugging-nextauth-prisma/) — The auth problems that motivated this migration
- [Deployment Secrets, Missing Columns, and Sitemap Hygiene](/posts/hustlestats-defensive-schema-email-config-sitemap-cleanup/) — Earlier HustleStats maintenance that exposed the Prisma/PostgreSQL friction
- [Session Cookie Auth, Forgot-Password Timeouts, and Killing Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/) — The Firebase Auth session management that came after this migration
