# Workflow

## 1. Intake

Collect:

- Reference directory and subject name.
- Existing character brief, style rules, or modeling reference document.
- Desired output root, defaulting to `Assets/Reference/`.
- Required pose: A-pose by default, T-pose only when requested.
- Required style: photoreal, stylized 3D, hand-painted, low-poly, anime, painterly, or project-specific.
- Hard requirements: image size, background, naming, whether to update documentation, and whether to use parallel agents.

## 2. Reference Triage

Classify each input by production role:

| Tier | Use | Examples |
| --- | --- | --- |
| P0 | Identity and must-match structure | clear full-body front/three-quarter, final concept sheet, approved three-view, approved T-pose |
| P1 | Local detail support | face closeup, hair detail, hands, boots, garment closeups, back accessory, color/material board |
| P2 | Weak reference | heavy perspective, cropped body, strong lighting, mood art, occluded action pose, inconsistent outfit |

Rules:

- Use P0 references to define the identity and structure block.
- Use P1 references to repair local details, never to override P0 identity.
- Use P2 only as style or mood support when it does not contradict P0.
- Do not infer body proportions from a single distorted camera angle or cropped image.
- Separate current character facts from possible redesign ideas.

## 3. Brief and Feature Extraction

Write the character as buildable constraints before generating images:

- One paragraph identity definition.
- 8-12 hard identity anchors.
- Negative constraints.
- Pose and view constraints.
- Style rules and material language.
- Prop separation decisions.

Use `feature-extraction.md` as the checklist. The brief should answer: role, age range, body type, head-to-body ratio, silhouette, clothing layers, hands, feet, hair, props, color palette, materials, and forbidden deviations.

## 4. Crop Board

Create a crop spec when the reference set is large, inconsistent, or scattered.

Recommended crop groups:

- Full-body silhouette.
- Front structure.
- Side structure.
- Back design.
- Face and expression.
- Hair shape.
- Headwear or large silhouette element.
- Torso and neckline.
- Sleeves and hands.
- Waist, belt, apron, or middle layer.
- Legs, pants, skirt, boots, and feet.
- Props, bags, tools, weapons, or accessories.
- Materials and color palette.

Use `build_character_reference_crops.py` to produce local crops and `contact_sheet.jpg`.

## 5. Modeling Reference Document

Write or update a project-local document that includes:

- Purpose and boundary: AI3D input preparation, not final retopology, UV, texture, rigging, or animation.
- Reference index and P0/P1/P2 roles.
- Character brief and identity anchors.
- Feature parameter table.
- Style rules, palette, materials, and forbidden references.
- Five-view generation strategy.
- Prompt templates and negative prompts.
- Review rubric and rejection rules.
- Saved output paths.

## 6. Five-View Generation

Generate five independent images:

- Front.
- Back.
- Left side.
- Right side.
- Top.

Use one shared identity/style block. Only change the `View request` paragraph. Keep pose, background, lighting, line/rendering style, and negative constraints identical.

If the user explicitly requests agents, spawn five workers:

- Worker 1 owns front output.
- Worker 2 owns back output.
- Worker 3 owns left side output.
- Worker 4 owns right side output.
- Worker 5 owns top output.

Each worker writes only its assigned file and reports the prompt summary. If subagents are unavailable, generate sequentially.

## 7. AI3D Input Package

When preparing for actual AI3D generation, save:

```text
<Subject>AI3DInput/
  01_brief/
    <subject>_AI3D_generation_brief.md
    <subject>_negative_constraints.md
  02_style/
    style_rules.md
    palette.png
    material_board.png
    negative_references.png
  03_character_refs/
    <subject>_five_view_contact_sheet.png
    <subject>_front_view.png
    <subject>_back_view.png
    <subject>_left_side_view.png
    <subject>_right_side_view.png
    <subject>_top_view.png
    <subject>_tpose_color.png
    <subject>_tpose_line.png
    <subject>_head_turnaround.png
    <subject>_prop_breakdown.png
  04_prompts/
    text_to_3d_prompt.md
    image_to_3d_prompt.md
    negative_prompt.md
```

T-pose, line art, head turnaround, prop breakdown, material board, and palette are optional unless the target AI3D tool requires them.

## 8. Project Save Policy

Built-in image generation saves under `.codex/generated_images` first. Copy final assets into the project output directory and leave the original generated image in place.

Recommended names:

```text
<prefix>_front_view.png
<prefix>_back_view.png
<prefix>_left_side_view.png
<prefix>_right_side_view.png
<prefix>_top_view.png
<prefix>_five_view_contact_sheet.png
```

## 9. Review

Create a contact sheet and check:

- Correct orthographic view direction.
- Same individual across all views.
- Same pose family and background.
- Full body visible with hands, feet, hair, clothing, and props not cropped.
- Head-to-body ratio and body proportions stay consistent.
- Front, side, and back garment layers do not contradict each other.
- Back view is designed, not randomly guessed.
- Hands, fingers, shoes, hems, belts, and sleeves are readable enough to repair.
- Props are separate or intentionally attached; no accidental fusion.
- Color palette and material language match the brief.
- No environment, dramatic lighting, smoke, text, watermark, or random ornaments.

Regenerate any view that fails view direction, identity, proportions, hands/feet readability, back design, or prop separation.
