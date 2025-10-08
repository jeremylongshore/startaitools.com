<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0c243c6189393ed7468e470ef2090049",
  "translation_date": "2025-08-18T11:00:41+00:00",
  "source_file": "02-Security/mcp-security-controls-2025.md",
  "language_code": "fr"
}
-->
# Contrôles de sécurité MCP - Mise à jour d'août 2025

> **Norme actuelle** : Ce document reflète les exigences de sécurité de la [Spécification MCP 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) et les [Bonnes pratiques de sécurité MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) officielles.

Le protocole Model Context Protocol (MCP) a considérablement évolué avec des contrôles de sécurité renforcés, répondant aux menaces traditionnelles en matière de sécurité logicielle ainsi qu'aux risques spécifiques à l'IA. Ce document fournit des contrôles de sécurité complets pour des implémentations MCP sécurisées à partir d'août 2025.

## **Exigences de sécurité OBLIGATOIRES**

### **Interdictions critiques de la spécification MCP :**

> **INTERDIT** : Les serveurs MCP **NE DOIVENT PAS** accepter de jetons qui n'ont pas été explicitement émis pour le serveur MCP  
>
> **PROHIBÉ** : Les serveurs MCP **NE DOIVENT PAS** utiliser de sessions pour l'authentification  
>
> **OBLIGATOIRE** : Les serveurs MCP mettant en œuvre une autorisation **DOIVENT** vérifier TOUTES les requêtes entrantes  
>
> **MANDATÉ** : Les serveurs proxy MCP utilisant des identifiants clients statiques **DOIVENT** obtenir le consentement de l'utilisateur pour chaque client enregistré dynamiquement  

---

## 1. **Contrôles d'authentification et d'autorisation**

### **Intégration avec des fournisseurs d'identité externes**

La **norme actuelle MCP (2025-06-18)** permet aux serveurs MCP de déléguer l'authentification à des fournisseurs d'identité externes, représentant une amélioration significative de la sécurité :

**Avantages de sécurité :**
1. **Élimination des risques liés à l'authentification personnalisée** : Réduit la surface de vulnérabilité en évitant les implémentations d'authentification sur mesure  
2. **Sécurité de niveau entreprise** : Exploite des fournisseurs d'identité établis comme Microsoft Entra ID avec des fonctionnalités de sécurité avancées  
3. **Gestion centralisée des identités** : Simplifie la gestion du cycle de vie des utilisateurs, le contrôle d'accès et les audits de conformité  
4. **Authentification multi-facteurs** : Hérite des capacités MFA des fournisseurs d'identité d'entreprise  
5. **Politiques d'accès conditionnel** : Bénéficie de contrôles d'accès basés sur les risques et d'une authentification adaptative  

**Exigences d'implémentation :**
- **Validation de l'audience des jetons** : Vérifiez que tous les jetons sont explicitement émis pour le serveur MCP  
- **Vérification de l'émetteur** : Validez que l'émetteur du jeton correspond au fournisseur d'identité attendu  
- **Vérification de la signature** : Validation cryptographique de l'intégrité des jetons  
- **Application des dates d'expiration** : Respect strict des limites de durée de vie des jetons  
- **Validation des portées** : Assurez-vous que les jetons contiennent les permissions appropriées pour les opérations demandées  

### **Sécurité de la logique d'autorisation**

**Contrôles critiques :**
- **Audits complets de l'autorisation** : Revues régulières de sécurité de tous les points de décision d'autorisation  
- **Défauts sécurisés** : Refusez l'accès lorsque la logique d'autorisation ne peut pas prendre de décision définitive  
- **Limites de permissions** : Séparation claire entre les différents niveaux de privilèges et l'accès aux ressources  
- **Journalisation des audits** : Enregistrement complet de toutes les décisions d'autorisation pour la surveillance de la sécurité  
- **Revue régulière des accès** : Validation périodique des permissions des utilisateurs et des attributions de privilèges  

## 2. **Sécurité des jetons et contrôles anti-transmission**

### **Prévention de la transmission des jetons**

**La transmission des jetons est explicitement interdite** dans la spécification d'autorisation MCP en raison de risques de sécurité critiques :

**Risques de sécurité traités :**
- **Contournement des contrôles** : Évite les contrôles de sécurité essentiels tels que la limitation de débit, la validation des requêtes et la surveillance du trafic  
- **Rupture de la responsabilité** : Rend l'identification des clients impossible, corrompant les pistes d'audit et les enquêtes sur les incidents  
- **Exfiltration via proxy** : Permet aux acteurs malveillants d'utiliser les serveurs comme proxys pour accéder à des données non autorisées  
- **Violations des frontières de confiance** : Brise les hypothèses de confiance des services en aval concernant l'origine des jetons  
- **Mouvements latéraux** : Les jetons compromis à travers plusieurs services permettent une expansion plus large des attaques  

