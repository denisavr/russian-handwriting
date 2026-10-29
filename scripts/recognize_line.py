#!/usr/bin/env python3
"""Local single-line CRNN inference; requires torch, numpy, Pillow.

Architecture: Puigcerver2017-compatible CNN/BiLSTM/CTC.
Weights: achimrabus/crnn-ctc-russian, Apache-2.0, pinned revision.
No network access or imports from downloaded model code.
"""
import argparse
import hashlib
import json
from pathlib import Path

MODEL_SHA256 = '74482bd0eb8e33b25a197d0452559b888809dd0ae4e014274301a513f553dd32'
MODEL_REVISION = 'ebb5fc91eb44f40f049bafd74bc95f7c0e2b1ee8'

def recognize(model_dir, line_path):
    import numpy as np
    import torch
    from torch import nn
    from torch.nn import functional as f
    from PIL import Image
    checkpoint_path = Path(model_dir) / 'best_model.pt'
    if hashlib.sha256(checkpoint_path.read_bytes()).hexdigest() != MODEL_SHA256:
        raise ValueError('Unsupported checkpoint: SHA-256 does not match the pinned model')
    checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
    state = checkpoint['model_state_dict']
    symbols = {int(k): (' ' if v in ('<SPACE>', '<space>') else v)
               for k,v in checkpoint['idx2char'].items()}
    torch.set_num_threads(4)
    image = Image.open(line_path).convert('L')
    target_width = max(1, round(128 * image.width / image.height))
    if target_width > 12000:
        raise ValueError('Expected one line; aspect ratio is too large')
    image = image.resize((target_width,128),Image.Resampling.LANCZOS)
    pixels = np.asarray(image,dtype=np.float32) / 127.5 - 1
    x = torch.from_numpy(pixels.copy())[None,None]
    recurrent = nn.LSTM(768,256,3,bidirectional=True,dropout=.5)
    recurrent.load_state_dict({k[4:]:v for k,v in state.items() if k.startswith('rnn.')})
    recurrent.eval()
    with torch.inference_mode():
        for conv,batch,pool in [(0,1,True),(4,5,True),(8,9,False),(11,12,True)]:
            x = f.conv2d(x,state[f'cnn.{conv}.weight'],state[f'cnn.{conv}.bias'],padding=1)
            x = f.batch_norm(x,state[f'cnn.{batch}.running_mean'],state[f'cnn.{batch}.running_var'],
                             state[f'cnn.{batch}.weight'],state[f'cnn.{batch}.bias'],training=False)
            x = f.leaky_relu(x,negative_slope=.2)
            if pool: x = f.max_pool2d(x,2)
        sequence = x.permute(3,0,1,2).flatten(2)
        encoded,_ = recurrent(sequence)
        probabilities = f.linear(encoded,state['fc.weight'],state['fc.bias']).softmax(2)
        scores,indices = probabilities.max(2)
    text=[];selected=[];last=-1
    for index,score in zip(indices[:,0].tolist(),scores[:,0].tolist()):
        if index and index!=last:
            char=symbols.get(index,'')
            if char:text.append(char);selected.append(score)
        last=index
    return {'text':''.join(text),'mean_nonblank_probability':sum(selected)/len(selected) if selected else 0,
            'probability_is_not_calibrated_correctness':True,'decoder':'greedy','device':'cpu',
            'engine':'achimrabus/crnn-ctc-russian','revision':MODEL_REVISION,
            'image_sha256':hashlib.sha256(Path(line_path).read_bytes()).hexdigest()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model_directory',type=Path)
    parser.add_argument('line_image',type=Path)
    args=parser.parse_args()
    try: result=recognize(args.model_directory,args.line_image)
    except (ValueError,KeyError,OSError) as exc:parser.exit(2,f'Error: {exc}\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
