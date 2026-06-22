---
name: ai3d-human-five-view
description: Create consistent AI3D-ready five-view human or stylized character reference images from photo sets, concept art, character briefs, or design boards. Use for people, characters, 人物, 角色, 人设, stylized 3D character workflows, AI3D five-view packages, orthographic front/back/left/right/top views, T-pose or A-pose input preparation, feature extraction, crop boards, prompt planning, multi-agent image generation, and structure-first review before AI 3D modeling.
---

# AI3D Human Five View

Use this skill to convert a human or character reference set into a controlled AI3D input package centered on five orthographic views: front, back, left side, right side, and top. The output should be saved into the user's project directory, not left only under `.codex/generated_images`.

## Required Inputs

Confirm or infer:

- Source photo, concept, or reference directory.
- Subject name or output prefix.
- Output root, defaulting to `Assets/Reference/`.
- Desired pose family: default A-pose, or T-pose when explicitly requested.
- Whether to update or create a modeling reference document.
- Existing character brief, style guide, three-view sheet, T-pose image, or AI3D input package.

If the user asks to generate images, use the built-in `imagegen` skill/tool by default. Do not use CLI, API, or external model controls unless the user explicitly asks.

## Workflow

1. Inspect the reference set and classify images into P0/P1/P2 production roles.
2. Extract identity and build constraints before prompting: role, age range, body type, head-to-body ratio, silhouette, face, hair, clothing layers, hands, feet, props, materials, color palette, and hard rejection traits.
3. Build a local crop board when useful. Use `scripts/build_character_reference_crops.py` with a crop spec to create focused feature crops and a contact sheet.
4. Write or update the modeling reference document with the character brief, feature parameters, style rules, input package paths, prompt strategy, and review rubric.
5. Generate five views with one prompt per view: front, back, left side, right side, top. Keep one shared identity/style block and change only camera direction.
6. Prefer five subagents when the user explicitly requests parallel agents. Assign one output file per worker. If subagents are unavailable, generate sequentially with the same prompts.
7. Copy final generated images from the built-in generated-images location into the project output directory.
8. Run `scripts/make_view_contact_sheet.py` to make a five-view review sheet.
9. Review structure first: silhouette, proportions, clothing layers, hands, feet, back design, prop separation, style consistency, and AI3D repairability. Do not accept a pretty view with broken structure.

## Output Layout

Default layout:

```text
Assets/Reference/
  <Subject>Photos/
  <Subject>Crops/
  <Subject>GeneratedViews/
    <prefix>_front_view.png
    <prefix>_back_view.png
    <prefix>_left_side_view.png
    <prefix>_right_side_view.png
    <prefix>_top_view.png
    <prefix>_five_view_contact_sheet.png
  <Subject>AI3DInput/
  <Subject>_ModelingReference.md
```

Never overwrite existing generated views unless the user explicitly asks. Use versioned filenames when needed.

## Reference Files

- Read `references/workflow.md` for the complete production sequence and required decisions.
- Read `references/feature-extraction.md` before writing the identity block or judging references.
- Read `references/prompt-templates.md` when preparing five view prompts.
- Read `references/ai3d-input-package.md` when the user asks for an AI3D input package, T-pose package, tool comparison, or generation log.
- Use `references/crop_spec.example.json` as the crop spec shape for `build_character_reference_crops.py`.

## Script Usage

Build local feature crops:

```bash
python3 /Users/a111/.codex/skills/ai3d-human-five-view/scripts/build_character_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/HeroPhotos \
  --out-dir Assets/Reference/HeroCrops
```

Make a five-view contact sheet:

```bash
python3 /Users/a111/.codex/skills/ai3d-human-five-view/scripts/make_view_contact_sheet.py \
  --views-dir Assets/Reference/HeroGeneratedViews \
  --prefix hero \
  --out Assets/Reference/HeroGeneratedViews/hero_five_view_contact_sheet.png
```

## Non-Negotiables

- Use orthographic, technical reference framing: plain white or light gray background, full body visible, minimal shadow, no scene, no text, no watermark.
- Default to neutral A-pose: arms slightly away from torso, palms and fingers readable, feet fully visible. Use T-pose only when requested or when preparing a dedicated T-pose input package.
- Keep one identity/style block across all prompts. The prompt deltas should only describe the view direction.
- Prioritize structure before color: body proportion, head-to-body ratio, silhouette, garment layers, hands, feet, and back design must survive before material polish.
- Preserve traceability: crops, generated images, prompts, and review notes should point back to source references.
- Treat merged clothing, hidden hands/feet, random back design, fused props, or inconsistent proportions as failed AI3D input.
