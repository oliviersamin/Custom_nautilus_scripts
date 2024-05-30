"""
Cut a single audio file into several parts. The new files are written in the same folder than the
original audio file.
"""

import argparse
from pydub import AudioSegment


class CutAudioInSeveralParts:
    def __init__(self):
        self.audio_path = ""
        self.first_part_path = ""
        self.second_part_path = ""
        self.time_to_cut = ""
        self.path = ""
        self.extension = ""
        self.__parse_arguments()
        self.audio_file = AudioSegment.from_file(self.audio_path)
        self.parts = []

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Cut an audiofile into several parts given the "
                                                     "times where to cut it")
        parser.add_argument("-f", "--audio", required=True, type=str,
                            help="Enter the absolute path of the audio to cut (with its extension)")
        parser.add_argument("-t", "--time", required=True, type=str,
                            help="a list separated coma of times expressed in minutes. Example 6.23 = 6minutes and 23 sec")
        self.args = parser.parse_args()
        self.audio_path = self.args.audio
        self.time_to_cut = self.args.time

    def __create_parts(self):
        """
        transform the self.time_to_cut into list and then create a dictionnary with the corresponding audio
        parts to be created.
        Details of this dictionnary: {"file": "", "file_absolute_path": ""}
        """
        # Get all the times as integer and sorted
        times = self.time_to_cut.split(",")
        times_int = []
        for time in times:
            times_int.append(int(time)*1000)
        times_int.sort()
        # create the dictionary
        if len(times_int) > 1:
            for index, time in enumerate(times_int):
                path = self.path + "_extract_" + str(index + 1) + "." + self.extension
                file = None
                if index == 0:
                    file = self.audio_file[:time]
                elif index < len(times_int) - 1:
                    time_past = times_int[index-1]
                    file = self.audio_file[time_past:time]
                elif index == len(times_int) - 1:
                    # the last segment creates 2 parts to get the whole file
                    time_past = times_int[index-1]
                    file = self.audio_file[time_past:time]
                    self.parts.append({"file": file, "file_absolute_path": path})
                    file = self.audio_file[time:]
                    path = self.path + "_extract_" + str(index + 2) + "." + self.extension
                self.parts.append({"file": file, "file_absolute_path": path})
        else:
            path = self.path + "_01." + self.extension
            self.parts.append({"file": self.audio_file[:times_int[0]], "file_absolute_path": path})
            path = self.path + "_02." + self.extension
            self.parts.append({"file": self.audio_file[times_int[0]:], "file_absolute_path": path})

    def __create_audio_base_path(self):
        path = self.audio_path[::-1][self.audio_path[::-1].find(".")+1:]
        extension = self.audio_path[::-1][:self.audio_path[::-1].find(".")]
        self.extension = extension[::-1]
        self.path = path[::-1]

    def __save_parts(self):
        for part in self.parts:
            part['file'].export(part['file_absolute_path'], format=self.extension)

    def start(self):
        self.__create_audio_base_path()
        self.__create_parts()
        self.__save_parts()


if __name__ == "__main__":
    CutAudioInSeveralParts().start()
