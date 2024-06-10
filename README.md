# Tomato
> TOMATO(auTOMAtic descripTiOn) is automatic barrier free movie making project using several AI model for blind people. 

# 0. Instruction

> If you want to make a barrier free movie, you should prepare  "_*.mp4_" file and "_*.docx_" file(which is movie scenario).
> When movie and scenario file are prepared, you have to put your files in "input" folder.
> Then, just run "run.sh" on the Linux OS. We recommend to use Ubuntu 20.04.  

* If you ran "run.sh", you will see the command line as below.
![image](https://github.com/junhypark/Tomato/assets/164970413/2da79014-8802-449d-a946-03e020aa147f)

And if your Python environment is set up correctly, you will convert the scenario and movie files into barrier-free movies correctly.
(But this will take a so long time and computer resources to complete...)

---
# 1. Models

* environments: Ubuntu 20.04 LTS, Anaconda3 with 3.9.19 python version
* Need: Memory about Higher than 16GB in CPU
---

## 1-1. Denoise

* We need a new virtual environment

* Used **Modelscope** which is from here
https://github.com/modelscope/modelscope

* we used **anaconda** for creating local python environment

      conda create -n modelscope python=3.8 
      conda activate modelscope

  * For using **modelscope framework**, install the core modelscope components:

        pip install modelscope

    or

        pip install modelscope[audio] -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html

* We used **FRCRN** which is developed by **Alibaba** https://github.com/alibabasglab/FRCRN

  * This model has a problem in above **PyTorch v1.11**

        conda install pytorch==1.11 torchaudio torchvision -c pytorch

  * for linux install ```libsndfile1```

        sudo apt-get update

        sudo apt-get install libsndfile1

---

## 1-2. Speech to Text

* We used **whisper** model developed by **OpenAI** repectively, https://github.com/openai/whisper

* Although **whisper** is developed in **Python 3.9.9** and **PyTorch 1.10.1**

* And thanks to **OpenAI**, it is also runnable in **Python 3.8.10** and **PyTorch 1.11**

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

## 1-3. ko-sentence-transformers

* To install, use pip:

        pip install -U sentence-transformers

* For more information please look at https://github.com/jhgan00/ko-sentence-transformers

* they recommend **Python 3.8 or higher**, at least **PyTorch 1.11.0**, and **transformers 4.32.0 or higher**

---

## 1-4. pyannote

* To install, use pip:

        pip install pyannote.audio==2.1.1

* In order to math same torch version, we used 2.1.1

---

## 1-5. MeloTTS

We use the MeloTTS for Text to Speech task, so you should install MeloTTS. 

Please refer to the link below for download method.
      https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md

* Nothing to handle with versions, do not worry

---

## 1-6. Additional Library

* To run Tomato you have to install ```pydub```, ```moviepy```, and ```python-docx```

        pip install pydub

        pip install moviepy

        pip install python-docx

* After install all library you can run init.py

---

## 1-7. Result

* After finish running python code, you can view result mp4 named in ```result.mp4```

---

# 2. Motivation

* 
