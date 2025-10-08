<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "beaeca2ae0ec007783e6310a3b63291f",
  "translation_date": "2025-10-06T21:51:56+00:00",
  "source_file": "changelog.md",
  "language_code": "fr"
}
-->
# Journal des modifications : Curriculum MCP pour débutants

Ce document sert de registre pour toutes les modifications significatives apportées au curriculum du protocole de contexte modèle (MCP) pour débutants. Les changements sont documentés par ordre chronologique inversé (les plus récents en premier).

## 6 octobre 2025

### Extension de la section "Premiers pas" – Utilisation avancée des serveurs et authentification simple

#### Utilisation avancée des serveurs (03-GettingStarted/10-advanced)
- **Nouveau chapitre ajouté** : Introduction d'un guide complet sur l'utilisation avancée des serveurs MCP, couvrant les architectures de serveurs régulières et de bas niveau.
  - **Serveur régulier vs. serveur de bas niveau** : Comparaison détaillée et exemples de code en Python et TypeScript pour les deux approches.
  - **Conception basée sur les gestionnaires** : Explication de la gestion des outils/ressources/prompts basée sur des gestionnaires pour des implémentations de serveurs évolutives et flexibles.
  - **Modèles pratiques** : Scénarios réels où les modèles de serveurs de bas niveau sont avantageux pour des fonctionnalités avancées et des architectures complexes.

#### Authentification simple (03-GettingStarted/11-simple-auth)
- **Nouveau chapitre ajouté** : Guide pas à pas pour implémenter une authentification simple dans les serveurs MCP.
  - **Concepts d'authentification** : Explication claire de la différence entre authentification et autorisation, et gestion des identifiants.
  - **Implémentation de l'authentification de base** : Modèles d'authentification basés sur des middlewares en Python (Starlette) et TypeScript (Express), avec des exemples de code.
  - **Progression vers une sécurité avancée** : Conseils pour commencer avec une authentification simple et évoluer vers OAuth 2.1 et RBAC, avec des références à des modules de sécurité avancés.

Ces ajouts offrent des conseils pratiques pour construire des serveurs MCP plus robustes, sécurisés et flexibles, reliant les concepts fondamentaux aux modèles de production avancés.

## 29 septembre 2025

### Laboratoires d'intégration de bases de données pour serveurs MCP – Parcours d'apprentissage pratique complet

#### 11-MCPServerHandsOnLabs - Nouveau curriculum complet sur l'intégration de bases de données
- **Parcours d'apprentissage en 13 laboratoires** : Ajout d'un curriculum pratique complet pour construire des serveurs MCP prêts pour la production avec intégration de bases de données PostgreSQL.
  - **Implémentation réelle** : Cas d'utilisation analytique de Zava Retail démontrant des modèles de niveau entreprise.
  - **Progression structurée de l'apprentissage** :
    - **Laboratoires 00-03 : Fondations** - Introduction, architecture de base, sécurité et multi-locataires, configuration de l'environnement.
    - **Laboratoires 04-06 : Construction du serveur MCP** - Conception et schéma de base de données, implémentation du serveur MCP, développement d'outils.
    - **Laboratoires 07-09 : Fonctionnalités avancées** - Intégration de recherche sémantique, tests et débogage, intégration VS Code.
    - **Laboratoires 10-12 : Production et meilleures pratiques** - Stratégies de déploiement, surveillance et observabilité, optimisation et meilleures pratiques.
  - **Technologies d'entreprise** : Framework FastMCP, PostgreSQL avec pgvector, embeddings Azure OpenAI, Azure Container Apps, Application Insights.
  - **Fonctionnalités avancées** : Sécurité au niveau des lignes (RLS), recherche sémantique, accès multi-locataires aux données, embeddings vectoriels, surveillance en temps réel.

