---
name: ai3d-human-five-view
description: Create consistent AI3D-ready five-view human or stylized character reference images with a rigging-friendly T-pose by default and explicit A-pose override support. Use for people, characters, 人物, 角色, 人设, stylized 3D character workflows, orthographic front/back/left/right/top views, shoulder and armpit separation, T-pose or A-pose input preparation, feature extraction, crop boards, prompt planning, multi-agent image generation, and structure-first review before AI 3D modeling or skeletal rigging.
---

# AI3D Human Five View

Use this skill to convert a human or character reference set into a controlled AI3D input package centered on five orthographic views: front, back, left side, right side, and top. The output should be saved into the user's project directory, not left only under `.codex/generated_images`.

## Required Inputs

Confirm or infer:

- Source photo, concept, or reference directory.
- Subject name or output prefix.
- Output root, defaulting to `Assets/Reference/`.
- Desired pose family: default T-pose, or A-pose only when explicitly requested.
- Whether to update or create a modeling reference document.
- Existing character brief, style guide, three-view sheet, T-pose image, or AI3D input package.

If the user asks to generate images, use the built-in `imagegen` skill/tool by default. Do not use CLI, API, or external model controls unless the user explicitly asks.

## Workflow

1. Inspect the reference set and classify images into P0/P1/P2 production roles.
2. Extract identity and build constraints before prompting: role, age range, body type, head-to-body ratio, silhouette, face, hair, shoulder width, arm span, upper-arm volume, armhole and armpit clearance, clothing layers, hands, feet, props, materials, color palette, and hard rejection traits.
3. Build a local crop board when useful. Use `scripts/build_character_reference_crops.py` with a crop spec to create focused feature crops and a contact sheet.
4. Write or update the modeling reference document with the character brief, feature parameters, style rules, input package paths, prompt strategy, and review rubric.
5. Generate five views with one prompt per view: front, back, left side, right side, top. Keep one shared identity/style block and change only camera direction.
6. Prefer five subagents when the user explicitly requests parallel agents. Assign one output file per worker. If subagents are unavailable, generate sequentially with the same prompts.
7. Run `scripts/organize_generation_outputs.py` after generation. Put final five view images under `GeneratedViews/views/` and prompts, previews, contact sheets, manifests, and other support artifacts under `GeneratedViews/support/`.
8. Run `scripts/make_view_contact_sheet.py` from the `views/` folder and save the review sheet under `support/`.
9. Review structure first: silhouette, proportions, clothing layers, hands, feet, back design, prop separation, style consistency, and AI3D repairability. Do not accept a pretty view with broken structure.

## Output Layout

Default layout:

```text
Assets/Reference/
  <Subject>Photos/
  <Subject>Crops/
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
python3 ~/.codex/skills/ai3d-human-five-view/scripts/build_character_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/HeroPhotos \
  --out-dir Assets/Reference/HeroCrops
```

Organize generated images, prompts, and previews:

```bash
python3 ~/.codex/skills/ai3d-human-five-view/scripts/organize_generation_outputs.py \
  --source-dir .codex/generated_images \
  --views-dir Assets/Reference/HeroGeneratedViews/views \
  --support-dir Assets/Reference/HeroGeneratedViews/support \
  --prefix hero
```

Make a five-view contact sheet:

```bash
python3 ~/.codex/skills/ai3d-human-five-view/scripts/make_view_contact_sheet.py \
  --views-dir Assets/Reference/HeroGeneratedViews/views \
  --prefix hero \
  --out Assets/Reference/HeroGeneratedViews/support/hero_five_view_contact_sheet.png
```

## Non-Negotiables

- Use orthographic, technical reference framing: plain white or light gray background, full body visible, minimal shadow, no scene, no text, no watermark.
- Default to a neutral T-pose: both arms abducted horizontally at shoulder height to form a straight line, elbows extended, palms facing down, fingers naturally together, legs straight, and feet parallel. Use A-pose only when the user explicitly requests it.
- Preserve the same pose across all five views. Side and top views must not lower, bend, omit, or redesign the arms.
- Keep visible background clearance through both armpits. Sleeves, upper arms, shoulders, and torso must have separate readable contours suitable for mesh separation and skeletal rigging.
- Frame wide enough to include both hands at full arm span. Scale the character down or use a wider canvas rather than cropping fingers, hands, hat, or feet.
- Keep one identity/style block across all prompts. The prompt deltas should only describe the view direction.
- Prioritize structure before color: body proportion, head-to-body ratio, silhouette, garment layers, hands, feet, and back design must survive before material polish.
- Keep the project output organized: only the final five angle images belong in `GeneratedViews/views/`; prompts, previews, drafts, review sheets, and manifests belong in `GeneratedViews/support/`.
- Preserve traceability: crops, generated images, prompts, and review notes should point back to source references.
- Treat lowered arms, bent elbows, uneven arm length, closed armpits, sleeves or upper arms fused to the torso, merged clothing, hidden hands/feet, random back design, fused props, or inconsistent proportions as failed AI3D input.
