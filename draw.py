
import textwrap

from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BG_FILE = 'background.jpg'


def rand_crop(x, dims=(9, 7), scale=1.0, resolution=54):
    
    h, w = x.shape[:2]
    w_new = int(scale * dims[0] * resolution)
    h_new = int(scale * dims[1] * resolution)
    if w_new > w or h_new > h:
        w_new, h_new = w, h
    left = int((w - w_new) * np.random.rand())
    top = int((h - h_new) * np.random.rand())
    
    return x[top:top + h_new, left:left + w_new, :]


def draw_card(text, out_path=None, dims=(9, 7), std_xy=1.0, text_size=20, bg_path=BG_FILE, max_angle=10, dy=0.45):

    w, h = dims
    facecolor=[1, 1, .98]

    x0 = std_xy * np.random.randn()
    y0 = std_xy * np.random.randn()
    scale = np.random.rand() + 1
    text_size /= scale
    
    xlim = [-scale * w/2, scale * w/2]
    ylim = [-scale * h/2, scale * h/2]
    fig, ax = plt.subplots(1, 1, figsize=(w, h))
    if bg_path is not None:
        im = np.array(Image.open(bg_path), dtype=np.uint8)
        im = rand_crop(im, dims=dims, scale=scale)
        ax.imshow(im, extent=xlim + ylim, origin='upper')
    
    ax.axis('off');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    lines = textwrap.fill(text, 42).split('\n')
    n_lines = sum(len(l) for l in lines) / max(len(l) for l in lines)
    rand_angle = max_angle * (2 * np.random.rand() - 1)
    rect = patches.FancyBboxPatch((x0 - w/2,y0 - h/2), w/1, h/1, linewidth=0, facecolor=facecolor,
                                  boxstyle="round,pad=0.0,rounding_size=0.5")
    transform = mpl.transforms.Affine2D().rotate_deg(rand_angle) + ax.transData
    rect.set_transform(transform)
    ax.add_patch(rect);
    y0 = y0 + dy * (n_lines - 1) / 2
    for i, line in enumerate(lines):
        y = y0 - dy * i
        if len(lines) > 1:
            # left-align multi-line prompts
            ax.text(x0 - w/2.8, y, line, size=text_size, color=[.2, .2, .3], name='helvetica',
                    ha='left', rotation=rand_angle, rotation_mode='anchor', transform=transform)
        else:
            # center single-line prompts
            ax.text(x0, y, line, size=text_size, color=[.2, .2, .3], # name='helvetica',
                    ha='center', rotation=rand_angle, rotation_mode='anchor', transform=transform)

    if out_path:
        fig.savefig(out_path, pad_inches=0.0, bbox_inches='tight')
