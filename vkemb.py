from itertools import chain
from typing import List, Tuple, Union
from tqdm import tqdm
import pandas as pd
import numpy as np
import pytorch_lightning as pl
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import BpeTrainer
from tokenizers.normalizers import Lowercase
from torch.utils.tensorboard import SummaryWriter
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import xgboost as xgb
import pyarrow.parquet as pq

import torch
import torch.nn as nn
import torch.optim as optim

from multiprocessing import freeze_support, Process


def pars(x):
    y = []
    for d in x:
        k = 0
        i1 = d.find('(')
        i2 = d.find(')') + 1
        xz = d[i1:i2].replace('(', '').replace(')', '')
        d = d[:i1-1] + d[i2:]
        i1 = d.find('(')
        i2 = d.find(')') + 1
        xz1 = d[i1:i2].replace('(', '').replace(')', '')
        if i1 == -1:
            k = 1
        else:
            d = d[:i1-1] + d[i2:]
        d = d.split(' ')
        d.insert(1, xz)
        if k == 1:
            pass
        else:
            d.insert(3, xz1)
        y.append(d)
    return y


from transformers import RobertaTokenizer, RobertaModel
tokenizerROBERTA = RobertaTokenizer.from_pretrained('roberta-base')
roberta_model = RobertaModel.from_pretrained('roberta-base')
text = ["Replace me by any text you'd like.", 'Hello, my name is Artem', 'Maching Learning is cool']
encoded_input = tokenizerROBERTA(text, return_tensors='pt', padding=True)
# output = model(**encoded_input)


device = 'cuda' if torch.cuda.is_available() else 'cpu'

roberta_model = roberta_model.to(device)

unlabeled = pd.DataFrame({'ua': [],
                          'ciphers': [],
                          'curves': []})


num_examples = 100000
chunk_size = 1000
unlabeled = pd.DataFrame()
counter = 0
parquet_file = pq.ParquetFile('C:/Users/dan4ak1/Desktop/hahahacaton/unlabelled.snappy.parquet')
for i in parquet_file.iter_batches(batch_size=chunk_size):
    counter += 1
    unlabeled = pd.concat([unlabeled, i.to_pandas()], ignore_index=True)
    if counter == num_examples // chunk_size:
        break

torch.set_float32_matmul_precision('high')
train = pd.read_parquet('C:/Users/dan4ak1/Desktop/hahahacaton/train.parquet')
test = pd.read_parquet('C:/Users/dan4ak1/Desktop/hahahacaton/test.parquet')
train['ua'] = pars(train['ua'].tolist())
test['ua'] = pars(test['ua'].tolist())
unlabeled['ua'] = pars(unlabeled['ua'].tolist())
train_nebot = train[train.label == 0]
train_nebot = pd.concat([train_nebot, train_nebot])

for i in range(1, train_nebot.shape[0]+1):
    train_nebot.iloc[i-1, 0] = i+62350

train = pd.concat([train, train_nebot])
train = shuffle(train, random_state=1)

tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.normalizer = Lowercase()
tokenizer.pre_tokenizer = Whitespace()

trainer = BpeTrainer(special_tokens=["[PAD]", "[UNK]", "[SEP]"], vocab_size=320)

tokenizer.train_from_iterator(
    [f"{row.ciphers} [SEP] {row.curves}" for row in chain(train.itertuples(), test.itertuples())],
    trainer=trainer
)
tokenizer.enable_padding()

PADDING_IDX = tokenizer.token_to_id("[PAD]")
VOCAB_SIZE = tokenizer.get_vocab_size()


class TestDataset(torch.utils.data.Dataset):
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.data.reset_index(drop=True, inplace=True)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[int, str, str]:
        # Forget about UA for now
        row = self.data.loc[idx]
        return row.id, f"{row.ciphers} [SEP] {row.curves}", f'{row.ua}'


class TrainDataset(torch.utils.data.Dataset):
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.data.reset_index(drop=True, inplace=True)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[int, str, int, str]:
        # Forget about UA for now
        row = self.data.loc[idx]
        return row.id, f"{row.ciphers} [SEP] {row.curves}", row.label, f'{row.ua}'


def tokenize(texts: List[str]) -> torch.Tensor:
    return torch.tensor([
        _.ids + [0]*(830-len(_.ids)) for _ in tokenizer.encode_batch(texts, add_special_tokens=True)
    ])

def tokenizeROBERTA(texts: List[str]) -> torch.Tensor:
    return {'input_ids': torch.tensor([
        _ + [1]*(122-len(_)) for _ in tokenizerROBERTA(texts, padding=True)['input_ids']
             ]),
             'attention_mask': torch.tensor([_ + (122-len(_))*[0] for _ in tokenizerROBERTA(texts, padding=True)['attention_mask']])
            }


