# CV Agent Skills — docs utilisateur (fr)

**De quoi il s’agit :** des [Agent Skills](https://agentskills.io/home) installables pour une banque de faits privée (`evidence-bank`, banque de faits) et un pipeline CV par candidature (`cv-creation`, pipeline CV).

**Ensuite :** ouvrir [`quick-start.md`](quick-start.md) (≈5 minutes), ou choisir une invite d’installation ci-dessous.

| Situation | Résultat | Ouvrir | Recommandation |
| :--- | :--- | :--- | :--- |
| Client Agent Skills **et** disposition à installer Python, bibliothèques et outils développeur associés (première fois) | Skills installés + validate/export **répétable** via scripts locaux | [`../../../prompts/fr/install-full.md`](../../../prompts/fr/install-full.md) | **Préférer Full** quand le client et la pile Python sont tous deux disponibles. |
| Client Agent Skills **mais** impossibilité ou refus d’installer cette pile Python (première fois) | Les skills se chargent dans l’agent ; artefacts surtout via l’agent (polissage possible dans Word / Docs / LibreOffice). Garanties scripts plus faibles | [`../../../prompts/fr/install-lite.md`](../../../prompts/fr/install-lite.md) | **Préférer Lite** quand vous avez un client mais refusez ou ne pouvez pas installer Python. |
| **Pas** de client Agent Skills — chatbot navigateur seulement | Méga-prompt structuré + enregistrer les fichiers hors du chat | [`web-chat.md`](web-chat.md) | Utiliser le Web chat **seulement** si vous n’avez pas de client skills. |

**Langues :** [English (SoT)](../../../README.md) · [Français](README.md) · [العربية](../ar/README.md)

**Confidentialité (court) :** [`privacy-security.md`](privacy-security.md) — matrice complète : [`SECURITY.md`](../../../SECURITY.md).

**Pour les mainteneurs :** [`docs/README.md`](../../README.md) (anglais).
