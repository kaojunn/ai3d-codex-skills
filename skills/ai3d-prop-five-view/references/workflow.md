# Workflow

## 1. Intake

Collect:

- Reference directory and target prop name.
- Prop category: wearable accessory, body-part asset, handheld prop, attached gadget, surface detail, or hard-surface object.
- Desired output root, defaulting to `Assets/Reference/`.
- Existing character/prop brief, prop split list, style rules, material board, or modeling reference document.
- Required style: photoreal, stylized 3D, hand-painted, low-poly, painterly, realistic, or project-specific.
- Optional support views: bottom, inside, exploded, scale/attachment sheet.
- Hard requirements: image size, background, naming, whether to update documentation, and whether to use parallel agents.

## 2. One-Prop Boundary

Every run handles one target object only.

Acceptable single targets:

- One hat.
- One pair of glasses.
- One left eye, one right eye, or one explicitly defined eye pair.
- One hard case.
- One radio.
- One badge.

Reject or split:

- Hat plus glasses.
- Head plus hat.
- Hand plus case.
- Full character with attached accessories.
- A tool bundle unless the bundle is the intended single prop model.

If a source image contains several props, crop or describe only the target. Treat all other objects as forbidden contaminants.

## 3. Reference Triage

Classify each source by production role:

| Tier | Use | Examples |
| --- | --- | --- |
| P0 | Identity and must-match prop structure | clear isolated prop, approved prop sheet, close crop with visible silhouette and material |
| P1 | Local detail support | fastener closeup, side thickness, underside, worn edge, material board, attachment area |
| P2 | Weak reference | prop attached to body, occluded, scene lighting, cropped, heavy perspective, inconsistent version |

Rules:

- Use P0 references to define the prop identity and structure block.
- Use P1 references to repair local details, never to override P0.
- Use P2 only for style or context if it does not contradict P0.
- Do not infer dimensions from a single distorted perspective view.
- Separate target prop facts from wearer, character, hand, table, scene, or mood facts.

## 4. Feature Extraction

Write the prop as buildable constraints before generating images:

- One paragraph prop definition.
- 8-12 hard identity anchors.
- Negative constraints.
- View-specific constraints.
- Style rules and material language.
- Scale and attachment/contact notes.

Use `feature-extraction.md` as the checklist.

## 5. Crop Board

Create a crop spec when the reference set is large, inconsistent, or attached to a character.

Recommended crop groups:

- Overall target prop.
- Front face.
- Back face.
- Left/right side profile and thickness.
- Top footprint.
- Underside or interior, if visible.
- Attachment/contact area.
- Fasteners, hinges, straps, nose pads, brim band, locks, buttons, seams, lenses, or other fine details.
- Materials and color palette.
- Negative/contamination examples when useful.

Use `build_prop_reference_crops.py` to produce local crops and `contact_sheet.jpg`.

## 6. Prop Modeling Reference Document

Write or update a project-local document that includes:

- Purpose and boundary: AI3D prop input preparation, not final topology, UV, texture, rigging, or engine integration.
- Reference index and P0/P1/P2 roles.
- Prop brief and identity anchors.
- Feature parameter table.
- Style rules, palette, materials, and forbidden contaminants.
- Scale and attachment/contact notes.
- Five-view generation strategy.
- Optional support view strategy.
- Prompt templates and negative prompts.
- Review rubric and rejection rules.
- Saved output paths.

## 7. Five-View Generation

Generate five independent final images:

- Front.
- Back.
- Left side.
- Right side.
- Top.

Use one shared identity/style block. Only change the `View request` paragraph. Keep background, lighting, rendering style, and negative constraints identical.

If the user explicitly requests agents, spawn five workers:

- Worker 1 owns front output.
- Worker 2 owns back output.
- Worker 3 owns left side output.
- Worker 4 owns right side output.
- Worker 5 owns top output.

Each worker writes only its assigned file and reports the prompt summary. If subagents are unavailable, generate sequentially.

## 8. Support Views

Generate support images only when they clarify model construction:

- Bottom: underside, inner brim, sole, base, ports, lock bottoms.
- Inside: hat interior, open case, lens thickness, hollow object interior.
- Exploded: separated lens/frame/temple, case lid/body/handle/locks, hat crown/brim/band.
- Scale/attachment: how the prop contacts a head, face, hand, belt, or torso.

Support views must go under `GeneratedViews/support/`. They must not replace the standard five final views.

## 9. Project Save Policy

Built-in image generation saves under `.codex/generated_images` first. Copy final assets into the project output directory and leave the original generated image in place.

Use `organize_generation_outputs.py` immediately after generation so view files and support files do not mix.

Recommended final structure:

```text
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
    prompts/
    drafts/
    rejected/
```

Default to copy mode when organizing from `.codex/generated_images`. Use `--mode move` only when cleaning a project-local staging folder.

## 10. Review

Create a contact sheet from `GeneratedViews/views/`, save it to `GeneratedViews/support/`, and check:

- Exactly one target prop appears.
- Correct orthographic view direction.
- Same prop identity, dimensions, and material across views.
- Full object visible, including thin parts and contact points.
- Front, side, back, and top geometry do not contradict each other.
- Thickness, underside/interior, hinges, straps, lenses, brim, handle, fasteners, and seams are readable enough to repair.
- No character body, head, face, hands, mannequin, wearer, environment, text, watermark, or extra props.
- Color palette and material language match the brief.

Regenerate or reject any view that fails target purity, view direction, full object visibility, dimensions, material identity, or contamination rules.
