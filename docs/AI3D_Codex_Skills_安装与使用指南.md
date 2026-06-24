# AI3D Codex Skills 安装与使用指南

版本日期：2026-06-24  
仓库地址：https://github.com/kaojunn/ai3d-codex-skills

## 1. 文档目的

本手册说明如何安装、更新、验证和使用以下三个 Codex Skill：

| Skill | 适用对象 | 核心结果 |
| --- | --- | --- |
| `ai3d-human-five-view` | 真人、人物角色、风格化角色 | 默认生成绑定友好的 T-pose 正、后、左、右、顶五视图 |
| `ai3d-prop-five-variants` | 尚未确定最终造型的单件道具 | 生成一件标准化原型和四件受控形状派生 |
| `ai3d-prop-five-view` | 已确定造型的单件道具或可拆部件 | 生成正、后、左、右、顶五视图和可选结构补充视图 |

三个 Skill 都用于 AI3D 建模前的参考输入准备，不直接完成拓扑、UV、最终贴图、骨骼、动画或引擎集成。

## 2. 如何选择 Skill

### 2.1 人物或角色

使用 `ai3d-human-five-view`。默认姿态为完整 T-pose，重点保证：

- 双臂在肩关节高度水平外展 90 度。
- 肘部伸直，手腕保持平直，掌心朝下。
- 腋窝保留清晰背景空隙。
- 肩部、袖子、上臂和躯干轮廓互不粘连。
- 正、后、左、右、顶五张图保持同一人物、比例、服装和姿态。

只有用户明确要求时才切换为 A-pose。

### 2.2 道具造型尚未确定

先使用 `ai3d-prop-five-variants`。它不会生成五个相机角度，而是生成五张严格正视图：

1. `variant_01`：标准化原型。
2. `variant_02`：整体宽高比和轮廓派生。
3. `variant_03`：主体与底座、顶部、口沿等质量比例派生。
4. `variant_04`：边缘、圆角和曲线语言派生。
5. `variant_05`：一个主要附属结构的形状派生。

颜色、花纹、材质、磨损、时代风格、功能和识别细节必须保持不变。

### 2.3 道具造型已经确定

使用 `ai3d-prop-five-view`。每次只处理一个目标：

- 可以处理一顶帽子、一副眼镜、一只箱子、一个徽章或一对作为单一资产的眼睛。
- 不可以在同一次任务中混合帽子和眼镜、箱子和手、帽子和头部。
- 最终 `views/` 中只能出现目标道具，不得出现角色、手、头部、模特、桌面或场景。

### 2.4 推荐组合流程

```text
参考照片或概念图
  -> 提取 P0/P1/P2 参考等级
  -> 提取身份特征、结构规则和禁止项
  -> ai3d-prop-five-variants 生成五个正视方案
  -> 选择一个方案并锁定造型
  -> ai3d-prop-five-view 生成五个正交角度
  -> 整理 prompts、support、manifest 和 contact sheet
  -> 提交 AI3D 工具生成初模
```

人物不需要经过道具派生 Skill，直接进入 `ai3d-human-five-view`。

## 3. 安装条件

### 3.1 必需条件

- 已安装支持本地 Skills 的 Codex。
- 可以访问公开 GitHub 仓库。
- 本机具有 Python 3。
- 安装或更新 Skill 后可以重启 Codex。

### 3.2 图片脚本依赖

裁切图板和 contact sheet 脚本使用 Pillow：

```bash
python3 -m pip install Pillow
```

验证 Pillow：

```bash
python3 -c "from PIL import Image; print(Image.__version__)"
```

### 3.3 图片生成方式

当任务需要生成图片时，三个 Skill 默认要求 Codex 使用内置 `imagegen`，不默认使用 CLI、API Key 或第三方图片模型控制参数。因此，使用这些 Skill 本身不要求 OpenAI API 余额。

## 4. 从 GitHub 首次安装

### 4.1 通过一句话让 Codex 安装

一次安装三个 Skill：

```text
请使用 skill-installer 从 GitHub 仓库 kaojunn/ai3d-codex-skills 安装 skills/ai3d-human-five-view、skills/ai3d-prop-five-variants 和 skills/ai3d-prop-five-view，安装完成后提醒我重启 Codex。
```

只安装人物 Skill：

```text
请使用 skill-installer 从 GitHub 仓库 kaojunn/ai3d-codex-skills 安装 skills/ai3d-human-five-view，安装完成后提醒我重启 Codex。
```

只安装道具派生 Skill：

```text
请使用 skill-installer 从 GitHub 仓库 kaojunn/ai3d-codex-skills 安装 skills/ai3d-prop-five-variants，安装完成后提醒我重启 Codex。
```

