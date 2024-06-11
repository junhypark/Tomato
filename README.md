# Tomato
> TOMATO(auTOMAtic descripTiOn) is automatic barrier free movie making project using several AI model for blind people.
> If you have any question, please use issues tab or contact us via: [![Gmail Badge](https://img.shields.io/badge/Gmail-d14836?style=flat-square&logo=Gmail&logoColor=white&link=mailto:jjuhee0913@gmail.com)](mailto:phjpurpleoob@gmail.com)

# 0. Instruction

> If you want to make a barrier free movie, you should prepare  "_*.mp4_" file and "_*.docx_" file(which is movie scenario).
> When movie and scenario file are prepared, you have to put your files in "input" folder.
> Then, just run "run.sh" on the Linux OS. We recommend to use Ubuntu 20.04.  

* If you ran "run.sh", you will see the command line as below.
![image](https://github.com/junhypark/Tomato/assets/164970413/2da79014-8802-449d-a946-03e020aa147f)

And if your Python environment is set up correctly, you will convert the scenario and movie files into barrier-free movies correctly.
(But this will take a so long time and computer resources to complete...)

* If you are using ```Anaconda``` Environemnt, please install torch using conda, not pip command

> If you already installed "torch, torchvision, torchaudio" via pip, please uninstall and download via conda

            pip uninstall torch torchvision torchaudio
            conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c pytorch

> We recommed you to use Anaconda Environment

* Via Anaconda, please use "runconda.sh", the example is below
![image](https://github.com/junhypark/Tomato/assets/58024443/278890fb-b5ba-4245-8477-db34a2511e8c)

---
# 1. Models

* environments: Ubuntu 20.04 LTS, Anaconda3 with 3.9.19 python version
* Need: Memory about Higher than 16GB in CPU
---
If you use conda virtual enviroment, please enter the below command.

            conda create -n modelscope python=3.9
            conda activate modelscope


## 1-1. Speech to Text

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

## 1-2. ko-sentence-transformers

To install, use pip:

            pip install -U sentence-transformers

For more information please look at https://github.com/jhgan00/ko-sentence-transformers

they recommend **Python 3.8 or higher**, at least **PyTorch 1.11.0**, and **transformers 4.32.0 or higher**

While using, there might be an error with ```ImportError: cannot import name 'get_full_repo_name' from 'huggingface_hub'```

Please run this command

            conda install chardet

It will fix the ImportError
---

## 1-3. pyannote

To install, use pip:

        pip install pyannote.audio==2.1.1

In order to math same torch version, we used 2.1.1

---

## 1-4. MeloTTS

We use the MeloTTS for Text to Speech task, so you should install MeloTTS. 

Please refer to the link below for download method.

            https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md

Before install MeloTTS library, you should install txtsplit-1.0.0. Please enter below command.

            pip install txtsplit

If "pip install txtsplit" is not working, you have to install manually.

            https://pypi.org/project/txtsplit/#files

Go to above link, and download "txtsplit-1.0.0.tar.gz". Unzip it, and put it to your working directory(tomato).

When you enter the "txtsplit" directory, you may see "setup.py". In the "txtsplit" folder, you enter below command.

            pip install -e .

Once you have installed the required dependent libraries, the txtsplit library will be installed. Please try it.

---

## 1-5. Additional Library

To run Tomato you have to install ```pydub```, ```moviepy```, and ```python-docx```

            pip install pydub

            pip install moviepy

            pip install python-docx
            
After install all library you can run init.py

---

## 1-6. Train KoBART

To paraphrase movie scenario description, we fine-tune KoBART(https://huggingface.co/gogamza/kobart-base-v2) pre-trained model. 

We deployed fine-tuned model on Google-Drive

            Google link

For you to train the model with your data, the dataset information used to train the model is as follows.
- Columns : Original, Paraphrased
- format of Dataset : "_.csv_"

In the "Original" column, you have to put in original movie description, and the "Paraphrased" column, you have to put in paraphrased original movie description. 

---
## 1-7. Result

After finish running python code, you can view result mp4 named in ```result.mp4```

---

# 2. Motivation

* 

---

# 3. With Web

* You can run this all file after finishing setting local WSL env with Python file, except ```toamto-app```

(We assume that Node.js is already installed)

First of all, please download all of your node package by running this command,

            npm install

Absolutely, you have to go to ```tomato-app``` via terminal

---

## Running

Set your terminal into proper folder path

1. run flask which is app.py

            python app.py

2. run node

            npm start

It will automatically, run WSL and python file

---

## Path

Although, the files are written in relative path, non-absolute path

In order to run all pipelines, you have to change folder path into your customized path in full path
