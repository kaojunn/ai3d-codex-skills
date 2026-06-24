# AI3D Handoff

Use this guide after the user selects one variant.

## Selection Record

Record:

- Selected variant number and path.
- Why its silhouette and proportions were chosen.
- Which shape changes are now approved and locked.
- Any detail that still needs manual correction.
- The original P0 references used to preserve colors, patterns, materials, and signature details.

## Five-View Handoff

Invoke `ai3d-prop-five-view` with:

- The selected variant as the primary P0 front reference.
- Original P0/P1 references for back, side, top, material, pattern, attachment, and construction facts.
- The selected variant's locked identity and approved shape parameters.
- A warning not to revert the selected geometry to the original prototype.

The later five-view run must infer missing angles from construction logic while keeping the selected front silhouette fixed.

## Recommended Handoff Layout

```text
<PropName>PropVariants/
  final/
    <prefix>_variant_XX_front.png
  support/
    <prefix>_variation_plan.json
    <prefix>_five_variants_contact_sheet.png

<PropName>PropPhotos/
<PropName>PropCrops/
<PropName>PropGeneratedViews/
<PropName>_PropModelingReference.md
```

## Boundary

This skill does not create side, back, top, bottom, inside, exploded, or scale views. It does not create topology, UVs, textures, rigs, or engine-ready assets.
