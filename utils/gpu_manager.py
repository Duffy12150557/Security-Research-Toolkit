# -*- coding: utf-8 -*-
"""GPU memory management (stub for optional CUDA)."""


def get_gpu_info():
    """Return list of GPU info dicts or empty list if no GPU."""
    try:
        import subprocess
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            lines = out.stdout.strip().split("\n")
            return [{"raw": line.strip()} for line in lines]
    except Exception:
        pass
    return []


def suggest_device():
    """Return 'cuda' if GPU available else 'cpu'."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
    except ImportError:
        pass
    return "cpu"
