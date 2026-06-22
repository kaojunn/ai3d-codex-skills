# AI3D Codex Skills

Reusable Codex skills for AI3D five-view reference workflows.

## Skills

- `skills/ai3d-cat-five-view`: Create consistent AI3D-ready five-view cat reference images from photo sets.
- `skills/ai3d-human-five-view`: Create consistent AI3D-ready five-view human or stylized character reference images from photos, concepts, briefs, or design boards.

## Install From GitHub

Use Codex's built-in skill installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo kaojunn/ai3d-codex-skills \
  --path skills/ai3d-cat-five-view skills/ai3d-human-five-view
```

Restart Codex after installing new skills.

## Local Copy

You can also copy a skill folder into a Codex skills directory:

```bash
cp -R skills/ai3d-cat-five-view ~/.codex/skills/
cp -R skills/ai3d-human-five-view ~/.codex/skills/
```

Each skill includes its own `SKILL.md`, reference templates, and helper scripts.

## Output Organization

Both five-view skills include `scripts/organize_generation_outputs.py`.

Recommended generated output layout:

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

## Notes

These skills store workflow instructions, templates, and helper scripts only. They do not include private project photos or generated assets.