#### Standardisation de la terminologie - Conversion de "Module" en "Laboratoire"
- **Mise à jour complète de la documentation** : Mise à jour systématique de tous les fichiers README dans 11-MCPServerHandsOnLabs pour utiliser la terminologie "Laboratoire" au lieu de "Module".
  - **En-têtes de section** : Modification de "Ce que couvre ce module" en "Ce que couvre ce laboratoire" dans les 13 laboratoires.
  - **Description du contenu** : Changement de "Ce module fournit..." en "Ce laboratoire fournit..." dans toute la documentation.
  - **Objectifs d'apprentissage** : Mise à jour de "À la fin de ce module..." en "À la fin de ce laboratoire...".
  - **Liens de navigation** : Conversion de toutes les références "Module XX:" en "Laboratoire XX:" dans les références croisées et la navigation.
  - **Suivi de la progression** : Mise à jour de "Après avoir terminé ce module..." en "Après avoir terminé ce laboratoire...".
  - **Références techniques préservées** : Maintien des références aux modules Python dans les fichiers de configuration (par exemple, `"module": "mcp_server.main"`).

#### Amélioration du guide d'étude (study_guide.md)
- **Carte visuelle du curriculum** : Ajout d'une nouvelle section "11. Laboratoires d'intégration de bases de données" avec une visualisation complète de la structure des laboratoires.
- **Structure du dépôt** : Mise à jour de dix à onze sections principales avec une description détaillée de 11-MCPServerHandsOnLabs.
- **Guidage du parcours d'apprentissage** : Instructions de navigation améliorées pour couvrir les sections 00-11.
- **Couverture technologique** : Ajout de détails sur l'intégration de FastMCP, PostgreSQL et des services Azure.
- **Résultats d'apprentissage** : Accent mis sur le développement de serveurs prêts pour la production, les modèles d'intégration de bases de données et la sécurité d'entreprise.

#### Amélioration de la structure du README principal
- **Terminologie basée sur les laboratoires** : Mise à jour du README.md principal dans 11-MCPServerHandsOnLabs pour utiliser systématiquement la structure "Laboratoire".
- **Organisation du parcours d'apprentissage** : Progression claire des concepts fondamentaux à l'implémentation avancée jusqu'au déploiement en production.
- **Focus sur le monde réel** : Accent mis sur l'apprentissage pratique avec des modèles et technologies de niveau entreprise.

### Améliorations de la qualité et de la cohérence de la documentation
- **Accent sur l'apprentissage pratique** : Renforcement de l'approche pratique basée sur les laboratoires dans toute la documentation.
- **Focus sur les modèles d'entreprise** : Mise en évidence des implémentations prêtes pour la production et des considérations de sécurité d'entreprise.
- **Intégration technologique** : Couverture complète des services modernes Azure et des modèles d'intégration AI.
- **Progression de l'apprentissage** : Chemin structuré clair des concepts de base au déploiement en production.

## 26 septembre 2025

### Amélioration des études de cas – Intégration du registre MCP GitHub

#### Études de cas (09-CaseStudy/) - Focus sur le développement de l'écosystème
- **README.md** : Expansion majeure avec une étude de cas complète sur le registre MCP GitHub.
  - **Étude de cas sur le registre MCP GitHub** : Nouvelle étude de cas complète examinant le lancement du registre MCP GitHub en septembre 2025.
    - **Analyse du problème** : Examen détaillé des défis liés à la découverte et au déploiement fragmentés des serveurs MCP.
    - **Architecture de la solution** : Approche centralisée du registre GitHub avec installation en un clic dans VS Code.
    - **Impact commercial** : Améliorations mesurables de l'intégration des développeurs et de la productivité.
    - **Valeur stratégique** : Focus sur le déploiement modulaire des agents et l'interopérabilité entre outils.
    - **Développement de l'écosystème** : Positionnement comme plateforme fondamentale pour l'intégration agentique.
  - **Structure améliorée des études de cas** : Mise à jour des sept études de cas avec un formatage cohérent et des descriptions complètes.
    - Agents de voyage Azure AI : Accent sur l'orchestration multi-agents.
    - Intégration Azure DevOps : Focus sur l'automatisation des workflows.
    - Récupération de documentation en temps réel : Implémentation du client console Python.
    - Générateur de plan d'étude interactif : Application web conversationnelle Chainlit.
    - Documentation dans l'éditeur : Intégration VS Code et GitHub Copilot.
    - Gestion des API Azure : Modèles d'intégration d'API d'entreprise.
    - Registre MCP GitHub : Développement de l'écosystème et plateforme communautaire.
  - **Conclusion complète** : Réécriture de la section conclusion mettant en évidence sept études de cas couvrant plusieurs dimensions d'implémentation MCP.
    - Intégration d'entreprise, orchestration multi-agents, productivité des développeurs.
    - Développement de l'écosystème, applications éducatives.
    - Insights améliorés sur les modèles architecturaux, les stratégies d'implémentation et les meilleures pratiques.
    - Accent sur MCP en tant que protocole mature et prêt pour la production.

