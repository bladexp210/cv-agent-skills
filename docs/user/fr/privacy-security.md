# Confidentialité et sécurité (aperçu utilisateur)

## Règles permanentes

- **Les PII de carrière vivent hors de ce dépôt.** Identité réelle, YAML de preuves et candidatures restent dans votre arborescence carrière privée. Ce dépôt livre seulement skills, docs et fixtures.
- **Les scripts n’appellent jamais le réseau.** Les scripts fournis utilisent uniquement des I/O fichiers locales. Pas de clients HTTP, sockets ni télémétrie dans le code des scripts.
- **Les chats d’agent sont séparés.** Coller du texte carrière ou des descriptions de poste dans un client Agent Skills peut quitter la machine selon la politique de ce produit. Traitez le texte JD non fiable comme un risque d’injection de prompt.

## Que faire ensuite

1. Gardez les données carrière privées dans votre propre projet carrière — pas dans ce pack de skills.
2. Lisez la matrice complète des scripts pour les lectures / écritures / sorties exactes : [`SECURITY.md`](../../../SECURITY.md) (anglais).
3. Signalez les vulnérabilités via GitHub Security Advisories sur ce dépôt (divulgation privée) — voir EN `SECURITY.md`.

**Langues :** [English SECURITY](../../../SECURITY.md) · [Français](privacy-security.md) · [العربية](../ar/privacy-security.md)