只安装道具五视图 Skill：

```text
请使用 skill-installer 从 GitHub 仓库 kaojunn/ai3d-codex-skills 安装 skills/ai3d-prop-five-view，安装完成后提醒我重启 Codex。
```

### 4.2 使用安装脚本

一次安装三个 Skill：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo kaojunn/ai3d-codex-skills \
  --path \
    skills/ai3d-human-five-view \
    skills/ai3d-prop-five-variants \
    skills/ai3d-prop-five-view
```

只安装一个 Skill 时，只保留对应路径：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo kaojunn/ai3d-codex-skills \
  --path skills/ai3d-prop-five-view
```

安装成功后重启 Codex。

### 4.3 安装器的重要限制

`skill-installer` 不会覆盖同名目录。如果 `~/.codex/skills/<skill-name>` 已存在，安装会终止。这是保护本地修改的安全机制，不是仓库错误。更新已有 Skill 时应使用第 6 章的方法。

## 5. 本地安装

克隆仓库：

```bash
git clone https://github.com/kaojunn/ai3d-codex-skills.git
cd ai3d-codex-skills
```

复制需要的 Skill：

```bash
cp -R skills/ai3d-human-five-view ~/.codex/skills/
cp -R skills/ai3d-prop-five-variants ~/.codex/skills/
cp -R skills/ai3d-prop-five-view ~/.codex/skills/
```

如果目标目录已经存在，不要直接使用 `cp -R` 叠加旧文件。先备份，再使用 `rsync --delete` 更新，确保仓库中已经删除的旧文件不会残留。

## 6. 更新、备份与卸载

### 6.1 更新前备份

```bash
stamp="$(date +%Y%m%d-%H%M%S)"
backup="$HOME/.codex/skills-backup/$stamp"
mkdir -p "$backup"

cp -R ~/.codex/skills/ai3d-human-five-view "$backup"/
cp -R ~/.codex/skills/ai3d-prop-five-variants "$backup"/
cp -R ~/.codex/skills/ai3d-prop-five-view "$backup"/
```

### 6.2 拉取并同步最新版本

```bash
git -C /path/to/ai3d-codex-skills pull --ff-only

rsync -a --delete \
  /path/to/ai3d-codex-skills/skills/ai3d-human-five-view/ \
  ~/.codex/skills/ai3d-human-five-view/

rsync -a --delete \
  /path/to/ai3d-codex-skills/skills/ai3d-prop-five-variants/ \
  ~/.codex/skills/ai3d-prop-five-variants/

rsync -a --delete \
  /path/to/ai3d-codex-skills/skills/ai3d-prop-five-view/ \
  ~/.codex/skills/ai3d-prop-five-view/
```

更新后重启 Codex。

### 6.3 卸载

确认不再需要后，删除对应目录：

```bash
rm -rf ~/.codex/skills/ai3d-human-five-view
rm -rf ~/.codex/skills/ai3d-prop-five-variants
rm -rf ~/.codex/skills/ai3d-prop-five-view
```

`rm -rf` 不可撤销。执行前应确认路径并保留备份。

## 7. 安装验证

检查目录：

```bash
ls ~/.codex/skills/ai3d-human-five-view
ls ~/.codex/skills/ai3d-prop-five-variants
ls ~/.codex/skills/ai3d-prop-five-view
```

每个目录至少应包含：

```text
SKILL.md
agents/openai.yaml
references/
scripts/
```

使用官方校验器：

```bash
uvx --with pyyaml python \
  ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ~/.codex/skills/ai3d-human-five-view
```

将最后一个路径替换为另外两个 Skill 可分别验证。预期输出为：

```text
Skill is valid!
```

如果 Codex 没有识别新 Skill，先完全退出并重启 Codex，再新建对话测试。

## 8. 使用 `ai3d-human-five-view`

### 8.1 输入

准备：

- 人物照片、角色设定图或概念图目录。
- 角色名称和输出前缀。
- 项目输出目录，默认是 `Assets/Reference/`。
- 风格规则、已有 Brief、三视图或 T-pose 图。
- 如需 A-pose，必须明确写出。

### 8.2 推荐调用

```text
使用 $ai3d-human-five-view 分析 Assets/Reference/HeroPhotos 中的人物参考。先划分 P0/P1/P2，提取身份锚点、头身比、体型、服装层级、肩宽、臂展和腋窝分离规则，再使用内置 imagegen 生成绑定友好的 T-pose 正、后、左、右、顶五视图。输出前缀为 hero，保存到 Assets/Reference/HeroGeneratedViews，并整理 views 和 support 文件夹。
```