#### Mises à jour du guide d'étude (study_guide.md)
- **Carte visuelle du curriculum** : Mise à jour de la carte mentale pour inclure le registre MCP GitHub dans la section Études de cas.
- **Description des études de cas** : Amélioration des descriptions génériques en une analyse détaillée des sept études de cas complètes.
- **Structure du dépôt** : Mise à jour de la section 10 pour refléter une couverture complète des études de cas avec des détails spécifiques d'implémentation.
- **Intégration du journal des modifications** : Ajout de l'entrée du 26 septembre 2025 documentant l'ajout du registre MCP GitHub et les améliorations des études de cas.
- **Mises à jour de la date** : Mise à jour de l'horodatage du pied de page pour refléter la dernière révision (26 septembre 2025).

### Améliorations de la qualité de la documentation
- **Amélioration de la cohérence** : Formatage et structure standardisés des études de cas dans les sept exemples.
- **Couverture complète** : Les études de cas couvrent désormais les scénarios d'entreprise, de productivité des développeurs et de développement de l'écosystème.
- **Positionnement stratégique** : Accent renforcé sur MCP en tant que plateforme fondamentale pour le déploiement de systèmes agentiques.
- **Intégration des ressources** : Mise à jour des ressources supplémentaires pour inclure le lien vers le registre MCP GitHub.

## 15 septembre 2025

### Extension des sujets avancés – Transports personnalisés et ingénierie du contexte

#### Transports personnalisés MCP (05-AdvancedTopics/mcp-transport/) - Nouveau guide d'implémentation avancée
- **README.md** : Guide complet d'implémentation pour les mécanismes de transport personnalisés MCP.
  - **Transport Azure Event Grid** : Implémentation complète de transport événementiel sans serveur.
    - Exemples en C#, TypeScript et Python avec intégration Azure Functions.
    - Modèles d'architecture événementielle pour des solutions MCP évolutives.
    - Récepteurs de webhook et gestion des messages push.
  - **Transport Azure Event Hubs** : Implémentation de transport en streaming à haut débit.
    - Capacités de streaming en temps réel pour des scénarios à faible latence.
    - Stratégies de partitionnement et gestion des points de contrôle.
    - Optimisation des performances et des lots de messages.
  - **Modèles d'intégration d'entreprise** : Exemples architecturaux prêts pour la production.
    - Traitement MCP distribué sur plusieurs fonctions Azure.
    - Architectures hybrides combinant plusieurs types de transport.
    - Stratégies de durabilité, fiabilité et gestion des erreurs des messages.
  - **Sécurité et surveillance** : Intégration Azure Key Vault et modèles d'observabilité.
    - Authentification par identité gérée et accès au moindre privilège.
    - Télémétrie Application Insights et surveillance des performances.
    - Modèles de disjoncteurs et de tolérance aux pannes.
  - **Cadres de test** : Stratégies de test complètes pour les transports personnalisés.
    - Tests unitaires avec doubles de test et frameworks de simulation.
    - Tests d'intégration avec Azure Test Containers.
    - Considérations sur les tests de performance et de charge.

