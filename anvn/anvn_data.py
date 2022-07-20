class AnvnData:
    def __init__(self, data=None, data_num=None, heads=None, layers=None, key=None, horizontal_headers=None, vertical_headers=None, horizontal_ids=None, vertical_ids=None):
        self.data = data
        self.data_num = data_num
        self.heads = heads
        self.layers = layers
        self.key = key
        self.horizontal_headers = horizontal_headers
        self.vertical_headers = vertical_headers
        self.vertical_ids = horizontal_ids
        self.horizontal_ids = vertical_ids
    
    def get_key(self):
        return self.key

    def get_data_num(self):
        return self.data_num

    def get_layers(self):
        return self.layers

    def get_heads(self):
        return self.heads
    
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
    
