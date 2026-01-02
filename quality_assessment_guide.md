# Phase A - Manual Quality Assessment Guide

## Purpose
This guide helps you manually evaluate each eye image for clinical acceptability and identify patterns in remote image submissions.

## Instructions
1. Open `manual_quality_assessment.csv` in Excel or Google Sheets
2. For each image, view it and complete the assessment columns
3. Use the rating scales below

---

## Assessment Criteria

### Overall Quality Rating (1-5 scale)
- **5 - Excellent**: Professional quality, exceeds requirements
- **4 - Good**: Meets all requirements, minor imperfections
- **3 - Acceptable**: Usable for analysis, some quality issues
- **2 - Poor**: Marginal quality, may be usable with processing
- **1 - Unacceptable**: Cannot be used for analysis

### Binary Assessments (Yes/No or 1-5)

#### 1. Pupil Clearly Visible
- Can you clearly identify the pupil?
- Is the pupil boundary well-defined?

#### 2. Iris Texture Visible
- Can you see iris patterns/texture?
- Is there enough detail for analysis?

#### 3. Sclera Visible
- Is the white part of the eye visible?
- Helps with segmentation

#### 4. Eyelashes Not Obstructing
- Are eyelashes blocking the iris or pupil?
- Critical for automated analysis

#### 5. Proper Focus
- Is the eye in sharp focus?
- Are details crisp and clear?

#### 6. Adequate Lighting
- Is the eye well-lit?
- Not too dark or overexposed?

#### 7. No Glare/Reflections
- Are there bright spots from flash or light sources?
- Do reflections obscure critical features?

#### 8. Eye Fully Open
- Is the eye wide open?
- Eyelids not cutting off pupil/iris?

#### 9. Image Orientation Correct
- Is the image right-side up?
- Proper landscape/portrait orientation?

#### 10. Color Accuracy
- Do colors look natural?
- Not overly saturated or washed out?

---

## Red Flags to Note

### Critical Issues (Immediate rejection)
- [ ] Completely out of focus
- [ ] More than 50% of iris obscured
- [ ] Severe glare covering pupil
- [ ] Wrong body part photographed
- [ ] Extremely low resolution (<1MP)

### Warning Signs (May need resubmission)
- [ ] Partial pupil obstruction
- [ ] Uneven lighting
- [ ] Minor focus issues
- [ ] Flash reflections
- [ ] Eyelashes partially covering

---

## Recommendations Section

Document specific feedback for each image:
- "Retake with better lighting"
- "Move camera closer"
- "Disable flash"
- "Open eye wider"
- "Focus on eye, not face"

---

## Phase A Learning Objectives

As you assess, track:
1. **Common user errors** - What mistakes do participants make?
2. **Device limitations** - Which phones produce poor images?
3. **Lighting issues** - Indoor vs outdoor, flash vs no flash
4. **Instructions clarity** - Where are users confused?
5. **Minimum acceptable quality** - Define your threshold

---

## Next Steps After Assessment

1. Calculate acceptance rate (%acceptable images)
2. Identify most common rejection reasons
3. Update app UI cues based on findings
4. Revise photo guidelines for users
5. Set minimum device specifications
6. Determine if you need more diverse samples
