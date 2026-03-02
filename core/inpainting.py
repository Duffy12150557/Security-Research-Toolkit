# -*- coding: utf-8 -*-
"""Neural inpainting algorithms (stub: no heavy ML deps by default)."""


def inpaint_frame(frame_region, mask_region, device="cpu"):
    """
    Inpaint a region of a frame using neural inpainting.
    Args:
        frame_region: image data (numpy or tensor)
        mask_region: binary mask
        device: 'cpu' or 'cuda'
    Returns:
        Inpainted region (same type as input).
    """
    # Stub: return as-is; replace with real model (e.g. AOT-GAN, LaMa) when needed
    return frame_region


def inpaint_video_frames(frames, masks, device="cpu"):
    """
    Inpaint multiple frames. Yields (frame_index, inpainted_frame).
    """
    for i, (fr, ma) in enumerate(zip(frames, masks)):
        yield i, inpaint_frame(fr, ma, device)
