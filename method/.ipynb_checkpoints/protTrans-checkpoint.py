import pandas as pd
import numpy as np

import torch
# only the encoder part of the mdoel
from transformers import T5EncoderModel, T5Tokenizer
import re
import gc

from method.utils import save_embedded_protTrans
from utils.common import read_json2list

'''
Aim to embed the CAID2 linker dataset (40 sequences in total). And save them to files.

Di
19 Oct, 2023

The embedding is actually runned on dunnion server.
This server does not have enough space to run it.
'''
def protTrans(path_input_dataset_json, path_output_features_protTrans):
    # 1. model
    tokenizer = T5Tokenizer.from_pretrained("Rostlab/prot_t5_xl_uniref50", do_lower_case=False)
    model = T5EncoderModel.from_pretrained("Rostlab/prot_t5_xl_uniref50")
    
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(f'device: {device}')
    model = model.to(device)
    model = model.eval()
    
    # 2. embed and save
    list_idrDataset = read_json2list(path_input_dataset_json)
    
    list_seq = []
    list_id = []
            
    for dict_idr in list_idrDataset:
        seq = ' '.join(dict_idr['sequence'])
        list_seq.append(seq)
        list_id.append(dict_idr['id'])
    
    save_embedded_protTrans(list_seq, list_id, path_output_features_protTrans, model, tokenizer)
    print('Done!!!')