# Workflow

## 1. Intake

Collect:

- Photo directory and subject name.
- Existing modeling reference document.
- Desired output root.
- Whether the user wants documentation updated.
- Any hard requirements: pose, style, background, image size, naming.

Default output root is `Assets/Reference/`.

## 2. Photo Triage

Classify photos by production role:

| Tier | Use | Examples |
| --- | --- | --- |
| P0 | Identity and must-match references | clear front/3-4 face, body, tail, major color blocks |
| P1 | Local detail support | eye closeups, side body, paws, back markings, fur volume |
| P2 | Weak references | far shots, heavy occlusion, extreme lighting, unusual poses |

Rules:

- Use P0 photos to define the identity block.
- Use P1 photos to repair details, never to override P0 identity.
- Do not use P2 photos as AI3D primary input.
- Do not infer proportions from a single distorted lens angle, crouch, sit, or top-down view.

## 3. Feature Extraction

Extract feature notes before generating prompts. Use `feature-extraction.md` as the checklist.

Required output:

- One paragraph identity definition.
- 8-12 hard identity anchors.
- Negative constraints.
- View-specific constraints.

## 4. Crop Board

Create a crop spec when the photo set is large or when identity details are scattered across photos.

Recommended crop groups:

- Overall identity.
- Standing structure.
- Front face.
- Eyes and muzzle.
- Ears.
- Chest/neck.
- Side body/backline.
- Paws.
- Hindquarters.
- Tail.
- Back markings.
- Color blocks.
- Fur volume.

Use `build_reference_crops.py` to produce local crops and `contact_sheet.jpg`.

## 5. Modeling Reference Document

Write or update a document that includes:

- Purpose and boundary: AI3D input preparation, not final retopology/UV/groom/rigging.
- Reference photo index.
- Feature parameters.
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

Use one shared identity block. Only change the camera/view paragraph. Keep style, background, pose, lighting, and negative constraints identical.

If the user explicitly requests agents, spawn five workers:

- Worker 1 owns front output.
- Worker 2 owns back output.
- Worker 3 owns left side output.
- Worker 4 owns right side output.
- Worker 5 owns top output.

Each worker writes only its assigned file and reports the prompt summary. If subagents are unavailable, generate sequentially.

## 7. Project Save Policy

Built-in image generation saves under `.codex/generated_images` first. Copy final assets into the project output directory and leave the original generated image in place.

Use `organize_generation_outputs.py` immediately after generation so view files and support files do not mix.

Recommended layout:

```text
<Subject>GeneratedViews/
  views/
    <prefix>_front_view.png
    <prefix>_back_view.png
    <prefix>_left_side_view.png
    <prefix>_right_side_view.png
    <prefix>_top_view.png
  support/
    <prefix>_five_view_contact_sheet.png
    <prefix>_organization_manifest.json
    prompts, previews, drafts, and other support files
```

Default to copy mode when organizing from `.codex/generated_images`. Use `--mode move` only when cleaning a project-local folder that already contains mixed generated files.

## 8. Review

Create a contact sheet from `GeneratedViews/views/`, save it to `GeneratedViews/support/`, and check:

- Correct view directions.
- Same individual across views.
- Same pose family and background.
- Full body visible.
- Tail not missing, cropped, or inconsistent.
- Body proportions consistent.
- Color blocks and markings match the identity block.
- No text, watermark, props, environment, or dramatic lighting.

Mark views for regeneration when they fail the rubric in `prompt-templates.md`.
