import pandas as pd
import numpy as np

from utils.sequence import unique_seqID, get_pidChainUnp
from method.utils import save_embedded_onehot
from params import *
from utils.common import read_json2list

'''
Aim to embed the Domain-linker by one-hot encoding. And save them to files.

Di
26 Sep, 2023
'''
# Embed and save
def onehot(path_input_dataset_json, path_output_features_onehot):
    list_idrDataset = read_json2list(path_input_dataset_json)
    
    list_seq = []
    list_id = []
            
    for dict_idr in list_idrDataset:
        seq = ''.join(dict_idr['sequence'])
        list_seq.append(seq)
        list_id.append(dict_idr['id'])
    
    save_embedded_onehot(list_seq, list_id, path_output_features_onehot)
    print('Done!!!')