### 8.3 T-pose 硬性要求

- 双臂水平外展 90 度，位于肩关节高度。
- 肩膀自然，不得耸肩。
- 肘部伸直，不得弯曲或左右长度不一致。
- 手腕平直，掌心朝下，手指自然并拢。
- 腋窝必须能看到背景空隙。
- 袖子、上臂、肩部和躯干不得融合。
- 画布必须容纳完整手指、头饰和脚，不得裁切。
- 侧视图中双臂沿相机轴线重叠是允许的，但不能降低、删除或重设计手臂。
- 顶视图必须保留完整指尖到指尖的 T 形轮廓。

### 8.4 默认输出

```text
Assets/Reference/
  HeroPhotos/
  HeroCrops/
  HeroGeneratedViews/
    views/
      hero_front_view.png
      hero_back_view.png
      hero_left_side_view.png
      hero_right_side_view.png
      hero_top_view.png
    support/
      hero_five_view_contact_sheet.png
      hero_organization_manifest.json
      prompts/
      previews/
      drafts/
  HeroAI3DInput/
  Hero_ModelingReference.md
```

### 8.5 辅助脚本

生成局部裁切板：

```bash
python3 ~/.codex/skills/ai3d-human-five-view/scripts/build_character_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/HeroPhotos \
  --out-dir Assets/Reference/HeroCrops
```

整理混合输出：

```bash
python3 ~/.codex/skills/ai3d-human-five-view/scripts/organize_generation_outputs.py \
  --source-dir .codex/generated_images \
  --views-dir Assets/Reference/HeroGeneratedViews/views \
  --support-dir Assets/Reference/HeroGeneratedViews/support \
  --prefix hero
```

生成五视图总览：

```bash
python3 ~/.codex/skills/ai3d-human-five-view/scripts/make_view_contact_sheet.py \
  --views-dir Assets/Reference/HeroGeneratedViews/views \
  --prefix hero \
  --out Assets/Reference/HeroGeneratedViews/support/hero_five_view_contact_sheet.png
```

整理脚本默认为复制。只有清理项目内临时目录时才使用 `--mode move`。自动识别失败时可以重复传入显式映射：

```bash
--view front=front.png --view back=back.png
```

## 9. 使用 `ai3d-prop-five-variants`

### 9.1 输入

准备：

- 只包含一个目标道具身份的照片、概念图或裁切图。
- 道具名称、功能和输出前缀。
- 不允许变化的颜色、花纹、材质、时代、磨损和识别细节。
- 允许变化的几何轴。

### 9.2 推荐调用

```text
使用 $ai3d-prop-five-variants 分析 Assets/Reference/VaseVariantPhotos 中的单个花瓶。锁定类别、功能、蓝白花纹内容与位置、陶瓷材质、釉面和磨损，只改变计划中的几何轮廓。生成 variant_01 标准原型和四个中等强度派生，保存到 Assets/Reference/VasePropVariants，并生成 variation plan、manifest 和五方案总览图。
```

### 9.3 锁定特征

必须锁定：

- 单一道具边界。
- 类别、功能和时代风格。
- 必需组件及其功能关系。
- 主色、辅色、强调色及其位置。
- 花纹内容、顺序、方向、密度和所在结构区域。
- 材质、表面语言和磨损程度。
- 标志性结构和对称规则。

花纹可以随曲面自然拉伸或压缩，但不能新增、删除、镜像、旋转或迁移到其他结构区域。

### 9.4 变化规则

- 每个派生最多一个主要变化轴和一个次要变化轴。
- 不允许通过换色、换材质、改灯光、转相机或改变画布裁切制造差异。
- 五张图必须都是严格正交正视图。
- `variant_01` 只能清理和标准化原型，不能重新设计。

### 9.5 默认输出

```text
Assets/Reference/
  VaseVariantPhotos/
  VaseVariantCrops/
  VasePropVariants/
    final/
      vase_variant_01_front.png
      vase_variant_02_front.png
      vase_variant_03_front.png
      vase_variant_04_front.png
      vase_variant_05_front.png
    support/
      vase_five_variants_contact_sheet.png
      vase_variation_plan.json
      vase_organization_manifest.json
      prompts/
      drafts/
      rejected/
  Vase_PropVariantReference.md
```

### 9.6 辅助脚本

生成道具裁切板：

```bash
python3 ~/.codex/skills/ai3d-prop-five-variants/scripts/build_prop_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/VaseVariantPhotos \
  --out-dir Assets/Reference/VaseVariantCrops
```

整理五个派生：

