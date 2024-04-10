import os
import pandas as pd
import numpy as np

import torch
import esm

import re
import gc

from utils.common import load_tab, save_np, load_np, read_json2list
from utils.alignmentParser import read_msa, greedy_select

torch.set_grad_enabled(False)
'''
Aim to embed the Disprot (include Linkers) Sequences. And save them to files.

Di
10 Mar, 2024
'''
def msaTrans(path_input_dataset_json, path_output_features_msaTrans, path_hmm):
    # 1. mdoel & tokenizer
    msa_transformer, msa_transformer_alphabet = esm.pretrained.esm_msa1b_t12_100M_UR50S()
    msa_transformer = msa_transformer.eval()
    msa_transformer_batch_converter = msa_transformer_alphabet.get_batch_converter()
    
    # 2. predict & save embedded sequences
    df_dataset = pd.DataFrame(read_json2list(path_input_dataset_json))
    df_dataset['length'] = [len(seq) for seq in df_dataset['sequence']]
    df_dataset['len_1022'] = [1 if l<=1022 else 0 for l in df_dataset['length']]

    long_seq_IDS = list(set(df_dataset.loc[df_dataset['len_1022']==0, 'id'].tolist()))
    
    if len(long_seq_IDS)>0:
        print(f"Note: MSA Transformer cannot embed sequences with length >= 1022!!!\nTherefore, we cannot embed: {long_seq_IDS}")
        
    # entyID_entityID
    seq_IDS = list(set(df_dataset.loc[df_dataset['len_1022']==1, 'id'].tolist()))
        
    for name in seq_IDS:
        print(name)
         # This is where the data is actually read in
        inputs = read_msa(os.path.join(path_hmm, f'{name}.a3m'))
        
        if len(inputs[0][1])>1022:
            print(f'Sequence (MSA searching results) length ({len(inputs[0][1])}) is greater than 1022. ')
            df_dataset.loc[df_dataset['id']==name, 'len_1022'] = 0
            continue
        
        inputs = greedy_select(inputs, num_seqs=128) # can change this to pass more/fewer sequences
        msa_transformer_batch_labels, msa_transformer_batch_strs, msa_transformer_batch_tokens = msa_transformer_batch_converter([inputs])
        msa_transformer_batch_tokens = msa_transformer_batch_tokens.to(next(msa_transformer.parameters()).device)
        # Extract per-residue representations (on CPU)
        with torch.no_grad():
            results = msa_transformer(msa_transformer_batch_tokens, repr_layers=[12], return_contacts=False)
        token_representations = results["representations"][12]
        seq_representation = token_representations[:, :, 1: ].mean(1)
        # save embedd sequences
        save_np(seq_representation, os.path.join(path_output_features_msaTrans, f'{name}.npy'))
    
    print('Done!!!')