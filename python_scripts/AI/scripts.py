"""
After quick tests on audio files, the maximum amount of time the model openai/whisper-large-v3 on 2024/06/01 can transcript
is above 2 minutes and a little bit less of 3 minutes. To take a margin, let's say that we must have 2 minutes audio files
"""


import argparse
from transformers import pipeline


DURATION_LIMIT = 2 * 60


class BaseModel:

    TRANSCRIPT_OUTPUT = ["automatic-speech-recognition"]
    SUMMARIZE_OUPUT = ["summarization"]
    AUDIO_OUPUT = ["translation"]
    TEXT_GENERATION = ["text-generation"]

    def __init__(self, input_file, language):
        self.input_file = input_file
        self.output_file = ""
        self.output_data = None
        self.model = ""
        self.action = ""
        self.pipe = None
        self.output_language = language

    def set_output_file(self):
        if self.action in self.TRANSCRIPT_OUTPUT:
            self.set_output_file_txt()
        elif self.action in self.AUDIO_OUPUT:
            self.set_output_file_audio()
        elif self.action in self.SUMMARIZE_OUPUT:
            self.set_output_file_summarize()
        elif self.action in self.TEXT_GENERATION:
            self.set_output_file_text_generation()

    def set_output_file_txt(self):
        name = self.input_file[::-1]
        name = name[name.find(".") + 1:][::-1]
        self.output_file = name + "_transcription.txt"

    def set_output_file_text_generation(self):
        name = self.input_file[::-1]
        name = name[name.find(".") + 1:][::-1]
        self.output_file = name + "_generated.txt"

    def set_output_file_summarize(self):
        name = self.input_file[::-1]
        name = name[name.find(".") + 1:][::-1]
        self.output_file = name + "_summarized.txt"

    def set_output_file_audio(self):
        name = self.input_file[::-1]
        name = name[name.find(".") + 1:][::-1]
        self.output_file = name + "_translation.mp3"

    def save_into_output_file(self):
        with open(self.output_file, "w") as file:
            file.write(self.output_data)

    def set_pipeline(self):
        self.pipe = pipeline(self.action, model=self.model)

    def create_output(self):
        self.output_data = self.pipe(self.input_file)["text"]


    def run(self):
        self.set_output_file()
        self.set_pipeline()
        self.create_output()
        print(self.output_data)
        self.save_into_output_file()


class Transcription(BaseModel):

    def __init__(self, input_file, model):
        super().__init__(input_file, model)
        self.action = "automatic-speech-recognition"
        self.model = "openai/whisper-large-v3"


class Translation(BaseModel):
    def __init__(self, input_file, language):
        super().__init__(input_file, language)
        self.action = "automatic-speech-recognition"
        self.model = "openai/whisper-large-v3"

    def create_output(self):
        self.output_data = self.pipe(self.input_file, generate_kwargs={"language": self.output_language})["text"]


class TextGeneration(BaseModel):
    def __init__(self, input_file, model):
        super().__init__(input_file, model)
        self.action = "text-generation"
        # self.model = "gradientai/Llama-3-8B-Instruct-Gradient-1048k" # MEMORY ISSUE
        # self.model = "mistralai/Mistral-7B-Instruct-v0.3" # MEMORY ISSUE
        # self.model = "openai-community/gpt2"  # WORKING
        # self.model = "meta-llama/Llama-2-7b-hf" # WAITING APPROVAL
        # self.model = "mistralai/Mistral-7B-v0.1" # MEMORY ISSUE
        self.model = "openai-community/gpt2-xl"
	
    def create_output(self):
        with open(self.input_file, "r") as file:
            text = file.read()

        self.output_data = self.pipe("I want you to summarize the following text: {}".format(text))[0]["generated_text"]


class Summarize(BaseModel):
    def __init__(self, input_file, model):
        super().__init__(input_file, model)
        self.action = "summarization"
        # self.model = "facebook/bart-large-cnn"
        # self.model = "openai-community/gpt2-xl"
        self.model = "microsoft/Phi-3-mini-4k-instruct"

    def get_text(self):
        with open(self.input_file, "r") as file:
            text = file.read()
        return text

    def set_summarize_parameters(self):
        text = self.get_text()
        max = len(text.split(" "))
        return {"max": max, "min": 100 if max > 100 else max, "text": text}

    def create_output(self, params):
        self.output_data = self.pipe("Write me a joke")[0]
        # self.output_data = self.pipe("I want a summary of the following text: {}".format(params["text"]))[0]["generated_text"]

    def run(self):
        self.set_output_file()
        self.set_pipeline()
        params = self.set_summarize_parameters()
        self.create_output(params)
        print(self.output_data)
        self.save_into_output_file()


def __parse_arguments():
    parser = argparse.ArgumentParser(description="Choose the Audio action")
    parser.add_argument("-a", "--action", required=True, type=str, choices=["transcription", "translation", "summarize", "text-generation"], help="The action to perform: transcription or translation")
    parser.add_argument("-f", "--file", required=True, type=str, help="Enter the absolute path of the input file")
    parser.add_argument("-l", "--ouput_language", required=False, type=str, default="en", help="The default is english")

    return parser.parse_args()


if __name__ == "__main__":

    args = __parse_arguments()
    if args.action == "transcription":
        Transcription(args.file, args.ouput_language).run()
    elif args.action == "translation":
        Translation(args.file, args.ouput_language).run()
    elif args.action == "summarize":
        Summarize(args.file, args.ouput_language).run()
    elif args.action == "text-generation":
        TextGeneration(args.file, args.ouput_language).run()
