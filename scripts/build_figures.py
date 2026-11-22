"""Regenerate the two project figures using the same equations as Milestones 3 and 4.

Run from the repository root: python scripts/build_figures.py
"""
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from skimage import data

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from compress import predicted_error, compression_ratio, k_for_error

FIGURES = ROOT / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

# Milestone 3: camera versus printed text
A, T = data.camera().astype(float), data.text().astype(float)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
for name, M in (("camera", A), ("text", T)):
    height, width = M.shape
    singular = np.linalg.svd(M, compute_uv=False)
    ranks = np.arange(1, len(singular) + 1)
    errs = np.array([predicted_error(singular, int(k)) for k in ranks])
    ratios = np.array([compression_ratio(height, width, int(k)) for k in ranks])
    ax1.plot(ranks, errs, label=name)
    ax2.semilogx(ratios, errs, label=name)
ax1.set(title="Relative error vs. rank", xlabel="Rank k", ylabel="Relative Frobenius error")
ax2.set(title="Relative error vs. compression ratio", xlabel="Compression ratio (log scale)", ylabel="Relative Frobenius error")
ax2.axvline(1, color="gray", linestyle="--", label="Ratio = 1")
for ax in (ax1, ax2):
    ax.grid(True, alpha=0.3)
    ax.legend()
plt.tight_layout()
fig.savefig(FIGURES / "error_vs_ratio.png", dpi=150)
plt.close(fig)

# Milestone 4: striped images rotated 0 to 90 degrees
N = 256
i, j = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
def stripes(angle, width=16):
    theta = np.deg2rad(angle)
    return 255.0 * (np.floor((i * np.cos(theta) + j * np.sin(theta)) / width) % 2)

angles = np.arange(0, 91, 5)
needed = [k_for_error(np.linalg.svd(stripes(float(a)), compute_uv=False), 0.05)
          for a in angles]
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(angles, needed, "o-")
ax.set(xlabel="Angle of stripes (degrees)", ylabel="k needed for 5% error",
       title="Same stripes, different angles")
ax.grid(True)
plt.tight_layout()
fig.savefig(FIGURES / "angles.png", dpi=150)
plt.close(fig)
print("Figure paths:", FIGURES / "error_vs_ratio.png", FIGURES / "angles.png")
print("Stripe ranks for angles 0, 5, 45, 90:", needed[0], needed[1], needed[9], needed[-1])
