# Phase A - Remote Tolerance Study: Analysis & Recommendations

**Analysis Date**: December 15, 2025
**Current Sample Size**: 9 images (4 left eye, 5 right eye)
**Target Sample Size**: 20-50 images

---

## Executive Summary

### Current Status: **NOT READY TO PROCEED**

**Reasons**:
1. Sample size (9) is below minimum target (20)
2. Critical quality issues identified
3. Insufficient device diversity
4. Need more data to establish baseline quality thresholds

---

## Key Findings

### 1. Sample Demographics

| Metric | Value |
|--------|-------|
| Total Images | 9 |
| Left Eye | 4 |
| Right Eye | 5 |
| Unique Camera Models | 5 |
| Images with EXIF Data | 7 (78%) |
| Images without EXIF | 2 (22%) |

### 2. Device Distribution

| Camera Model | Count | % of Total |
|--------------|-------|------------|
| iPhone 16 | 2 | 22% |
| iPhone 11 | 2 | 22% |
| iPhone 11 Pro Max | 2 | 22% |
| Galaxy A06 | 1 | 11% |
| Unknown (N/A) | 2 | 22% |

**Concern**: Heavy bias toward Apple devices (67% iPhone). Need more Android diversity.

### 3. Image Quality Metrics

#### Resolution
- **Range**: 0.24 MP - 12.19 MP
- **Mean**: 6.61 MP
- **Median**: 3.29 MP

**CRITICAL ISSUE**: Galaxy A06 image is only 0.24 MP (475x506 pixels) - likely unusable for analysis.

#### Brightness
- **Range**: 87.75 - 135.10
- **Mean**: 117.93
- **Std Dev**: 16.98

**Finding**: Fairly consistent brightness across submissions. Good sign for lighting instructions.

#### Sharpness
- **Range**: 26.54 - 137.56
- **Mean**: 69.74
- **Std Dev**: 39.81

**CONCERN**: Wide variation suggests focus issues. Some images may be out of focus.

#### File Size
- **Range**: 67.94 KB - 2527.41 KB
- **Mean**: 1263.78 KB

**Finding**: Large variation likely correlates with resolution differences.

---

## Quality Concerns Identified

### Critical Issues (Potential Rejections)

1. **Ultra-Low Resolution**
   - `20251126_211140.jpg` (Galaxy A06): 475x506 pixels (0.24 MP)
   - **Action Required**: Determine minimum acceptable resolution

2. **Very Low Sharpness**
   - `image.jpg` (RIGHT): Sharpness score 26.54
   - `IMG_1155.jpeg` (iPhone 16 RIGHT): Sharpness score 33.85
   - **Action Required**: Investigate focus quality, possible motion blur

3. **Missing EXIF Data**
   - 2 images have no camera metadata
   - **Impact**: Cannot verify device specifications or camera settings
   - **Action Required**: Investigate why EXIF is missing (edited images? Privacy settings?)

### Warning Signs

1. **Wide Sharpness Variation**
   - Suggests users are having trouble focusing properly
   - May need clearer instructions on focus/distance

2. **Device Quality Disparity**
   - Budget devices (Galaxy A06) producing dramatically worse results
   - May need minimum device specifications

3. **Small Sample from Android**
   - Only 1 Android submission (Galaxy A06)
   - Cannot assess Android device performance adequately

---

## Recommendations

### Immediate Actions (Before Phase A Completion)

#### 1. Collect More Samples
- **Target**: Minimum 11 more images to reach 20 total
- **Ideal**: 31-41 more images to reach 40-50 range
- **Focus Areas**:
  - More Android devices (Samsung Galaxy S series, Google Pixel, OnePlus)
  - Budget devices (to understand minimum specs)
  - Various lighting conditions (indoor, outdoor, evening)
  - Different age groups (if relevant to your study)

#### 2. Manual Quality Assessment
- Use `manual_quality_assessment.csv` to evaluate all 9 existing images
- Follow `quality_assessment_guide.md` for standardized evaluation
- Determine which images are clinically acceptable
- Calculate preliminary acceptance rate

#### 3. Generate Visual Analysis
- Run `python visualize_data.py` to create analysis dashboard
- Review quality distributions
- Identify patterns in quality issues

#### 4. Define Quality Thresholds
Based on manual assessment, establish:
- Minimum acceptable resolution (recommend: 2-3 MP minimum)
- Minimum sharpness score threshold
- Acceptable brightness range
- Maximum/minimum file size