**Contrôles d'implémentation :**
```yaml
Token Validation Requirements:
  audience_validation: MANDATORY
  issuer_verification: MANDATORY  
  signature_check: MANDATORY
  expiration_enforcement: MANDATORY
  scope_validation: MANDATORY
  
Token Lifecycle Management:
  rotation_frequency: "Short-lived tokens preferred"
  secure_storage: "Azure Key Vault or equivalent"
  transmission_security: "TLS 1.3 minimum"
  replay_protection: "Implemented via nonce/timestamp"
```

### **Modèles sécurisés de gestion des jetons**

**Bonnes pratiques :**
- **Jetons de courte durée** : Réduisez la fenêtre d'exposition avec une rotation fréquente des jetons  
- **Émission juste-à-temps** : Émettez des jetons uniquement lorsque nécessaire pour des opérations spécifiques  
- **Stockage sécurisé** : Utilisez des modules de sécurité matériels (HSM) ou des coffres-forts sécurisés  
- **Association des jetons** : Associez les jetons à des clients, sessions ou opérations spécifiques lorsque possible  
- **Surveillance et alertes** : Détection en temps réel des abus de jetons ou des modèles d'accès non autorisés  

## 3. **Contrôles de sécurité des sessions**

### **Prévention du détournement de session**

**Vecteurs d'attaque traités :**
- **Injection de prompts dans les sessions détournées** : Événements malveillants injectés dans l'état de session partagé  
- **Impersonation de session** : Utilisation non autorisée d'ID de session volés pour contourner l'authentification  
- **Attaques sur les flux repris** : Exploitation de la reprise d'événements envoyés par le serveur pour injecter du contenu malveillant  

**Contrôles obligatoires des sessions :**
```yaml
Session ID Generation:
  randomness_source: "Cryptographically secure RNG"
  entropy_bits: 128 # Minimum recommended
  format: "Base64url encoded"
  predictability: "MUST be non-deterministic"

Session Binding:
  user_binding: "REQUIRED - <user_id>:<session_id>"
  additional_identifiers: "Device fingerprint, IP validation"
  context_binding: "Request origin, user agent validation"
  
Session Lifecycle:
  expiration: "Configurable timeout policies"
  rotation: "After privilege escalation events"
  invalidation: "Immediate on security events"
  cleanup: "Automated expired session removal"
```

**Sécurité des transports :**
- **Application de HTTPS** : Toutes les communications de session via TLS 1.3  
- **Attributs sécurisés des cookies** : HttpOnly, Secure, SameSite=Strict  
- **Épinglage des certificats** : Pour les connexions critiques afin de prévenir les attaques MITM  

### **Considérations sur les sessions avec état vs sans état**

**Pour les implémentations avec état :**
- L'état de session partagé nécessite une protection supplémentaire contre les attaques par injection  
- La gestion des sessions basée sur des files d'attente nécessite une vérification de l'intégrité  
- Plusieurs instances de serveur nécessitent une synchronisation sécurisée de l'état des sessions  

**Pour les implémentations sans état :**
- Gestion des sessions basée sur JWT ou un système similaire  
- Vérification cryptographique de l'intégrité de l'état des sessions  
- Surface d'attaque réduite mais nécessite une validation robuste des jetons  

## 4. **Contrôles de sécurité spécifiques à l'IA**

### **Défense contre l'injection de prompts**

**Intégration de Microsoft Prompt Shields :**
```yaml
Detection Mechanisms:
  - "Advanced ML-based instruction detection"
  - "Contextual analysis of external content"
  - "Real-time threat pattern recognition"
  
Protection Techniques:
  - "Spotlighting trusted vs untrusted content"
  - "Delimiter systems for content boundaries"  
  - "Data marking for content source identification"
  
Integration Points:
  - "Azure Content Safety service"
  - "Real-time content filtering"
  - "Threat intelligence updates"
```

**Contrôles d'implémentation :**
- **Assainissement des entrées** : Validation et filtrage complets de toutes les entrées utilisateur  
- **Définition des limites de contenu** : Séparation claire entre les instructions système et le contenu utilisateur  
- **Hiérarchie des instructions** : Règles de priorité appropriées pour les instructions conflictuelles  
- **Surveillance des sorties** : Détection des sorties potentiellement nuisibles ou manipulées  

### **Prévention de l'empoisonnement des outils**

