from abc import ABC, abstractmethod

class BasicModel(ABC):
    def load_model(self):
        pass
    
    def predict(self, text):
        pass