# Tomato
> TOMATO(auTOMAtic descripTiOn) is automatic barrier free movie making project using several AI model for blind people
> Please read carefully, all of these instructions

* If you have any question, please use issues tab or contact us via: [![Gmail Badge](https://img.shields.io/badge/Gmail-d14836?style=flat-square&logo=Gmail&logoColor=white&link=mailto:jjuhee0913@gmail.com)](mailto:phjpurpleoob@gmail.com)

# 0. Instruction

> * You should prepare  **.mp4** file and **.docx** file (which is movie scenario)
> * When movie and scenario file are prepared, you have to put your files in *input* folder
> * Then, just run **run.sh** or **runconda.sh** on the Linux OS. We recommend to use Ubuntu 20.04

* If you ran **run.sh**, you will see the command line as below
* NOTICE! activate correct conda environment before executing **run.sh**

![image](https://github.com/junhypark/Tomato/assets/58024443/ee6fd60a-851d-4e03-967a-98711a6363d1)

And if your Python environment is set up correctly, you will convert the scenario and movie files into barrier-free movies

> (But this will take a long time and computer resources to complete)

* If you are using ```Anaconda``` Environemnt, please install torch using **conda**, not pip command

> If you already installed **torch, torchvision, torchaudio** via pip, please uninstall and download via conda

            pip uninstall torch torchvision torchaudio
            conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c pytorch

> ### We recommed you to use Anaconda Environment

* Via Anaconda, please use **runconda.sh**, the example is below

![image](https://github.com/junhypark/Tomato/assets/58024443/fa7324b4-2c7d-4090-af24-1677de5583a1)

> ### Possible Error
> * If you copied files from **Windows** to **Ubuntu**

            sed -i 's/\r$//' FILE_NAME

---
# 1. Models

> **This pipeline is tested on WSL environment and anaconda**

* environments: Ubuntu 20.04 LTS, Anaconda3 with 3.9.19 python version
* Need: Memory about Higher than 16GB in CPU

In conda virtual enviroment, please enter the below command

            conda create -n modelscope python=3.9
            conda activate modelscope

### Sample Data

> Sample input data is on [gdrive](https://drive.google.com/drive/folders/1wI-GRdFcFO4lJnyJNsac2zU2YFBVp1FD?usp=sharing)
> * sample_input.mp4: sample video input
> * sample_docx.docx: sample docx input
---

## 1-1. Whisper

We used **whisper** model developed by **OpenAI** repectively, https://github.com/openai/whisper

Although **whisper** is developed in **Python 3.9.9** and **PyTorch 1.10.1**

And thanks to **OpenAI**, it is also runnable in **Python 3.9** and **PyTorch 1.11**

### So, we do not need to update any of them!

* for setup,

      pip install git+https://github.com/openai/whisper.git

* To update the package to the latest version of this repository, run:

      pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

* The **whisper** also requires the command-line tool ```ffmpeg```:

> for Ubuntu

    sudo apt install ffmpeg

If you need ```rust``` installed as well, please findout in the whisper github https://github.com/openai/whisper

---

## 1-2. Ko-SBERT

To install, use pip:

            pip install -U sentence-transformers

For more information please look at https://huggingface.co/jhgan/ko-sbert-sts

they recommend **Python 3.8 or higher**, at least **PyTorch 1.11.0**, and **transformers 4.32.0 or higher**

> ### Handling Possible Error
> * Via Anaconda Env, there might be an error with ```ImportError: cannot import name 'getfullreponame' from 'huggingfacehub'```
> * Please run this command

            conda install chardet

---

## 1-3. Pyannote

To install, use pip:

        pip install pyannote.audio==2.1.1

In order to math same torch version, we used 2.1.1

For more information please look at https://github.com/pyannote/pyannote-audio/releases/tag/2.1.1

> For token key, use private pyannote token keys
> * Follow this steps
> 1. visit [pyannote.speaker-diarization](https://huggingface.co/pyannote/speaker-diarization) and accept user conditions
> 2. visit [pyannote.segmentation](https://huggingface.co/pyannote/segmentation) and accept user conditions
> 3. visit [your tokens](https://huggingface.co/settings/tokens) to create an access token
> 4. instantiate pretrained speaker diarization pipeline
> * From https://huggingface.co/pyannote/speaker-diarizationFrom 
---

## 1-4. MeloTTS

We use the MeloTTS for Text to Speech task

1. ```transforemrs``` version is **4.27.4**
2. ```sentence-transforemrs``` version is **3.0.0**
3. ```boto3, botocore``` versions are **1.34.120** and **1.34.120**

Please refer to the link below for download method

            https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md

**Before install MeloTTS library, you should install txtsplit-1.0.0. Please enter below command**

            pip install txtsplit

> ### Possible Error
> If ```pip install txtsplit``` is not working, you have to install manually

            https://pypi.org/project/txtsplit/#files

> Go to above link, and download ```txtsplit-1.0.0.tar.gz```. Unzip it, and put it to your working directory(tomato)

In the [txtsplit](https://github.com/junhypark/Tomato/tree/main/txtsplit-1.0.0) directory, you may see ```setup.py```

In the ```txtsplit``` folder, you enter below command in terminal

            pip install -e .

Once you have installed the required dependent libraries, the txtsplit library will be installed

> ### Possible Error
> If version error occurs, please follow this instruction
> * ```transformers```

            pip uninstall transformers
            pip install transformers==4.27.4

> * ```sentence-transforemrs```

            pip uninstall sentence-transformers
            pip install sentence-transformers==3.0.0

> * ```boto3, botocore```

            pip uninstall boto3 botocore
            pip install boto3==1.34.120 botocore==1.34.120
---

## 1-5. Train KoBART

To paraphrase movie scenario description, we fine-tune [KoBART](https://huggingface.co/gogamza/kobart-base-v2) pre-trained model

We deployed fine-tuned model on [Google-Drive](https://drive.google.com/drive/folders/1VtR-CTfg2O8RCzLA52j2PZrrMu7rihBA?usp=drivelink)

> Please put files into [/train/model](https://github.com/junhypark/Tomato/tree/main/train/model)

For fine-tunining the model with your data, the dataset information used to train the model is as follows
- Columns : Original, Paraphrased
- format of Dataset : **.csv**

In the **Original** column, you have to put in original movie description, and the **Paraphrased** column, you have to put in paraphrased original movie description

> ### Data
> * [Example data](https://github.com/junhypark/Tomato/blob/main/train/data/train_sample.csv) is in **/train/data**

> ### Fine-tuning
> * Please change [train_koBART.py](https://github.com/junhypark/Tomato/blob/main/train/train_koBART.py) into your data
> * The data type is **.csv**

            ...
            def main():
                datapath = "YOUR_DATA_FILE_PATH"
            ...

> * For example

            ...
            def main():
                datapath = "./mydata/train.csv"
            ...
            
---

## 1-6. Additional Library

To run Tomato you have to install ```pydub```, ```moviepy```, and ```python-docx```

            pip install pydub

            pip install moviepy

            pip install python-docx
            
After install all library you can run ```runconda.sh``` or ```run.sh```

---

## 1-7. Result

After finish running python code, you can view result mp4 named in ```result.mp4```

---

# 2. With Web

* You can run this all file after finishing setting local WSL env with Python file, except ```toamto-app```

(We assume that Node.js is already installed)

First of all, please download all of your node package by running this command,

            npm install

Absolutely, you have to go to ```tomato-app``` via terminal

---

### 2-1. Running

Set your terminal into proper folder path

1. run flask which is app.py

            python app.py

2. run node

            npm start

It will automatically, run WSL and python file

1. input **.mp4** file

![image](https://github.com/junhypark/Tomato/assets/58024443/50f0884e-6c4a-4144-8863-73c252fb2e8d)

2. input **.docx** file

![image](https://github.com/junhypark/Tomato/assets/58024443/78fc0b96-a897-4ba2-a405-8ea9c820016b)

3. input **absolute path in WSL** and **conda env name**

ex)

![image](https://github.com/junhypark/Tomato/assets/58024443/ea7813b7-4645-4531-8d0a-99dc10d85d23)

4. Wait until processing is end

> When processing is finished, it automatically move to next step

![image](https://github.com/junhypark/Tomato/assets/58024443/f888e453-915c-4391-a227-93a6484cc3a5)

5. Click download button for result

![image](https://github.com/junhypark/Tomato/assets/58024443/da8a15ec-dc87-46ee-9501-0a70f8511d62)

> ## Path
> * In order to run all pipelines, absoulte path should be like **/home/usr_name/dir_name**