**Cadre de sécurité des outils :**
```yaml
Tool Definition Protection:
  validation:
    - "Schema validation against expected formats"
    - "Content analysis for malicious instructions" 
    - "Parameter injection detection"
    - "Hidden instruction identification"
  
  integrity_verification:
    - "Cryptographic hashing of tool definitions"
    - "Digital signatures for tool packages"
    - "Version control with change auditing"
    - "Tamper detection mechanisms"
  
  monitoring:
    - "Real-time change detection"
    - "Behavioral analysis of tool usage"
    - "Anomaly detection for execution patterns"
    - "Automated alerting for suspicious modifications"
```

**Gestion dynamique des outils :**
- **Flux de travail d'approbation** : Consentement explicite de l'utilisateur pour les modifications des outils  
- **Capacités de retour en arrière** : Possibilité de revenir aux versions précédentes des outils  
- **Audit des modifications** : Historique complet des modifications des définitions des outils  
- **Évaluation des risques** : Évaluation automatisée de la posture de sécurité des outils  

## 5. **Prévention des attaques de type "Confused Deputy"**

### **Sécurité des proxys OAuth**

**Contrôles de prévention des attaques :**
```yaml
Client Registration:
  static_client_protection:
    - "Explicit user consent for dynamic registration"
    - "Consent bypass prevention mechanisms"  
    - "Cookie-based consent validation"
    - "Redirect URI strict validation"
    
  authorization_flow:
    - "PKCE implementation (OAuth 2.1)"
    - "State parameter validation"
    - "Authorization code binding"
    - "Nonce verification for ID tokens"
```

**Exigences d'implémentation :**
- **Vérification du consentement de l'utilisateur** : Ne jamais ignorer les écrans de consentement pour l'enregistrement dynamique des clients  
- **Validation des URI de redirection** : Validation stricte basée sur une liste blanche des destinations de redirection  
- **Protection des codes d'autorisation** : Codes de courte durée avec application d'une utilisation unique  
- **Vérification de l'identité des clients** : Validation robuste des identifiants et métadonnées des clients  

## 6. **Sécurité de l'exécution des outils**

### **Isolation et confinement**

**Isolation basée sur des conteneurs :**
```yaml
Execution Environment:
  containerization: "Docker/Podman with security profiles"
  resource_limits:
    cpu: "Configurable CPU quotas"
    memory: "Memory usage restrictions"
    disk: "Storage access limitations"
    network: "Network policy enforcement"
  
  privilege_restrictions:
    user_context: "Non-root execution mandatory"
    capability_dropping: "Remove unnecessary Linux capabilities"
    syscall_filtering: "Seccomp profiles for syscall restriction"
    filesystem: "Read-only root with minimal writable areas"
```

**Isolation des processus :**
- **Contexte de processus séparé** : Chaque exécution d'outil dans un espace de processus isolé  
- **Communication inter-processus** : Mécanismes IPC sécurisés avec validation  
- **Surveillance des processus** : Analyse du comportement en temps réel et détection des anomalies  
- **Application des ressources** : Limites strictes sur le CPU, la mémoire et les opérations d'E/S  

### **Mise en œuvre du principe du moindre privilège**

**Gestion des permissions :**
```yaml
Access Control:
  file_system:
    - "Minimal required directory access"
    - "Read-only access where possible"
    - "Temporary file cleanup automation"
    
  network_access:
    - "Explicit allowlist for external connections"
    - "DNS resolution restrictions" 
    - "Port access limitations"
    - "SSL/TLS certificate validation"
  
  system_resources:
    - "No administrative privilege elevation"
    - "Limited system call access"
    - "No hardware device access"
    - "Restricted environment variable access"
```

## 7. **Contrôles de sécurité de la chaîne d'approvisionnement**

### **Vérification des dépendances**

**Sécurité complète des composants :**
```yaml
Software Dependencies:
  scanning: 
    - "Automated vulnerability scanning (GitHub Advanced Security)"
    - "License compliance verification"
    - "Known vulnerability database checks"
    - "Malware detection and analysis"
  
  verification:
    - "Package signature verification"
    - "Checksum validation"
    - "Provenance attestation"
    - "Software Bill of Materials (SBOM)"

AI Components:
  model_verification:
    - "Model provenance validation"
    - "Training data source verification" 
    - "Model behavior testing"
    - "Adversarial robustness assessment"
  
  service_validation:
    - "Third-party API security assessment"
    - "Service level agreement review"
    - "Data handling compliance verification"
    - "Incident response capability evaluation"
```

### **Surveillance continue**

