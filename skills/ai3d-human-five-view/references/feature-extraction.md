# Feature Extraction

Use this checklist to convert character references into a stable identity block before generating five views.

## Identity Definition

Write a concise target statement:

```text
Create the same character as the references: <role>, <age range>, <body type>, <head-to-body ratio>, <face/hair>, <silhouette anchors>, <clothing layers>, <props>, <palette/materials>, <style>.
```

## Feature Dimensions

Extract each dimension from multiple references when possible:

| Dimension | Record | Common mistakes |
| --- | --- | --- |
| Role and archetype | protagonist, NPC, parent, merchant, enemy, worker, fantasy class, civilian role | prompt collapses into generic hero, model, or cosplay figure |
| Age and body type | child/youth/adult/elder, slim/heavy/tall/short/stooped/athletic, posture | adultifying children, making elders too upright, random bodybuilder shape |
| Head-to-body ratio | realistic 7-8 heads, stylized 5-6 heads, chibi 3-4 heads | inconsistent proportions between views |
| Silhouette | large hair, hood, hat, robe, cape, backpack, apron, boots, tool shape | losing the far-view recognizable outline |
| Face and expression | face shape, nose/mouth/eyes, expression intensity, ethnicity/region if specified | glamorized generic face, wrong age, excessive expression |
| Hair/headwear | hair mass, bangs, ponytail, bun, braid, hood, scarf, hat, visible back shape | hair changes between front/back, headwear floats or fuses |
| Neck/shoulders/torso | shoulder width, neck length, chest/waist relationship, spine posture | front and side torso volumes contradict |
| Clothing layers | inner shirt, outer coat/robe, belt, apron, scarf, armor, cape, skirt, pants | merged garments, unreadable openings, random seams |
| Sleeves/hands | sleeve length, cuffs, gloves, visible fingers, hand pose | hands hidden, fused fingers, sleeves swallow hands |
| Lower body/feet | pants/skirt shape, leg length, boots/shoes, sole visibility, stance width | hidden feet, cropped shoes, unstable stance |
| Props/accessories | bags, tools, weapons, jewelry, charms, glasses; separate vs attached | props fused to body, random extra ornaments, missing required prop |
| Materials | cloth, leather, wood, metal, worn fabric, dust, painted surfaces | material only works as texture, not geometry |
| Color palette | main, secondary, accent colors, brightness relationship, color placement | random palette per view, noisy patterns, wrong accent placement |
| Style language | stylized 3D, hand-painted, low-poly planes, anime, painterly, realistic | view set mixes styles or becomes final illustration instead of reference |

## Identity Anchors

Choose 8-12 anchors that must survive every generated view. Good anchors are visible in medium view and distinguish the character from a generic person.

Examples:

- Exact role and age range.
- Head-to-body ratio.
- Body type and posture.
- Large silhouette item such as hood, robe, big hair, backpack, or boots.
- Face shape and expression level.
- Hair mass and back hair shape.
- Neckline, collar, sleeve, belt, hem, and boot structure.
- Required prop and whether it is independent or attached.
- Main color blocking and accent color placement.
- Material language such as worn cloth, leather belt, wooden tool, or hand-painted low-poly planes.

## Negative Constraints

Always include negative constraints for:

- Wrong pose or wrong view angle.
- Wrong age, body type, or head-to-body ratio.
- Hidden hands, fused fingers, cropped feet, or swallowed shoes.
- Merged clothing layers, random garment openings, or unreadable back view.
- Missing required props, fused props, or unrequested weapons.
- Random jewelry, festival costume, religious symbols, regional patterns, or ornaments not in references.
- Photoreal skin when the project requires stylized 3D.
- Dramatic smoke, complex background, scene props, text, watermark, or cinematic lighting.

## AI3D-Specific Priority

For initial AI3D input, prefer:

1. Readable full-body anatomy.
2. Correct head-to-body ratio and silhouette.
3. Clear clothing layer boundaries.
4. Hands, fingers, feet, boots, sleeves, hems, belts, and collars that can be repaired.
5. Back design that matches the front and side logic.
6. Required props that are separated or intentionally attached.
7. Major color blocks and material language.
8. Fine texture, pattern, and surface polish.

Reject beautiful images if structure, pose, identity, or repairability is wrong.
