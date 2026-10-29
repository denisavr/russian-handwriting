#!/usr/bin/env python3
"""Launch configured local inference without installing or downloading anything."""
import argparse,json,os,sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('line_image',type=Path)
    parser.add_argument('--config',type=Path,default=Path(os.environ.get('RUSSIAN_HANDWRITING_CONFIG',str(Path.home()/'.codex/russian-handwriting-runtime.json'))))
    args=parser.parse_args()
    try:
        config=json.loads(args.config.read_text())
        python=Path(config['python']);model=Path(config['model_directory'])
        if not python.is_absolute() or not model.is_absolute():raise ValueError('Runtime paths must be absolute')
        if not python.is_file() or not model.is_dir():raise ValueError('Configured local runtime or model is missing')
        if not args.line_image.is_file():raise ValueError('Input image is missing')
    except (OSError,ValueError,KeyError) as exc:parser.exit(2,f'Local HTR unavailable: {exc}\n')
    backend=Path(__file__).with_name('recognize_line.py')
    os.execv(str(python),[str(python),str(backend),str(model),str(args.line_image)])

if __name__=='__main__':main()
