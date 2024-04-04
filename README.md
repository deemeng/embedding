
# 🫠 Protein Sequence Embedding
This project provide three type of protein sequence embedding, including 1️⃣ onehot, 2️⃣ protTrans , and 3️⃣ MSA Transformer.
In this introduction, we provide two methods to run the programe and embed your proteins sequences
## 1. Docker (recommended)
* Pull the Docker image from  <a href="https://hub.docker.com/repository/docker/dimeng851/embedding/general">DockerHub</a>

  ```sh
  docker pull dimeng851/embedding:v1
  ```
* Edit the embeeding methods in Docker file
  >Default: apply all three emedding methods: 1️⃣ onehot, 2️⃣ protTrans , and 3️⃣ MSA Transformer. If you want to generate embedding from only one or two of the embedding methods\
  >  a. open Dockerfile\
  >  b. delete the embedding methods you don't want from
    ```sh
    CMD python /embedding/main.py --embeddingType onehot,protTrans,msaTrans
    ```
  
* run Containner
  ```sh
  docker run -d \
  -it \
  --name CONTAINER_NAME \
  --mount type=bind,source=PATH_TO_INPUT_FASTA_FILE,target=/embedding/data/input.fasta \
  --mount type=bind,source=PATH_TO_INPUT_A3M_FOLDER,target=/embedding/data/hmm \
  --mount type=bind,source=PATH_TO_INPUT_OUTPUT_FOLDER,target=/embedding/data/output \
  dimeng851/embedding:v1
  ```
  >Please replace the following parts:\
  >`CONTAINER_NAME` with any container name you like, 
  >`PATH_TO_INPUT_FASTA_FILE` with input fasta file path,
  >`PATH_TO_INPUT_A3M_FOLDER` with the folder to Hblits searching results, here we require `.a3m` files, and
  >`PATH_TO_INPUT_OUTPUT_FOLDER` with the folder you want to put the embedding sequences. Do not change the other parts.
  
  *Here is an example,*
  ```sh
  docker run -d \
  -it \
  --name embed_con \
  --mount type=bind,source=/Users/deemeng/Downloads/data/linker/linker.fasta,target=/embedding/data/input.fasta \
  --mount type=bind,source=/Users/deemeng/Downloads/data/linker/a3m,target=/embedding/data/hmm \
  --mount type=bind,source=/Users/deemeng/Downloads/data/linker/output/embedding,target=/embedding/data/output \
  dimeng851/embedding:v1
  ```
* Check the embedded results from the output folder you provided
* Here are some information about the Docker version this project used
  ```sh
  Client:
     Cloud integration: v1.0.35+desktop.10
     Version:           25.0.3
     API version:       1.44
     Go version:        go1.21.6
     Git commit:        4debf41
     Built:             Tue Feb  6 21:13:26 2024
     OS/Arch:           darwin/amd64
     Context:           desktop-linux

  Server: Docker Desktop 4.27.2 (137060)
     Engine:
      Version:          25.0.3
      API version:      1.44 (minimum version 1.24)
      Go version:       go1.21.6
      Git commit:       f417435
      Built:            Tue Feb  6 21:14:25 2024
      OS/Arch:          linux/amd64
      Experimental:     false
     containerd:
      Version:          1.6.28
      GitCommit:        ae07eda36dd25f8a1b98dfbf587313b99c0190bb
     runc:
      Version:          1.1.12
      GitCommit:        v1.1.12-0-g51d5e94
     docker-init:
      Version:          0.19.0
      GitCommit:        de40ad0
  ```
## 2. DOWNLOAD SOURCE CODE
* Download source code from this Git page
* Create env based on the `requirements.txt`
* Edit file/foler paths
  ```python
  '''*****************************USER-EDIT START*********************************'''
  '''Please edit this part if you prefer to change the path of input & output'''
  path_input = os.path.join(path_data, 'input.fasta')
  path_output = os.path.join(path_data, 'output')
  path_hmm = os.path.join(path_data, 'hmm')
  '''*****************************USER-EDIT END***********************************'''
  ```
  *Here is an example*
  ```python
  '''*****************************USER-EDIT START*********************************'''
  '''Please edit this part if you prefer to change the path of input & output'''
  path_input = '/Users/deemeng/Downloads/data/linker/linker.fasta'
  path_output = '/Users/deemeng/Downloads/data/linker/output/embedding'
  path_hmm = '/Users/deemeng/Downloads/data/linker/a3m'
  '''*****************************USER-EDIT END***********************************'''
  ```
* Run the programe on Terminal
  ```sh
  python main.py --embeddingType onehot,protTrans,msaTrans
  ```
* Check the embedded results from the output folder you provided

# Contact
Di Meng - di.meng@ucdconnect.ie
Gianluca Pollastri - gianluca.pollastri@ucd.ie
Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
