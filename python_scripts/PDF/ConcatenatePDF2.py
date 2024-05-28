#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  23 22:28:58 2024

@author: oliviersamin
"""
from PyPDF2 import PdfFileMerger
import sys
import os
import argparse


class concatenatePDF:
    
    def __init__(self):
        self.files_to_concatenate = []
        self.final_name = None
        self.working_directory = None
        self.merger = PdfFileMerger()

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Concatenate pdf files into one")
        parser.add_argument("-n", "--name", required=True, type=str,
                            help="Enter the name of the new PDF without its extension")
        parser.add_argument("-f", "--files", required=True, type=str,
                            help="the list of pdf files to concqtenqte sepqrqted by commas")

        self.args = parser.parse_args()
        self.final_name = self.args.name + ".pdf"
        self.files_to_concatenate = self.args.files.split(",")
        self.working_directory = self.files_to_concatenate[0][::-1][self.files_to_concatenate[0][::-1].find("/") + 1:][::-1]
        print("start: ", self.working_directory)

    def concatenate_files(self):
        for pdf in self.files_to_concatenate:
            print("pdf = ", pdf)
            self.merger.append(pdf, import_outline=False)
        self.merger.write(self.final_name)
        self.merger.close()

    def launch(self):
        if __name__ == "__main__":
            self.__parse_arguments()
            os.chdir(self.working_directory)
            self.concatenate_files()

if __name__ == "__main__":
    concatenatePDF().launch()
