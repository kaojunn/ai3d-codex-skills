# Prompt Templates

Use one shared identity/style block for all five views. Change only the `View request` paragraph.

## Shared Prompt Skeleton

```text
Use case: AI3D character modeling input
Asset type: orthographic full-body reference image
Primary request: Generate one <VIEW> orthographic reference image of the same human character from the provided references.
Scene/backdrop: clean white to very light gray studio background, no environment, no props except required character-held or worn props, no text, no watermark.
Subject identity: <IDENTITY BLOCK>
Style/medium: <PROJECT STYLE>, technical character modeling reference, clear silhouette and readable geometry.
Composition/framing: full body and full fingertip-to-fingertip arm span visible, centered, generous padding, strict orthographic view, no perspective angle. Use a wide canvas or reduce character scale rather than cropping hands, fingers, hat, or feet.
Pose: neutral T-pose by default. Both arms are abducted exactly 90 degrees and extend horizontally at shoulder-joint height, shoulders relaxed, elbows fully extended, wrists straight, palms facing down, fingers naturally together, legs straight, and feet parallel. Use A-pose only when the user explicitly requests it.
Lighting/mood: even soft studio lighting, minimal ground shadow, neutral technical reference mood.
Constraints: same individual across all five views, same T-pose, same body proportions, same head-to-body ratio, same shoulder-joint height, same arm span, same outfit, same major colors, same required props, readable front/side/back garment logic. Keep visible background gaps through both armpits. Keep shoulders, sleeves, upper arms, and torso as separate readable contours for mesh generation and skeletal rigging.
Avoid: A-pose unless explicitly requested, lowered or diagonal arms, bent elbows, raised shoulders, uneven arm length, closed armpits, sleeves or upper arms fused to torso, missing or duplicated arms, wrong view, three-quarter view unless requested, cropped body, cropped hands, hidden hands, fused fingers, cropped feet, merged clothing, random back design, random jewelry, extra props, weapon not in reference, complex background, dramatic smoke, cinematic lighting, text, watermark.
```

## View Requests

### Front

```text
View request: exact front orthographic view. The character faces the camera directly in a complete T-pose. Both arms form one level horizontal line through the shoulder joints, both elbows are straight, both palms face down, and both hands are fully visible. Clear white background gaps remain between each armpit and torso; sleeves and upper arms do not touch or merge into the body. Face, hair front, chest, collar, sleeves, belt, hands, legs, boots/feet, front color placement, and required front props are clearly visible. Both shoulders, arms, and feet are symmetrical unless the character design explicitly requires asymmetry.
```

### Back

```text
View request: exact rear/back orthographic view. The character faces away from the camera in the same complete T-pose. Both arms remain level at shoulder height, both elbows are straight, palms face down, and both hands are fully visible. Clear white background gaps remain through both armpits; back shoulder seams, armholes, sleeves, upper arms, and torso stay separate. Back hair shape, back collar, cape/robe/backpack/strap logic, waist and belt continuation, garment hems, back of hands, legs, heels/soles, and back color placement are clearly visible. Do not show the face except tiny side edges if natural.
```

### Left Side

```text
View request: exact left side orthographic view. The character head points toward the left side of the image. Preserve the complete T-pose: both arms remain at shoulder height and extend along the camera axis, one toward the camera and one away from it. The near arm may occlude the far arm, but do not lower, bend, omit, duplicate, or rotate either arm. Keep the near shoulder joint, armhole, armpit clearance, sleeve, upper arm, straight elbow, wrist, palm-down hand, and fingers structurally readable. Body depth, posture, nose/chin profile, hair mass, shoulder-to-hip depth, garment layer thickness, belt thickness, leg profile, boot/foot profile, and prop side placement are visible. Use strict side framing, not three-quarter.
```

### Right Side

```text
View request: exact right side orthographic view. The character head points toward the right side of the image. Preserve the complete T-pose: both arms remain at shoulder height and extend along the camera axis, one toward the camera and one away from it. The near arm may occlude the far arm, but do not lower, bend, omit, duplicate, or rotate either arm. Keep the near shoulder joint, armhole, armpit clearance, sleeve, upper arm, straight elbow, wrist, palm-down hand, and fingers structurally readable. Body depth, posture, nose/chin profile, hair mass, shoulder-to-hip depth, garment layer thickness, belt thickness, leg profile, boot/foot profile, and prop side placement are visible. Use strict side framing, not three-quarter.
```

### Top

```text
View request: exact top-down orthographic view from directly above. Preserve the complete T-pose and show the uninterrupted horizontal silhouette from left fingertips through both shoulders to right fingertips. Both elbows remain straight, palms face down toward the floor, and neither hand is cropped. The entire head, hair mass, shoulders, armholes, armpit clearances, torso footprint, arms, hands, hips, legs, feet, required props, and garment footprint are visible. Avoid perspective tilt. The silhouette and arm span must match the front, back, and side proportions.
```

## Negative Prompt Template

```text
wrong character, wrong age, wrong body type, wrong head-to-body ratio, A-pose unless explicitly requested, lowered arms, diagonal arms, bent elbows, raised shoulders, uneven arm length, missing arm, duplicated arm, closed armpits, no armpit background gap, sleeve fused to torso, upper arm fused to torso, wrong palm direction, wrong pose, wrong view, perspective angle, three-quarter view, cropped head, cropped feet, cropped hands, hidden hands, fused fingers, mitten hands, melted feet, merged clothing layers, random back design, missing required prop, fused prop, extra weapon, extra jewelry, random religious symbol, random regional pattern, overly complex ornament, dramatic lighting, smoke, environment, scene background, text, watermark, logo, final illustration composition
```

## Batch Generation Strategy

Run at least three prompt variants when the first set is uncertain:

| Batch | Priority | Prompt emphasis |
| --- | --- | --- |
| A | Structure first | T-pose, shoulder height, arm span, armpit clearance, head-to-body ratio, body type, silhouette, clothing layers, hands, feet |
| B | Identity first | Face, hair, role, age, posture, recognizable silhouette anchors |
| C | Outfit and color first | Garment layout, back design, palette, material language, props |

Prefer the batch with the strongest structure and repairability. Do not choose a batch only because the render is attractive.

## Review Rubric

Score each view from 0-5:

| Item | 5 | 0 |
| --- | --- | --- |
| View direction | exact requested orthographic view | wrong view or three-quarter |
| Full body | full head/body/hands/feet visible | cropped or hidden critical parts |
| Identity | matches anchors | generic or wrong character |
| Proportion | head-to-body ratio and body type stable | adultified, childified, too thin, too bulky, inconsistent |
| T-pose | level arms, straight elbows, palms down, equal arm length | A-pose, lowered/bent/missing/uneven arms |
| Armpit separation | visible background gaps; sleeves, arms, and torso separate | closed armpits or fused sleeve/arm/torso contours |
| Silhouette | recognizable from distance | loses key shape anchors |
| Clothing layers | collars, sleeves, belt, hems, boots readable | merged or random layers |
| Back design | logical continuation of front/side | random or empty back |
| Hands/feet | repairable fingers, palms, shoes/boots | fused, hidden, cropped, melted |
| Props | required props present and separable | missing, fused, or extra |
| Background | clean technical reference | environment, props, text, watermark |

Regenerate any view with a 0 in view direction, full body, identity, proportion, T-pose, armpit separation, hands/feet, or back design.
