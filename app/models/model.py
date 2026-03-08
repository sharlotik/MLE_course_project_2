import torch
import urllib.request
from PIL import Image
from transformers import EfficientNetImageProcessor, EfficientNetForImageClassification


class Model:
    """
    Класс для вызова модели
    model_path (str): путь до модели
    """
    '''  
    def __init__(self, model_path):
        self.model_path = Path(model_path)
        self._load_model()
       
    def _load_model(self):
        if self.model_path.exists():
            self._is_loaded = True
        else:
            print(f'Ошибка загрузки модели')
            self._is_loaded = False
    '''

    def predict(self, input_data: str) -> str:
        img = Image.open(input_data)
        preprocessor = EfficientNetImageProcessor.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")
        model = EfficientNetForImageClassification.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")
        # Preprocessing the input
        inputs = preprocessor(img, return_tensors="pt")
        # Running the inference
        with torch.no_grad():
            logits = model(**inputs).logits

        # Getting the predicted label
        predicted_label = logits.argmax(-1).item()
        return model.config.id2label[predicted_label]