<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1c767a35642f753127dc08545c25a290",
  "translation_date": "2025-08-18T10:58:24+00:00",
  "source_file": "02-Security/README.md",
  "language_code": "fr"
}
-->
# Sécurité MCP : Protection complète des systèmes d'IA

[![Meilleures pratiques de sécurité MCP](../../../translated_images/03.175aed6dedae133f9d41e49cefd0f0a9a39c3317e1eaa7ef7182696af7534308.fr.png)](https://youtu.be/88No8pw706o)

_(Cliquez sur l'image ci-dessus pour visionner la vidéo de cette leçon)_

La sécurité est essentielle dans la conception des systèmes d'IA, c'est pourquoi nous la plaçons au cœur de notre deuxième section. Cela s'aligne avec le principe **Secure by Design** de Microsoft issu de l'[Initiative pour un avenir sécurisé](https://www.microsoft.com/security/blog/2025/04/17/microsofts-secure-by-design-journey-one-year-of-success/).

Le protocole Model Context Protocol (MCP) apporte de nouvelles capacités puissantes aux applications basées sur l'IA tout en introduisant des défis de sécurité uniques qui vont au-delà des risques traditionnels des logiciels. Les systèmes MCP sont confrontés à des préoccupations de sécurité établies (codage sécurisé, privilèges minimaux, sécurité de la chaîne d'approvisionnement) ainsi qu'à de nouvelles menaces spécifiques à l'IA, notamment l'injection de prompts, l'empoisonnement des outils, le détournement de session, les attaques de type "confused deputy", les vulnérabilités de transmission de jetons et la modification dynamique des capacités.

Cette leçon explore les risques de sécurité les plus critiques dans les implémentations MCP, couvrant l'authentification, l'autorisation, les permissions excessives, l'injection indirecte de prompts, la sécurité des sessions, les problèmes de "confused deputy", la gestion des jetons et les vulnérabilités de la chaîne d'approvisionnement. Vous apprendrez des contrôles pratiques et des meilleures pratiques pour atténuer ces risques tout en utilisant des solutions Microsoft telles que Prompt Shields, Azure Content Safety et GitHub Advanced Security pour renforcer votre déploiement MCP.

## Objectifs d'apprentissage

À la fin de cette leçon, vous serez capable de :

- **Identifier les menaces spécifiques au MCP** : Reconnaître les risques uniques dans les systèmes MCP, notamment l'injection de prompts, l'empoisonnement des outils, les permissions excessives, le détournement de session, les problèmes de "confused deputy", les vulnérabilités de transmission de jetons et les risques liés à la chaîne d'approvisionnement
- **Appliquer des contrôles de sécurité** : Mettre en œuvre des mesures efficaces, notamment une authentification robuste, un accès avec privilèges minimaux, une gestion sécurisée des jetons, des contrôles de sécurité des sessions et une vérification de la chaîne d'approvisionnement
- **Utiliser les solutions de sécurité Microsoft** : Comprendre et déployer Microsoft Prompt Shields, Azure Content Safety et GitHub Advanced Security pour protéger les charges de travail MCP
- **Valider la sécurité des outils** : Reconnaître l'importance de la validation des métadonnées des outils, surveiller les modifications dynamiques et se défendre contre les attaques d'injection indirecte de prompts
- **Intégrer les meilleures pratiques** : Combiner les fondamentaux de la sécurité établis (codage sécurisé, durcissement des serveurs, zéro confiance) avec des contrôles spécifiques au MCP pour une protection complète

# Architecture et contrôles de sécurité MCP

Les implémentations modernes de MCP nécessitent des approches de sécurité en couches qui répondent à la fois aux menaces traditionnelles des logiciels et aux risques spécifiques à l'IA. La spécification MCP, en constante évolution, continue de renforcer ses contrôles de sécurité, permettant une meilleure intégration avec les architectures de sécurité d'entreprise et les meilleures pratiques établies.

Les recherches du [Microsoft Digital Defense Report](https://aka.ms/mddr) montrent que **98 % des violations signalées pourraient être évitées grâce à une hygiène de sécurité robuste**. La stratégie de protection la plus efficace combine des pratiques de sécurité fondamentales avec des contrôles spécifiques au MCP : les mesures de sécurité de base éprouvées restent les plus impactantes pour réduire les risques globaux.

## Paysage actuel de la sécurité

> **Note** : Ces informations reflètent les normes de sécurité MCP en date du **18 août 2025**. Le protocole MCP évolue rapidement, et les implémentations futures pourraient introduire de nouveaux modèles d'authentification et des contrôles améliorés. Consultez toujours la [spécification MCP actuelle](https://spec.modelcontextprotocol.io/), le [référentiel GitHub MCP](https://github.com/modelcontextprotocol) et la [documentation des meilleures pratiques de sécurité](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) pour les dernières recommandations.

### Évolution de l'authentification MCP

La spécification MCP a considérablement évolué dans son approche de l'authentification et de l'autorisation :

- **Approche initiale** : Les premières spécifications exigeaient que les développeurs implémentent des serveurs d'authentification personnalisés, les serveurs MCP agissant comme des serveurs d'autorisation OAuth 2.0 gérant directement l'authentification des utilisateurs
- **Norme actuelle (2025-06-18)** : La spécification mise à jour permet aux serveurs MCP de déléguer l'authentification à des fournisseurs d'identité externes (tels que Microsoft Entra ID), améliorant la posture de sécurité et réduisant la complexité de l'implémentation
- **Sécurité de la couche de transport** : Support renforcé pour les mécanismes de transport sécurisé avec des modèles d'authentification appropriés pour les connexions locales (STDIO) et distantes (Streamable HTTP)

## Sécurité de l'authentification et de l'autorisation

### Défis de sécurité actuels

Les implémentations modernes de MCP sont confrontées à plusieurs défis en matière d'authentification et d'autorisation :

### Risques et vecteurs de menace

- **Logique d'autorisation mal configurée** : Une implémentation défaillante de l'autorisation dans les serveurs MCP peut exposer des données sensibles et appliquer incorrectement les contrôles d'accès
- **Compromission des jetons OAuth** : Le vol de jetons de serveurs MCP locaux permet aux attaquants de se faire passer pour des serveurs et d'accéder à des services en aval
- **Vulnérabilités de transmission de jetons** : Une gestion incorrecte des jetons crée des contournements des contrôles de sécurité et des lacunes en matière de responsabilité
- **Permissions excessives** : Les serveurs MCP surpriviliégiés violent les principes de privilèges minimaux et augmentent les surfaces d'attaque

#### Transmission de jetons : un anti-modèle critique

**La transmission de jetons est explicitement interdite** dans la spécification actuelle d'autorisation MCP en raison de graves implications en matière de sécurité :

##### Contournement des contrôles de sécurité
- Les serveurs MCP et les API en aval implémentent des contrôles de sécurité critiques (limitation de débit, validation des requêtes, surveillance du trafic) qui dépendent d'une validation correcte des jetons
- L'utilisation directe de jetons client-API contourne ces protections essentielles, compromettant l'architecture de sécurité

##### Défis de responsabilité et d'audit  
- Les serveurs MCP ne peuvent pas distinguer les clients utilisant des jetons émis en amont, brisant les pistes d'audit
- Les journaux des serveurs de ressources en aval montrent des origines de requêtes trompeuses plutôt que les intermédiaires réels des serveurs MCP
- Les enquêtes sur les incidents et les audits de conformité deviennent beaucoup plus difficiles

##### Risques d'exfiltration de données
- Les revendications de jetons non validées permettent aux acteurs malveillants disposant de jetons volés d'utiliser les serveurs MCP comme des proxys pour l'exfiltration de données
- Les violations des frontières de confiance permettent des modèles d'accès non autorisés qui contournent les contrôles de sécurité prévus

##### Vecteurs d'attaque multi-services
- Les jetons compromis acceptés par plusieurs services permettent des mouvements latéraux entre les systèmes connectés
- Les hypothèses de confiance entre les services peuvent être violées lorsque les origines des jetons ne peuvent pas être vérifiées

### Contrôles de sécurité et mesures d'atténuation

**Exigences de sécurité critiques :**

> **OBLIGATOIRE** : Les serveurs MCP **NE DOIVENT PAS** accepter de jetons qui n'ont pas été explicitement émis pour le serveur MCP

#### Contrôles d'authentification et d'autorisation

- **Examen rigoureux de l'autorisation** : Effectuer des audits complets de la logique d'autorisation des serveurs MCP pour garantir que seuls les utilisateurs et clients prévus peuvent accéder aux ressources sensibles
  - **Guide d'implémentation** : [Azure API Management comme passerelle d'authentification pour les serveurs MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
  - **Intégration d'identité** : [Utilisation de Microsoft Entra ID pour l'authentification des serveurs MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)

- **Gestion sécurisée des jetons** : Implémenter les [meilleures pratiques de validation et de cycle de vie des jetons de Microsoft](https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  - Valider que les revendications d'audience des jetons correspondent à l'identité du serveur MCP
  - Mettre en œuvre des politiques de rotation et d'expiration des jetons appropriées
  - Prévenir les attaques par relecture de jetons et les usages non autorisés

- **Stockage sécurisé des jetons** : Stockage sécurisé des jetons avec chiffrement au repos et en transit
  - **Meilleures pratiques** : [Directives de stockage et de chiffrement des jetons sécurisés](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

#### Implémentation des contrôles d'accès

- **Principe de privilèges minimaux** : Accorder aux serveurs MCP uniquement les permissions minimales nécessaires à leur fonctionnalité prévue
  - Révisions régulières des permissions et mises à jour pour éviter l'accumulation de privilèges
  - **Documentation Microsoft** : [Accès sécurisé avec privilèges minimaux](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)

- **Contrôle d'accès basé sur les rôles (RBAC)** : Implémenter des attributions de rôles granulaires
  - Limiter les rôles à des ressources et actions spécifiques
  - Éviter les permissions larges ou inutiles qui augmentent les surfaces d'attaque

- **Surveillance continue des permissions** : Mettre en œuvre des audits et une surveillance continue des accès
  - Surveiller les modèles d'utilisation des permissions pour détecter les anomalies
  - Remédier rapidement aux privilèges excessifs ou inutilisés

## Menaces spécifiques à l'IA

### Attaques par injection de prompts et manipulation des outils

Les implémentations modernes de MCP sont confrontées à des vecteurs d'attaque sophistiqués spécifiques à l'IA que les mesures de sécurité traditionnelles ne peuvent pas entièrement contrer :

#### **Injection indirecte de prompts (injection de prompts inter-domaines)**

**L'injection indirecte de prompts** représente l'une des vulnérabilités les plus critiques dans les systèmes d'IA activés par MCP. Les attaquants intègrent des instructions malveillantes dans des contenus externes—documents, pages web, emails ou sources de données—que les systèmes d'IA traitent ensuite comme des commandes légitimes.

**Scénarios d'attaque :**
- **Injection basée sur des documents** : Instructions malveillantes cachées dans des documents traités qui déclenchent des actions non prévues de l'IA
- **Exploitation de contenu web** : Pages web compromises contenant des prompts intégrés qui manipulent le comportement de l'IA lorsqu'elles sont analysées
- **Attaques basées sur les emails** : Prompts malveillants dans des emails qui poussent les assistants IA à divulguer des informations ou à effectuer des actions non autorisées
- **Contamination des sources de données** : Bases de données ou API compromises servant du contenu altéré aux systèmes d'IA

**Impact réel** : Ces attaques peuvent entraîner l'exfiltration de données, des violations de la vie privée, la génération de contenu nuisible et la manipulation des interactions utilisateur. Pour une analyse détaillée, voir [Injection de prompts dans MCP (Simon Willison)](https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/).

![Diagramme d'attaque par injection de prompts](../../../translated_images/prompt-injection.ed9fbfde297ca877c15bc6daa808681cd3c3dc7bf27bbbda342ef1ba5fc4f52d.fr.png)

#### **Attaques par empoisonnement des outils**

**L'empoisonnement des outils** cible les métadonnées qui définissent les outils MCP, exploitant la manière dont les LLM interprètent les descriptions et paramètres des outils pour prendre des décisions d'exécution.

**Mécanismes d'attaque :**
- **Manipulation des métadonnées** : Les attaquants injectent des instructions malveillantes dans les descriptions des outils, les définitions de paramètres ou les exemples d'utilisation
- **Instructions invisibles** : Prompts cachés dans les métadonnées des outils qui sont traités par les modèles d'IA mais invisibles pour les utilisateurs humains
- **Modification dynamique des outils ("Rug Pulls")** : Les outils approuvés par les utilisateurs sont ensuite modifiés pour effectuer des actions malveillantes sans que les utilisateurs en soient conscients
- **Injection de paramètres** : Contenu malveillant intégré dans les schémas de paramètres des outils qui influence le comportement des modèles

**Risques des serveurs hébergés** : Les serveurs MCP distants présentent des risques accrus car les définitions des outils peuvent être mises à jour après l'approbation initiale des utilisateurs, créant des scénarios où des outils auparavant sûrs deviennent malveillants. Pour une analyse complète, voir [Attaques par empoisonnement des outils (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).

![Diagramme d'attaque par injection d'outils](../../../translated_images/tool-injection.3b0b4a6b24de6befe7d3afdeae44138ef005881aebcfc84c6f61369ce31e3640.fr.png)

#### **Autres vecteurs d'attaque IA**

- **Injection de prompts inter-domaines (XPIA)** : Attaques sophistiquées exploitant du contenu provenant de plusieurs domaines pour contourner les contrôles de sécurité
- **Modification dynamique des capacités** : Changements en temps réel des capacités des outils qui échappent aux évaluations de sécurité initiales
- **Empoisonnement de la fenêtre contextuelle** : Attaques manipulant de grandes fenêtres contextuelles pour cacher des instructions malveillantes
- **Attaques de confusion des modèles** : Exploitation des limitations des modèles pour créer des comportements imprévisibles ou dangereux

### Impact des risques de sécurité IA

**Conséquences à fort impact :**
- **Exfiltration de données** : Accès non autorisé et vol de données sensibles d'entreprise ou personnelles
- **Violations de la vie privée** : Exposition d'informations personnelles identifiables (PII) et de données confidentielles d'entreprise  
- **Manipulation des systèmes** : Modifications non prévues des systèmes et workflows critiques
- **Vol d'identifiants** : Compromission des jetons d'authentification et des identifiants de service
- **Mouvement latéral** : Utilisation de systèmes d'IA compromis comme pivots pour des attaques réseau plus larges

### Solutions de sécurité IA de Microsoft

#### **AI Prompt Shields : Protection avancée contre les attaques par injection**

Les **AI Prompt Shields** de Microsoft offrent une défense complète contre les attaques par injection directe et indirecte grâce à plusieurs couches de sécurité :

##### **Mécanismes de protection principaux :**

1. **Détection et filtrage avancés**
   - Algorithmes d'apprentissage automatique et techniques NLP détectant les instructions malveillantes dans le contenu externe
   - Analyse en temps réel des documents, pages web, emails et sources de données pour identifier les menaces intégrées
   - Compréhension contextuelle des modèles de prompts légitimes vs malveillants

2. **Techniques de mise en lumière**  
   - Distinction entre les instructions système de confiance et les entrées externes potentiellement compromises
   - Méthodes de transformation de texte améliorant la pertinence des modèles tout en isolant le contenu malveillant
   - Aide les systèmes d'IA à maintenir une hiérarchie d'instructions correcte et à ignorer les commandes injectées

3. **Systèmes de délimitation et de marquage des données**
   - Définition explicite des frontières entre les messages système de confiance et le texte d'entrée externe
   - Marqueurs spéciaux mettant en évidence les limites entre les sources de données de confiance et non fiables
   - Séparation claire empêchant la confusion des instructions et l'exécution de commandes non autorisées

4. **Intelligence continue sur les menaces**
   - Microsoft surveille en permanence les modèles d'attaque émergents et met à jour les défenses
   - Recherche proactive des nouvelles techniques d'injection et vecteurs d'attaque
   - Mises à jour régulières des modèles de sécurité pour maintenir l'efficacité face aux menaces évolutives

5. **Intégration avec Azure Content Safety**
   - Partie intégrante de la suite complète Azure AI Content Safety
   - Détection supplémentaire des tentatives de contournement, du contenu nuisible et des violations des politiques de sécurité
   - Contrôles de sécurité unifiés pour les composants des applications IA

**Ressources d'implémentation** : [Documentation Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)

![Protection Microsoft Prompt Shields](../../../translated_images/prompt-shield.ff5b95be76e9c78c6ec0888206a4a6a0a5ab4bb787832a9eceef7a62fe0138d1.fr.png)


## Menaces avancées de sécurité MCP

### Vulnérabilités de détournement de session

Le **détournement de session** représente un vecteur d'attaque critique dans les implémentations MCP avec état, où des parties non autorisées obtiennent et abusent des identifiants de session légitimes pour se faire passer pour des clients et effectuer des actions non autorisées.

#### **Scénarios d'attaque et risques**

- **Injection de prompts dans les sessions détournées** : Les attaquants disposant d'identifiants de session volés injectent des événements malveillants dans les serveurs partageant l'état de session, déclenchant potentiellement des actions nuisibles ou accédant
- **Génération sécurisée de sessions** : Utilisez des identifiants de session cryptographiquement sécurisés et non déterministes, générés avec des générateurs de nombres aléatoires sécurisés.  
- **Association spécifique à l'utilisateur** : Associez les identifiants de session à des informations spécifiques à l'utilisateur en utilisant des formats comme `<user_id>:<session_id>` pour éviter les abus de sessions entre utilisateurs.  
- **Gestion du cycle de vie des sessions** : Mettez en œuvre une expiration, une rotation et une invalidation appropriées pour limiter les fenêtres de vulnérabilité.  
- **Sécurité des transports** : HTTPS obligatoire pour toutes les communications afin d'empêcher l'interception des identifiants de session.  

### Problème du "Confused Deputy"

Le **problème du "confused deputy"** survient lorsque les serveurs MCP agissent comme des proxys d'authentification entre les clients et des services tiers, créant des opportunités de contournement d'autorisation via l'exploitation d'identifiants clients statiques.

#### **Mécanismes d'attaque et risques**

- **Contournement du consentement basé sur les cookies** : Une authentification utilisateur précédente crée des cookies de consentement que les attaquants exploitent via des requêtes d'autorisation malveillantes avec des URI de redirection forgées.  
- **Vol de codes d'autorisation** : Les cookies de consentement existants peuvent amener les serveurs d'autorisation à ignorer les écrans de consentement, redirigeant les codes vers des points de terminaison contrôlés par l'attaquant.  
- **Accès non autorisé aux API** : Les codes d'autorisation volés permettent un échange de jetons et une usurpation d'identité utilisateur sans approbation explicite.  

#### **Stratégies d'atténuation**

**Contrôles obligatoires :**  
- **Exigences de consentement explicite** : Les serveurs proxy MCP utilisant des identifiants clients statiques **DOIVENT** obtenir le consentement de l'utilisateur pour chaque client enregistré dynamiquement.  
- **Mise en œuvre de la sécurité OAuth 2.1** : Suivez les meilleures pratiques de sécurité OAuth actuelles, y compris PKCE (Proof Key for Code Exchange) pour toutes les requêtes d'autorisation.  
- **Validation stricte des clients** : Mettez en œuvre une validation rigoureuse des URI de redirection et des identifiants clients pour éviter les exploitations.  

### Vulnérabilités liées au transfert de jetons  

Le **transfert de jetons** représente un anti-modèle explicite où les serveurs MCP acceptent des jetons clients sans validation appropriée et les transmettent aux API en aval, violant les spécifications d'autorisation MCP.

#### **Implications de sécurité**

- **Contournement des contrôles** : L'utilisation directe de jetons client-API contourne les contrôles critiques de limitation de débit, de validation et de surveillance.  
- **Corruption des pistes d'audit** : Les jetons émis en amont rendent l'identification des clients impossible, compromettant les capacités d'enquête sur les incidents.  
- **Exfiltration de données via proxy** : Les jetons non validés permettent aux acteurs malveillants d'utiliser les serveurs comme proxys pour accéder à des données non autorisées.  
- **Violations des frontières de confiance** : Les hypothèses de confiance des services en aval peuvent être violées lorsque les origines des jetons ne peuvent pas être vérifiées.  
- **Expansion des attaques multi-services** : Les jetons compromis acceptés par plusieurs services permettent des mouvements latéraux.  

#### **Contrôles de sécurité requis**

**Exigences non négociables :**  
- **Validation des jetons** : Les serveurs MCP **NE DOIVENT PAS** accepter des jetons qui ne leur sont pas explicitement destinés.  
- **Vérification de l'audience** : Validez toujours que les revendications d'audience des jetons correspondent à l'identité du serveur MCP.  
- **Cycle de vie approprié des jetons** : Mettez en œuvre des jetons d'accès de courte durée avec des pratiques de rotation sécurisées.  

## Sécurité de la chaîne d'approvisionnement pour les systèmes d'IA

La sécurité de la chaîne d'approvisionnement s'est étendue au-delà des dépendances logicielles traditionnelles pour englober l'ensemble de l'écosystème de l'IA. Les implémentations modernes de MCP doivent vérifier et surveiller rigoureusement tous les composants liés à l'IA, car chacun peut introduire des vulnérabilités potentielles compromettant l'intégrité du système.

### Composants élargis de la chaîne d'approvisionnement de l'IA

**Dépendances logicielles traditionnelles :**  
- Bibliothèques et frameworks open source  
- Images de conteneurs et systèmes de base  
- Outils de développement et pipelines de construction  
- Composants et services d'infrastructure  

**Éléments spécifiques à l'IA :**  
- **Modèles fondamentaux** : Modèles pré-entraînés provenant de divers fournisseurs nécessitant une vérification de provenance  
- **Services d'embedding** : Services externes de vectorisation et de recherche sémantique  
- **Fournisseurs de contexte** : Sources de données, bases de connaissances et dépôts de documents  
- **API tierces** : Services d'IA externes, pipelines de ML et points de terminaison de traitement des données  
- **Artefacts de modèles** : Poids, configurations et variantes de modèles ajustés  
- **Sources de données d'entraînement** : Jeux de données utilisés pour l'entraînement et l'ajustement des modèles  

### Stratégie complète de sécurité de la chaîne d'approvisionnement

#### **Vérification des composants et confiance**  
- **Validation de provenance** : Vérifiez l'origine, la licence et l'intégrité de tous les composants d'IA avant leur intégration.  
- **Évaluation de sécurité** : Effectuez des analyses de vulnérabilité et des revues de sécurité pour les modèles, sources de données et services d'IA.  
- **Analyse de réputation** : Évaluez les antécédents et pratiques de sécurité des fournisseurs de services d'IA.  
- **Vérification de conformité** : Assurez-vous que tous les composants respectent les exigences de sécurité et réglementaires de l'organisation.  

#### **Pipelines de déploiement sécurisés**  
- **Sécurité CI/CD automatisée** : Intégrez des analyses de sécurité tout au long des pipelines de déploiement automatisés.  
- **Intégrité des artefacts** : Mettez en œuvre une vérification cryptographique pour tous les artefacts déployés (code, modèles, configurations).  
- **Déploiement par étapes** : Utilisez des stratégies de déploiement progressif avec validation de sécurité à chaque étape.  
- **Dépôts d'artefacts de confiance** : Déployez uniquement à partir de registres et dépôts d'artefacts vérifiés et sécurisés.  

#### **Surveillance continue et réponse**  
- **Analyse des dépendances** : Surveillance continue des vulnérabilités pour toutes les dépendances logicielles et composants d'IA.  
- **Surveillance des modèles** : Évaluation continue du comportement des modèles, des dérives de performance et des anomalies de sécurité.  
- **Suivi de la santé des services** : Surveillez les services d'IA externes pour leur disponibilité, incidents de sécurité et changements de politique.  
- **Intégration de renseignements sur les menaces** : Intégrez des flux de menaces spécifiques aux risques de sécurité liés à l'IA et au ML.  

#### **Contrôle d'accès et principe du moindre privilège**  
- **Permissions au niveau des composants** : Restreignez l'accès aux modèles, données et services en fonction des besoins métier.  
- **Gestion des comptes de service** : Implémentez des comptes de service dédiés avec les permissions minimales nécessaires.  
- **Segmentation réseau** : Isolez les composants d'IA et limitez l'accès réseau entre les services.  
- **Contrôles des passerelles API** : Utilisez des passerelles API centralisées pour contrôler et surveiller l'accès aux services d'IA externes.  

#### **Réponse aux incidents et récupération**  
- **Procédures de réponse rapide** : Processus établis pour corriger ou remplacer les composants d'IA compromis.  
- **Rotation des identifiants** : Systèmes automatisés pour la rotation des secrets, clés API et identifiants de service.  
- **Capacités de retour en arrière** : Possibilité de revenir rapidement à des versions précédentes connues comme sûres des composants d'IA.  
- **Récupération après violation de la chaîne d'approvisionnement** : Procédures spécifiques pour répondre aux compromissions des services d'IA en amont.  

### Outils de sécurité Microsoft et intégration

**GitHub Advanced Security** offre une protection complète de la chaîne d'approvisionnement, notamment :  
- **Analyse des secrets** : Détection automatisée des identifiants, clés API et jetons dans les dépôts.  
- **Analyse des dépendances** : Évaluation des vulnérabilités pour les dépendances open source et bibliothèques.  
- **Analyse CodeQL** : Analyse statique du code pour les vulnérabilités de sécurité et les problèmes de codage.  
- **Aperçus de la chaîne d'approvisionnement** : Visibilité sur la santé et le statut de sécurité des dépendances.  

**Intégration Azure DevOps et Azure Repos :**  
- Intégration fluide des analyses de sécurité sur les plateformes de développement Microsoft.  
- Vérifications de sécurité automatisées dans Azure Pipelines pour les charges de travail d'IA.  
- Application de politiques pour un déploiement sécurisé des composants d'IA.  

**Pratiques internes de Microsoft :**  
Microsoft met en œuvre des pratiques de sécurité de la chaîne d'approvisionnement étendues dans tous ses produits. Découvrez des approches éprouvées dans [The Journey to Secure the Software Supply Chain at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/).  


### **Solutions de sécurité Microsoft**
- [Documentation sur Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Service Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)
- [Sécurité Microsoft Entra ID](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)
- [Bonnes pratiques de gestion des jetons Azure](https://learn.microsoft.com/entra/identity-platform/access-tokens)
- [GitHub Advanced Security](https://github.com/security/advanced-security)

### **Guides de mise en œuvre et tutoriels**
- [Azure API Management comme passerelle d'authentification MCP](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)
- [Authentification Microsoft Entra ID avec les serveurs MCP](https://den.dev/blog/mcp-server-auth-entra-id-session/)
- [Stockage sécurisé des jetons et chiffrement (Vidéo)](https://youtu.be/uRdX37EcCwg?si=6fSChs1G4glwXRy2)

### **Sécurité DevOps et chaîne d'approvisionnement**
- [Sécurité Azure DevOps](https://azure.microsoft.com/products/devops)
- [Sécurité Azure Repos](https://azure.microsoft.com/products/devops/repos/)
- [Parcours de sécurité de la chaîne d'approvisionnement Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/the-journey-to-secure-the-software-supply-chain-at-microsoft/)

## **Documentation de sécurité supplémentaire**

Pour des conseils de sécurité complets, consultez ces documents spécialisés dans cette section :

- **[Bonnes pratiques de sécurité MCP 2025](./mcp-security-best-practices-2025.md)** - Bonnes pratiques complètes pour les implémentations MCP  
- **[Mise en œuvre d'Azure Content Safety](./azure-content-safety-implementation.md)** - Exemples pratiques pour l'intégration d'Azure Content Safety  
- **[Contrôles de sécurité MCP 2025](./mcp-security-controls-2025.md)** - Derniers contrôles et techniques de sécurité pour les déploiements MCP  
- **[Guide de référence rapide des bonnes pratiques MCP](./mcp-best-practices.md)** - Guide de référence rapide pour les pratiques de sécurité essentielles MCP  

---

## Et après

Prochain chapitre : [Chapitre 3 : Premiers pas](../03-GettingStarted/README.md)

**Avertissement** :  
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue d'origine doit être considéré comme la source faisant autorité. Pour des informations critiques, il est recommandé de faire appel à une traduction humaine professionnelle. Nous déclinons toute responsabilité en cas de malentendus ou d'interprétations erronées résultant de l'utilisation de cette traduction.