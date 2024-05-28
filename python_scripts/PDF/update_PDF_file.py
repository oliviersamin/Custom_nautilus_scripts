"""
Aim:
----

Update one PDF (ex: add a signature)

Usage:
------
This script can be used by right clicking from any repo on the PDF to update, then follow the instructions of the popup.

Steps performed by the script:
------------------------------

Step 1: convert the PDF into images into a temporary folder
A popup appear at this stage to instruct the user to do watever is needed, when the changes are made click on the popup
Step 2: All the images of the temp repo are converted into PDF
Step 3: All the PDF of the temp repo are concatened to create the final PDF into the temp repo.
This final PDF is copied into the same repo as the original PDF then the whole temporary repo is erased

Comments:
---------
This script is triggered by a shell script in the nautilus repo to be able to be used by right clicking

"""


from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger, PdfFileReader
import sys
import os
from fpdf import FPDF
import img2pdf
from PIL import Image
import pdfkit
import argparse
import shutil
import tkinter as tk
from tkinter import messagebox


TEMP_DIR_NAME = "temp_directory"
TEMP_DIR_PATH = ""
ORIGIN_DIRECTORY_PATH = ""
PDF_NAME = ""
IMAGE_NAME = ""
NEW_PDF_NAME = ""


class TransformToImage:
    def __init__(self, ORIGIN_DIRECTORY_PATH, PDF_NAME, IMAGE_NAME, TEMP_DIR_PATH):
        self.args = ''
        self.working_directory = ORIGIN_DIRECTORY_PATH
        self.file_name = PDF_NAME
        self.images = ''
        self.image_name = IMAGE_NAME
        self.images_saved = []
        self.new_directory = TEMP_DIR_PATH

    def __convert(self):
        self.images = convert_from_path(self.file_name)

    def __save(self):
        for ind,image in enumerate(self.images):
            name = self.image_name + str(ind+1) + ".png"
            self.images_saved.append(name)
            os.chdir(self.new_directory)
            image.save(name)
            os.chdir(self.working_directory)

    def start(self):
        print("-" * 200)
        print("{} - {} - {} - {}".format(self.working_directory, self.new_directory, self.image_name, self.file_name))
        os.mkdir(self.new_directory)
        os.chdir(self.working_directory)
        self.__convert()
        self.__save()


class ImageToPDF:
    def __init__(self, image, TEMP_DIR_PATH):
        self.args = ''
        self.working_directory = TEMP_DIR_PATH
        self.image = image
        self.image_name = ""
        self.pdf_name = ""

    def __set_arguments(self):
        dico = self.__get_directory_and_pdf_name(self.image)
        self.pdf_name = dico['pdf_name']

    def __get_directory_and_pdf_name(self, image):
        """ image is an attribute of Ticket in models.py of base_app """
        pdf_name = self.image[:self.image.find('.')] + '.pdf'
        return {'pdf_name': pdf_name}

    def enleverAlpha(self, image):
        im = Image.open(image)
        newI = Image.new('RGB', (im.size[0], im.size[1]), (255, 0, 255))
        cmpI = Image.composite(im, newI, im).quantize(colors=256, method=2)
        cmpI.save(image)

    def convertir(self):
        with open(self.pdf_name, "wb") as f:
            f.write(img2pdf.convert(self.image))

    def lancer(self):
        self.__set_arguments()
        os.chdir(self.working_directory)
        try:
            self.enleverAlpha(self.image)
        except ValueError:
            pass
        self.convertir()