```bash
python3 ~/.codex/skills/ai3d-prop-five-variants/scripts/organize_variant_outputs.py \
  --source-dir .codex/generated_images \
  --final-dir Assets/Reference/VasePropVariants/final \
  --support-dir Assets/Reference/VasePropVariants/support \
  --prefix vase \
  --variation-plan variation_plan.json
```

自动识别不明确时，可以显式指定：

```bash
--variant 01=prototype.png --variant 02=wide.png --variant 03=mass.png
```

五个编号必须完整且唯一。缺失编号或重复候选会使脚本终止。

生成五方案总览：

```bash
python3 ~/.codex/skills/ai3d-prop-five-variants/scripts/make_variant_contact_sheet.py \
  --final-dir Assets/Reference/VasePropVariants/final \
  --prefix vase \
  --out Assets/Reference/VasePropVariants/support/vase_five_variants_contact_sheet.png
```

### 9.7 交接到道具五视图

选择一个方案后：

1. 在 `<PropName>_PropVariantReference.md` 记录编号、文件路径和选择原因。
2. 将选中图作为 `ai3d-prop-five-view` 的 P0 正面参考。
3. 同时提供原始 P0/P1 图，用于补充背面、厚度、顶部、底部、材质和连接结构。
4. 明确禁止后续五视图重新回到原始未选择造型。

## 10. 使用 `ai3d-prop-five-view`

### 10.1 输入

准备：

- 一个明确的目标道具或可拆部件。
- 已选定的正面方案。
- 背面、侧面、顶部、底部、内部或连接区域参考。
- 道具名称、类别、功能、尺寸比例、材质和输出前缀。
- 是否需要底视、内部、爆炸图或比例连接图。

### 10.2 推荐调用

```text
使用 $ai3d-prop-five-view，以 Assets/Reference/VasePropVariants/final/vase_variant_03_front.png 作为 P0 正面造型，结合原始照片补充背面、侧面厚度、顶部口沿和底足结构。生成严格正交的正、后、左、右、顶五视图，最终 views 中只出现花瓶，其他提示词、预览图、底视和总览图放入 support。
```

### 10.3 单一道具边界

- 每次只处理一个目标或一个明确不可分割的组合。
- 一副眼镜可以作为一个目标；帽子加眼镜不可以。
- 一对眼睛可以作为一个资产；眼睛加完整脸部不可以。
- 支持图可以使用淡化的人体连接轮廓，但支持图不得进入最终 `views/`。

### 10.4 默认输出

```text
Assets/Reference/
  VasePropPhotos/
  VasePropCrops/
  VasePropGeneratedViews/
    views/
      vase_front_view.png
      vase_back_view.png
      vase_left_side_view.png
      vase_right_side_view.png
      vase_top_view.png
    support/
      vase_five_view_contact_sheet.png
      vase_organization_manifest.json
      vase_bottom_view.png
      vase_inside_view.png
      vase_exploded_view.png
      vase_scale_attachment_sheet.png
      prompts/
      drafts/
      rejected/
  VasePropAI3DInput/
  Vase_PropModelingReference.md
```

### 10.5 辅助脚本

生成局部裁切板：

```bash
python3 ~/.codex/skills/ai3d-prop-five-view/scripts/build_prop_reference_crops.py \
  --spec crop_spec.json \
  --photo-dir Assets/Reference/VasePropPhotos \
  --out-dir Assets/Reference/VasePropCrops
```

整理输出：

```bash
python3 ~/.codex/skills/ai3d-prop-five-view/scripts/organize_generation_outputs.py \
  --source-dir .codex/generated_images \
  --views-dir Assets/Reference/VasePropGeneratedViews/views \
  --support-dir Assets/Reference/VasePropGeneratedViews/support \
  --prefix vase
```

生成五视图总览：

```bash
python3 ~/.codex/skills/ai3d-prop-five-view/scripts/make_view_contact_sheet.py \
  --views-dir Assets/Reference/VasePropGeneratedViews/views \
  --prefix vase \
  --out Assets/Reference/VasePropGeneratedViews/support/vase_five_view_contact_sheet.png
```

## 11. 文件整理规则

### 11.1 五视图 Skill

只有五张最终角度图进入 `views/`：

```text
front
back
left_side
right_side
top
```

以下文件进入 `support/`：

- prompts 和 negative prompts。
- 预览图、草稿和废弃图。
- contact sheet。
- organization manifest。
- 底视、内部图、爆炸图和连接关系图。

### 11.2 五派生 Skill

只有 `variant_01` 到 `variant_05` 进入 `final/`。计划文件、提示词、草稿、废弃图、总览图和 manifest 全部进入 `support/`。

