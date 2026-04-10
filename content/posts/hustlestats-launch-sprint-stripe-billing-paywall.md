+++
title = 'HustleStats Launch Sprint: From Firebase Auth to Production SaaS with Stripe Billing in One Day'
slug = 'hustlestats-launch-sprint-stripe-billing-paywall'
date = 2025-11-16T10:00:00-06:00
draft = false
tags = ["stripe", "billing", "firebase", "firestore", "rbac", "saas", "hustlestats", "webhooks"]
categories = ["Technical Deep-Dive"]
description = "33 commits across 4 phases: Prisma removal, Stripe pricing with 4 tiers, workspace guards with RBAC, and global paywall enforcement with plan-limit warnings. From authenticated app to production SaaS in a single day."
+++

## The Starting Point

Yesterday ended with 7 dashboard pages running on Firebase Auth. The app could authenticate users and display their data. What it couldn't do: charge money, enforce plan limits, or prevent free users from accessing paid features.

Today's goal: ship a complete billing system. Not "billing someday" — billing today, with Stripe checkout, webhooks, plan enforcement, and a customer portal.

33 commits. Four phases.

## Phase 4: Final Prisma Cleanup

Before adding anything new, the last traces of PostgreSQL needed to go.

A migration script walked the remaining Prisma-to-Firestore data transformations. User preferences, notification settings, and feature flags that had been stored in PostgreSQL columns were restructured as Firestore document fields. The script ran idempotently — safe to run multiple times without duplicating data.

After the script completed:
- Removed `prisma` from `package.json` scripts
- Deleted the `DATABASE_URL` environment variable from all deployment configs
- Removed the PostgreSQL health check from the CI pipeline
- Archived the NextAuth configuration in a `_deprecated/` directory (kept for 30 days, then deleted)

Clean slate. No database dependencies except Firebase.

## Phase 5: Stripe Pricing and Checkout

Four pricing tiers, each with hard limits:

| Tier | Price | Players | Games/Month |
|------|-------|---------|-------------|
| **Free** | $0 | 1 | 5 |
| **Starter** | $9/mo | 3 | 20 |
| **Pro** | $29/mo | 10 | 200 |
| **Elite** | $49/mo | Unlimited | Unlimited |

The limits reflect how youth sports coaches actually use the app. A parent tracking one kid's baseball season needs Free. A rec league coach with 3 players needs Starter. A travel ball coach running full rosters needs Pro. An organization managing multiple teams needs Elite.

### The Workspace Model

Every user gets a workspace. The workspace stores the active plan, billing status, Stripe customer ID, and current usage counts. Plan limits are enforced against the workspace, not the user — this keeps the billing boundary clean if multi-user workspaces are added later.

