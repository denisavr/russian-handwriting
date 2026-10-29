#!/usr/bin/env python3
"""Create a deterministic local manuscript view. Requires optional Pillow."""
import argparse
import hashlib
import json
from pathlib import Path


def prepare(source, output, box=None, scale=1, grayscale=False, contrast=1):
    from PIL import Image,ImageEnhance
    if source.resolve()==output.resolve():
        raise ValueError('output must not overwrite the original')
    if not 0 < scale <= 4 or not 0 < contrast <= 4:
        raise ValueError('scale and contrast must be in (0,4]')
    original=source.read_bytes()
    with Image.open(source) as image:
        view=image.convert('RGB')
        if box is not None:
            x,y,w,h=box
            if min(x,y)<0 or min(w,h)<=0 or x+w>image.width or y+h>image.height:
                raise ValueError('crop outside source image')
            view=view.crop((x,y,x+w,y+h))
        if grayscale:view=view.convert('L')
        if contrast!=1:view=ImageEnhance.Contrast(view).enhance(contrast)
        if scale!=1:view=view.resize((round(view.width*scale),round(view.height*scale)),Image.Resampling.BICUBIC)
        output.parent.mkdir(parents=True,exist_ok=True)
        view.save(output)
        size=list(view.size)
    return dict(source_sha256=hashlib.sha256(original).hexdigest(),box_xywh=box,
                scale=scale,grayscale=grayscale,contrast=contrast,output_size=size,
                output_sha256=hashlib.sha256(output.read_bytes()).hexdigest())


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--box',type=int,nargs=4,metavar=('X','Y','WIDTH','HEIGHT'))
    p.add_argument('--scale',type=float,default=1)
    p.add_argument('--grayscale',action='store_true')
    p.add_argument('--contrast',type=float,default=1)
    a=p.parse_args()
    try:result=prepare(a.source,a.output,a.box,a.scale,a.grayscale,a.contrast)
    except ImportError:p.error('Pillow is needed only for this optional helper; use an image-capable runtime or the host viewer.')
    except ValueError as e:p.error(str(e))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
