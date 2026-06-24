# Prompt Templates

Use one shared locked block for all five images. Keep the camera and rendering block identical. Change only the variant delta.

## Shared Prompt

```text
Use case: AI3D prop concept selection before multi-view generation.
Asset type: one isolated single-prop exact-front orthographic reference image.
Primary request: Generate <VARIANT NAME> of the same target prop identity from the references.
Scene/backdrop: clean white to very light gray studio background; no environment, wearer, character, body, head, face, hands, mannequin, table, extra props, text, or watermark.
Locked identity: <CATEGORY, FUNCTION, ERA/STYLE, REQUIRED COMPONENTS, SIGNATURE DETAILS>.
Locked appearance: preserve the exact main/secondary/accent color placement, motif content and structural location, material stack, texture, glaze/wear language, and rendering style.
Composition: target faces the camera directly; exact front orthographic view; full object centered with generous equal padding; same image dimensions, object scale basis, baseline, and alignment as the other variants; no three-quarter angle.
Lighting: identical even soft studio lighting, minimal neutral shadow.
Allowed change: <VARIANT DELTA>.
Constraints: change shape only; keep function and component logic plausible; one primary and at most one secondary shape axis.
Avoid: camera change, object rotation, perspective, crop change, recolor, new pattern, removed pattern, relocated motif, new material, changed wear, added ornament, missing component, extra object, character contamination, scene, text, watermark.
```

## Variant Deltas

### Variant 01

```text
Variant delta: standardized prototype. Preserve the source shape and proportions. Only isolate, clean, center, and clarify the original prop as an exact front orthographic technical reference. Do not redesign it.
```

### Variant 02

```text
Variant delta: medium controlled overall-proportion derivative. Change the width-to-height ratio and main outer silhouette, with a compatible taper as the only secondary change. Preserve all locked features and component relationships.
```

### Variant 03

```text
Variant delta: medium controlled mass-distribution derivative. Change the proportion between the main body and its base, rim, top, lid, neck, or equivalent structural zone. Adjust only the transition position as a secondary change.
```

### Variant 04

```text
Variant delta: medium controlled contour derivative. Change the dominant edge radius, corner treatment, shoulder curve, or side contour language. Do not change the component inventory, colors, patterns, or materials.
```

### Variant 05

```text
Variant delta: medium controlled accessory-geometry derivative. Change the shape of one major accessory structure such as a handle, frame temple, brim, foot, support, or latch zone, with its mounting position as the only secondary change. Preserve its function and all other geometry families.
```

## Negative Prompt

```text
different object category, changed function, changed historical era, unrelated style,
multiple objects, side view, back view, top view, three-quarter view, perspective,
rotated object, cropped object, camera variation, lighting variation, color variation,
new color, missing color block, new motif, missing motif, mirrored motif, relocated motif,
new material, changed texture, changed wear, added ornament, missing component,
character, human, hand, fingers, head, face, wearer, mannequin, table, environment,
dramatic shadow, smoke, text, watermark, comparison sheet inside final image
```

## Review Rubric

Score each image 0-5:

| Item | 5 | 0 |
| --- | --- | --- |
| Target purity | One isolated prop | Character, scene, or extra object |
| Front view | Exact front orthographic | Side, top, back, or perspective |
| Identity | Same category, function, era, components | Different object |
| Shape delta | Matches planned axes | No geometry change or uncontrolled redesign |
| Family coherence | Clearly one series | Unrelated concepts |
| Palette | Exact color hierarchy and placement | Recolored |
| Pattern | Same motifs and regions | New, missing, or relocated motifs |
| Material/wear | Same stack and surface language | Material or wear drift |
| Functional logic | Plausible construction | Broken or missing relationships |

Regenerate any image with 0 in target purity, front view, identity, shape delta, palette, pattern, or material/wear.
