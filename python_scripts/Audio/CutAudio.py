"""
Cut a single audio file into several parts. The new files are written in the same folder than the
original audio file.
"""

import argparse
from pydub import AudioSegment
import os


class CutAudioInSeveralParts:
    def __init__(self):
        self.audio_path = ""
        self.first_part_path = ""
        self.second_part_path = ""
        self.time_to_cut = ""
        self.path = ""
        self.base_path = ""
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
        self.times = []

    def __set_times_and_labels(self):
        """
        the time input can be of two types:
        1. it just give a list of times: 3.12,6.45,10.34...
        2. it give time and also the label of the extract, they are separated by ":". Example: 3.12,6.45:test_label,10.32,12.45:test2_label....
        the last label will always be used for the cut before the last one.
        If you want to add a label for the last cut, in your time list you will have to add the symbol |
        Check out the example:
          3.12,6.45:test_label,10.32,12.45:test2_label, 30.45:before_last_label|lastlabel
        :return: a dictionnary with label and time for each input. If the label is empty, just use the default label value, otherwize replace it
        """
        input = self.time_to_cut.split(",")
        output = []
        for data in input:
            if ":" in data:
                output.append({"label": data.split(":")[1], "time": self.__convert_time(data.split(":")[0])})
            else:
                output.append({"label": "", "time": self.__convert_time(data.split(":")[0])})
        return output

    def __convert_time(self, time):
        """entry : a string representing a time written as follow
        7.02 = 7 minutes and 2 secondes
        2.36 = 2 minutes and 36 secondes
        3.75 does not exist because more than 59 secondes is a minute more --> raise an error
        Final result in milliseconds because this is how it is managed by the AudioSegment instance
        """
        minutes = int(float(time))
        seconds = round(float(time) - minutes, 2)*100
        if seconds <= 59:
            return int(minutes * 60 + seconds) * 1000
        else:
            print("\n############# ERROR ####################\n"
                  "The value of seconds cannot be more than 59\n"
                  "Incorrect example: 3.76\n"
                  "Correct example: 4.23\n"
                  "############# ERROR ####################\n")

        return (minutes * 60 + seconds) * 1000

    def __create_parts(self):
        """
        transform the self.time_to_cut into list and then create a dictionnary with the corresponding audio
        parts to be created.
        Details of this dictionnary: {"file": "", "file_absolute_path": ""}
        """
        # Get all the times as integer and sorted
        self.times = self.__set_times_and_labels()
        self.times = sorted(self.times, key=lambda x: x["time"])
        if len(self.times) > 1:
            for index, time in enumerate(self.times):
                if not time["label"]:
                    path = self.path + "_extract_" + str(index + 1) + "." + self.extension
                else:
                    path = os.path.join(self.base_path, time["label"] + "." + self.extension)
                file = None
                if index == 0:
                    file = self.audio_file[:time["time"]]
                elif index < len(self.times) - 1:
                    time_past = self.times[index-1]["time"]
                    file = self.audio_file[time_past:time["time"]]
                elif index == len(self.times) - 1:
                    # the last segment creates 2 parts to get the whole file
                    path1 = ""
                    path2 = ""
                    if "|" in path:
                        path1 = path[:path.find("|")] + "." + self.extension
                        label = path[path.find("|") + 1:]
                        path2 = os.path.join(self.base_path, label)
                    time_past = self.times[index-1]["time"]
                    file = self.audio_file[time_past:time["time"]]
                    self.parts.append({"file": file, "file_absolute_path": path1 or path})
                    file = self.audio_file[time["time"]:]
                    path = path2 or self.path + "_extract_" + str(index + 2) + "." + self.extension
                self.parts.append({"file": file, "file_absolute_path": path})
        else:
            if self.times[0]["label"]:
                if "|" in self.times[0]["label"]:
                    label = self.times[0]["label"]
                    path1 = os.path.join(self.base_path, label.split("|")[0] + "." + self.extension)
                    self.parts.append({"file": self.audio_file[:self.times[0]["time"]], "file_absolute_path": path1})
                    path2 = os.path.join(self.base_path, label.split("|")[1] + "." + self.extension)
                    self.parts.append({"file": self.audio_file[self.times[0]["time"]:], "file_absolute_path": path2})
                else:
                    path = os.path.join(self.base_path, self.times[0]["label"] + "." + self.extension)
                    self.parts.append({"file": self.audio_file[:self.times[0]["time"]], "file_absolute_path": path})
                    path = self.path + "_02." + self.extension
                    self.parts.append({"file": self.audio_file[self.times[0]["time"]:], "file_absolute_path": path})
            else:
                path = self.path + "_01." + self.extension
                self.parts.append({"file": self.audio_file[:self.times[0]["time"]], "file_absolute_path": path})
                path = self.path + "_02." + self.extension
                self.parts.append({"file": self.audio_file[self.times[0]["time"]:], "file_absolute_path": path})

    def __create_audio_base_path(self):
        path = self.audio_path[::-1][self.audio_path[::-1].find(".")+1:]
        extension = self.audio_path[::-1][:self.audio_path[::-1].find(".")]
        self.extension = extension[::-1]
        self.path = path[::-1]
        self.base_path = path[path.find("/"):][::-1]

    def __save_parts(self):
        if self.parts:
            for part in self.parts:
                part['file'].export(part['file_absolute_path'], format=self.extension)
            print("-" * 20 + " {}".format([part['file_absolute_path'] for part in self.parts]))
        else:
            print("-" * 20 + " {}".format([self.audio_path]))

    def start(self):
        self.__create_audio_base_path()
        self.__create_parts()
        self.__save_parts()


if __name__ == "__main__":
    CutAudioInSeveralParts().start()
