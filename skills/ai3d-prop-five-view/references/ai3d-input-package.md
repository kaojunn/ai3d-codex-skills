# AI3D Prop Input Package

Use this guide when moving from generated prop five views into AI3D model generation.

## Purpose

The AI3D stage should produce an initial prop model worth continuing by hand. It is not expected to produce final topology, UVs, textures, rigging, animation, or engine integration.

Acceptable initial models have repairable dimensions, silhouette, side thickness, material separation, and major construction volumes. Reject models that only look attractive because of texture or rendering.

## Required Content

Prepare the minimum package:

- Prop AI3D generation brief.
- Negative constraints.
- Style rules.
- Five orthographic views.
- Prompt files.
- Generation log.

Add optional support when useful:

- Bottom view.
- Inside/interior view.
- Exploded construction view.
- Scale/attachment sheet.
- Material board.
- Color palette.
- Negative reference board.

## Brief Checklist

The brief must describe:

- Exact single target prop boundary.
- Prop category and function.
- Width/height/depth proportions.
- Silhouette keywords.
- Front/back/side/top construction.
- Underside/interior needs.
- Attachment/contact points, if any.
- Material stack and color palette.
- Forbidden contaminants and style drift.

Passing standard: someone can ignore the story and still know what object is being modeled, what is excluded, how thick it is, what materials it uses, and how it attaches or functions.

## Concept and Multi-View Requirements

AI3D tools read structure better than atmospheric art. Prefer:

- Plain or light gray background.
- Target prop isolated from character, hand, head, wearer, and scene.
- Front, side, back, and top views as close to orthographic as possible.
- Consistent object proportions and material between views.
- Thin parts, handles, hinges, straps, temples, brim, locks, buttons, seams, lenses, and contact points visible.
- Back view explicitly designed.
- Support view for underside/interior when the final five views cannot show construction.

Do not use final mood art as the primary AI3D input when it hides structure behind lighting, smoke, scenery, hands, clothing, or action pose.

## Recommended Package Layout

```text
<PropName>PropAI3DInput/
  01_brief/
    <prefix>_AI3D_prop_brief.md
    <prefix>_negative_constraints.md
    <prefix>_scale_attachment_notes.md
  02_style/
    style_rules.md
    palette.png
    material_board.png
    negative_references.png
  03_prop_refs/
    five_views/
      <prefix>_front_view.png
      <prefix>_back_view.png
      <prefix>_left_side_view.png
      <prefix>_right_side_view.png
      <prefix>_top_view.png
    support_views/
      <prefix>_bottom_view.png
      <prefix>_inside_view.png
      <prefix>_exploded_view.png
      <prefix>_scale_attachment_sheet.png
      <prefix>_five_view_contact_sheet.png
      <prefix>_organization_manifest.json
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
single isolated 3D prop asset, orthographic reference input,
clear silhouette, consistent dimensions, readable side thickness,
front back side top construction consistent, clean seams hinges straps handles
or attachment points where applicable, material separation, simple background,
no character, no body, no head, no hands, no scene, no extra props
```

## Negative Prompt Template

```text
multiple objects, character body, head, face, hand, fingers, wearer, mannequin,
scene background, dramatic smoke, cropped object, fused parts, missing thickness,
random back design, incorrect scale, extra ornaments, wrong material, unreadable
hinges or straps, logo/text unless part of the prop, props fused to body
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
| Single image to 3D | quick mass check | side/back are guessed |
| Multi-view to 3D | best chance for consistent prop structure | input views must match |
| Text to 3D | early exploration | weak identity and dimensions |
| Image plus prompt | practical default | prompt must constrain what image cannot show |

## Result Evaluation

Grade each generated model:

| Check | Pass | Failure |
| --- | --- | --- |
| Target purity | one prop only | character or extra objects fused in |
| Silhouette | recognizable from far view | key shape missing |
| Proportion | dimensions match references | too flat, too thick, toy scale |
| Front/side/back/top | construction is coherent | random back or impossible depth |
| Thin parts | lenses, handles, straps, brim, hinges, locks are repairable | melted, missing, or fused |
| Material | material zones are separable | only texture looks correct |
| Attachment | contact points are clear if needed | floats or cannot mount |
| Repairability | Blender cleanup is plausible | broken surfaces dominate |

Conclusion categories:

- A: Use as the main initial prop model and enter manual cleanup.
- B: Keep only as local reference for shape, material, or detail.
- C: Reject and return to input views or prompts.
