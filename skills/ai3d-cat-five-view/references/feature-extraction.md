# Feature Extraction

Use this checklist to convert photo observations into a stable identity block.

## Identity Definition

Write a concise target statement:

```text
Create the same cat as the reference photos: <body type>, <head/face>, <eye color/shape>, <fur length>, <color pattern>, <tail>, <pose/temperament>.
```

## Feature Dimensions

Extract each dimension from multiple photos:

| Dimension | Record | Common mistakes |
| --- | --- | --- |
| Overall body | size, roundness, torso length, weight distribution, low/high stance | letting a standing photo make the cat too long or lean |
| Head and face | round/triangular face, muzzle length, cheek volume, forehead markings | cute generic face, fox face, long muzzle |
| Eyes | color, shape, eye spacing, expression | big cartoon eyes, wrong color, over-bright glass eyes |
| Ears | size, spacing, angle, inner fur | oversized ears, folded ears, rabbit-like ears |
| Neck/chest | neck length, ruff, bib shape, chest width | long neck, narrow chest, chest color as flat patch |
| Legs/paws | leg length, sock color, paw shape, stance | long legs, fused paws, missing socks |
| Torso/back | backline, belly line, shoulder/hip volume | thin torso, broken backline, overlong body |
| Tail | length, thickness, curve, tail root, tip color | missing tail, thin tail, tail stuck to body |
| Fur | short/medium/long, volume zones, flow direction | uniform fur length, over-fluffy silhouette, short slick coat |
| Color blocks | white/orange/dark areas, tabby continuity, face marks | random noisy coat, hard paint borders, generic calico |
| Temperament | calm, alert, playful, sleepy | expression that contradicts key references |

## Identity Anchors

Choose 6-10 anchors that must survive every generated view. Good anchors are visible in medium view and distinguish the subject from a generic cat.

Examples:

- Compact low body.
- Round face and short muzzle.
- Large white chest/bib.
- White socks or paw pattern.
- Specific eye color and eye shape.
- Orange cheek patch or dark forehead tabby.
- Bushy tail with dark tip.
- Back/side tabby pattern.

## Negative Constraints

Always include negative constraints for:

- Wrong pose.
- Wrong view angle.
- Wrong body type.
- Wrong face type.
- Wrong eye type.
- Missing or inconsistent tail.
- Fused legs/paws.
- Props, environment, text, watermark.
- Cartoon, toy, fantasy, or over-stylized rendering.

## AI3D-Specific Priority

For initial AI3D input, prefer:

1. Readable anatomy.
2. Correct body silhouette.
3. Correct head/face direction.
4. Tail root and tail length.
5. Major color blocks.
6. Fine material/fur details.

Reject beautiful images if anatomy, pose, or identity is wrong.
