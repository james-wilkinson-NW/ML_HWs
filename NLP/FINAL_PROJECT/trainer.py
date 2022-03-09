from transformers import GPT2Tokenizer, GPT2Model, GPT2LMHeadModel
from transformers import Trainer, TrainingArguments
from torch.utils.data import Dataset
import torch

# implemented with inspo from https://towardsdatascience.com/guide-to-fine-tuning-text-generation-models-gpt-2-gpt-neo-and-t5-dc5de6b3bc5e

class WozDataset(Dataset): # basic torch dataset to let the trainer function
    def __init__(self, prompt, resp): # prompt and response text as inputs

        # initializations
        self.x = []
        self.y = []
        self.attention_mask = []

        assert len(prompt) == len(resp)

        for i in range(len(prompt)):
            in_encoded_dict = tokenizer(prompt[i], add_special_tokens=True, padding="max_length",
                                        max_length=96)  # pad to make sure all inputs are same dimension
            out_encoded_dict = tokenizer(resp[i], add_special_tokens=True, padding="max_length", max_length=96)

            self.x.append(torch.tensor(in_encoded_dict['input_ids']))
            self.attention_mask.append(torch.tensor(in_encoded_dict['attention_mask']))
            self.y.append(torch.tensor(out_encoded_dict['input_ids']))

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.attention_mask[idx], self.y[idx]

def main():
    '''
    Literally just a wrapper so I can run this in collab
    '''
    base_model = 'gpt2'
    torch.manual_seed(1)
    train_name = 'woz.train_b.txt'

    tokenizer = GPT2Tokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token # set the padding token
    model = GPT2LMHeadModel.from_pretrained(base_model, pad_token_id=tokenizer.eos_token_id)
    if torch.cuda.is_available():
        model = model.cuda()

    # format and tokenize the training dataset
    train_x = []
    train_y = []
    with open(train_name, 'rt') as f:
        for line in f:
            if line.split(' ')[0] == '[USER]': # only train on replies by [SYSTEM] (that start with prompt by [USER])
                line = line.replace('\n', '')
                SYS_index = line.index('[SYSTEM]')
                prompt = line[:SYS_index].strip(' ')
                resp = line[SYS_index:].strip(' ')
                train_x.append(prompt)
                train_y.append(resp)

    dataset = WozDataset(train_x, train_y)

    # config for training
    config = TrainingArguments(output_dir='./results/', num_train_epochs=2, logging_steps=20,
                               load_best_model_at_end=False, save_strategy="epoch",
                               per_device_train_batch_size=2, per_gpu_eval_batch_size=2,
                               warmup_steps=100, weight_decay=0.01, logging_dir='./Logs')

    # start training
    Trainer(model=model, args=config, train_dataset=dataset)

