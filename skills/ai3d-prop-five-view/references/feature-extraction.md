# Feature Extraction

Use this checklist to convert prop references into a stable identity block before generating five views.

## Identity Definition

Write a concise target statement:

```text
Create the same single prop as the references: <prop category>, <function>, <main silhouette>, <dimensions/proportions>, <front/back/side/top structure>, <materials>, <colors>, <surface details>, <attachment/contact logic>, <style>.
```

## Feature Dimensions

Extract each dimension from multiple references when possible:

| Dimension | Record | Common mistakes |
| --- | --- | --- |
| Prop category and function | wearable accessory, body-part asset, handheld prop, attached gadget, case, tool, badge | prompt turns it into a generic object or character costume |
| Single-target boundary | exactly what is included and excluded | hat plus head, glasses plus face, case plus hand |
| Overall silhouette | outline, major protrusions, handles, brim, temples, straps, lens shape | losing far-view recognizability |
| Dimensions/proportions | width/height/depth ratio, thin vs bulky, relative scale to wearer if known | wrong thickness, toy scale, oversized details |
| Front design | face-facing geometry, visible logos/details, symmetry | front/back swapped or random front details |
| Back design | rear face, closures, seams, hinges, strap continuation | blank or randomly guessed back |
| Side thickness | object depth, profile curve, edge bevels, hinge thickness, lens thickness, brim thickness | side view becomes flat graphic |
| Top footprint | top silhouette, crown/handle/temple layout, object footprint | top view becomes angled perspective |
| Underside/interior | bottom, inner brim, case inside, lens back, hollow zones | model lacks needed construction information |
| Attachment/contact points | head contact, nose bridge, ears, hand grip, belt clip, shoulder strap, mount points | prop fuses to body or floats |
| Mechanical details | hinges, locks, buttons, screws, clasp, handle, seam lines | over-ornamented fake details |
| Materials | cloth, leather, plastic, metal, glass, rubber, foam, painted wood, worn fabric | material only appears as texture, not geometry |
| Color palette | main, secondary, accent colors, brightness relationship, color placement | random palette per view |
| Surface wear and texture | dust, scratches, stitching, grain, transparent lens, reflective metal | noisy damage or cinematic dirt hides structure |
| Symmetry/asymmetry | mirrored sides, deliberate one-sided detail | accidental asymmetric changes between views |
| Style language | stylized 3D, realistic, hand-painted, low-poly, painterly | view set mixes styles or becomes illustration |

## Category Notes

### Hat

Record crown height, crown top shape, brim width/thickness, brim curve, band color/material, vent holes, inner rim, underside, and head-contact opening. Final views must show only the hat, no head, hair, face, or mannequin.

### Glasses

Record lens shape, frame thickness, bridge, nose pads, hinges, temple arms, transparent lens material, metal/plastic color, and folded/open state. Final views must show only glasses, no eyes, face, ears, or head.

### Eye or Eye Pair

Record whether the target is one eye or a pair. Capture eyeball shape, iris color, pupil shape, sclera color, cornea/gloss, eyelid boundary if it is part of the asset, left/right spacing for pairs, and whether lashes/tear duct are included. Do not include full face, nose, eyebrows, skin patch, or head unless the target explicitly includes an eyelid module.

### Hard Case or Box

Record box dimensions, corner bevels, handle, hinge, latch/lock, panel seams, rubber feet, ridges, material, color, open/closed state, and interior if support view is needed. No hand or character limb in final views.

### Attached Gadget or Badge

Record clip, strap, cable, pin, antenna, screen/button layout, mounting face, thickness, and orientation on the character. Final views isolate the gadget; save wearer/contact placement only as support.

## Identity Anchors

Choose 8-12 anchors that must survive every generated view. Good anchors are visible in medium view and distinguish the prop from a generic object.

Examples:

- Exact prop category and one-target boundary.
- Width/height/depth ratio.
- Distinctive silhouette: brim, handle, lens shape, antenna, clasp, temple arms.
- Front-facing detail placement.
- Back/underside construction.
- Side thickness and bevels.
- Attachment/contact points.
- Main material stack.
- Main color blocks and accent color placement.
- Surface wear or texture level.
- Symmetry or deliberate asymmetry.

## Negative Constraints

Always include negative constraints for:

- Multiple props in one final view.
- Character body, face, head, hair, hands, wearer, mannequin, table scene, environment, text, watermark, or logo unless the logo is part of the target prop.
- Wrong view angle, perspective angle, or three-quarter view.
- Cropped object, hidden thin parts, merged pieces, impossible hinges, random back, missing underside or contact points when required.
- Fused prop-body geometry or ghost wearer in final views.
- Random ornaments, unrequested symbols, excessive decorative patterns, unrelated tools or weapons.
- Material drift, color drift, over-dramatic lighting, smoke, cinematic shadows.

## AI3D-Specific Priority

For initial AI3D prop input, prefer:

1. Single target purity.
2. Correct silhouette and dimensions.
3. Clear front/back/side/top geometry.
4. Readable thickness, bevels, handles, hinges, lenses, straps, locks, seams, or contact points.
5. Logical underside/interior support if needed.
6. Major color blocks and material language.
7. Surface details that can be repaired.

Reject beautiful images if target purity, view direction, thickness, structure, or attachment logic is wrong.
