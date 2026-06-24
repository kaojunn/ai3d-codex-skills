# Workflow

## 1. Intake and Boundary

Collect the reference directory, one target prop name, prefix, category, function, output root, project style, and any approved palette or material board. Every run handles one prop identity only. A coherent pair or inseparable set is acceptable only when it is intended as one asset, such as one pair of glasses.

Exclude characters, hands, heads, wearers, stands, tables, scenery, and unrelated objects from final images.

## 2. Reference Triage

Classify sources:

| Tier | Use |
| --- | --- |
| P0 | Approved prop identity, silhouette, colors, patterns, materials, signature details |
| P1 | Local construction, pattern, wear, attachment, and material details |
| P2 | Weak, occluded, perspective-heavy, scene-lit, or inconsistent references |

Use P0 to define locked identity. Use P1 to repair details. Use P2 only when it does not contradict P0.

## 3. Crop Board

Create crops when the target is small, attached, occluded, or mixed with other objects. Recommended crops:

- Overall prop and front silhouette.
- Main color blocks and pattern regions.
- Material and surface wear.
- Signature hardware or construction.
- Shape-variable regions such as rim, base, neck, handle, frame, corners, or supports.
- Forbidden contaminants when useful.

Use `build_prop_reference_crops.py` and save its contact sheet under `<PropName>VariantCrops/`.

## 4. Lock and Variation Plan

Record:

- Locked category, function, style/era, palette, pattern, materials, wear, components, and signature details.
- Variable silhouette, width/height ratio, mass distribution, contour curvature, and one accessory geometry.
- Global forbidden changes.
- One primary and at most one secondary shape axis for each derivative.

Use `variation_plan.example.json`. Do not start generation until the five entries are distinct and non-conflicting.

## 5. Generation

Use one shared identity/style block for all images. Keep exact front orthographic camera, object-facing direction, image dimensions, object scale basis, vertical alignment, background, lighting, and rendering style unchanged.

Generate:

1. Standardized prototype.
2. Overall proportion/silhouette derivative.
3. Main mass-ratio derivative.
4. Edge/contour derivative.
5. Accessory-structure derivative.

When five agents are explicitly requested, assign one variant per agent and provide the same locked block plus only that variant's delta.

## 6. Organization

Run `organize_variant_outputs.py`. The script must fail on missing or duplicate variant numbers unless explicit mappings resolve the ambiguity. Save exactly five final images under `final/`.

Save plans, prompts, previews, drafts, rejected images, and manifests under `support/`. Use copy mode for `.codex/generated_images`; use move mode only for a project-local staging folder.

## 7. Review

Create a contact sheet and check:

- Exactly one target prop per image.
- All five are exact front orthographic views.
- `variant_01` matches the prototype identity.
- Variants 02-05 show meaningful shape differences.
- The five still read as one product or artifact family.
- Category, function, style/era, color placement, pattern identity, material, wear, and signature details remain fixed.
- Patterns conform naturally to changed surfaces without new motifs or relocation.
- No change is caused only by camera, pose, crop, lighting, color, or texture.
- No character, hand, scene, text, watermark, or extra object appears.

Reject any image with identity drift, wrong camera, contamination, material/color/pattern drift, negligible shape change, or redesign beyond the planned axes.

## 8. Selection and Handoff

Record the chosen variant number and reason in `<PropName>_PropVariantReference.md`. Copy or reference that image as a P0 front source for `ai3d-prop-five-view`. The selected shape becomes locked identity for the later five-view run.
