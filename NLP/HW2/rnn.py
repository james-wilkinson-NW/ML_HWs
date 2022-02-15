import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.nn.functional as F
from dataset import wiki_dataset
from dataloader import wiki_dataloader
import torchmetrics
import pytorch_lightning as pl
import pytorch_lightning.loggers as pl_loggers
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import time
import matplotlib.pyplot as plt

class rnn(pl.LightningModule):
    def __init__(self, n_vocab, embedding_size, hidden_size, num_layers):
        super(rnn, self).__init__()
        self.embed = nn.Embedding(n_vocab, embedding_size)
        nn.init.uniform_(self.embed.weight, a=-0.1, b=0.1)
        self.rnn = nn.RNN(input_size=embedding_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=False, dropout=0.2)
        nn.init.uniform_(self.rnn.weight_ih_l0, a=-0.1, b=0.1)
        nn.init.uniform_(self.rnn.weight_hh_l0, a=-0.1, b=0.1)
        nn.init.uniform_(self.rnn.weight_ih_l1, a=-0.1, b=0.1)
        nn.init.uniform_(self.rnn.weight_hh_l1, a=-0.1, b=0.1)
        self.fc = nn.Linear(hidden_size, n_vocab)
        self.fc.weight = self.embed.weight
        self.loss = nn.CrossEntropyLoss()

    def forward(self, x):
        x = self.embed(x)
        x, hidden = self.rnn(x)
        x = x[:, -1, :]
        logits = self.fc(x)
        return logits

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=1e-3)

    def training_step(self, batch, batch_idx):
        data, label = batch
        logits = self.forward(data)
        loss = self.loss(logits, label)
        tensorboard_logs = {'loss': {'train': loss.detach()}}
        self.log("train loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return {"loss": loss, "log": tensorboard_logs}

    def validation_step(self, batch, batch_idx):
        data, label = batch
        logits = self.forward(data)
        loss = self.loss(logits, label)
        tensorboard_logs = {'loss': {'val': loss.detach()}}
        self.log("val loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return {"loss": loss, "log": tensorboard_logs}

    def test_step(self, batch, batch_idx):
        data, label = batch
        logits = self.forward(data)
        loss = self.loss(logits, label)
        tensorboard_logs = {'loss': {'test': loss.detach()}}
        self.log("test loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return {"loss": loss, "log": tensorboard_logs}

if __name__ == '__main__':
    # Load datasets
    train = wiki_dataset('wiki.train.txt', training=True, token_map='create', window=30)
    valid = wiki_dataset('wiki.valid.txt', training=False, token_map=train.token_map, window=30)
    test = wiki_dataset('wiki.test.txt', training=False, token_map=train.token_map, window=30)
    datasets = [train, valid, test]

    # Load dataloader
    dataloader = wiki_dataloader(datasets=datasets, batch_size=20)

    # Make model and train
    model = rnn(n_vocab=len(train.unique_tokens), embedding_size=100, hidden_size=100, num_layers=2)
    tb_logger = pl_loggers.TensorBoardLogger("./lightning_logs/", name="ff")
    trainer = pl.Trainer(logger=tb_logger, max_epochs=20, gpus=1, callbacks=[EarlyStopping(monitor='val loss')])
    trainer.fit(model, dataloader)
    result = trainer.test(model, dataloader)
    print(result)
