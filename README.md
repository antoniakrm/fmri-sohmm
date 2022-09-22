Extracting token-level signals from fmri data

## How to Run

To replicate the results, run

```bash ./run_all.sh```

It will run first baseline, then type-level-experiment and last token-level.

Or run them individually by running: 
```bash ./run_fmri_MB.sh [baseline | type | token]```

## Setup Instructions

### Setup Python Virtual Environment with Conda
    1. apt-get update
    2. sudo apt install python3-pip
    3. download the installer for your python version at https://docs.conda.io/en/latest/miniconda.html#linux-installers
    (run "python -V" or "python3 -V" to see your version)
    4. run the installer and follow instructions
    5. source ~/.bashrc #or restart shell
    6. conda install python=3.9
    7. conda create --name fmrienv python=3.9

### Install Requirements
    1. conda activate fmrienv
    2. python -m pip install -r requirements.txt

### Citation:
```
@inproceedings{bingel-etal-2016-extracting,
    title = "Extracting token-level signals of syntactic processing from f{MRI} - with an application to {P}o{S} induction",
    author = "Bingel, Joachim  and
      Barrett, Maria  and
      S{\o}gaard, Anders",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P16-1071",
    doi = "10.18653/v1/P16-1071",
    pages = "747--755",
}
```
