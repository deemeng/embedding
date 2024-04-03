import re
import pandas as pd
from utils.common import read_json2dict

def sequence_mapping(list_seq: list) -> list:
    '''
    Given a list of sequences, map rarely Amino Acids [U Z O B] to [X].
    
    params:
        list_seq - list of sequences, e.g. ['A E T C Z A O', 'S K T Z P']
        
    return:
        the list of sequences with rarely AAs mapped to X.
    '''
    return [re.sub(f'[UZOB]', 'X', sequence) for sequence in list_seq]

def unique_seqID(df_loop: pd.DataFrame) -> list:
    '''
    Generate the seqID, uniprotAcc_start_end
    
    params:
        df_loop - dataframe, columns: [unp_acc, start_unp, end_unp]
    return:
        idx_loop - list of unique seqIDs
    '''
    idx_loop = [f'{acc}_{s}_{e}' for acc, s, e in zip(df_loop['unp_acc'], df_loop['start_unp'], df_loop['end_unp'])]
    return idx_loop

def get_pidChainUnp(path_pdb_chain_unp) -> list:
    '''
    Given uniprot & pdbChain mapping information, generate a list of pdbId_chainId_unpAcc.
    
    params:
        path_pdb_chain_unp - path to a json file, which saves the mapping between pdbChains & UniprotIDs
    
    return:
        list_pidChainUnp - e.g. ['1a04_a_uniprotID', '1a0i_a_uniprotID', '1a0p_a_uniprotID', ...]
    '''
    
    dict_pdb_chain_unp = read_json2dict(path_pdb_chain_unp)
    # # ['1a04_a_uniprotID', '1a0i_a_uniprotID', '1a0p_a_uniprotID', ...]
    list_pidChainUnp = []

    for pid, dict_chain_unp in dict_pdb_chain_unp.items():
        pid = pid.lower()
        for chain, unps in dict_chain_unp.items():
            list_pidChainUnp += [f'{pid}_{chain.lower()}_{unp}' for unp in unps]
    return list_pidChainUnp