#### Ingénierie du contexte (05-AdvancedTopics/mcp-contextengineering/) - Discipline émergente en IA
- **README.md** : Exploration complète de l'ingénierie du contexte en tant que domaine émergent.
  - **Principes fondamentaux** : Partage complet du contexte, sensibilisation aux décisions d'action et gestion des fenêtres de contexte.
  - **Alignement avec le protocole MCP** : Comment la conception MCP répond aux défis de l'ingénierie du contexte.
    - Limitations des fenêtres de contexte et stratégies de chargement progressif.
    - Détermination de la pertinence et récupération dynamique du contexte.
    - Gestion multi-modale du contexte et considérations de sécurité.
  - **Approches d'implémentation** : Architectures mono-thread et multi-agents.
    - Techniques de découpage et de priorisation du contexte.
    - Chargement progressif du contexte et stratégies de compression.
    - Approches contextuelles en couches et optimisation de la récupération.
  - **Cadre de mesure** : Métriques émergentes pour l'évaluation de l'efficacité du contexte.
    - Efficacité des entrées, performances, qualité et considérations d'expérience utilisateur.
    - Approches expérimentales pour l'optimisation du contexte.
    - Analyse des échecs et méthodologies d'amélioration.

#### Mises à jour de la navigation dans le curriculum (README.md)
- **Structure améliorée des modules** : Mise à jour du tableau du curriculum pour inclure les nouveaux sujets avancés.
  - Ajout des entrées Ingénierie du contexte (5.14) et Transport personnalisé (5.15).
  - Formatage cohérent et liens de navigation dans tous les modules.
  - Descriptions mises à jour pour refléter la portée actuelle du contenu.

### Améliorations de la structure des répertoires
- **Standardisation des noms** : Renommage de "mcp transport" en "mcp-transport" pour une cohérence avec les autres dossiers de sujets avancés.
- **Organisation du contenu** : Tous les dossiers 05-AdvancedTopics suivent désormais un modèle de nommage cohérent (mcp-[sujet]).

### Améliorations de la qualité de la documentation
- **Alignement avec la spécification MCP** : Tout le nouveau contenu fait référence à la spécification MCP actuelle 2025-06-18.
- **Exemples multi-langages** : Exemples de code complets en C#, TypeScript et Python.
- **Focus sur l'entreprise** : Modèles prêts pour la production et intégration cloud Azure tout au long.
- **Documentation visuelle** : Diagrammes Mermaid pour la visualisation des architectures et des flux.

## 18 août 2025

### Mise à jour complète de la documentation – Normes MCP 2025-06-18

#### Meilleures pratiques de sécurité MCP (02-Security/) - Modernisation complète
- **MCP-SECURITY-BEST-PRACTICES-2025.md** : Réécriture complète alignée avec la spécification MCP 2025-06-18.
  - **Exigences obligatoires** : Ajout d'exigences explicites DOIT/NE DOIT PAS de la spécification officielle avec des indicateurs visuels clairs.
  - **12 pratiques de sécurité essentielles** : Restructuration d'une liste de 15 éléments en domaines de sécurité complets.
    - Sécurité des jetons et authentification avec intégration de fournisseurs d'identité externes.
    - Gestion des sessions et sécurité des transports avec exigences cryptographiques.
    - Protection contre les menaces spécifiques à l'IA avec intégration Microsoft Prompt Shields.
    - Contrôle d'accès et permissions avec principe du moindre privilège.
    - Sécurité du contenu et surveillance avec intégration Azure Content Safety.
    - Sécurité de la chaîne d'approvisionnement avec vérification complète des composants.
    - Sécurité OAuth et prévention des attaques de type "Confused Deputy" avec implémentation PKCE.
    - Réponse aux incidents et récupération avec capacités automatisées.
    - Conformité et gouvernance avec alignement réglementaire.
    - Contrôles de sécurité avancés avec architecture de confiance zéro.
    - Intégration de l'écosystème de sécurité Microsoft avec solutions complètes.
    - Évolution continue de la sécurité avec pratiques adaptatives.
  - **Solutions de sécurité Microsoft** : Guide d'intégration amélioré pour Prompt Shields, Azure Content Safety, Entra ID et GitHub Advanced Security.
  - **Ressources d'implémentation** : Liens de ressources complets catégorisés par documentation officielle MCP, solutions de sécurité Microsoft, normes de sécurité et guides d'implémentation.