def collate_to_train_batch(batch: List[Tuple[int, str, int, str]]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    ids, texts, labels, ua_texts = zip(*batch)

    ids_tensor = torch.tensor(ids, dtype=torch.long).view(-1, 1)
    texts_tensor = tokenize(texts)
    ua_texts_tenzor = tokenizeROBERTA(ua_texts)
    label_tensor = torch.tensor(labels, dtype=torch.float).view(-1, 1)

    return ids_tensor, texts_tensor, label_tensor, ua_texts_tenzor


def collate_to_test_batch(batch: List[Tuple[int, str, str]]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    ids, texts, ua_texts = zip(*batch)

    ids_tensor = torch.tensor(ids, dtype=torch.long).view(-1, 1)
    texts_tensor = tokenize(texts)
    ua_texts_tenzor = tokenizeROBERTA(ua_texts)

    return ids_tensor, texts_tensor, ua_texts_tenzor


train_dl = torch.utils.data.DataLoader(
    TrainDataset(train), batch_size=16, num_workers=0, collate_fn=collate_to_train_batch, pin_memory=False
)
test_dl = torch.utils.data.DataLoader(
    TestDataset(test), batch_size=16, num_workers=0, collate_fn=collate_to_test_batch, pin_memory=False
)


class Model(nn.Module):
    def __init__(self, padding_idx: int, vocab_size: int, embed_size: int, hidden_size: int, dropout: float) -> None:
        super().__init__()

        self.vocab_size = vocab_size
        self.emded_size = embed_size
        self.hidden_size = hidden_size

        # initialize embedding layers
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embed_size, padding_idx=padding_idx)
        # self.ua_embedding = nn.Embedding(num_embeddings=vocab_sizeua, embedding_dim=embed_size, padding_idx=padding_idxua)

        # attention layers
        self.attention1 = nn.MultiheadAttention(embed_size, 2)
        self.linear1 = nn.Linear(embed_size, hidden_size)
        self.relu = nn.ReLU()
        self.attention2 = nn.MultiheadAttention(hidden_size, 2)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linearUA = nn.Linear(768, hidden_size)
        self.dropout = nn.Dropout(p=dropout)

        # hidden layers
        self.hidden = nn.Sequential(
            nn.Linear(hidden_size * (831), hidden_size),  # concatenate UA and TLS embeddings
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Dropout(p=dropout),
        )

        # classification layer
        self.clf = nn.Linear(hidden_size, 1)

    def get_embeds(self, tensor: torch.Tensor, ua_tensor: dict) -> torch.Tensor:
        tensor = tensor.to(device)
        tensor = tensor.transpose(0, 1)
        for key in ua_tensor:
            ua_tensor[key] = ua_tensor[key].to(device)
        #     print("ua_tensor device:", ua_tensor[key].device)
        # print("tensor device:", tensor.device)

        # ua_tensor = ua_tensor.to(device)
        # ua_tensor = ua_tensor.transpose(0, 1)

        # get embeddings for TLS
        tls_embeds = self.embedding(tensor.to(device))
        tls_embeds, _ = self.attention1(tls_embeds, tls_embeds, tls_embeds)
        tls_embeds = self.relu(tls_embeds)
        tls_embeds = self.linear1(tls_embeds)
        tls_embeds = self.relu(tls_embeds)
        tls_embeds, _ = self.attention2(tls_embeds, tls_embeds, tls_embeds)
        tls_embeds = self.relu(tls_embeds)
        tls_embeds = self.linear2(tls_embeds)
        tls_embeds = torch.flatten(tls_embeds.transpose(0, 1), start_dim=1)

        # get embeddings for User-Agent
        tls_embeds_ua = roberta_model(**ua_tensor)[1]
        tls_embeds_ua = self.linearUA(tls_embeds_ua)
        tls_embeds_ua = torch.flatten(tls_embeds_ua, start_dim=1)

        # concatenate embeddings
        embeds = torch.cat((tls_embeds_ua, tls_embeds), dim=1)

        return embeds

    def forward(self, tensor: torch.Tensor, ua_tensor: dict) -> torch.Tensor:
        embeds = self.dropout(self.get_embeds(tensor, ua_tensor))
        hiddens = self.hidden(embeds)
        return self.clf(hiddens)


class LightningModel(pl.LightningModule):
    def __init__(self, model) -> None:
        super().__init__()
        self.model = model
        self.criterion = nn.BCEWithLogitsLoss()

    def training_step(self, batch: torch.Tensor) -> torch.Tensor:
        _, X, y, X1 = batch
        X = X.to(device)
        y = y.to(device)
        for key in X1:
            X1[key] = X1[key].to(device)
        #X1 = X1.to(device)
        return self.criterion(self.model(X, X1), y)

    def predict_step(self, batch: torch.Tensor, _) -> torch.Tensor:
        ids, X, X1, *_ = batch
        X = X.to(device)
        #X1 = X1.to(device)
        for key in X1:
            X1[key] = X1[key].to(device)
        return ids, torch.sigmoid(self.model(X, X1))

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.AdamW(self.parameters(), lr=0.005, weight_decay=0.05)

    def forward(self, tensor: torch.Tensor) -> torch.Tensor:
        return self.model(tensor)


model = LightningModel(
    Model(vocab_size=VOCAB_SIZE, embed_size=64, hidden_size=48, padding_idx=PADDING_IDX, dropout=0.1)
)

model = model.to(device)

trainer = pl.Trainer(max_epochs=4)
trainer.fit(model=model, train_dataloaders=train_dl)


ids, probs = zip(*trainer.predict(model, dataloaders=test_dl))

(
    pd.DataFrame({
        "id": torch.concat(ids).squeeze().numpy(),
        "is_bot": torch.concat(probs).squeeze().numpy()
    })
    .to_csv("baseline_submission_chas145.csv", index=None)
)