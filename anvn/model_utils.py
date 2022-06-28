from typing import List
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

    def signal_connect(self, callback_func):
        self.signal.connect(callback_func)
    
    def data_process(self, data_list, batch_size=2, num_workers=1):
        data = []
        for dl in data_list:
            t_data = self.token(dl)
            t_data[self.original_text] = self.token.batch_decode(t_data[self.input_ids])
            data.append(t_data)
        dataset = AnvnDataset(data=data)
        return DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, collate_fn=AnvnDataCollator(tokenizer=self.token))
    
    def model_run(self, data_loader):
        self.model.eval()
        outputs = None
        keys = None
        all_ots = []
        all_iis = []
        with torch.no_grad():
            for dl, ots, iis in data_loader:
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
        return outputs,  all_ots, all_iis


class AnvnDataset(Dataset):
        def __init__(self, data) -> None:
            super().__init__()
            self.data = data
        
        def __getitem__(self, index):
            return self.data[index]

        def __len__(self):
            return len(self.data)

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