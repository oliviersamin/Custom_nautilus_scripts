"""
Create an audio file with silence of x seconds using pydub library
"""

import argparse
from pydub import AudioSegment



class CreateSilentFile:
    def __init__(self):
        self.audio_name = ""
        self.time = 0
        self.audio_file = None
        self.extension = ""

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Create a silent file of the given time in seconds")
        parser.add_argument("-a", "--audio", required=True, type=str,
                            help="Enter the name with absolute path of the audio file (with its extension)")
        parser.add_argument("-t", "--time", required=True, type=str,
                            help="Enter the time of silence needed in seconds")
        self.args = parser.parse_args()
        self.audio_name = self.args.audio
        self.time = int(self.args.time) * 1000

    def __get_extension(self):
        self.extension = self.audio_name[::-1][:self.audio_name[::-1].find(".")]
        self.extension = self.extension[::-1]

    def __create_file(self):
        self.audio_file = AudioSegment.silent(duration=self.time)
        self.audio_file.export(self.audio_name, format=self.extension)

    def start(self):
        self.__parse_arguments()
        self.__get_extension()
        self.__create_file()


if __name__ == "__main__":
    CreateSilentFile().start()
