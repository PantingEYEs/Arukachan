#!/usr/bin/python

import os
import time
from datetime import datetime
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from transformers import pipeline
from transformers.pipelines.audio_utils import ffmpeg_microphone_live
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import Optional, Any, Dict, List

#Initialize display settings
pixels_size = (128, 64)
max_x, max_y = 22, 5
display_lines = []
fontsize = 12

#Configure I2C bus
serial = i2c(port=1, address=0x3C)
#Create an instance of the SSD1306 device
device = ssd1306(serial, width=pixels_size[0], height=pixels_size[1])

llm: Optional[LlamaCpp] = None
callback_manager: Any = None
model_file = "llama-2-7b-chat.Q4_K_M.gguf"
template_tiny = """<|system|>
                   Your name is Arukachan. A smart, wise, powerful AI girl.</s>
                   <|user|>
                   {question}</s>
                   <|assistant|>"""
template_llama = """<s>[INST] <<SYS>>
                    Your name is Arukachan. A smart, wise, powerful AI girl.</SYS>>
                    {question} [/INST]"""
template = template_tiny

asr_model_id = "openai/whisper-tiny.en"
transcriber = pipeline("automatic-speech-recognition",
                       model=asr_model_id,
                       device="cpu")

if not os.path.isfile(model_file):
    print(f"Model file not found: {model_file}")

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerif-Light.ttf",fontsize,encoding='UTF-8') 
except IOError:
    print("Font not found, falling back to default.")
    font = ImageFont.load_default()
    
class StreamingCustomCallbackHandler(StreamingStdOutCallbackHandler):
    """ Callback handler for LLM streaming """

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """ Run when LLM starts running """
        print("<LLM Started>")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """ Run when LLM ends running """
        print("<LLM Ended>")

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """ Run on new LLM token. Only available when streaming is enabled """
        print(f"{token}", end="")
        add_display_tokens(token)
        
def asr_init():
    """ Initialize automatic speech recognition model """
    global transcriber
    transcriber = pipeline("automatic-speech-recognition", model=asr_model_id, device="cpu")
        
def transcribe_mic(chunk_length_s: float) -> str:
    """ Transcribe the audio from a microphone """
    global transcriber
    sampling_rate = transcriber.feature_extractor.sampling_rate
    mic = ffmpeg_microphone_live(
            sampling_rate=sampling_rate,
            chunk_length_s=chunk_length_s,
            stream_chunk_s=chunk_length_s,
        )
    
    result = ""
    for item in transcriber(mic):
        result = item["text"]
        if not item["partial"][0]:
            break
    return result.strip()
    
def llm_init():
    """ Load large language model """
    global llm
    # Initialize the callback handler
    callback_handler = StreamingCustomCallbackHandler()
    llm = LlamaCpp(
        model_path=model_file,
        temperature=0.1,
        n_gpu_layers=0,
        n_batch=256,
        callbacks=[callback_handler],  # Use callbacks instead of callback_manager
        verbose=True,
    )


def llm_start(question: str):
    """ Ask LLM a question """
    global llm, template

    prompt = PromptTemplate(template=template, input_variables=["question"])
    chain = prompt | llm | StrOutputParser()
    chain.invoke({"question": question}, config={})
    
def add_display_line(text: str):
    #Add a new line with scrolling
    global display_lines
    #Split line into chunks according to screen width
    text_chunks = [text[i:i + max_x] for i in range(0, len(text), max_x)]
    for chunk in text_chunks:
        for line in chunk.split("\n"):
            display_lines.append(line)
            # Keep only the last max_y lines
            display_lines = display_lines[-max_y:]
    #Update the display
    with canvas(device) as draw:    
        for idx, line in enumerate(display_lines):
            draw.text((0,idx*fontsize), line, font=font, fill="white")
            
def add_display_tokens(text: str):
    """ Add new tokens with or without extra line break """
    global display_lines
    last_line = display_lines.pop()
    new_line = last_line + text
    add_display_line(new_line)

if __name__ == "__main__":
    add_display_line("Init automatic speech recogntion...")
    asr_init()

    add_display_line("Init LLaMA GPT...")
    llm_init()

    while True:
        # Q-A loop:
        add_display_line("Start speaking")
        add_display_line("")
        question = transcribe_mic(chunk_length_s=5.0)
        if len(question) > 0:
            add_display_tokens(f"> {question}")
            add_display_line("")

            llm_start(question)
