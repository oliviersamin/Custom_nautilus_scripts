#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:05:56 2021

@author: oliviersamin
"""
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import argparse


class CutVideo:
    
    def __init__(self):
        self.starting_working_directory = os.path.abspath(os.path.curdir)
        self.working_directory = ''
        self.original_video = ''
        self.extract = ''
        self.start = 0.
        self.end = 0.
        self.args = ''

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="cut video file giving the starting time and ending time")
        parser.add_argument("-v", "--video", required=True, type=str,
                            help="Enter the full path of the video to cut with its extension")
        parser.add_argument("-n", "--extract_filename", required=True, type=str,
                            help="Enter the name of the extract without its extension")
        parser.add_argument("-s", "--start_time", required=True, type=float,
                            help="Enter the time in minutes where to start the extract, exemple: 6.23 = 6min et 23sec")
        parser.add_argument("-e", "--end_time", required=True, type=float,
                            help="Enter the time in minutes where to end the extract, exemple: 6.23 = 6min et 23sec")

        self.args = parser.parse_args()
        dico = self.__get_directory_and_video_name(self.args.video)
        self.working_directory = dico['directory']
        os.chdir(self.working_directory)
        self.original_video = dico['video_name']
        self.extract = self.args.extract_filename + ".mp4"
        self.start = self.__convert_time(self.args.start_time)
        self.end = self.__convert_time(self.args.end_time)

    def __convert_time(self, time):
        """entry : a string representing a time written as follow
        7.02 = 7 minutes and 2 secondes
        2.36 = 2 minutes and 36 secondes
        3.75 does not exist because more than 59 secondes is a minute more --> raise an error
        Final result in seconds
        """
        minutes = int(time)
        seconds = round(time - int(time), 2)*100
        if seconds <= 59:
            return int(minutes * 60 + seconds)
        else:
            print("\n############# ERROR ####################\n"
                  "The value of seconds cannot be more than 59\n"
                  "Incorrect example: 3.76\n"
                  "Correct example: 4.23\n"
                  "############# ERROR ####################\n")

    def __get_directory_and_video_name(self, video):
        """ image is an attribute of Ticket in models.py of base_app """
        video_name = video[::-1][:video[::-1].find('/')]
        directory = video[::-1][video[::-1].find('/')+1:]
        return {'video_name': video_name[::-1], 'directory': directory[::-1]}

    def __cut(self):
        ffmpeg_extract_subclip(self.original_video, self.start,
                               self.end, targetname=self.extract)

    def execute(self):
        self.__parse_arguments()
        self.__cut()
        os.chdir(self.starting_working_directory)

#
# class CollerVideos():
#     def __init__(self):
#         self.videos=[]
#         self.montage=''
#
#     def coller(self):
#         print ("Coller videos à faire")
#         self.montage=input("Entrer le nom de la vidéo finale (sans l'extension) : ")+'.mp4'
#
#         # ffmpeg_extract_subclip(self.videoInitiale, self.debut,
#         #                        self.fin, targetname=self.extraitVideo)
#
#     def choisirDossierTravail(self):
#         print ('Le chemin de travail actuel est :\n{}\n'.format(os.path.abspath(os.path.curdir)))
#         self.dossierTravail=input('Entrer le chemin du dossier de travail : ')
#         print ('Le dossier de travail choisi est :\n{}\n'.format(self.dossierTravail))
#         os.chdir(self.dossierTravail)
#
#
#     def choisirVideos(self):
#         self.boucle=True
#         while self.boucle:
#             self.videos.append(input('Entrer le nom de la vidéo à ajouter (avec extension) : '))
#             self.continuer=input("Ajouter une autre vidéo? (o/n) : ")
#             if (self.continuer == 'n'):
#                 self.boucle=False
#             elif (self.continuer != 'o') & (self.continuer != 'n'):
#                 self.continuer=input("DERNIER ESSAI : Ajouter une autre vidéo? (o/n) : ")
#                 if self.continuer != 'o':
#                     self.boucle = False
#
#     def lancer(self):
#         self.choisirDossierTravail()
#         self.choisirVideos()
#         self.coller()


if __name__ == "__main__":
    CutVideo().execute()
