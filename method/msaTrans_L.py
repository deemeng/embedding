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

def _msaTrans_long(length: int, name: str, path_hmm: str, msa_transformer_batch_tokens, msa_transformer):
    '''
    params:
        length - int, sequence length
        name - protein ID, for reading NAME.a3m file
        path_hmm - folder dir to .a3m files
        msa_transformer_batch_tokens - array, (1, 128, length)

    return:
        embed_seq - numpy array, shape: (1,length ,768), where 768 is number of features

    IDEA:
        window size: 1000 residues
        step size: 500
        except real head&tail, embedding for the first 50 AAs and last 50 AAs are not used since they are not reliable. For other overlapped residues 
    '''
    embed_seq = np.empty([1, length, 768])
    
    # separate the long sequence
    for i in range(length//500):
        # tail
        if (i+2)*500>=length:
            batch_token = msa_transformer_batch_tokens[:, :, [0]+list(range(i*500+1, length+1))]
        else:
            batch_token = msa_transformer_batch_tokens[:, :, [0]+list(range(i*500+1, i*500+1000+1))]
        with torch.no_grad():
            results = msa_transformer(batch_token, repr_layers=[12], return_contacts=False)
        token_representations = results["representations"][12]
        seq_representation = token_representations[:, :, 1: ].mean(1)
        seq_rep = seq_representation.detach().cpu().numpy()
        # head
        if i==0:
            embed_seq[:, i: i+1000, :] = seq_rep
        else:
            seq_rep[:, 50:450, :] = (embed_seq[:, (i-1)*500+1000-450:(i-1)*500+1000-50, :] + seq_rep[:, 50:450, :])/2
            
            if (i+2)*500>=length:
                embed_seq[:, (i-1)*500+1000-450:, :] = seq_rep[:, 50:, :]
            else:
                embed_seq[:, (i-1)*500+1000-450:i*500+1000, :] = seq_rep[:, 50:, :]
    return embed_seq
    
def msaTrans(path_input_dataset_json, path_output_features_msaTrans, path_hmm):
    # 1. mdoel & tokenizer
    msa_transformer, msa_transformer_alphabet = esm.pretrained.esm_msa1b_t12_100M_UR50S()
    msa_transformer = msa_transformer.eval()
    msa_transformer_batch_converter = msa_transformer_alphabet.get_batch_converter()
    
    # 2. predict & save embedded sequences
    df_dataset = pd.DataFrame(read_json2list(path_input_dataset_json))
    df_dataset['length'] = [len(seq) for seq in df_dataset['sequence']]
    df_dataset_long = df_dataset[df_dataset['length']>1022]
    
    df_dataset = df_dataset[df_dataset['length']<=1022]
    
    # 2.1. short sequences
    # entyID_entityID
    seq_IDS = list(set(df_dataset['id'].tolist()))
    for name in seq_IDS:
        print(name)
        # This is where the data is actually read in
        inputs = read_msa(os.path.join(path_hmm, f'{name}.a3m'))
        
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
    
    # 2.2. long sequences
    # for sequence length greater than 1022(1022 + start/end tokens)
    for idx, row in df_dataset_long.iterrows():
        length = row['length']
        name = row['id']
        print(name)
        # load the long sequence
        inputs = read_msa(os.path.join(path_hmm, f'{name}.a3m'))
        inputs = greedy_select(inputs, num_seqs=128)
        _, _, msa_transformer_batch_tokens = msa_transformer_batch_converter([inputs])
        msa_transformer_batch_tokens = msa_transformer_batch_tokens.to(next(msa_transformer.parameters()).device)
        
        embed_seq = _msaTrans_long(length, name, path_hmm, msa_transformer_batch_tokens, msa_transformer)
        # save embedd sequences
        save_np(embed_seq, os.path.join(path_output_features_msaTrans, f'{name}.npy'))
    print('Done!!!')