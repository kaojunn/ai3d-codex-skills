# Prompt Templates

Use one shared prop identity/style block for all five final views. Change only the `View request` paragraph.

## Shared Prompt Skeleton

```text
Use case: AI3D prop modeling input
Asset type: orthographic single-prop reference image
Primary request: Generate one <VIEW> orthographic reference image of the same single target prop from the provided references.
Scene/backdrop: clean white to very light gray studio background, no environment, no wearer, no character body, no head, no face, no hands, no mannequin, no table scene, no extra props, no text, no watermark.
Subject identity: <PROP IDENTITY BLOCK>
Style/medium: <PROJECT STYLE>, technical prop modeling reference, clear silhouette and readable geometry.
Composition/framing: full target prop visible, centered, generous padding, strict orthographic view, no perspective angle.
Lighting/mood: even soft studio lighting, minimal ground shadow, neutral technical reference mood.
Constraints: same single prop across all five views, same dimensions, same thickness, same front/back/side/top logic, same material stack, same major colors, same attachment/contact design if applicable.
Avoid: wrong view, perspective angle, three-quarter view, cropped prop, missing thin parts, merged parts, random back design, extra props, character, head, face, hands, body, wearer, mannequin, table, scene background, dramatic smoke, cinematic lighting, text, watermark.
```

## View Requests

### Front

```text
View request: exact front orthographic view. The target prop faces the camera directly. Front silhouette, front face details, main color placement, handles/hinges/lenses/brim/fasteners visible from the front, and attachment/contact points that are visible from the front are clearly readable. Use strict front framing, not three-quarter.
```

### Back

```text
View request: exact rear/back orthographic view. The target prop faces away from the camera. Back silhouette, rear seams, back face details, closures, strap/hinge/temple continuation, back color placement, and rear attachment/contact logic are clearly visible. Do not show the front face except tiny side edges if natural.
```

### Left Side

```text
View request: exact left side orthographic view. The target prop points toward the left side of the image when direction matters. Side thickness, profile curve, bevels, hinge depth, lens/brim/handle/strap thickness, side seam logic, and side contact points are visible. Use strict side framing, not three-quarter.
```

### Right Side

```text
View request: exact right side orthographic view. The target prop points toward the right side of the image when direction matters. Side thickness, profile curve, bevels, hinge depth, lens/brim/handle/strap thickness, side seam logic, and side contact points are visible. Use strict side framing, not three-quarter.
```

### Top

```text
View request: exact top-down orthographic view from directly above. The entire target prop footprint, top silhouette, top surface details, openings, straps, hinges, handles, temples, brim/crown footprint, lens/frame footprint, and top color placement are visible. Avoid perspective tilt. The footprint should match the front and side proportions.
```

## Optional Support View Requests

Support views belong in `GeneratedViews/support/`, not final `views/`.

### Bottom

```text
Support view request: exact bottom orthographic view. Show underside shape, bottom seams, feet, inner rim, base plane, bottom locks, ports, or underside contact surfaces. No character or scene.
```

### Inside

```text
Support view request: clean orthographic inside/interior reference. Show interior cavity, padding, lining, lens backside, hat inner band, case interior, or hollow construction. No character or scene.
```

### Exploded

```text
Support view request: simple exploded technical reference of the same single prop, with major parts separated just enough to show construction. Keep parts aligned and isolated on a plain background. No text labels unless explicitly requested.
```

### Scale/Attachment

```text
Support view request: scale and attachment reference showing how the prop contacts the relevant body area or mounting point. Use a faint neutral ghost silhouette only if necessary. This is support only and must not be used as a final five-view prop image.
```

## Negative Prompt Template

```text
wrong object, multiple props, wrong view, perspective angle, three-quarter view, cropped object, hidden thin parts, fused pieces, random back design, missing side thickness, missing contact points, extra prop, character, human body, head, face, eyes unless target is eye asset, hair, hand, fingers, mannequin, wearer, table scene, environment, dramatic lighting, smoke, complex background, text, watermark, logo unless part of the target prop, final illustration composition
```

## Batch Generation Strategy

Run at least three prompt variants when the first set is uncertain:

| Batch | Priority | Prompt emphasis |
| --- | --- | --- |
| A | Structure first | silhouette, dimensions, front/back/side/top geometry, side thickness |
| B | Detail first | hinges, locks, brim band, lens shape, buttons, seams, attachment points |
| C | Material/color first | palette, material stack, transparent/reflective parts, wear level |

Prefer the batch with the strongest structure and repairability. Do not choose a batch only because the render is attractive.

## Review Rubric

Score each view from 0-5:

| Item | 5 | 0 |
| --- | --- | --- |
| Target purity | exactly one target prop, no contamination | character/body/hand/extra prop present |
| View direction | exact requested orthographic view | wrong view or three-quarter |
| Full object | full object and thin parts visible | cropped or missing critical pieces |
| Identity | matches anchors | generic or wrong object |
| Dimensions | width/height/depth stable | inconsistent or impossible proportions |
| Silhouette | recognizable from distance | loses key shape anchors |
| Thickness | side/top thickness readable | flat graphic or contradictory depth |
| Front/back logic | front and back details are coherent | random or blank back |
| Materials/colors | stable material stack and palette | material/color drift |
| Attachment | contact points readable where required | floats, fuses, or missing mount logic |
| Background | clean technical reference | environment, text, watermark, scene |

Regenerate any view with a 0 in target purity, view direction, full object, identity, dimensions, or thickness.