### 11.3 覆盖策略

脚本默认不会覆盖已有文件，而是创建带版本后缀的新文件。只有明确希望覆盖时才使用 `--overwrite`。

## 12. 验收与失败判定

### 12.1 人物五视图

立即淘汰：

- 视角错误或出现三分之四视角。
- 人物身份、头身比或体型不一致。
- T-pose 手臂降低、弯肘、长度不一致或掌心方向错误。
- 腋窝封闭，袖子或上臂与躯干融合。
- 手、脚、头饰或完整臂展被裁切。
- 服装前后逻辑矛盾或背面随机生成。

### 12.2 道具五派生

立即淘汰：

- 不是正视图。
- 颜色、花纹、材质、磨损或功能发生变化。
- 仅通过镜头、裁切或灯光制造差异。
- 派生几乎没有几何差异。
- 同时改变多个未经批准的主要结构。

### 12.3 道具五视图

立即淘汰：

- 最终图中出现角色、手、头部、场景或额外道具。
- 视角错误、道具被裁切或薄部件消失。
- 前后左右顶部尺寸相互矛盾。
- 背面随机、厚度缺失或连接点无法解释。
- 材质和颜色在各视图间漂移。

## 13. 常见问题

### 13.1 安装提示目标目录已存在

原因：安装器为了保护现有内容，不覆盖同名目录。  
处理：先执行第 6 章备份，再用 `rsync --delete` 更新。

### 13.2 Skill 没有触发

处理顺序：

1. 重启 Codex。
2. 确认目录名和 `SKILL.md` 名称正确。
3. 在提示词中显式写 `$ai3d-human-five-view`、`$ai3d-prop-five-variants` 或 `$ai3d-prop-five-view`。
4. 运行 `quick_validate.py`。

### 13.3 报错 `No module named PIL`

安装 Pillow：

```bash
python3 -m pip install Pillow
```

确保安装 Pillow 的 Python 与运行脚本的 `python3` 是同一个解释器。

### 13.4 五视图整理后缺少某个角度

文件名可能无法被自动识别。使用显式映射：

```bash
--view front=/path/front.png \
--view back=/path/back.png \
--view left_side=/path/left.png \
--view right_side=/path/right.png \
--view top=/path/top.png
```

### 13.5 五派生提示重复候选

同一编号匹配了多张图。删除或移出多余候选，或者使用 `--variant ID=PATH` 明确选择。

### 13.6 生成文件仍然混乱

生成完成后立即运行 organizer。五视图使用 `organize_generation_outputs.py`，五派生使用 `organize_variant_outputs.py`。从 `.codex/generated_images` 整理时保持默认 copy 模式；只有清理项目内部暂存目录时才使用 move。

### 13.7 图片好看但无法建模

三个 Skill 都采用结构优先规则。漂亮渲染不能弥补错误姿态、轮廓、厚度、前后矛盾、融合部件或不可修复的手脚。应回到参考分级、身份锚点和 negative prompt 后重新生成。

## 14. 可直接粘贴的任务指令

### 14.1 人物五视图

```text
使用 $ai3d-human-five-view 处理我提供的人物参考目录。先提取 P0/P1/P2 和角色身份锚点，再使用内置 imagegen 生成同一人物的绑定友好 T-pose 正、后、左、右、顶五视图。双臂必须水平外展 90 度，肘部伸直，掌心朝下，腋窝、袖子、上臂和躯干清晰分离。最终五张图放入 views，提示词、预览图、草稿、manifest 和 contact sheet 放入 support。
```

### 14.2 道具五派生

```text
使用 $ai3d-prop-five-variants 处理我提供的单一道具参考。锁定类别、功能、时代风格、颜色位置、花纹、材质、磨损和标志性细节，生成一件标准化原型和四件中等强度形状派生。五张图都必须是同一尺度的严格正交正视图，只允许按 variation plan 改变几何形状。
```

### 14.3 道具五视图

```text
使用 $ai3d-prop-five-view 处理我选定的单一道具方案。以选中正视图为 P0 造型参考，结合其他照片补充背面、侧面厚度、顶部、底部和连接结构，生成严格正交的正、后、左、右、顶五视图。最终图中只能出现目标道具，支持视图和其他过程文件全部放入 support。
```

## 15. 安全边界

- 不要把私人照片、未授权素材、API Key、Token 或项目机密提交到 Skill 仓库。
- Skill 仓库只保存工作流、模板和辅助脚本。
- 生成结果应保存到具体项目目录，不应提交到通用 Skill 仓库。
- 更新前保留本地备份，确认差异后再使用 `rsync --delete`。