class ConcatenatePDF:

    def __init__(self, files, NEW_PDF_NAME, TEMP_DIR_PATH, ORIGIN_DIRECTORY_PATH):
        self.files_to_concatenate = [os.path.join(TEMP_DIR_PATH, file) for file in files]
        self.final_name = NEW_PDF_NAME
        self.working_directory = TEMP_DIR_PATH
        self.origin_directory = ORIGIN_DIRECTORY_PATH
        self.new_pdf_path = os.path.join(self.working_directory, self.final_name)
        self.merger = PdfFileMerger()
        print("#" * 200)
        print(self.working_directory, self.origin_directory)

    def concatenate_files(self):
        for pdf in self.files_to_concatenate:
            print("pdf = ", pdf)
            self.merger.append(pdf, import_outline=False)
        self.merger.write(self.final_name)
        self.merger.close()

    def move_file_to_origin_directory(self):
        print("" * 200)
        print("|" * 200)
        print(self.new_pdf_path, self.origin_directory)
        shutil.copy(self.new_pdf_path, self.origin_directory)

    def delete_temp_directory(self):
        shutil.rmtree(self.working_directory)

    def launch(self):
        os.chdir(self.working_directory)
        self.concatenate_files()
        self.move_file_to_origin_directory()
        self.delete_temp_directory()


def __parse_arguments():
    parser = argparse.ArgumentParser(description="Update a PDF file to a new PDF file")
    parser.add_argument("-f", "--file_path", required=True, type=str,
                        help="Enter the path of the PDF to transform")
    parser.add_argument("-n", "--new_pdf_name", required=True, type=str,
                        help="Enter the name of the new PDF to be created without its extension")

    args = parser.parse_args()
    ORIGIN_DIRECTORY_PATH = os.path.abspath(args.file_path)
    ORIGIN_DIRECTORY_PATH = ORIGIN_DIRECTORY_PATH[::-1][ORIGIN_DIRECTORY_PATH[::-1].find('/') + 1:]
    ORIGIN_DIRECTORY_PATH = ORIGIN_DIRECTORY_PATH[::-1]
    TEMP_DIR_PATH = os.path.join(ORIGIN_DIRECTORY_PATH, TEMP_DIR_NAME)
    PDF_NAME = args.file_path[::-1][:args.file_path[::-1].find("/")][::-1]
    IMAGE_NAME = PDF_NAME[:PDF_NAME.find('.')]
    NEW_PDF_NAME = args.new_pdf_name + ".pdf"
    return ORIGIN_DIRECTORY_PATH, TEMP_DIR_PATH, PDF_NAME, IMAGE_NAME, NEW_PDF_NAME


def show_popup(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Waiting for user validation to continue", message)
    root.destroy()


def main():
    ORIGIN_DIRECTORY_PATH, TEMP_DIR_PATH, PDF_NAME, IMAGE_NAME, NEW_PDF_NAME = __parse_arguments()
    print("{} - {} - {} - {} - {} ".format(ORIGIN_DIRECTORY_PATH, TEMP_DIR_PATH, PDF_NAME, IMAGE_NAME, NEW_PDF_NAME))
    StepOne = TransformToImage(ORIGIN_DIRECTORY_PATH, PDF_NAME, IMAGE_NAME, TEMP_DIR_PATH)
    StepOne.start()

    # Show popup before continuing to step two
    message = """
    - The PDF has been transformed into images into the temporary folder.
    \n\n- Each updated image file must be named exactly as the original image file.
    \n\n- Each updated image file must replace the original file in the temporary repo 
    \n\n- Once it is done you can close this window, the process will continue."""
    show_popup(message)

    pdf_names = []
    print("." * 200)
    print(StepOne.images_saved)
    for image in StepOne.images_saved:
        StepTwo = ImageToPDF(image, TEMP_DIR_PATH)
        StepTwo.lancer()
        pdf_names.append(StepTwo.pdf_name)
    print("@" * 200)
    print("{} - {} ".format(ORIGIN_DIRECTORY_PATH, TEMP_DIR_PATH))
    StepThree = ConcatenatePDF(pdf_names, NEW_PDF_NAME, TEMP_DIR_PATH, ORIGIN_DIRECTORY_PATH)
    StepThree.launch()


if __name__ == "__main__":
    main()
