"""
Get an audio file of x secondes a create a loop of this file for y seconds
"""

import argparse
from pydub import AudioSegment


class MultiplyAudioFile:
    def __init__(self):
        self.original_file = ""
        self.number_of_loops = 1  # number of loops of the original file

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Create a chosen number of loops over an audio file")
        parser.add_argument("-a", "--audio", required=True, type=str,
                            help="Enter the absolute path of the audio to cut (with its extension)")
        parser.add_argument("-l", "--number_of_loops", required=True, type=int,
                            help="Enter the number of loops wanted to create the new audio file")
        self.args = parser.parse_args()
        self.original_file = self.args.audio
        self.number_of_loops = self.args.number_of_loops

    def __get_extension(self, file):
        extension = file[::-1][:file[::-1].find(".")]
        name = file[::-1][file[::-1].find(".")+1:]
        extension = extension[::-1]
        name = name[::-1]
        return name, extension


    def __create_loops(self):
        final = AudioSegment.from_file(self.original_file)
        final = final * self.number_of_loops
        name, extension = self.__get_extension(self.original_file)
        name = name + "_looped." + extension
        final.export(name, format=extension)

    def start(self):
        self.__parse_arguments()
        self.__create_loops()

if __name__ == "__main__":
    MultiplyAudioFile().start()