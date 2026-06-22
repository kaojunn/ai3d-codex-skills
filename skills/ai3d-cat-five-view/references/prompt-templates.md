# Prompt Templates

Use one shared identity block for all five views. Change only the `View request` paragraph.

## Shared Prompt Skeleton

```text
Use case: photorealistic-natural
Asset type: AI3D orthographic reference image
Primary request: Generate one <VIEW> orthographic reference image of the same cat from the provided reference photos.
Scene/backdrop: clean white to very light gray studio background, no environment, no props, no text, no watermark.
Subject identity: <IDENTITY BLOCK>
Style/medium: photorealistic studio animal reference, technical AI3D modeling input.
Composition/framing: full body visible, centered, generous padding, strict orthographic view, no perspective angle.
Lighting/mood: even soft studio lighting, minimal ground shadow, neutral technical reference mood.
Constraints: same individual across all five views, same body proportions, same fur length, same major markings and tail.
Avoid: seated pose, lying pose, three-quarter view unless requested, long slim body, wrong eye color, missing tail, thin tail, fused legs, cropped paws, cropped tail, cartoon, toy, fantasy creature, props, environment, text, watermark.
```

## View Requests

### Front

```text
View request: exact front view. The cat faces the camera directly in a neutral four-foot standing pose. The face, chest, front paws, and front color pattern are clearly visible. Both ears are symmetrical. Tail may be visible behind or to the side but must not obscure the body.
```

### Back

```text
View request: exact rear/back view. The cat faces away from the camera in a neutral four-foot standing pose. Back markings, rounded hips, rear paws, tail root, full tail, and tail tip are clearly visible. No face is visible except tiny side edges if natural.
```

### Left Side

```text
View request: exact left side view. The cat head points toward the left side of the image. Body length, backline, belly line, leg spacing, tail root, full tail, and side markings are visible. Use strict side orthographic framing, not three-quarter.
```

### Right Side

```text
View request: exact right side view. The cat head points toward the right side of the image. Body length, backline, belly line, leg spacing, tail root, full tail, and side markings are visible. Use strict side orthographic framing, not three-quarter.
```

### Top

```text
View request: exact top-down orthographic view from directly above. The entire head, torso, four paws, back markings, tail root, full tail, and tail tip are visible. Avoid perspective tilt. The silhouette should match the side/front body proportions.
```

## Review Rubric

Score each view from 0-5:

| Item | 5 | 0 |
| --- | --- | --- |
| View direction | exact requested orthographic view | wrong view or three-quarter |
| Full body | full head/body/paws/tail visible | cropped, missing paws, missing tail |
| Identity | matches anchors | generic or wrong cat |
| Body | matches target proportions | long, thin, tall, or inconsistent |
| Markings | major color blocks stable | random, mirrored wrongly, or absent |
| Tail | correct length/thickness/tip | missing, thin, cropped, glued |
| Background | clean technical reference | environment, props, text, watermark |

Regenerate any view with a 0 in view direction, tail, full body, or identity.
