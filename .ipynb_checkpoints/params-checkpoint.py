import os

'''
utils function
'''
def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
'''
Path
'''
ROOT = os.path.realpath('.')
path_data = os.path.join(ROOT, 'data')
path_input_dataset_json = os.path.join(path_data, 'dataset.json')

'''*****************************USER-EDIT START*********************************'''
'''Please edit this part if you prefer to change the path of input & output'''
# path_input = os.path.join(path_data, 'input.fasta')
# path_output = os.path.join(path_data, 'output')
# path_hmm = os.path.join(path_data, 'hmm')

path_input = '/home/dimeng/caid3/linker_long.fasta'
path_output = '/home/dimeng/caid3/output'
path_hmm = '/home/dimeng/project/linker_caid/a3m'
'''*****************************USER-EDIT END***********************************'''
create_folder(path_output)
create_folder(path_hmm)

path_output_features_onehot = os.path.join(path_output, 'onehot')
path_output_features_protTrans = os.path.join(path_output, 'protTrans')
path_output_features_msaTrans = os.path.join(path_output, 'msaTrans')

create_folder(path_output_features_onehot)
create_folder(path_output_features_protTrans)
create_folder(path_output_features_msaTrans)