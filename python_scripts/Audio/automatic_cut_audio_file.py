"""
Automatic cut an audio file that esceed the max duration of 120 seconds to be transcripted properly into several files
"""

import argparse
import subprocess


MAX_DURATION = 14 # number of seconds for tests purpose only
# MAX_DURATION = 120  # number of seconds the actual AI model can transcript without cutting the message


class AutomaticCut:

    def __init__(self):
        self.file_path = ""
        self.times = []
        self.duration = 0
        self.__parse_arguments()
        self.set_times_attributes()
        self.files_path = []

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Cut an audiofile into several parts that does not exceed"
                                                     "the max amount of time to be able to transcript (120 seconds)")
        parser.add_argument("-f", "--audio", required=True, type=str,
                            help="Enter the absolute path of the audio to cut (with its extension)")
        parser.add_argument("-d", "--duration", required=True, type=str,
                            help="Enter the duration of the audio file in seconds")

        self.args = parser.parse_args()
        self.duration = int(self.args.duration)
        self.file_path = self.args.audio

    def set_times_attributes(self):
        if self.duration > MAX_DURATION:
            total_number = self.duration // MAX_DURATION
            if self.duration % MAX_DURATION:
                total_number += 1
            for i in range(total_number):
                if i + 1 < total_number:
                    time = (i + 1) * MAX_DURATION
                    time = str(time // 60) + "." + str(time % 60)
                    self.times.append(str(time))
            self.times = ",".join(self.times)

    def run(self):
        if self.times:
            command = [
                'python3',
                '/home/olivier/Documents/Projects/nautilus/Custom_nautilus_scripts/python_scripts/Audio/CutAudio.py',
                '-f',
                self.file_path,
                '-t',
                self.times,
            ]
            print("command = ", command)
            data = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = data.communicate()
            print(stdout, stderr)
        else:
            print("-" * 20 + " {}".format(self.file_path))


if __name__ == "__main__":
    AutomaticCut().run()
