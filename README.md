# Tomato
TOMATO: For Barrier Free Movie Automatic Description

0. Introduction

1. Models

environments: Ubuntu 20.04 LTS

1-1. Denoise

We need a new virtual environment

Used Modelscope which is from here
https://github.com/modelscope/modelscope

we used anaconda for creating local python environment

```conda create -n modelscope python=3.8```

```conda activate modelscope```

For using modelscope framework, install the core modelscope components:

```pip install modelscope```

or

```pip install modelscope[audio] -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html```

We used FRCRN which is developed by Alibaba https://github.com/alibabasglab/FRCRN

This model has a problem in above PyTorch v1.11

```conda install pytorch==1.11 torchaudio torchvision -c pytorch```

for linux install libsndfile1

```sudo apt-get update```

```sudo apt-get install libsndfile1```

1-2. Speech to Text

We used whisper model developed by OpenAI repectively, https://github.com/openai/whisper

Although whisper is developed in Python 3.9.9 and PyTorch 1.10.1, fortunatley Python 3.8.10 and PyTorch 2.3.0 is also runnable

And thanks to OpenAI, it is also runnable in Python 3.8.10 and PyTorch 1.11

So, we donot need to update any of them!

for setup,

```pip install git+https://github.com/openai/whisper.git```

To update the package to the latest version of this repository, run:

```pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git```

The whisper also requires the command-line tool ffmpeg:

for Ubuntu

```sudo apt install ffmpeg```

If you need rust installed as well, please findout in the whisper github https://github.com/openai/whisper

1-3. ko-sentence-transformers

To install, use pip:

For more information please look at https://github.com/jhgan00/ko-sentence-transformers

```pip install -U sentence-transformers```

they recommend Python 3.8 or higher, at least PyTorch 1.11.0, and transformers 4.32.0 or higher
