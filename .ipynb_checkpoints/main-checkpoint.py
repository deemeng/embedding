import os
import argparse
import datetime

from Bio import SeqIO
import params as params
from utils.common import dump_list2json

def list_of_strings(arg):
    return arg.split(',')
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Take args from CMD."
    )
    # choices=['onehot', 'protTrans', 'msaTrans']
    parser.add_argument("--embeddingType", required=True,
                        type=list_of_strings, help="Choose one from ['onehot', 'protTrans', 'msaTrans']")
    # Parse the command-line arguments
    args = parser.parse_args()
    list_embeddingType = args.embeddingType

    '''
    1. JSON file
    '''
    # get FASTA file
    fasta_sequences = SeqIO.parse(open(params.path_input),'fasta')
    list_entity = []
    for entity in fasta_sequences:
        dict_e = {}
        dict_e['id'], dict_e['sequence'] = entity.id, str(entity.seq)
        list_entity.append(dict_e)

    # save JSON file
    dump_list2json(list_entity, params.path_input_dataset_json)
    print(f'input JSON file is created under: {params.path_input_dataset_json}')

    '''
    2. Embedding
    '''
    for embeddingType in list_embeddingType:
        comment = f'Running Embedding: {embeddingType}\nstarted at {str(datetime.datetime.now())}'
        print(comment)
        if embeddingType == 'onehot':
            from method.onehot import onehot
            path_output_features = params.path_output_features_onehot
            onehot(params.path_input_dataset_json, path_output_features)
        elif embeddingType == 'protTrans':
            from method.protTrans import protTrans
            path_output_features = params.path_output_features_protTrans
            protTrans(params.path_input_dataset_json, path_output_features)
        elif embeddingType == 'msaTrans':
            from method.msaTrans import msaTrans
            path_output_features = params.path_output_features_msaTrans
            msaTrans(params.path_input_dataset_json, path_output_features, params.path_hmm)
            
    if os.path.exists(params.path_input_dataset_json):
        os.remove(params.path_input_dataset_json)
        print(f'input JSON file is deleted: {params.path_input_dataset_json}')
    else:
        print(f'input JSON file does not exist: {params.path_input_dataset_json}') 
    
            