**Détection des menaces dans la chaîne d'approvisionnement :**
- **Surveillance de la santé des dépendances** : Évaluation continue de toutes les dépendances pour les problèmes de sécurité  
- **Intégration de renseignements sur les menaces** : Mises à jour en temps réel sur les menaces émergentes dans la chaîne d'approvisionnement  
- **Analyse comportementale** : Détection des comportements inhabituels dans les composants externes  
- **Réponse automatisée** : Containment immédiat des composants compromis  

## 8. **Contrôles de surveillance et de détection**

### **Gestion des informations et des événements de sécurité (SIEM)**

**Stratégie complète de journalisation :**
```yaml
Authentication Events:
  - "All authentication attempts (success/failure)"
  - "Token issuance and validation events"
  - "Session creation, modification, termination"
  - "Authorization decisions and policy evaluations"

Tool Execution:
  - "Tool invocation details and parameters"
  - "Execution duration and resource usage"
  - "Output generation and content analysis"
  - "Error conditions and exception handling"

Security Events:
  - "Potential prompt injection attempts"
  - "Tool poisoning detection events"
  - "Session hijacking indicators"
  - "Unusual access patterns and anomalies"
```

### **Détection des menaces en temps réel**

**Analytique comportementale :**
- **Analytique du comportement des utilisateurs (UBA)** : Détection des modèles d'accès utilisateur inhabituels  
- **Analytique du comportement des entités (EBA)** : Surveillance du comportement des serveurs MCP et des outils  
- **Détection des anomalies par apprentissage automatique** : Identification des menaces de sécurité alimentée par l'IA  
- **Corrélation des renseignements sur les menaces** : Correspondance des activités observées avec des modèles d'attaque connus  

## 9. **Réponse aux incidents et reprise**

### **Capacités de réponse automatisée**

**Actions de réponse immédiate :**
```yaml
Threat Containment:
  session_management:
    - "Immediate session termination"
    - "Account lockout procedures"
    - "Access privilege revocation"
  
  system_isolation:
    - "Network segmentation activation"
    - "Service isolation protocols"
    - "Communication channel restriction"

Recovery Procedures:
  credential_rotation:
    - "Automated token refresh"
    - "API key regeneration"
    - "Certificate renewal"
  
  system_restoration:
    - "Clean state restoration"
    - "Configuration rollback"
    - "Service restart procedures"
```

### **Capacités d'investigation**

**Support d'enquête :**
- **Préservation des pistes d'audit** : Journalisation immuable avec intégrité cryptographique  
- **Collecte de preuves** : Collecte automatisée des artefacts de sécurité pertinents  
- **Reconstruction de la chronologie** : Séquence détaillée des événements menant aux incidents de sécurité  
- **Évaluation des impacts** : Évaluation de l'étendue de la compromission et de l'exposition des données  

## **Principes clés de l'architecture de sécurité**

### **Défense en profondeur**
- **Couches de sécurité multiples** : Aucun point de défaillance unique dans l'architecture de sécurité  
- **Contrôles redondants** : Mesures de sécurité superposées pour les fonctions critiques  
- **Mécanismes de secours** : Défauts sécurisés lorsque les systèmes rencontrent des erreurs ou des attaques  

### **Mise en œuvre du Zero Trust**
- **Ne jamais faire confiance, toujours vérifier** : Validation continue de toutes les entités et requêtes  
- **Principe du moindre privilège** : Droits d'accès minimaux pour tous les composants  
- **Micro-segmentation** : Contrôles granulaires du réseau et des accès  

### **Évolution continue de la sécurité**
- **Adaptation au paysage des menaces** : Mises à jour régulières pour répondre aux menaces émergentes  
- **Efficacité des contrôles de sécurité** : Évaluation et amélioration continues des contrôles  
- **Conformité aux spécifications** : Alignement avec les normes de sécurité MCP en évolution  

---

## **Ressources d'implémentation**

### **Documentation officielle MCP**
- [Spécification MCP (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [Bonnes pratiques de sécurité MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [Spécification d'autorisation MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **Solutions de sécurité Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)  

### **Normes de sécurité**
- [Bonnes pratiques de sécurité OAuth 2.0 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 pour les modèles de langage étendu](https://genai.owasp.org/)  
- [Cadre de cybersécurité NIST](https://www.nist.gov/cyberframework)  

---

> **Important** : Ces contrôles de sécurité reflètent la spécification MCP actuelle (2025-06-18). Vérifiez toujours les [documents officiels](https://spec.modelcontextprotocol.io/) car les normes évoluent rapidement.

**Avertissement** :  
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue d'origine doit être considéré comme la source faisant autorité. Pour des informations critiques, il est recommandé de faire appel à une traduction humaine professionnelle. Nous déclinons toute responsabilité en cas de malentendus ou d'interprétations erronées résultant de l'utilisation de cette traduction.