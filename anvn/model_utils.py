from transformers import AutoModel, AutoTokenizer
class AnvnPreModel:
    def __init__(self, model_path) -> None:
        self.model = AutoModel.from_pretrained(model_path)
        self.token = AutoTokenizer.from_pretrained(model_path)
        