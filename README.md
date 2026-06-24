# AI3D Codex Skills

Reusable Codex skills for preparing consistent AI3D reference images from photos, concepts, and design boards.

## Available Skills

| Skill | Purpose | Main output |
| --- | --- | --- |
| `ai3d-cat-five-view` | Build consistent cat references for AI3D modeling | Front, back, left, right, and top views |
| `ai3d-human-five-view` | Build rigging-friendly human or stylized character references | Five orthographic T-pose views by default |
| `ai3d-prop-five-variants` | Explore controlled geometry alternatives for one prop | One prototype and four front-view shape variants |
| `ai3d-prop-five-view` | Prepare one isolated prop or detachable part for AI3D | Front, back, left, right, and top views |

Use `ai3d-prop-five-variants` before `ai3d-prop-five-view` when the prop shape has not been approved:

```text
source references
  -> five controlled front-view variants
  -> select one variant
  -> generate five orthographic views
  -> submit the package to an AI3D tool
```

## Install From GitHub

Install one skill:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo kaojunn/ai3d-codex-skills \
  --path skills/ai3d-human-five-view
```

Install the three human and prop skills together:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo kaojunn/ai3d-codex-skills \
  --path \
    skills/ai3d-human-five-view \
    skills/ai3d-prop-five-variants \
    skills/ai3d-prop-five-view
```

Restart Codex after installation. The installer stops when a destination skill directory already exists; use the update procedure in the manual instead of installing over an existing copy.

## Natural-Language Installation

Paste this into Codex:

```text
请使用 skill-installer 从 GitHub 仓库 kaojunn/ai3d-codex-skills 安装 skills/ai3d-human-five-view、skills/ai3d-prop-five-variants 和 skills/ai3d-prop-five-view，安装完成后提醒我重启 Codex。
```

## Local Installation

Clone the repository and copy only the skills you need:

```bash
git clone https://github.com/kaojunn/ai3d-codex-skills.git
cd ai3d-codex-skills

cp -R skills/ai3d-human-five-view ~/.codex/skills/
cp -R skills/ai3d-prop-five-variants ~/.codex/skills/
cp -R skills/ai3d-prop-five-view ~/.codex/skills/
```

## Updating Existing Installations

Back up existing skill directories, pull the repository, and synchronize the selected skills:

```bash
stamp="$(date +%Y%m%d-%H%M%S)"
mkdir -p ~/.codex/skills-backup/"$stamp"

cp -R ~/.codex/skills/ai3d-human-five-view ~/.codex/skills-backup/"$stamp"/
cp -R ~/.codex/skills/ai3d-prop-five-variants ~/.codex/skills-backup/"$stamp"/
cp -R ~/.codex/skills/ai3d-prop-five-view ~/.codex/skills-backup/"$stamp"/

git -C ai3d-codex-skills pull --ff-only

rsync -a --delete ai3d-codex-skills/skills/ai3d-human-five-view/ ~/.codex/skills/ai3d-human-five-view/
rsync -a --delete ai3d-codex-skills/skills/ai3d-prop-five-variants/ ~/.codex/skills/ai3d-prop-five-variants/
rsync -a --delete ai3d-codex-skills/skills/ai3d-prop-five-view/ ~/.codex/skills/ai3d-prop-five-view/
```

Restart Codex after updating.

## Usage Examples

```text
使用 $ai3d-human-five-view 分析这个人物参考目录，默认采用绑定友好的 T-pose，生成正、后、左、右、顶五视图并整理到项目的 Assets/Reference 下。
```

```text
使用 $ai3d-prop-five-variants 从这个花瓶参考生成一件标准化原型和四件受控造型派生，只改变几何轮廓，不改变颜色、花纹、材质和磨损。
```

```text
使用 $ai3d-prop-five-view 从选中的花瓶方案生成正、后、左、右、顶五视图，并把预览图、提示词和接触表放进 support 文件夹。
```

## Requirements

- Codex with local Skill support.
- Python 3.
- Pillow for crop-board and contact-sheet scripts: `python3 -m pip install Pillow`.
- Built-in `imagegen` when image generation is requested.
- Restart Codex after installing or replacing a Skill.

The skills do not require an OpenAI API key by default. They contain instructions, templates, and deterministic local helper scripts; they do not include private photos or generated project assets.

## Documentation

Detailed Chinese installation and usage documentation:

- [`docs/AI3D_Codex_Skills_安装与使用指南.md`](docs/AI3D_Codex_Skills_安装与使用指南.md)
- [`docs/AI3D_Codex_Skills_安装与使用指南.docx`](docs/AI3D_Codex_Skills_安装与使用指南.docx)
