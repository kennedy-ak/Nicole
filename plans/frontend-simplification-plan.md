# Frontend Simplification Plan

## Objective
Remove all marketing and mission content from the frontend while keeping only the essential upload form and brief instructions.

## Files to Modify

### 1. `eye_data_collection/templates/base.html`

**Current Header Section (Lines 104-116):**
```html
<div class="header-section">
    <h1>👁️ Belmont Solutions</h1>
    <p class="tagline">AI-Powered Cataract Screening for Africa</p>
    <p class="mission">
        Democratizing eye health across Africa by reducing screening costs to $1.50 and enabling scale via mobile devices.
        Your participation helps us validate our AI model to prevent avoidable blindness.
    </p>
    <div class="mt-4">
        <span class="impact-badge">📱 Mobile-first & Offline</span>
        <span class="impact-badge">🌍 Locally Trained AI</span>
    </div>
</div>
```

**Proposed Change:**
Replace with a minimal header:
```html
<div class="header-section">
    <h1>Eye Data Upload</h1>
</div>
```

**CSS Adjustments Needed:**
- Remove unused styles: `.tagline`, `.mission`, `.impact-badge`
- Simplify `.header-section` styling for minimal header

---

### 2. `eye_data_collection/templates/uploads/upload_form.html`

#### Section 1: Remove "Why Your Data Matters" (Lines 9-42)

**Content to Remove:**
- Entire card with title "🎯 Why Your Data Matters"
- Three explanatory cards about AI Model Training, Device Diversity, and Local Adaptation
- All marketing copy about Belmont Solutions and cost comparisons

#### Section 2: Keep Upload Form (Lines 44-121)

**Content to Keep:**
- Card with header "📸 Upload Your Eye Images"
- Lead paragraph: "Please upload the following three images to help validate our AI model:"
- Form with three image upload fields (Left Eye, Right Eye, Camera Specs)
- Submit button

**Note:** This section is essential and must remain unchanged.

#### Section 3: Keep Instructions Accordion (Lines 126-165)

**Content to Keep:**
- Card with header "📋 Instructions for Best Results"
- Accordion with two sections:
  - Image Capture Guide (lighting, distance, focus, stability)
  - Screenshot Guide (how to find camera specs)

**Note:** These are brief instructions and should be kept.

#### Section 4: Remove "Your Contribution Matters" (Lines 167-189)

**Content to Remove:**
- Entire card with gradient background
- Title "🌟 Your Contribution Matters"
- Three impact icons: Validate Accuracy, Prove Cost Savings, Enable Scale
- All marketing/impact messaging

#### Section 5: Remove Privacy & Ethics (Lines 191-201)

**Content to Remove:**
- Entire card with header "🔒 Privacy & Ethics"
- Data Security, Anonymity, and Ethics statements

---

## Final Layout After Changes

### Simplified `base.html`:
- Minimal header with just "Eye Data Upload" title
- Messages section (for alerts)
- Content block

### Simplified `upload_form.html`:
- **Left Column:**
  - Upload form only
- **Right Column:**
  - Instructions accordion only

## Summary of Changes

| Section | Action | Reason |
|---------|--------|--------|
| Company branding (Belmont Solutions) | Remove | Marketing content |
| Tagline and mission statement | Remove | Marketing/mission content |
| Impact badges | Remove | Marketing content |
| "Why Your Data Matters" section | Remove | Marketing/mission content |
| Three explanatory cards | Remove | Marketing content |
| Upload form | **Keep** | Essential functionality |
| Instructions accordion | **Keep** | Brief instructions |
| "Your Contribution Matters" card | Remove | Marketing/impact content |
| Privacy & Ethics section | Remove | Non-essential (can be added back if needed) |

## Expected Outcome

The frontend will be:
- **Cleaner**: No marketing or mission statements
- **Focused**: Only the upload form and instructions
- **Simpler**: Reduced cognitive load for users
- **Functional**: All core features remain intact

## Implementation Order

1. Update `base.html` header and remove unused CSS
2. Remove "Why Your Data Matters" section from `upload_form.html`
3. Remove "Your Contribution Matters" card from `upload_form.html`
4. Remove Privacy & Ethics section from `upload_form.html`
5. Test the application to ensure functionality is preserved
