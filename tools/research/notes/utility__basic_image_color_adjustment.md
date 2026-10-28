## Color Balance

**Purpose**: Adjust RGB color balance separately in **shadows, midtones, and highlights**.

**Highlights**: Real-time GPU fragment shader; independent sliders for precise color grading.

**Use when**: Fixing color casts, matching tone across the image, or cinematic split-toning without crushing contrast.

---

## Brightness and Contrast

**Purpose**: Change overall image **brightness** and **contrast**.

**Highlights**: GPU shader; simple controls with fast preview for exposure tweaks.

**Use when**: Brightening underexposed shots, taming highlights, or boosting/separating subject from background.

---

## Image Levels

**Purpose**: Set **black point, white point, and gamma** to control tonal distribution.

**Highlights**: Familiar Levels-style workflow; GPU shader with live preview.

**Use when**: Expanding dynamic range, fixing flat or crushed blacks, before other color passes.

---

## Glow

**Purpose**: Add **bloom / glow** around bright areas of the image.

**Highlights**: GPU shader; adjustable strength, radius, blend mode, and tint color.

**Use when**: Dreamy, neon, or cinematic halation around lights and specular highlights.

---

## Chromatic Aberration

**Purpose**: Simulate lens **color fringing** (e.g. red/cyan edges).

**Highlights**: GPU real-time; adjustable strength and direction for strong stylization.

**Use when**: Vintage, film, or lo-fi lens character; subtle edge accent effects.

---

## Film Grain

**Purpose**: Overlay procedural **film grain** texture.

**Highlights**: GPU shader; control grain size, amount, and related parameters.

**Use when**: Reducing overly clean digital look; adding cinematic texture and depth.

---

## Color Adjustment

**Purpose**: Tune global **saturation, temperature, tint, and vibrance**.

**Highlights**: GPU real-time; broad global grade that complements zone-based Color Balance.

**Use when**: Quick warm/cool shifts or overall saturation changes for mood.

---

## Hue and Saturation

**Purpose**: Shift **hue**, **saturation**, and **lightness**.

**Highlights**: GPU shader; channel or global modes depending on subgraph controls.

**Use when**: Creative recoloring, desaturation, or pushing a specific color palette.

---

## Built-in Color Adjustment Blueprints Demo

This workflow demonstrates built-in image color and tone **subgraphs** from ComfyUI **blueprints**. **Load Image** on the left feeds every branch; **Preview Image** on the right shows each result side by side.

### Tips
- Drag any subgraph from the Comfy Subgraph in the Node library into your own graphs, or keep this layout for comparison.
- All color subgraphs use **GPU fragment shaders** for low-latency preview and export.

### Strongly recommended
Enable **[Nodes 2.0](https://docs.comfy.org/interface/nodes-2)** in ComfyUI settings for proxied subgraph widgets, canvas previews, and a smoother editing experience.