#### Contrôles de sécurité avancés (02-Security/) - Implémentation d'entreprise
- **MCP-SECURITY-CONTROLS-2025.md** : Refonte complète avec cadre de sécurité de niveau entreprise.
  - **9 domaines de sécurité complets** : Expansion des contrôles de base en un cadre d'entreprise détaillé.
    - Authentification et autorisation avancées avec intégration Microsoft Entra ID.
    - Sécurité des jetons et contrôles anti-passage avec validation complète.
    - Contrôles de sécurité des sessions avec prévention des détournements.
    - Contrôles de sécurité spécifiques à l'IA avec prévention des injections de prompts et empoisonnement des outils.
    - Prévention des attaques de type "Confused Deputy" avec sécurité proxy OAuth.
    - Sécurité de l'exécution des outils avec sandboxing et isolation.
    - Contrôles de sécurité de la chaîne d'approvisionnement avec vérification des dépendances.
    - Contrôles de surveillance et de détection avec intégration SIEM.
    - Réponse aux incidents et récupération avec capacités automatisées.
  - **Exemples d'implémentation** : Ajout de blocs de configuration YAML détaillés et d'exemples de code.
  - **Intégration des solutions Microsoft** : Couverture complète des services de sécurité Azure, GitHub Advanced Security et gestion des identités d'entreprise.
#### Sécurité des sujets avancés (05-AdvancedTopics/mcp-security/) - Mise en œuvre prête pour la production
- **README.md** : Réécriture complète pour une mise en œuvre de sécurité d'entreprise
  - **Alignement avec la spécification actuelle** : Mise à jour selon la spécification MCP 2025-06-18 avec exigences de sécurité obligatoires
  - **Authentification améliorée** : Intégration de Microsoft Entra ID avec des exemples complets en .NET et Java Spring Security
  - **Intégration de la sécurité IA** : Mise en œuvre de Microsoft Prompt Shields et Azure Content Safety avec des exemples détaillés en Python
  - **Atténuation avancée des menaces** : Exemples de mise en œuvre complets pour :
    - Prévention des attaques de type "Confused Deputy" avec PKCE et validation du consentement utilisateur
    - Prévention du passage de jetons avec validation de l'audience et gestion sécurisée des jetons
    - Prévention du détournement de session avec liaison cryptographique et analyse comportementale
  - **Intégration de la sécurité d'entreprise** : Surveillance avec Azure Application Insights, pipelines de détection des menaces et sécurité de la chaîne d'approvisionnement
  - **Liste de contrôle de mise en œuvre** : Contrôles de sécurité obligatoires vs recommandés avec avantages de l'écosystème de sécurité Microsoft

### Qualité de la documentation et alignement avec les normes
- **Références de spécification** : Mise à jour de toutes les références selon la spécification MCP 2025-06-18
- **Écosystème de sécurité Microsoft** : Guide d'intégration amélioré dans toute la documentation de sécurité
- **Mise en œuvre pratique** : Ajout d'exemples de code détaillés en .NET, Java et Python avec des modèles d'entreprise
- **Organisation des ressources** : Catégorisation complète de la documentation officielle, des normes de sécurité et des guides de mise en œuvre
- **Indicateurs visuels** : Marquage clair des exigences obligatoires vs pratiques recommandées

#### Concepts fondamentaux (01-CoreConcepts/) - Modernisation complète
- **Mise à jour de la version du protocole** : Référence mise à jour selon la spécification MCP 2025-06-18 avec versionnement basé sur la date (format AAAA-MM-JJ)
- **Affinement de l'architecture** : Descriptions améliorées des hôtes, clients et serveurs pour refléter les modèles d'architecture MCP actuels
  - Les hôtes sont désormais clairement définis comme des applications IA coordonnant plusieurs connexions client MCP
  - Les clients sont décrits comme des connecteurs de protocole maintenant des relations serveur un-à-un
  - Les serveurs sont enrichis avec des scénarios de déploiement local vs distant
