from anvn_config import AnvnConfig
from anvn_utils import AnvnUtils
class AnvnBasicData:
    
    def __init__(self, model_tokenizer_names=None, data_num=[0], heads=None, layers=None, key=None, decimal_digit=5, basic_data=None) -> None:
        
        if basic_data is not None:
            self.model_tokenizer_names = basic_data.model_tokenizer_names.copy()
            self.data_num = basic_data.data_num.copy()
            self.heads = AnvnUtils.deepcopy(basic_data.heads)
            self.layers = AnvnUtils.deepcopy(basic_data.layers)
            self.key = basic_data.key
            self.decimal_digit = basic_data.decimal_digit
        else:
            self.model_tokenizer_names = model_tokenizer_names
            self.data_num = data_num
            self.heads = heads
            self.layers = layers
            self.key = key
            self.decimal_digit = decimal_digit
        
        self.__init_heads_layers()

    def __init_heads_layers(self):

        if self.heads is None:
            self.heads = {}
            for model_tokenizer_name in self.model_tokenizer_names:
                self.heads[model_tokenizer_name] = [0]

        if self.layers is None:
            self.layers = {}
            for model_tokenizer_name in self.model_tokenizer_names:
                self.layers[model_tokenizer_name] = [0]

    def get_decimal_digit(self):
        return self.decimal_digit

    def set_decimal_digit(self, decimal_digit):
        self.decimal_digit = decimal_digit

    def copy(self):
        return AnvnBasicData(basic_data=self)

    def set_data_num(self, data_num):
        self.data_num = data_num
    
    def set_heads(self, heads):
        self.heads = heads
    
    def set_layers(self, layers):
        self.layers = layers
    
    def set_key(self, key):
        self.key = key

    def get_data_num(self):
        return self.data_num
    
    def get_heads(self):
        return self.heads

    def get_layers(self):
        return self.layers

    def get_layer_len(self, key):
        return len(self.layers[key])
    
    def get_data_len(self):
        return len(self.data_num)
    
    def get_head_len(self, key):
        return len(self.heads[key])

    def get_key(self):
        return self.key
    
    def get_model_tokenizer_names(self):
        return self.model_tokenizer_names

class AnvnVisualData:
    def __init__(self, data, horizontal_headers, vertical_headers, key=None):
        self.data = data
        self.horizontal_headers = horizontal_headers
        self.vertical_headers = vertical_headers
        self.data_op = None
        self.horizontal_headers_op = None
        self.vertical_headers_op = None
        self.key = key
    
    def set_data_op(self, data_op):
        self.data_op = data_op
    
    def set_horizontal_headers_op(self, horizontal_headers_op):
        self.horizontal_headers_op = horizontal_headers_op
    
    def set_vertical_headers_op(self, vertical_headers_op):
        self.vertical_headers_op = vertical_headers_op

    def get_data(self, data_op=None):
        if data_op is None:
            data_op = self.data_op
        return self.__op(self.data, data_op)
    
    def __op(self, d, op):
        for o in op:
            d = d[o]
        return d

    def set_key(self, key):
        self.key = key
    
    def get_key(self):
        self.key
    
    def get_horizontal_header(self, horizontal_headers_op=None):
        if horizontal_headers_op is None:
            horizontal_headers_op = self.horizontal_headers_op
        return self.__op(self.horizontal_headers, horizontal_headers_op)

    def get_vertical_header(self, vertical_headers_op=None):
        if vertical_headers_op is None:
            vertical_headers_op = self.vertical_headers_op
        return self.__op(self.vertical_headers, vertical_headers_op)

class AnvnTableData(AnvnBasicData):
    def __init__(self, data=None, basic_data: AnvnBasicData=None, horizontal_headers=None, vertical_headers=None, horizontal_ids=None, vertical_ids=None, tokenizers=None, config: AnvnConfig=None):
        super().__init__(basic_data=basic_data)
        self.tokenizers = tokenizers
        self.data = data
        self.config = config
        self.horizontal_headers = horizontal_headers
        self.vertical_headers = vertical_headers
        self.vertical_ids = vertical_ids
        self.horizontal_ids = horizontal_ids
        self.ops = [(None, [self.get_model_tokenizer_names()[0], 0, 0, 0, list(AnvnUtils.get_fuse_op().keys())[0], config.dim_name.data_name])]
        self.op_index = 0

    def get_tokenizer(self, key):
        return self.tokenizers[key[1]]

    def set_op_index(self, index):
        self.op_index = index
    
    def get_op(self):
        return self.ops[self.op_index]

    def get_op_index(self):
        return self.op_index

    def set_dim_name(self, name):
        self.ops[self.op_index][1][5] = name

    def get_config(self):
        return self.config

    def copy_op_message(self):
        return AnvnUtils.deepcopy(self.data, self.horizontal_headers, self.vertical_headers, self.horizontal_ids, self.vertical_ids)
    
    def get_model_tokenizer_key(self, index=None):
        if index is not None:
            return self.ops[index][1][0]
        return self.ops[self.op_index][1][0]
    
    def get_data_index(self, index=None):
        if index is not None:
            return self.ops[index][1][1]
        return self.ops[self.op_index][1][1]
    
    def get_layer_index(self, index=None):
        if index is not None:
            return self.ops[index][1][2]
        return self.ops[self.op_index][1][2]
    
    def get_head_index(self, index=None):
        if index is not None:
            return self.ops[index][1][3]
        return self.ops[self.op_index][1][3]

    def get_fuse_key(self, index=None):
        if index is not None:
            return self.ops[index][1][4]
        return self.ops[self.op_index][1][4]

    def get_dim_name(self, index=None):
        if index is not None:
            return self.ops[index][1][5]
        return self.ops[self.op_index][1][5]
    
    def get_vertical_headers(self):
        return self.vertical_headers
    
    def get_horizontal_headers(self):
        return self.horizontal_headers

    def get_data(self):
        return self.data

    def get_vertical_ids(self):
        return self.vertical_ids
    
    def get_horizontal_ids(self):
        return self.horizontal_ids
    
