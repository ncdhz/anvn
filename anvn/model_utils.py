import torch
from transformers import AutoModel, AutoTokenizer, PreTrainedTokenizerBase
from PyQt5.QtCore import QThread, pyqtSignal
from torch.utils.data import Dataset, DataLoader
from dataclasses import dataclass

class AnvnPreModel(QThread):
    signal = pyqtSignal()
    original_text = 'original_text'
    input_ids = 'input_ids'

    def __init__(self, model_path) -> None:
        super(AnvnPreModel, self).__init__()
        self.model = None
        self.token = None
        self.model_path = model_path

    def run(self):
        self.model = AutoModel.from_pretrained(self.model_path)
        self.token = AutoTokenizer.from_pretrained(self.model_path)
        self.signal.emit()
    
    def get_tokenizer(self):
        return self.token

    def get_model(self):
        return self.model

    def signal_connect(self, callback_func):
        self.signal.connect(callback_func)

class _AnvnDataset(Dataset):
    def __init__(self, data) -> None:
        super().__init__()
        self.data = data
    def __getitem__(self, index):
        return self.data[index]
    def __len__(self):
        return len(self.data)

class AnvnDataset(QThread):

    signal = pyqtSignal(int)
    success = -1

    def __init__(self) -> None:
        super().__init__()
        self.data_list = None
        self.tokenizer = None
        self.data = None

    def set_data_list(self, data_list):
        self.data_list = data_list

    def set_tokenizer(self, tokenizer):
        self.tokenizer = tokenizer
    
    def run(self):
        data = []
        for i, dl in enumerate(self.data_list):
            t_data = self.tokenizer(dl)
            t_data[AnvnPreModel.original_text] = self.tokenizer.batch_decode(t_data[AnvnPreModel.input_ids])
            data.append(t_data)
            self.signal.emit(i + 1)
        self.signal.emit(self.success)
        self.data = data

    def get_dataset(self):
        return _AnvnDataset(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data_list)
    
    def signal_connect(self, callback_func):
        self.signal.connect(callback_func)


class AnvnModelRun(QThread):
    success = -1
    signal = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.model = None
        self.data_loader = None
        
        self.outputs = None
        self.all_ots = None
        self.all_iis = None

    def get_outputs(self):
        return self.outputs
    
    def get_all_ots(self):
        return self.all_ots
    
    def get_all_iis(self):
        return self.all_iis

    def set_data_loader(self, dataset: Dataset, tokenizer, batch_size = 1, num_workers = 1):
        self.data_loader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, collate_fn=AnvnDataCollator(tokenizer=tokenizer))

    def set_model(self, model):
        self.model = model

    def __len__(self):
        if self.data_loader == None:
            return 0
        return len(self.data_loader)

    def run(self):
        self.model.eval()
        outputs = None
        keys = None
        all_ots = []
        all_iis = []
        with torch.no_grad():
            for ri, (dl, ots, iis) in enumerate(self.data_loader):
                all_ots.extend(ots)
                all_iis.extend(iis)
                output = self.model(**dl, output_hidden_states=True, output_attentions=True)
                keys = list(output.keys())
                # init outputs
                if outputs == None:
                    outputs = {key: [] for key in keys}
                    for key in keys:
                        o_k = output[key]
                        if type(o_k) == tuple:
                            for _ in o_k:
                                outputs[key].append([])
                
                for key in keys:
                    key_out = output[key]
                    if type(key_out) == tuple:
                        for i, key_out_i in enumerate(key_out):
                            for j, ot in enumerate(ots):
                                len_ot = len(ot)
                                if len(key_out_i.shape) == 3:
                                    outputs[key][i].append(key_out_i[j, :len_ot].cpu().tolist())
                                else:
                                    outputs[key][i].append(key_out_i[j,:,:len_ot,: len_ot].cpu().tolist())
                    else:
                        if len(key_out.shape) == 3:
                            for i, ot in enumerate(ots):
                                len_ot = len(ot)
                                outputs[key].append(key_out[i,:len_ot].cpu().tolist())
                        else:
                            outputs[key].extend(key_out.cpu().tolist())
                self.signal.emit(ri + 1)
        self.outputs = outputs
        self.all_ots = all_ots
        self.all_iis = all_iis
        self.signal.emit(self.success)

    def signal_connect(self, callback_func):
        self.signal.connect(callback_func)

@dataclass
class AnvnDataCollator:
    
    tokenizer: PreTrainedTokenizerBase

    def __call__(self, features):
        original_texts = []
        input_ids = []
        for feature in features:
            original_texts.append(feature.pop(AnvnPreModel.original_text))
            input_ids.append(feature[AnvnPreModel.input_ids])
        batch = self.tokenizer.pad(
            features,
            return_tensors='pt'
        )
        return batch, original_texts, input_ids