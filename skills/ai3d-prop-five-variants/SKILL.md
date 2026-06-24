---
name: ai3d-prop-five-variants
description: "Create five consistent front-view design variants from exactly one prop reference: one standardized prototype and four controlled shape derivatives. Use for 道具派生, 物品变体, 五件同系列道具, 器型变化, shape exploration, silhouette variants, product-family concept sheets, prop style preservation, and AI3D prop concept selection where color, pattern, material, wear, function, and identity details must stay fixed while outline and major geometry change."
---

# AI3D Prop Five Variants

Use this skill to derive five isolated front-view prop concepts from one reference identity. Generate one standardized prototype plus four medium-strength shape variants. Keep category, function, palette, pattern, material, wear, era/style, and signature details fixed. Change only planned shape variables.

This skill is for design selection. It does not generate front/back/left/right/top views or a 3D model. After selection, pass the chosen variant to `ai3d-prop-five-view`.

## Required Inputs

Confirm or infer:

- Source photo, concept, crop, or reference directory.
- One target prop name and output prefix.
- Output root, defaulting to `Assets/Reference/`.
- Prop category and function.
- Existing palette, pattern, material, or project style rules.
- Whether to create or update `<PropName>_PropVariantReference.md`.

If the user asks to generate images, use the built-in `imagegen` skill/tool by default. Do not use CLI, API, or external model controls unless explicitly requested.

## Workflow

1. Enforce one-prop-per-run. Treat characters, hands, scenes, and other objects as forbidden contaminants.
2. Classify references into P0/P1/P2 roles and isolate the target with crops when useful.
3. Extract `Locked Features` and `Variable Features` before prompting. Read `references/feature-lock-and-variation.md`.
4. Write a variation plan from `references/variation_plan.example.json`. Give each variant one primary shape axis and at most one secondary axis.
5. Generate five independent exact-front orthographic images with identical framing, scale basis, background, lighting, rendering style, and locked features:
   - `variant_01`: standardized prototype.
   - `variant_02`: overall proportion and silhouette.
   - `variant_03`: main body-to-base/rim/top mass ratio.
   - `variant_04`: edge, corner, and contour curvature.
   - `variant_05`: one major accessory structure.
6. Run `scripts/organize_variant_outputs.py`. Put exactly five final images under `PropVariants/final/`; put prompts, drafts, rejected images, plans, contact sheets, and manifests under `PropVariants/support/`.
7. Run `scripts/make_variant_contact_sheet.py` and compare all five in numeric order.
8. Reject identity drift, material/color/pattern drift, weak variation, excessive redesign, perspective views, or contamination.
9. Record the selected variant and hand it to `ai3d-prop-five-view` as a P0 front reference.

## Output Layout

```text
Assets/Reference/
  <PropName>VariantPhotos/
  <PropName>VariantCrops/
  <PropName>PropVariants/
    final/
      <prefix>_variant_01_front.png
      <prefix>_variant_02_front.png
      <prefix>_variant_03_front.png
      <prefix>_variant_04_front.png
      <prefix>_variant_05_front.png
    support/
      <prefix>_five_variants_contact_sheet.png
      <prefix>_variation_plan.json
      <prefix>_organization_manifest.json
      prompts/
      drafts/
      rejected/
  <PropName>_PropVariantReference.md
```

Never overwrite existing final variants unless explicitly requested. Use versioned filenames when needed.

## Reference Files

- Read `references/workflow.md` for the complete production sequence and review gates.
- Read `references/feature-lock-and-variation.md` before writing the shared identity block or variation plan.
- Read `references/prompt-templates.md` before generating the five images.
- Read `references/ai3d-handoff.md` when a variant is selected for five-view or 3D preparation.
- Use `references/crop_spec.example.json` for crop-board structure.
- Use `references/variation_plan.example.json` for the machine-readable variation plan.

## Script Usage

Build target crops:

```bash
python3 ~/.codex/skills/ai3d-prop-five-variants/scripts/build_prop_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/VaseVariantPhotos \
  --out-dir Assets/Reference/VaseVariantCrops
```

Organize generated variants:

```bash
python3 ~/.codex/skills/ai3d-prop-five-variants/scripts/organize_variant_outputs.py \
  --source-dir .codex/generated_images \
  --final-dir Assets/Reference/VasePropVariants/final \
  --support-dir Assets/Reference/VasePropVariants/support \
  --prefix vase \
  --variation-plan variation_plan.json
```

Make the comparison sheet:

```bash
python3 ~/.codex/skills/ai3d-prop-five-variants/scripts/make_variant_contact_sheet.py \
  --final-dir Assets/Reference/VasePropVariants/final \
  --prefix vase \
  --out Assets/Reference/VasePropVariants/support/vase_five_variants_contact_sheet.png
```

## Non-Negotiables

- Process exactly one target prop identity per run.
- Generate five front orthographic images, not five camera views.
- Keep `variant_01` as a clean standardized rendering of the prototype.
- Keep category, function, era/style, palette, pattern content and placement, material stack, wear language, and signature details fixed across all variants.
- Give variants 02-05 meaningful but controlled shape differences. Do not merely recolor, retexture, rotate, resize the canvas, or change camera perspective.
- Limit each derivative to one primary and at most one secondary shape axis.
- Allow patterns to conform proportionally to changed surfaces; do not add, remove, replace, mirror, or relocate motifs without explicit approval.
- Final images must contain one isolated prop only: no character, hand, wearer, mannequin, table scene, environment, extra prop, text, or watermark.
- Put only the five final variants in `final/`. Put all combined sheets and non-final artifacts in `support/`.