- **Restructuration des primitives** : Refonte complète des primitives serveur et client
  - Primitives serveur : Ressources (sources de données), Prompts (modèles), Outils (fonctions exécutables) avec explications et exemples détaillés
  - Primitives client : Échantillonnage (complétions LLM), Élicitation (entrée utilisateur), Journalisation (débogage/surveillance)
  - Mise à jour avec les modèles de méthode actuels de découverte (`*/list`), récupération (`*/get`) et exécution (`*/call`)
- **Architecture du protocole** : Introduction d'un modèle d'architecture à deux couches
  - Couche de données : Fondation JSON-RPC 2.0 avec gestion du cycle de vie et primitives
  - Couche de transport : STDIO (local) et HTTP streamable avec SSE (transport distant)
- **Cadre de sécurité** : Principes de sécurité complets incluant consentement explicite de l'utilisateur, protection de la confidentialité des données, sécurité de l'exécution des outils et sécurité de la couche de transport
- **Modèles de communication** : Mise à jour des messages du protocole pour montrer les flux d'initialisation, de découverte, d'exécution et de notification
- **Exemples de code** : Exemples multi-langages actualisés (.NET, Java, Python, JavaScript) pour refléter les modèles MCP SDK actuels

#### Sécurité (02-Security/) - Révision complète de la sécurité  
- **Alignement avec les normes** : Alignement complet avec les exigences de sécurité de la spécification MCP 2025-06-18
- **Évolution de l'authentification** : Documentation de l'évolution des serveurs OAuth personnalisés vers la délégation à des fournisseurs d'identité externes (Microsoft Entra ID)
- **Analyse des menaces spécifiques à l'IA** : Couverture améliorée des vecteurs d'attaque modernes liés à l'IA
  - Scénarios détaillés d'attaques par injection de prompts avec exemples réels
  - Mécanismes d'empoisonnement des outils et modèles d'attaques "rug pull"
  - Empoisonnement de la fenêtre contextuelle et attaques de confusion des modèles
- **Solutions de sécurité IA de Microsoft** : Couverture complète de l'écosystème de sécurité Microsoft
  - Prompt Shields IA avec techniques avancées de détection, mise en lumière et délimitation
  - Modèles d'intégration Azure Content Safety
  - GitHub Advanced Security pour la protection de la chaîne d'approvisionnement
- **Atténuation avancée des menaces** : Contrôles de sécurité détaillés pour :
  - Détournement de session avec scénarios d'attaque spécifiques à MCP et exigences cryptographiques pour les ID de session
  - Problèmes de "Confused Deputy" dans les scénarios de proxy MCP avec exigences de consentement explicites
  - Vulnérabilités de passage de jetons avec contrôles de validation obligatoires
- **Sécurité de la chaîne d'approvisionnement** : Couverture élargie de la chaîne d'approvisionnement IA incluant modèles de base, services d'embeddings, fournisseurs de contexte et API tierces
- **Sécurité de base** : Intégration améliorée avec des modèles de sécurité d'entreprise incluant l'architecture zéro confiance et l'écosystème de sécurité Microsoft
- **Organisation des ressources** : Liens de ressources catégorisés par type (Docs officiels, Normes, Recherche, Solutions Microsoft, Guides de mise en œuvre)

### Améliorations de la qualité de la documentation
- **Objectifs d'apprentissage structurés** : Objectifs d'apprentissage améliorés avec résultats spécifiques et actionnables
- **Références croisées** : Ajout de liens entre les sujets liés à la sécurité et aux concepts fondamentaux
- **Informations actuelles** : Mise à jour de toutes les références de dates et liens de spécification selon les normes actuelles
- **Guide de mise en œuvre** : Ajout de directives de mise en œuvre spécifiques et actionnables dans les deux sections

## 16 juillet 2025