```typescript
interface Workspace {
  id: string;
  ownerId: string;
  plan: 'free' | 'starter' | 'pro' | 'elite';
  status: 'active' | 'past_due' | 'canceled' | 'trialing';
  stripeCustomerId: string | null;
  stripeSubscriptionId: string | null;
  currentPeriodEnd: Timestamp | null;
  playerCount: number;
  gamesThisMonth: number;
  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

### Checkout Flow

Stripe Checkout handles the payment UI. The app creates a Checkout Session with the selected price, redirects to Stripe's hosted page, and handles the redirect back with a success or cancel URL.

```typescript
const session = await stripe.checkout.sessions.create({
  customer: workspace.stripeCustomerId,
  mode: 'subscription',
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${baseUrl}/dashboard/billing?success=true`,
  cancel_url: `${baseUrl}/dashboard/billing?canceled=true`,
  metadata: { workspaceId: workspace.id },
});
```

The `metadata.workspaceId` is critical. When the webhook fires, it carries this metadata, which maps the Stripe event back to the correct workspace in Firestore.

### Webhook Handler

Five Stripe events, one handler each:

1. `checkout.session.completed` — creates/updates workspace billing fields
2. `customer.subscription.updated` — plan changes, status changes
3. `customer.subscription.deleted` — cancellations
4. `invoice.payment_succeeded` — resets `gamesThisMonth` counter on new billing period
5. `invoice.payment_failed` — sets workspace status to `past_due`

Each handler extracts the workspace ID from Stripe metadata and updates Firestore. The pattern is consistent: read current workspace state, compute the delta, write the update, record a billing ledger event.

Smoke tests verified: create checkout session, complete payment (Stripe test mode), webhook fires, workspace plan updates, user sees new plan in dashboard. End-to-end in under 5 seconds.

## Phase 6: Workspace Guards, Billing UI, and RBAC

### Workspace Guards

Every write operation checks plan limits before executing:

```typescript
async function guardPlayerCreation(workspaceId: string): Promise<void> {
  const workspace = await getWorkspace(workspaceId);
  const limits = PLAN_LIMITS[workspace.plan];

  if (workspace.playerCount >= limits.maxPlayers) {
    throw new PlanLimitError(
      `${workspace.plan} plan allows ${limits.maxPlayers} players. ` +
      `You have ${workspace.playerCount}. Upgrade to add more.`
    );
  }
}

async function guardGameCreation(workspaceId: string): Promise<void> {
  const workspace = await getWorkspace(workspaceId);
  const limits = PLAN_LIMITS[workspace.plan];

  if (workspace.gamesThisMonth >= limits.maxGamesPerMonth) {
    throw new PlanLimitError(
      `${workspace.plan} plan allows ${limits.maxGamesPerMonth} games/month. ` +
      `You've used ${workspace.gamesThisMonth}. Upgrade or wait for next billing cycle.`
    );
  }
}
```

Guards run before the Firestore write. If the limit is exceeded, the write never happens and the user sees the upgrade prompt.

### Billing Page

A dedicated `/dashboard/billing` page shows:
- Current plan and status
- Usage vs. limits (players used / max, games used / max)
- Plan comparison table
- Upgrade/downgrade buttons
- Invoice history (pulled from Stripe API)

### Email Notifications

Transactional emails via Resend for three billing events:
- Welcome email on first subscription
- Payment failure warning (with link to update payment method)
- Plan change confirmation

### Firebase Storage for Photos

Player profile photos moved to Firebase Storage. Each photo is stored at `users/{uid}/players/{pid}/photo.{ext}` with a signed URL for display. The security rule mirrors the Firestore hierarchy — users can only upload to their own path.

### RBAC Foundation

Role-based access control at the workspace level. Two roles for now:

- **Owner** — full access, billing management, member invites
- **Member** — read/write players and games, no billing access

Roles are stored on the workspace document. The RBAC check runs after auth verification but before any data operation.

## Phase 7: Global Paywall Enforcement

This is where the billing system becomes a real paywall, not just advisory limits.

### Subscription Middleware

Global Next.js middleware checks subscription status on every dashboard route:

```typescript
// middleware.ts (extended)
export async function middleware(request: NextRequest) {
  // Layer 1: Auth check (existing)
  const session = request.cookies.get('session');
  if (!session) return NextResponse.redirect(new URL('/login', request.url));

  // Layer 2: Subscription check (new)
  const workspace = await getWorkspaceFromToken(session.value);
  if (workspace.status === 'canceled' && isPaidRoute(request.nextUrl.pathname)) {
    return NextResponse.redirect(new URL('/dashboard/billing', request.url));
  }

  return NextResponse.next();
}
```

Canceled subscriptions can still view their data (read routes) but cannot create or modify data (write routes). This preserves the user experience — they don't lose access to historical stats, they just can't add new ones until they resubscribe.

### useWorkspaceAccess Hook

A React hook that provides plan-aware state to every component:

```typescript
function useWorkspaceAccess() {
  const { workspace } = useWorkspace();
  const limits = PLAN_LIMITS[workspace.plan];

  return {
    canAddPlayer: workspace.playerCount < limits.maxPlayers,
    canAddGame: workspace.gamesThisMonth < limits.maxGamesPerMonth,
    playerUsagePercent: (workspace.playerCount / limits.maxPlayers) * 100,
    gameUsagePercent: (workspace.gamesThisMonth / limits.maxGamesPerMonth) * 100,
    isAtLimit: workspace.playerCount >= limits.maxPlayers,
    isNearLimit: workspace.playerCount >= limits.maxPlayers * 0.8,
  };
}
```

Components use `canAddPlayer` to disable buttons. The `isNearLimit` flag triggers warning UI before the hard limit hits.

### PaywallNotice and Customer Portal

A `PaywallNotice` component replaces generic error messages when users hit plan limits. It shows the current limit, what the next tier offers, and a direct link to the billing page.

Color thresholds make limits visible before they hit: green (0-79%), yellow (80-99% with a nav badge), red (100% with disabled buttons and the PaywallNotice).

Self-service plan management runs through Stripe's hosted customer portal. Users update payment methods, view invoices, change plans, and cancel without any custom billing UI to maintain.

## What Shipped

33 commits. The app went from "Firebase Auth works" to:

- 4-tier pricing with hard limits
- Stripe Checkout + webhooks + customer portal
- Global subscription middleware
- Plan-aware UI with color-coded warnings
- RBAC foundation
- Billing page with invoice history
- Transactional emails for billing events
- Firebase Storage for player photos

The entire billing surface — from checkout to paywall to self-service management — was built and tested in one day.

## The Workspace Pattern

The workspace abstraction was the key architectural decision. By putting billing state on the workspace instead of the user, the system supports:

- Multi-user workspaces (future: coaches sharing a team roster)
- Clean billing boundaries (one subscription per workspace)
- Plan enforcement at the data level, not the auth level
- Usage tracking independent of who performed the action

Every SaaS I've built ends up needing a workspace or organization entity. Starting with it from day one avoided the painful retrofit.

---

**Related Posts:**

- [Building an Idempotent Stripe Billing Enforcement Engine for Firestore](/posts/building-idempotent-stripe-billing-enforcement-firestore/) — The plan enforcement engine that replaced the duplicate webhook logic from this sprint
- [HustleStats Firebase Auth Cutover: 7 Dashboard Pages, 3-Layer Defense](/posts/hustlestats-firebase-auth-cutover-seven-pages/) — Yesterday's auth cutover that set the stage for billing
- [Session Cookie Auth, Forgot-Password Timeouts, and Killing Flaky E2E Tests](/posts/session-cookies-forgot-password-flaky-e2e-tests/) — Firebase session management patterns used in the paywall middleware
