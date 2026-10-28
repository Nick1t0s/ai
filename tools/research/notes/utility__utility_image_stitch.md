# Image Stitch Grid Workflow

4 images → 2×2 grid → saved at 2048×2048.

**How it chains:**
1. `Image Stitch (right)` — joins top-left + top-right into a row
2. `Image Stitch (right)` — joins bottom-left + bottom-right into a row
3. `Image Stitch (down)` — stacks both rows into the final grid

**Key settings:**
- `direction` — `right` for horizontal, `down` for vertical
- `match_image_size: ON` — auto-resizes mismatched inputs