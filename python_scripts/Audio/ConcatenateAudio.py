"""
Concatenate several audio files with the same extensions to create one with the same extension
"""

import os
import argparse
from pydub import AudioSegment


class Concatenate:
    def __init__(self):
        self.files = []
        self.directory = ""
        self.name_final_file = ""

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="Concatenate audio files from the same folder and with same extensions "
                        "into one audio file with same extension")
        parser.add_argument("-f", "--files", required=True, type=str,
                            help="Enter the file names with it extension separated by comma")
        parser.add_argument("-d", "--directory", required=True, type=str,
                            help="Enter the absolute path to the directory where are all the files")
        parser.add_argument("-fn", "--final_name", required=True, type=str,
                            help="Enter the name of the final audio file with its extension")
        self.args = parser.parse_args()
        self.directory = self.args.directory
        self.files = self.args.files
        self.name_final_file = self.args.final_name

    def __get_all_files(self):
        """
        Get all the audio files from string separated by comma to list
        :return:
        """
        self.files = self.files.split(",")

    def __get_extension(self, file):
        extension = file[::-1][:file[::-1].find(".")]
        extension = extension[::-1]
        return extension

    def __concatenate_files(self):
        os.chdir(self.directory)
        final = AudioSegment.silent(duration=1)
        for file in self.files:
            final += AudioSegment.from_file(file)
        extension = self.__get_extension(self.files[0])
        final.export(self.name_final_file, format=extension)

    def start(self):
        self.__parse_arguments()
        self.__get_all_files()
        self.__concatenate_files()


if __name__ == "__main__":
    Concatenate().start()
