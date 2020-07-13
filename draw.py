
import textwrap

from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BG_FILE = 'background.jpg'


def rand_crop(x, w_new=650, h_new=400):
    
    h, w = x.shape[:2]
    left = int((w - w_new) * np.random.rand())
    top = int((h - h_new) * np.random.rand())
    
    return x[top:top + h_new, left:left + w_new, :]


def draw_card(text, out_path=None, dims=(13, 8), text_size=24, linewidth=0, bg_path=BG_FILE, max_angle=10):

    w, h = dims
    edgecolor=[.2, .2, .2]
    facecolor=[1, 1, .98]
    bg_scale = 1.4
    im_zoom = 2
    text_size /= bg_scale
    
    xlim = [-bg_scale * w/2, bg_scale * w/2]
    ylim = [-bg_scale * h/2, bg_scale * h/2]

    fig, ax = plt.subplots(1, 1, figsize=(w, h))
    if bg_path is not None:
        im = np.array(Image.open(bg_path), dtype=np.uint8)
        im = rand_crop(im)
        ax.imshow(im, extent=xlim + ylim, origin='upper')
    
    ax.axis('off');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    lines = textwrap.fill(text, 39).split('\n')
    dy = 0.8
    n_lines = sum(len(l) for l in lines) / max(len(l) for l in lines)
    y0 = dy * (n_lines - 1) / 2
    rand_angle = max_angle * (2 * np.random.rand() - 1)
    for i, line in enumerate(lines):
        y = y0 - dy * i
        ax.text(0, y, line, ha='center', size=text_size, rotation=rand_angle, color=[.2, .2, .2])
    rect = patches.FancyBboxPatch((-w/2.2,-h/2.2), w/1.1, h/1.1, linewidth=linewidth, ec=edgecolor, fc=facecolor,
                                  boxstyle="round,pad=0.03,rounding_size=0.65")
    rect.set_transform(mpl.transforms.Affine2D().rotate_deg(rand_angle) + ax.transData)
    ax.add_patch(rect);
    if out_path:
        fig.savefig(out_path, pad_inches=0.0, bbox_inches='tight')
