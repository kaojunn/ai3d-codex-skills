# AI3D Input Package

Use this guide when the user wants to move from generated five views into AI3D model generation.

## Purpose

The AI3D stage should produce an initial model that is worth continuing by hand. It is not expected to produce final topology, UVs, textures, rigging, animation, or groom.

Acceptable initial models have repairable proportions, silhouette, clothing hierarchy, and major volumes. Reject models that are only attractive because of texture or rendering.

## Required Content

Prepare the minimum package:

- Character AI3D generation brief.
- Negative constraints.
- Style rules.
- Five orthographic T-pose views, unless the user explicitly requested an A-pose override.
- Prompt files.
- Generation log.

Add optional but recommended support:

- T-pose line art derived from the final views when simplified structural input is useful.
- Head turnaround.
- Prop breakdown.
- Material board.
- Color palette.
- Negative reference board.

## Brief Checklist

The brief must describe:

- Character type and role.
- Age range and body type.
- Head-to-body ratio.
- Pose convention: default T-pose or an explicitly requested A-pose override.
- Shoulder width, shoulder-joint height, arm span, upper-arm volume, palm direction, and required armpit clearance.
- Silhouette keywords.
- Clothing layers from inside to outside.
- Props and whether each prop should be separate.
- Material language and color palette.
- Forbidden symbols, ornaments, costumes, or style drift.

Passing standard: someone can ignore the story and still know the body type, silhouette, clothing stack, required props, and forbidden deviations.

## Concept and Multi-View Requirements

AI3D tools read structure better than atmospheric art. Prefer:

- Plain or light gray background.
- Full body, no cropped feet or hands.
- Front, side, and back views as close to orthographic as possible.
- Consistent body proportions and outfit between views.
- One complete T-pose across all five views: arms horizontal at shoulder height, elbows straight, palms down, fingers naturally together, legs straight, and feet parallel.
- Visible background clearance through both armpits; shoulders, armholes, sleeves, upper arms, and torso are separate readable contours.
- Side views retain strict side cameras while the arms extend along the camera axis; arms must not be lowered for visibility.
- Top view includes the complete fingertip-to-fingertip arm span.
- Sleeves and cuffs not hiding hand shape.
- Back view explicitly designed.
- Line art with style noise removed when preparing T-pose line input.
- Props shown separately when they are important or likely to fuse.

Do not use final mood art as the primary AI3D input when it hides structure behind lighting, smoke, scenery, or action pose.

## Recommended Package Layout

```text
<Subject>AI3DInput/
  01_brief/
    <subject>_AI3D_generation_brief.md
    <subject>_negative_constraints.md
    <subject>_prop_split_list.md
  02_style/
    style_rules.md
    palette.png
    material_board.png
    negative_references.png
  03_character_refs/
    <subject>_front_view.png
    <subject>_back_view.png
    <subject>_left_side_view.png
    <subject>_right_side_view.png
    <subject>_top_view.png
    <subject>_five_view_contact_sheet.png
    <subject>_tpose_line.png
    <subject>_head_turnaround.png
    <subject>_prop_breakdown.png
  04_prompts/
    text_to_3d_prompt.md
    image_to_3d_prompt.md
    negative_prompt.md
  05_runs/
    meshy_v01/
    tripo_v01/
    rodin_v01/
    hunyuan3d_v01/
    compare_sheet.png
    ai3d_generation_log.md
```

## AI3D Prompt Template

```text
stylized 3D game character, full body, orthographic reference input,
complete T-pose, arms horizontal at shoulder height, straight elbows, palms down,
visible background gaps through both armpits, sleeves and upper arms separated from torso,
clear silhouette, consistent head-to-body ratio, readable garment layers,
readable hands and boots, clean collar sleeves belt hem structure,
hand painted material style, low-poly blocky planes where appropriate,
simple background, no dramatic lighting, no environment, no extra ornaments
```

## Negative Prompt Template

```text
photorealistic skin if stylized is required, random jewelry, festival costume,
excessive patterns, merged clothes, fused fingers, hidden feet, cropped body,
lowered arms, bent elbows, raised shoulders, uneven arm length, closed armpits,
sleeves fused to torso, upper arms fused to torso, missing or duplicated arms,
dramatic smoke, complex background, weapon not in reference, unreadable back view,
wrong age, wrong body type, wrong head-to-body ratio, props fused to body
```

## Tool Comparison Strategy

Do not run one generation and decide.

- Choose 2-3 AI3D tools when available.
- Run 3 versions per tool.
- Preserve input images, prompts, negative prompts, parameters, export format, screenshots, and notes.
- Compare gray model structure before evaluating texture.

Typical routes:

| Route | Use | Risk |
| --- | --- | --- |
| Single image to 3D | quick body-mass check | side/back are often guessed |
| Multi-view to 3D | best chance for consistent structure | input views must have matching proportions |
| Text to 3D | early exploration | weak character identity |
| Image plus prompt | practical default | prompt must constrain what image cannot show |

## Result Evaluation

Grade each generated model:

| Check | Pass | Failure |
| --- | --- | --- |
| Silhouette | recognizable from far view | hair, robe, bag, and limbs fuse |
| Proportion | head-to-body, shoulders, hands, and feet match references | adultified, childified, too thin, too bulky |
| T-pose | level shoulder-height arms, straight elbows, palms down, equal arm span | lowered/bent/uneven/missing arms or wrong palm direction |
| Armpits/shoulders | visible clearance and separable shoulder, sleeve, upper-arm, torso volumes | closed armpits or fused mesh-prone contours |
| Front/side/back | back is not random | front and back clothing contradict |
| Clothing layers | inner/outer layers, belt, hem, boots are separate | clothes and body are glued together |
| Hands/feet | fingers, cuffs, shoes can be repaired | melted hands, feet swallowed by hem |
| Props | important props can be separated or rebuilt | props fuse to body |
| Style | gray model already has stylized volumes | only texture looks good |
| Repairability | Blender cleanup is plausible | broken surfaces or unreadable parts dominate |

Conclusion categories:

- A: Use as the main initial model and enter manual cleanup.
- B: Keep only as local reference for head, clothing, prop, or silhouette.
- C: Reject and return to input views or prompts.
