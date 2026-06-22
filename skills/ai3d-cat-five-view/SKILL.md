---
name: ai3d-cat-five-view
description: Create consistent AI3D-ready five-view cat reference images from photo sets. Use when turning cat or similar pet reference photos into front, back, left side, right side, and top orthographic images for AI3D/3D modeling, including photo triage, feature extraction, crop boards, prompt planning, multi-agent image generation, and view consistency review.
---

# AI3D Cat Five View

Use this skill to convert a cat reference photo set into a controlled five-view image package for AI3D modeling: front, back, left side, right side, and top. The output should be a project-local asset package, not loose preview images left under `.codex/generated_images`.

## Required Inputs

Confirm or infer:

- Source photo directory.
- Subject name or output prefix.
- Output root, defaulting to `Assets/Reference/`.
- Whether the user wants project-specific documentation updated.
- Existing identity/reference document, if any.

If the user asks to generate images, use the built-in `imagegen` skill/tool by default. Do not use CLI fallback unless the user explicitly asks for CLI/API/model controls.

## Workflow

1. Inspect the photo set and classify images into P0/P1/P2 reference roles.
2. Extract identity features before prompting: body type, head/face, eyes, ears, legs/paws, tail, fur, color blocks, and hard rejection traits.
3. Build a local crop board when useful. Use `scripts/build_reference_crops.py` with a crop spec to create focused feature crops and a contact sheet.
4. Write or update the modeling reference document with the identity anchors, feature parameters, photo roles, and AI3D constraints.
5. Generate five views with one prompt per view: front, back, left side, right side, top. Keep the shared identity block identical and change only camera direction.
6. Prefer five subagents when the user explicitly requests parallel agents. Assign one output file per worker. If subagents are unavailable, generate sequentially with the same prompts.
7. Run `scripts/organize_generation_outputs.py` after generation. Put final five view images under `GeneratedViews/views/` and prompts, previews, contact sheets, manifests, and other support artifacts under `GeneratedViews/support/`.
8. Run `scripts/make_view_contact_sheet.py` from the `views/` folder and save the review sheet under `support/`.
9. Review and report risks: view direction, pose, body consistency, color consistency, tail continuity, background cleanliness, and whether any view is too stylized or too far from the subject.

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
  <Subject>_ModelingReference.md
```

Never overwrite existing generated views unless the user explicitly asks. Use versioned filenames when needed.

## Reference Files

- Read `references/workflow.md` for the complete production sequence and required decisions.
- Read `references/feature-extraction.md` before writing the identity block or judging references.
- Read `references/prompt-templates.md` when preparing the five view prompts.
- Use `references/crop_spec.example.json` as the crop spec shape for `build_reference_crops.py`.

## Script Usage

Build local feature crops:

```bash
python3 ~/.codex/skills/ai3d-cat-five-view/scripts/build_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/CatPhotos \
  --out-dir Assets/Reference/CatCrops
```

Organize generated images, prompts, and previews:

```bash
python3 ~/.codex/skills/ai3d-cat-five-view/scripts/organize_generation_outputs.py \
  --source-dir .codex/generated_images \
  --views-dir Assets/Reference/CatGeneratedViews/views \
  --support-dir Assets/Reference/CatGeneratedViews/support \
  --prefix cat
```

Make a five-view contact sheet:

```bash
python3 ~/.codex/skills/ai3d-cat-five-view/scripts/make_view_contact_sheet.py \
  --views-dir Assets/Reference/CatGeneratedViews/views \
  --prefix cat \
  --out Assets/Reference/CatGeneratedViews/support/cat_five_view_contact_sheet.png
```

## Non-Negotiables

- Use orthographic, technical reference framing: plain light background, complete body, minimal shadow, no props, no text.
- Use four-foot neutral standing pose for front/back/side views unless the user explicitly asks otherwise.
- Keep identity consistent across all prompts. The prompt deltas should only describe the view direction.
- Keep the project output organized: only the final five angle images belong in `GeneratedViews/views/`; prompts, previews, drafts, review sheets, and manifests belong in `GeneratedViews/support/`.
- Preserve traceability: every crop and generated image should be traceable to source photos, prompt text, and review notes.
- Treat a pretty image with wrong anatomy or wrong identity as a failed AI3D input.
