import pandas as pd
import torch.nn as nn
from datasets import Dataset
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer
from transformers import DataCollatorForSeq2Seq
from sklearn.model_selection import train_test_split

# remove newline and Nan rows
def preprocess_csv(data):
    processed_data = data.replace('\n', ' ', regex=True)
    processed_data = processed_data.dropna(axis=0)
    processed_data = processed_data.reset_index(drop=True)
    return processed_data

# function to create train & valid dataset
def preprocess_function(examples):
    inputs = tokenizer(examples['Original'], max_length=256, truncation=True, padding='max_length')
    targets = tokenizer(examples['Summary'], max_length=256, truncation=True, padding='max_length')

    inputs['labels'] = targets['input_ids']
    return inputs

# class Model():
#     def __init__(self):
#         pass

def main():
    data_path = "./data/train.csv"

    data = pd.read_csv(data_path, encoding='utf-8')
    data = data[['Original', 'Summary']]
    data = preprocess_csv(data)

    train_data, valid_data = train_test_split(data, test_size=0.2, random_state=42)
    train_dataset = Dataset.from_pandas(train_data)
    valid_dataset = Dataset.from_pandas(valid_data)

    tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-base-v2')
    model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-base-v2')

    no_freeze_param = ['model.decoder.layernorm_embedding.weight', 'model.decoder.layernorm_embedding.bias',
                       'lm_head.weight']

    # freeze encoder layers and only train decoders
    for name, para in model.named_parameters():
        # print(name, para.shape)
        if name in no_freeze_param:
            para.requires_grad = True
        elif 'model.decoder' in name:
            para.requires_grad = True
        else:
            para.requires_grad = False
        # print(para)

    train_dataset = train_dataset.map(preprocess_function, batched=True, remove_columns=train_dataset.column_names)
    valid_dataset = valid_dataset.map(preprocess_function, batched=True, remove_columns=valid_dataset.column_names)

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)

    output_dir = './results'
    logging_dir = './logs'

    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=100,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        weight_decay=0.01,
        logging_dir=logging_dir,
        logging_steps=1000,
        do_eval = True,
        eval_steps=1000,
        evaluation_strategy='steps',
        save_strategy='steps',
        save_steps=5000
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        data_collator=data_collator
    )

    print('Model training is running...')
    trainer.train()
    model.save_pretrained('/home/softn/tomato/model')
    tokenizer.save_pretrained('/home/softn/tomato/model')


if __name__ == '__main__':
    main()

