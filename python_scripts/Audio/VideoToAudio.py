"""
Transform a video file into an audio file
"""

import os
import argparse
import moviepy.editor as mp

class VideoToMp3:
    def __init__(self):
        self.path_video = ""
        self.video_clip = None
        self.mp3 = None

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Convert one movie file into one MP3 file. "
                                                     "The file is created in the same folder as the "
                                                     "video one")
        parser.add_argument("-v", "--video", required=True, type=str,
                            help="Enter the absolute path of the video to convert (with its extension)")
        self.args = parser.parse_args()
        self.path_video = self.args.video

    def __create_mp3_file_name(self):
        self.mp3 = self.path_video[::-1]
        self.mp3 = self.mp3[self.mp3.find(".")+1:]
        self.mp3 = self.mp3[::-1] + ".mp3"

    def __convert_to_mp3(self):
        self.video_clip = mp.VideoFileClip(self.path_video)
        self.video_clip.audio.write_audiofile(self.mp3)

    def start(self):
        """
        used when the program is launch as main
        :return:
        """
        self.__parse_arguments()
        self.__create_mp3_file_name()
        self.__convert_to_mp3()

    def __set_video_path(self, video_path):
        """
        used when hte program is called as a module
        :return:
        """
        self.path_video = video_path

    def convert_to_mp3(self, video_path):
        """
        used when this program is a module
        :return:
        """
        self.__set_video_path(video_path)
        self.__create_mp3_file_name()
        self.__convert_to_mp3()


if __name__ == "__main__":
    VideoToMp3().start()