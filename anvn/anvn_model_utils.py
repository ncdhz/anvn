import torch
from transformers import AutoModel, AutoTokenizer, PreTrainedTokenizerBase
from PyQt5.QtCore import QThread, pyqtSignal
from torch.utils.data import Dataset, DataLoader
from dataclasses import dataclass
from anvn_data import AnvnModelData, AnvnDataLoaders, AnvnModelOutputData
import numpy as np

class AnvnModelInfo:
    success = -100
    error = -50
    original_text = 'original_text'
    input_ids = 'input_ids'


class AnvnPreModel(QThread):
    handle = pyqtSignal(int)

    def __init__(self, model_names, tokenizer_names) -> None:
        super(AnvnPreModel, self).__init__()
        self.model_data = AnvnModelData(model_names, tokenizer_names)

    def run(self):
        try:
            for model_name in self.model_data.get_model_names():
                if not self.model_data.exist_model(model_name):
                    self.model_data.add_model(model_name, AutoModel.from_pretrained(model_name))

            for tokenizer_name in self.model_data.get_tokenizer_names():
                if not self.model_data.exist_tokenizer(tokenizer_name):
                    self.model_data.add_tokenizer(tokenizer_name, AutoTokenizer.from_pretrained(tokenizer_name))

            self.handle.emit(AnvnModelInfo.success)
        except :
            self.handle.emit(AnvnModelInfo.error)

    def get_model_data(self):
        return self.model_data

class _AnvnDataset(Dataset):
    def __init__(self, data) -> None:
        super().__init__()
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)


class AnvnDataset(QThread):

    handle = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.data: list = None
        self.model_data: AnvnModelData = None
        self.data_loaders: AnvnDataLoaders = None
        self.batch_size = 1
        self.shuffle = False
        self.num_workers = 0
    
    def set_data(self, data):
        self.data = data

    def set_model_data(self, model_data):
        self.model_data = model_data

    def run(self):
        try:
            self.data_loaders = AnvnDataLoaders()
            j = 0
            for tokenizer_name in self.model_data.get_tokenizer_names():
                if not self.data_loaders.exist_data_loader(tokenizer_name):
                    td = []
                    tokenizer = self.model_data.get_tokenizer(tokenizer_name)

                    for dl in self.data:
                        j += 1
                        t_data = tokenizer(*dl)
                        t_data[AnvnModelInfo.original_text] = tokenizer.batch_decode(
                            t_data[AnvnModelInfo.input_ids])
                        td.append(t_data)
                        self.handle.emit(j)
                    self.data_loaders.add_data_loader(tokenizer_name, self.__get_data_loader(td, tokenizer))
            
            self.handle.emit(AnvnModelInfo.success)
        except:
            self.handle.emit(AnvnModelInfo.error)

    def __get_data_loader(self, dataset, tokenizer):
        return DataLoader(
            _AnvnDataset(dataset), batch_size=self.batch_size, num_workers=self.num_workers, shuffle=self.shuffle, collate_fn=AnvnDataCollator(tokenizer=tokenizer))

    def get_data_loaders(self):
        return self.data_loaders

    def __len__(self):
        return len(self.data) * self.model_data.get_tokenizer_num()


class AnvnModelRun(QThread):
    handle = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.model_data: AnvnModelData = None
        self.data_loaders: AnvnDataLoaders = None
        self.model_output_data = None

    def set_data_loaders(self, data_loaders):
        self.data_loaders = data_loaders

    def set_model_data(self, model_data):
        self.model_data = model_data

    def get_model_output(self):
        return self.model_output_data

    def __len__(self):
        if len(self.data_loaders) == 0:
            return 0
        return len(self.data_loaders[self.data_loaders.keys()[0]]) * self.model_data.get_dr_len()

    def run(self):
        try:
            self.model_output_data = AnvnModelOutputData(self.model_data.get_model_names(), self.model_data.get_tokenizer_names(), self.model_data.get_tokenizers())
            i = 0
            for model_name, tokenizer_name in self.model_data.iter_names():
                model_tokenizer_name = (model_name, tokenizer_name)
                if not self.model_output_data.exist_data(model_tokenizer_name):
                    data_loader = self.data_loaders.get_data_loader(tokenizer_name)
                    model = self.model_data.get_model(model_name)
                    model.eval()

                    outputs = None
                    keys = None
                    all_ots = []
                    all_iis = []
                    with torch.no_grad():
                        for dl, ots, iis in data_loader:
                            for oti, ii in zip(ots, iis):
                                all_ots.append(np.array(oti, dtype=object))
                                all_iis.append(np.array(ii, dtype=object))

                            output = model(
                                **dl, output_hidden_states=True, output_attentions=True)
                            
                            # init outputs
                            if outputs == None:
                                keys = list(output.keys())
                                outputs = {key: [] for key in keys}

                            for key in keys:
                                key_out = output[key]
                                if type(key_out) == tuple:
                                    key_out = torch.stack(key_out, dim=0).transpose(0, 1)

                                    for i, ot in enumerate(ots):
                                        len_ot = len(ot)
                                        if len(key_out.shape) == 4:
                                            outputs[key].append(
                                                key_out[i, :, :len_ot].cpu().numpy())
                                        else:
                                            outputs[key].append(
                                                key_out[i, :, :, :len_ot, :len_ot].cpu().numpy())
                                else:
                                    if len(key_out.shape) == 3:
                                        for i, ot in enumerate(ots):
                                            len_ot = len(ot)
                                            outputs[key].append(
                                                key_out[i, :len_ot].cpu().numpy())
                                    else:
                                        outputs[key].extend(key_out.cpu().numpy())
                            self.handle.emit(i + 1)
                            i += 1
                    
                    self.model_output_data.add_output(model_tokenizer_name, outputs)
                    self.model_output_data.add_ots(model_tokenizer_name, all_ots)
                    self.model_output_data.add_iis(model_tokenizer_name, all_iis)
            self.handle.emit(AnvnModelInfo.success)
        except:
            self.handle.emit(AnvnModelInfo.error)

@dataclass
class AnvnDataCollator:

    tokenizer: PreTrainedTokenizerBase

    def __call__(self, features):
        original_texts = []
        input_ids = []
        for feature in features:
            original_texts.append(feature.pop(AnvnModelInfo.original_text))
            input_ids.append(feature[AnvnModelInfo.input_ids])
        batch = self.tokenizer.pad(
            features,
            return_tensors='pt'
        )
        return batch, original_texts, input_ids