#### 5. Review Camera Spec Screenshots
- Check the 6 camera spec screenshots you collected
- Document specifications for each device
- Compare specs to actual image quality
- Identify if spec sheets correlate with image quality

### Medium-Term Actions (Phase A Refinement)

#### 1. Update App Instructions
Based on common errors found:
- Add distance guidance (e.g., "Hold phone 4-6 inches from eye")
- Include focus instructions ("Tap on your eye to focus")
- Provide lighting tips ("Use natural light, avoid harsh overhead lights")
- Show example good/bad images

#### 2. Implement Real-Time Quality Checks
Consider adding to your app:
- Minimum resolution check (reject <2 MP)
- Brightness check (warn if too dark/bright)
- Blur detection (basic sharpness check)
- Eye detection (confirm eye is in frame)

#### 3. Set Device Requirements
Based on findings:
- **Minimum Resolution**: 2 MP rear camera
- **Operating System**: iOS 12+ / Android 8.0+
- **Note**: May need to exclude very budget devices

#### 4. Diversify Sample Collection
Recruit participants with:
- Various Android manufacturers (Samsung, Google, Motorola, OnePlus)
- Older iPhone models (iPhone 8, XR)
- Mid-range devices
- Different geographic locations (lighting conditions)

---

## Device-Specific Findings

### iPhone 16 (2 images)
- **Resolution**: 12.19 MP
- **Avg Brightness**: 103.36
- **Avg Sharpness**: 48.12
- **Concern**: Lower sharpness than expected for flagship device - may indicate user error (motion, poor focus)

### iPhone 11 (2 images)
- **Resolution**: 2.77-3.29 MP (downsized from original)
- **Avg Brightness**: 121.74
- **Avg Sharpness**: 135.01 (EXCELLENT)
- **Note**: Best sharpness scores in dataset

### iPhone 11 Pro Max (2 images)
- **Resolution**: 2.18-2.25 MP (downsized)
- **Avg Brightness**: 124.93
- **Avg Sharpness**: 49.29
- **Note**: Consistent quality

### Galaxy A06 (1 image)
- **Resolution**: 0.24 MP (CRITICAL CONCERN)
- **Brightness**: 91.78 (darkest in set)
- **Sharpness**: 75.04
- **Verdict**: Likely UNACCEPTABLE due to resolution
- **Action**: Investigate if this is user error or device limitation

### Unknown/N/A (2 images)
- **Resolution**: 12.19 MP
- **Avg Brightness**: 134.78
- **Avg Sharpness**: 43.92
- **Issue**: Missing EXIF - investigate cause

---

## Phase A Completion Criteria

Before proceeding to next phase, ensure:

- [ ] Minimum 20 images collected (recommend 30-40)
- [ ] At least 10 different participants
- [ ] At least 5 different camera models
- [ ] At least 30% Android devices
- [ ] Manual quality assessment completed for all images
- [ ] Acceptance rate calculated (target: >70%)
- [ ] Quality thresholds defined and documented
- [ ] Common user errors identified
- [ ] UI/instruction improvements documented
- [ ] Minimum device specifications determined

---

## Data Analysis Tools Created

1. **`image_analysis.py`**: Automated EXIF extraction and quality metrics
2. **`phase_a_image_tracking.csv`**: Complete data for all images
3. **`manual_quality_assessment.csv`**: Template for clinical evaluation
4. **`quality_assessment_guide.md`**: Standardized assessment protocol
5. **`visualize_data.py`**: Generate analysis dashboard
6. **`analysis_report.json`**: Summary statistics

---

## Next Steps

### Week 1
1. Collect 11-31 more images to reach 20-40 total
2. Complete manual quality assessment for all images
3. Run visualization dashboard
4. Calculate acceptance rate

### Week 2
1. Analyze common rejection reasons
2. Update app UI cues and instructions
3. Define minimum quality thresholds
4. Set device requirements

### Week 3
1. Recruit more Android users
2. Test with budget devices
3. Validate quality improvements
4. Prepare for Phase B

---

## Questions to Answer Before Proceeding

1. What is your minimum acceptable resolution for analysis?
2. What acceptance rate is acceptable? (70%? 80%?)
3. Will you support budget Android devices, or set minimum specs?
4. How will you handle images without EXIF data?
5. What lighting conditions are acceptable?
6. Do you need both eyes from each participant?

---

## Contact for Analysis

For questions about this analysis or Phase A study:
- Review all CSV files and visualization dashboard
- Use manual assessment guide for clinical evaluation
- Run additional analysis using provided Python scripts

**Generated**: December 15, 2025
