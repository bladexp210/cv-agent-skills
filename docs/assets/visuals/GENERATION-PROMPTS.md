# Image generation prompts (v1)

Hand this file to an image-gen agent. Do **not** invent extra assets.

**Style (all images):**
- Flat vector / clean line illustration
- White (or near-white) background
- Ink: near-black `#1A1A1A`
- Accent only: slate blue `#2F4A6E`
- No people, no faces, no photos
- No purple gradients, neon glow, 3D clay, or stock-office scenes
- No vendor logos (Cursor, ChatGPT, Google, etc.)
- Little or no tiny text inside the image (labels go in Markdown)
- ESL-friendly: few shapes, clear silhouette, lots of whitespace

**Output folder:** `docs/assets/visuals/`  
**Shipped format:** JPEG (`.jpeg`). PNG drafts are fine for generation; save final embeds as JPEG.  
**Note:** The CV icon may include a simple silhouette for readability (bend of the no-faces rule).

---

## I1 — README hero

**Filename:** `hero-readme.png`  
**Aspect:** 16:9 (about 1600×900)

**Prompt:**

```text
Flat vector documentation hero banner, 16:9, lots of white space.
Near-black ink line art with a single accent color slate blue #2F4A6E on pure white background.
Abstract composition: two simple folder/card shapes connected by a short arrow to a third card suggesting a CV document (rectangle with a few horizontal lines).
Left card suggests a "facts bank" (small checklist marks). Middle/right suggests "tailored document".
No people, no faces, no logos, no screenshots, no purple, no gradients, no glow, no 3D.
Minimal, calm, professional open-source docs style. No readable paragraphs of text; at most 1–2 tiny abstract line labels if needed.
```

---

## I2a — evidence-bank icon

**Filename:** `icon-evidence-bank.png`  
**Aspect:** 1:1 (512×512)

**Prompt:**

```text
Flat vector app icon, square 1:1, centered on transparent or white background.
Simple line icon of a card catalog or evidence folder: rounded rectangle with three horizontal fact lines and one small checkmark.
Colors: near-black #1A1A1A strokes, accent slate blue #2F4A6E for the checkmark or tab only.
No text, no people, no logos, no gradients, no shadows beyond a tiny flat offset if needed.
Clean, thick-enough strokes to stay clear at 64px.
```

---

## I2b — cv-creation icon

**Filename:** `icon-cv-creation.png`  
**Aspect:** 1:1 (512×512)

**Prompt:**

```text
Flat vector app icon, square 1:1, centered on transparent or white background.
Simple line icon of a single-page CV/document with a small arrow or path mark suggesting "tailored for one job".
Colors: near-black #1A1A1A strokes, accent slate blue #2F4A6E for the arrow or header bar only.
No text, no people, no logos, no gradients, no purple, no 3D.
Clean, thick-enough strokes to stay clear at 64px. Visually distinct from a folder/catalog icon.
```

---

## I3 — web-chat path mark

**Filename:** `mark-web-chat.png`  
**Aspect:** 1:1 or 4:3 small (512×512 or 640×480)

**Prompt:**

```text
Small flat vector badge/mark for a "web chat path" in documentation (not a warning, not "weak").
Friendly but professional: simple chat-bubble outline containing a tiny document or folder silhouette, suggesting guided CV help in chat.
Colors: near-black #1A1A1A and slate blue #2F4A6E on white or transparent.
No exclamation marks, no red warning triangle, no "beta" sticker look, no people faces, no vendor logos.
Calm, inviting, clear at small size.
```

---

## Acceptance checklist (for the gen agent)

- [ ] Accent is slate blue `#2F4A6E` only (plus black/white)
- [ ] No faces / no vendor logos
- [ ] Icons readable when shrunk
- [ ] Hero is not a busy infographic
- [ ] Filenames match exactly above
- [ ] Files saved under `docs/assets/visuals/`
