#from charset_normalizer.md import getLogger
from eda.EventEmitter import EventEmitter, EventChannels
from eda.MessageUtil import MessageUtil
from log.LoggerFactory import LoggerFactory

class OcrWorker:
    def __init__(self, reader, event_emitter: EventEmitter):
        self.reader = reader
        self.__event_emitter = event_emitter
        self.__loger = LoggerFactory.create_logger(self.__class__.__name__)
        self.__listen_to_ocr_channel()

    def __listen_to_ocr_channel(self):
        self.__loger.info("Listening to OCR channel")
        self.__event_emitter.add_consumer(EventChannels.OCR_CHANNEL.value, lambda message: self.__emit_text_event(
            self.__read_png(message.get_message_body())))

    def __read_png(self, data: bytes) -> list[str]:
        self.__loger.info("Reading data from OCR channel with detail=0")
        return self.reader.readtext(data, detail=0)

    def __emit_text_event(self, text: list[str]):
        val = " ".join(text)
        self.__loger.info(f"Emitting \"{val}\" to channel: {EventChannels.OCR_TEXT_CHANNEL.value}")
        self.__event_emitter.emit_event(MessageUtil.build_string_message(val, EventChannels.OCR_TEXT_CHANNEL.value))