class AnvnModelData:
    def __init__(self, model_names, tokenizer_names) -> None:
        self.model_names = model_names
        self.tokenizer_names = tokenizer_names
        self.models = {}
        self.tokenizers = {}
    
    def get_model_names(self):
        return self.model_names
    
    def get_tokenizer_names(self):
        return self.tokenizer_names

    def get_tokenizers(self):
        return self.tokenizers

    def iter_names(self):
        for model_name, tokenizer_name in zip(self.model_names, self.tokenizer_names):
            yield model_name, tokenizer_name
    
    def get_dr_len(self):
        mt_dr = set()
        for model_name, tokenizer_name in self.iter_names():
            mt_dr.add((model_name, tokenizer_name))
        return len(mt_dr)

    def get_model(self, model_name):
        return self.models[model_name]
    
    def get_tokenizer(self, tokenizer_name):
        return self.tokenizers[tokenizer_name]

    def add_model(self, model_name, model):
        self.models[model_name] = model
    
    def add_tokenizer(self, tokenizer_name, tokenizer):
        self.tokenizers[tokenizer_name] = tokenizer
    
    def exist_model(self, model_name):
        return model_name in self.models
    
    def exist_tokenizer(self, tokenizer_name):
        return tokenizer_name in self.tokenizers

    def get_tokenizer_num(self):
        return len(self.tokenizers)

class AnvnDataLoaders:
    def __init__(self):
        self.data_loaders = {}
    
    def add_data_loader(self, tokenizer_name, data_loader):
        self.data_loaders[tokenizer_name] = data_loader
    
    def exist_data_loader(self, token_name):
        return token_name in self.data_loaders

    def get_data_loader(self, token_name):
        return self.data_loaders[token_name]
    
    def keys(self):
        return list(self.data_loaders.keys())
    
    def __len__(self):
        return len(self.data_loaders)
    
    def __getitem__(self, index):
        return self.data_loaders[index]

class AnvnModelOutputData:
    def __init__(self, model_names, tokenizer_names, tokenizers) -> None:
        self.model_names = model_names
        self.tokenizer_names = tokenizer_names
        self.tokenizers = tokenizers

        self.outputs = {}
        self.all_ots = {}
        self.all_iis = {}
        self.config = AnvnConfig()

    def get_tokenizers(self):
        return self.tokenizers

    def get_config(self):
        return self.config

    def __len__(self):
        model_tokenizer_name = self.first_model_tokenizer_name()
        if model_tokenizer_name not in self.all_iis:
            return 0
        return len(self.all_ots[model_tokenizer_name])
    
    def get_layer_len(self, model_tokenizer_names, key):
        layer_len = {}
        for model_tokenizer_name in model_tokenizer_names:
            layer_len[model_tokenizer_name] = len(self.outputs[model_tokenizer_name][key][0])
        return layer_len

    def get_head_len(self, model_tokenizer_names, key):
        head_len = {}
        for model_tokenizer_name in model_tokenizer_names:
            head_len[model_tokenizer_name] = len(self.outputs[model_tokenizer_name][key][0][0])
        return head_len
    
    def get_hidden_len(self, model_tokenizer_names, key):
        hidden_len = {}
        for model_tokenizer_name in model_tokenizer_names:
            hidden_len[model_tokenizer_name] = self.outputs[model_tokenizer_name][key][0].shape[-1]
        return hidden_len

    def first_model_tokenizer_name(self):
        return (self.model_names[0], self.tokenizer_names[0])

    def exist_data(self, data_name):
        return data_name in self.outputs

    def add_ots(self, data_name, ots):
        self.all_ots[data_name] = ots
    
    def add_iis(self, data_name, iis):
        self.all_iis[data_name] = iis
    
    def add_output(self, data_name, output):
        self.outputs[data_name] = output
    
    def get_data(self, model_tokenizer_name, key, data_num, heads, layers):
        data = {}
        all_ots = {}
        all_iis = {}
        for model_tokenizer in model_tokenizer_name:
            output = self.outputs[model_tokenizer][key]
            data[model_tokenizer] = []
            all_ots[model_tokenizer] = []
            all_iis[model_tokenizer] = []

            for i in data_num:
                all_ots[model_tokenizer].append(AnvnUtils.deepcopy(self.all_ots[model_tokenizer][i]))
                all_iis[model_tokenizer].append(AnvnUtils.deepcopy(self.all_iis[model_tokenizer][i]))
                if key == AnvnConfig.AnvnModelOutput.last_hidden_state or key == AnvnConfig.AnvnModelOutput.pooler_output:
                    data[model_tokenizer].append(AnvnUtils.deepcopy(output[i]))
                elif key == AnvnConfig.AnvnModelOutput.hidden_states:
                    data[model_tokenizer].append(AnvnUtils.deepcopy(output[i][layers[model_tokenizer]]))
                else:
                    data[model_tokenizer].append(AnvnUtils.deepcopy(output[i][layers[model_tokenizer]][:, heads[model_tokenizer]]))

        return data, all_ots, all_iis