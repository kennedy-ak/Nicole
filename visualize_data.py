import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Read data
df = pd.read_csv(r'C:\Users\User2\Desktop\Nicole\phase_a_image_tracking.csv')

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# 1. Camera Model Distribution
ax1 = plt.subplot(3, 3, 1)
camera_counts = df['camera_model'].value_counts()
colors = sns.color_palette("husl", len(camera_counts))
ax1.bar(range(len(camera_counts)), camera_counts.values, color=colors)
ax1.set_xticks(range(len(camera_counts)))
ax1.set_xticklabels(camera_counts.index, rotation=45, ha='right')
ax1.set_title('Camera Model Distribution', fontweight='bold')
ax1.set_ylabel('Count')
ax1.grid(axis='y', alpha=0.3)

# 2. Resolution Distribution
ax2 = plt.subplot(3, 3, 2)
resolutions = df['megapixels'].values
ax2.hist(resolutions, bins=8, color='skyblue', edgecolor='black', alpha=0.7)
ax2.axvline(resolutions.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {resolutions.mean():.2f} MP')
ax2.set_title('Resolution Distribution', fontweight='bold')
ax2.set_xlabel('Megapixels')
ax2.set_ylabel('Frequency')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 3. Brightness Distribution
ax3 = plt.subplot(3, 3, 3)
brightness = df['brightness'].values
ax3.hist(brightness, bins=8, color='gold', edgecolor='black', alpha=0.7)
ax3.axvline(brightness.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {brightness.mean():.2f}')
ax3.set_title('Brightness Distribution', fontweight='bold')
ax3.set_xlabel('Brightness Score')
ax3.set_ylabel('Frequency')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# 4. Sharpness Distribution
ax4 = plt.subplot(3, 3, 4)
sharpness = df['sharpness_score'].values
ax4.hist(sharpness, bins=8, color='lightcoral', edgecolor='black', alpha=0.7)
ax4.axvline(sharpness.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {sharpness.mean():.2f}')
ax4.set_title('Sharpness Distribution', fontweight='bold')
ax4.set_xlabel('Sharpness Score')
ax4.set_ylabel('Frequency')
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

# 5. Eye Side Distribution
ax5 = plt.subplot(3, 3, 5)
eye_counts = df['eye_side'].value_counts()
ax5.pie(eye_counts.values, labels=eye_counts.index, autopct='%1.1f%%',
        colors=['lightblue', 'lightcoral'], startangle=90)
ax5.set_title('Left vs Right Eye Distribution', fontweight='bold')

# 6. File Size vs Resolution
ax6 = plt.subplot(3, 3, 6)
scatter = ax6.scatter(df['megapixels'], df['file_size_kb'],
                      c=df['brightness'], cmap='viridis', s=100, alpha=0.6)
ax6.set_xlabel('Resolution (MP)')
ax6.set_ylabel('File Size (KB)')
ax6.set_title('File Size vs Resolution (colored by brightness)', fontweight='bold')
plt.colorbar(scatter, ax=ax6, label='Brightness')
ax6.grid(alpha=0.3)

# 7. Quality Metrics by Camera Model
ax7 = plt.subplot(3, 3, 7)
camera_quality = df.groupby('camera_model')[['megapixels', 'brightness', 'sharpness_score']].mean()
x_pos = np.arange(len(camera_quality))
width = 0.25

bars1 = ax7.bar(x_pos - width, camera_quality['megapixels'], width, label='Resolution (MP)', alpha=0.8)
bars2 = ax7.bar(x_pos, camera_quality['brightness']/20, width, label='Brightness/20', alpha=0.8)
bars3 = ax7.bar(x_pos + width, camera_quality['sharpness_score']/20, width, label='Sharpness/20', alpha=0.8)

ax7.set_xlabel('Camera Model')
ax7.set_ylabel('Normalized Values')
ax7.set_title('Quality Metrics by Camera Model', fontweight='bold')
ax7.set_xticks(x_pos)
ax7.set_xticklabels(camera_quality.index, rotation=45, ha='right')
ax7.legend()
ax7.grid(axis='y', alpha=0.3)

# 8. Brightness vs Sharpness
ax8 = plt.subplot(3, 3, 8)
for camera in df['camera_model'].unique():
    subset = df[df['camera_model'] == camera]
    ax8.scatter(subset['brightness'], subset['sharpness_score'],
                label=camera, s=100, alpha=0.6)
ax8.set_xlabel('Brightness')
ax8.set_ylabel('Sharpness Score')
ax8.set_title('Brightness vs Sharpness by Camera', fontweight='bold')
ax8.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax8.grid(alpha=0.3)

# 9. Summary Statistics Table
ax9 = plt.subplot(3, 3, 9)
ax9.axis('off')

summary_text = f"""
PHASE A SUMMARY STATISTICS
{'='*40}

Total Images: {len(df)}
Left Eye: {len(df[df['eye_side']=='LEFT'])}
Right Eye: {len(df[df['eye_side']=='RIGHT'])}

Unique Cameras: {df['camera_model'].nunique()}

RESOLUTION
  Mean: {df['megapixels'].mean():.2f} MP
  Min: {df['megapixels'].min():.2f} MP
  Max: {df['megapixels'].max():.2f} MP

BRIGHTNESS
  Mean: {df['brightness'].mean():.2f}
  Std: {df['brightness'].std():.2f}

SHARPNESS
  Mean: {df['sharpness_score'].mean():.2f}
  Std: {df['sharpness_score'].std():.2f}

FILE SIZE
  Mean: {df['file_size_kb'].mean():.0f} KB
  Range: {df['file_size_kb'].min():.0f} - {df['file_size_kb'].max():.0f} KB
"""

ax9.text(0.1, 0.95, summary_text, transform=ax9.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()
plt.savefig(r'C:\Users\User2\Desktop\Nicole\phase_a_analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("Dashboard saved to: phase_a_analysis_dashboard.png")
plt.show()

# Generate individual camera reports
print("\n" + "="*60)
print("DETAILED CAMERA ANALYSIS")
print("="*60)

for camera in df['camera_model'].unique():
    camera_df = df[df['camera_model'] == camera]
    print(f"\n{camera.upper()}")
    print("-" * 40)
    print(f"  Image Count: {len(camera_df)}")
    print(f"  Avg Resolution: {camera_df['megapixels'].mean():.2f} MP")
    print(f"  Avg Brightness: {camera_df['brightness'].mean():.2f}")
    print(f"  Avg Sharpness: {camera_df['sharpness_score'].mean():.2f}")
    print(f"  Avg File Size: {camera_df['file_size_kb'].mean():.0f} KB")

    # Flash usage if available
    flash_info = camera_df['flash'].value_counts()
    if not flash_info.empty and flash_info.index[0] != 'N/A':
        print(f"  Flash Usage: {flash_info.to_dict()}")

# Identify quality concerns
print("\n" + "="*60)
print("QUALITY CONCERNS")
print("="*60)

# Low resolution images
low_res = df[df['megapixels'] < 2]
if not low_res.empty:
    print(f"\nLOW RESOLUTION IMAGES (<2 MP): {len(low_res)}")
    for _, row in low_res.iterrows():
        print(f"  - {row['filename']}: {row['megapixels']} MP ({row['camera_model']})")

# Low sharpness images
low_sharp = df[df['sharpness_score'] < 40]
if not low_sharp.empty:
    print(f"\nLOW SHARPNESS IMAGES (<40): {len(low_sharp)}")
    for _, row in low_sharp.iterrows():
        print(f"  - {row['filename']}: {row['sharpness_score']:.2f} ({row['camera_model']})")

# Dark images
dark = df[df['brightness'] < 100]
if not dark.empty:
    print(f"\nDARK IMAGES (<100 brightness): {len(dark)}")
    for _, row in dark.iterrows():
        print(f"  - {row['filename']}: {row['brightness']:.2f} ({row['camera_model']})")

# Missing EXIF data
no_exif = df[df['camera_model'] == 'N/A']
if not no_exif.empty:
    print(f"\nIMAGES WITH MISSING EXIF DATA: {len(no_exif)}")
    for _, row in no_exif.iterrows():
        print(f"  - {row['filename']}")
