import easyocr
from transformers import VisionEncoderDecoderModel, TrOCRProcessor


class OcrFactory:
    @staticmethod
    def create_tr_ocr():
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        return processor, model

    @staticmethod
    def create_easyocr(languages: list[str] = ["en"]):
        return easyocr.Reader(languages)