### Améliorations du README et de la navigation
- Refonte complète de la navigation du curriculum dans README.md
- Remplacement des balises `<details>` par un format basé sur des tableaux plus accessible
- Création d'options de mise en page alternatives dans le nouveau dossier "alternative_layouts"
- Ajout d'exemples de navigation en style cartes, onglets et accordéon
- Mise à jour de la section sur la structure du dépôt pour inclure tous les fichiers récents
- Amélioration de la section "Comment utiliser ce curriculum" avec des recommandations claires
- Mise à jour des liens de spécification MCP pour pointer vers les URL correctes
- Ajout de la section sur l'ingénierie contextuelle (5.14) à la structure du curriculum

### Mises à jour du guide d'étude
- Révision complète du guide d'étude pour s'aligner sur la structure actuelle du dépôt
- Ajout de nouvelles sections pour les clients MCP et outils, ainsi que les serveurs MCP populaires
- Mise à jour de la carte visuelle du curriculum pour refléter avec précision tous les sujets
- Amélioration des descriptions des sujets avancés pour couvrir toutes les zones spécialisées
- Mise à jour de la section études de cas pour refléter des exemples réels
- Ajout de ce journal des modifications complet

### Contributions communautaires (06-CommunityContributions/)
- Ajout d'informations détaillées sur les serveurs MCP pour la génération d'images
- Ajout d'une section complète sur l'utilisation de Claude dans VSCode
- Ajout des instructions de configuration et d'utilisation du client terminal Cline
- Mise à jour de la section client MCP pour inclure toutes les options populaires
- Amélioration des exemples de contributions avec des échantillons de code plus précis

### Sujets avancés (05-AdvancedTopics/)
- Organisation de tous les dossiers de sujets spécialisés avec des noms cohérents
- Ajout de matériaux et exemples sur l'ingénierie contextuelle
- Ajout de documentation sur l'intégration des agents Foundry
- Amélioration de la documentation sur l'intégration de la sécurité Entra ID

## 11 juin 2025

### Création initiale
- Publication de la première version du curriculum MCP pour débutants
- Création de la structure de base pour les 10 sections principales
- Mise en œuvre de la carte visuelle du curriculum pour la navigation
- Ajout de projets d'exemple initiaux dans plusieurs langages de programmation

### Premiers pas (03-GettingStarted/)
- Création des premiers exemples d'implémentation de serveur
- Ajout de conseils pour le développement de clients
- Inclusion des instructions d'intégration des clients LLM
- Ajout de documentation sur l'intégration avec VS Code
- Mise en œuvre d'exemples de serveur avec Server-Sent Events (SSE)

### Concepts fondamentaux (01-CoreConcepts/)
- Ajout d'explications détaillées sur l'architecture client-serveur
- Création de documentation sur les composants clés du protocole
- Documentation des modèles de messagerie dans MCP

## 23 mai 2025

### Structure du dépôt
- Initialisation du dépôt avec une structure de dossiers de base
- Création de fichiers README pour chaque section majeure
- Mise en place de l'infrastructure de traduction
- Ajout d'actifs d'image et de diagrammes

### Documentation
- Création du README.md initial avec aperçu du curriculum
- Ajout de CODE_OF_CONDUCT.md et SECURITY.md
- Mise en place de SUPPORT.md avec des conseils pour obtenir de l'aide
- Création de la structure préliminaire du guide d'étude

## 15 avril 2025

### Planification et cadre
- Planification initiale du curriculum MCP pour débutants
- Définition des objectifs d'apprentissage et du public cible
- Définition de la structure en 10 sections du curriculum
- Développement du cadre conceptuel pour les exemples et études de cas
- Création de prototypes initiaux pour les concepts clés

---

**Avertissement** :  
Ce document a été traduit à l'aide du service de traduction automatique [Co-op Translator](https://github.com/Azure/co-op-translator). Bien que nous nous efforcions d'assurer l'exactitude, veuillez noter que les traductions automatisées peuvent contenir des erreurs ou des inexactitudes. Le document original dans sa langue d'origine doit être considéré comme la source faisant autorité. Pour des informations critiques, il est recommandé de recourir à une traduction humaine professionnelle. Nous ne sommes pas responsables des malentendus ou des interprétations erronées résultant de l'utilisation de cette traduction.