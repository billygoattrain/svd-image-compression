"""Shared SVD image-compression functions for MATH 344L."""
import numpy as np

def rank_k_approx(A, k):
    A = np.asarray(A, dtype=float)
    if not (1 <= k <= min(A.shape)):
        raise ValueError("k must be between 1 and min(image dimensions)")
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    return (U[:, :k] * s[:k]) @ Vt[:k, :]

def storage(m, n, k):
    return int(k * (m + n + 1))

def compression_ratio(m, n, k):
    return m * n / storage(m, n, k)

def rel_error(A, B):
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    denominator = np.linalg.norm(A)
    return np.linalg.norm(A-B) / denominator if denominator else float(np.linalg.norm(A-B))

def predicted_error(s, k):
    s = np.asarray(s, dtype=float)
    return np.sqrt(np.sum(s[k:]**2) / np.sum(s**2)) if np.any(s) else 0.0

def k_for_error(s, target):
    for k in range(1, len(s)+1):
        if predicted_error(s, k) <= target:
            return k
    return len(s)
