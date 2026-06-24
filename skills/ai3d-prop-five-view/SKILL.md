---
name: ai3d-prop-five-view
description: Create consistent AI3D-ready five-view reference images for exactly one prop, detachable accessory, or separable character part at a time. Use for 道具, 配件, 部件, 帽子, 眼镜, 眼睛, 手提箱, 工具, 徽章, radios, bags, weapons, handheld props, wearable accessories, prop extraction from character sheets, one-prop crop boards, orthographic front/back/left/right/top prop views, support views such as bottom/inside/exploded, AI3D prop input packages, and structure-first prop review before 3D modeling.
---

# AI3D Prop Five View

Use this skill to extract one target prop or detachable part from reference images and prepare a controlled AI3D input package: front, back, left side, right side, and top orthographic views. Each run handles exactly one target object. Do not mix a hat with glasses, a case with a hand, or eyes with a face in the final `views/` images.

## Required Inputs

Confirm or infer:

- Source photo, concept, crop, or reference directory.
- Single target prop/part name and output prefix.
- Prop category: wearable accessory, body-part asset, handheld prop, attached gadget, surface detail, or hard-surface object.
- Output root, defaulting to `Assets/Reference/`.
- Whether optional support views are needed: bottom, inside, exploded, scale/attachment sheet.
- Whether to create or update a prop modeling reference document.
- Existing character brief, prop split list, style guide, material board, or AI3D input package.

If the user asks to generate images, use the built-in `imagegen` skill/tool by default. Do not use CLI, API, or external model controls unless the user explicitly asks.

## Workflow

1. Enforce one-prop-per-run. If the source includes several props, select one target and treat all other objects as forbidden contaminants.
2. Inspect references and classify images into P0/P1/P2 production roles.
3. Extract prop constraints before prompting: category, function, silhouette, dimensions, front/back design, side thickness, top footprint, underside/interior, attachment/contact points, materials, colors, surface wear, symmetry/asymmetry, and hard rejection traits.
4. Build a local crop board when useful. Use `scripts/build_prop_reference_crops.py` with a crop spec to create focused feature crops and a contact sheet.
5. Write or update the prop modeling reference document with reference roles, feature parameters, style rules, scale/attachment notes, prompt strategy, and review rubric.
6. Generate five final views with one prompt per view: front, back, left side, right side, top. Keep one shared prop identity/style block and change only camera direction.
7. Generate optional support images only when useful: bottom, inside, exploded, scale/attachment. Support images must go under `GeneratedViews/support/`, not final `views/`.
8. Run `scripts/organize_generation_outputs.py` after generation. Put final five view images under `GeneratedViews/views/`; put prompts, previews, drafts, rejected images, support views, contact sheets, and manifests under `GeneratedViews/support/`.
9. Run `scripts/make_view_contact_sheet.py` from the `views/` folder and save the review sheet under `support/`.
10. Review structure first: single-target purity, view direction, dimensions, thickness, attachment logic, material/color consistency, no character contamination, and AI3D repairability.

## Output Layout

Default layout:

```text
Assets/Reference/
  <PropName>PropPhotos/
  <PropName>PropCrops/
  <PropName>PropGeneratedViews/
    views/
      <prefix>_front_view.png
      <prefix>_back_view.png
      <prefix>_left_side_view.png
      <prefix>_right_side_view.png
      <prefix>_top_view.png
    support/
      <prefix>_five_view_contact_sheet.png
      <prefix>_organization_manifest.json
      <prefix>_bottom_view.png
      <prefix>_inside_view.png
      <prefix>_exploded_view.png
      <prefix>_scale_attachment_sheet.png
      prompts/
      drafts/
      rejected/
  <PropName>PropAI3DInput/
  <PropName>_PropModelingReference.md
```

Never overwrite existing generated views unless the user explicitly asks. Use versioned filenames when needed.

## Reference Files

- Read `references/workflow.md` for the complete one-prop production sequence and required decisions.
- Read `references/feature-extraction.md` before writing the prop identity block or judging references.
- Read `references/prompt-templates.md` when preparing five-view prompts.
- Read `references/ai3d-input-package.md` when preparing an AI3D prop input package or generation log.
- Use `references/crop_spec.example.json` as the crop spec shape for `build_prop_reference_crops.py`.

## Script Usage

Build local feature crops:

```bash
python3 ~/.codex/skills/ai3d-prop-five-view/scripts/build_prop_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/HatPropPhotos \
  --out-dir Assets/Reference/HatPropCrops
```

Organize generated images, prompts, support views, and rejected drafts:

```bash
python3 ~/.codex/skills/ai3d-prop-five-view/scripts/organize_generation_outputs.py \
  --source-dir .codex/generated_images \
  --views-dir Assets/Reference/HatPropGeneratedViews/views \
  --support-dir Assets/Reference/HatPropGeneratedViews/support \
  --prefix hat
```

Make a five-view contact sheet:

```bash
python3 ~/.codex/skills/ai3d-prop-five-view/scripts/make_view_contact_sheet.py \
  --views-dir Assets/Reference/HatPropGeneratedViews/views \
  --prefix hat \
  --out Assets/Reference/HatPropGeneratedViews/support/hat_five_view_contact_sheet.png
```

## Non-Negotiables

- Process exactly one target prop or one defined prop pair/group per run. A pair of eyes or a pair of glasses can be one target; a hat plus glasses cannot.
- Use orthographic, technical reference framing: plain white or light gray background, full object visible, minimal shadow, no scene, no text, no watermark.
- Final `GeneratedViews/views/` images must contain only the target prop. No character body, head, face, hands, mannequin, wearer, table scene, extra props, or attachment ghost.
- Keep one identity/style block across all prompts. The prompt deltas should only describe camera direction.
- Put bottom, inside, exploded, scale, attachment, drafts, and rejected images under `GeneratedViews/support/`, never in final `views/`.
- Preserve traceability: crops, prompts, generated images, support views, rejected drafts, and review notes should point back to source references.
- Treat a pretty prop image with wrong view, fused character parts, missing thickness, random back design, inconsistent material, or multiple target objects as failed AI3D input.
