from pdf2image import convert_from_path
import os
import argparse

class TransformToImage:
    def __init__(self):
        self.args = ''
        self.starting_working_directory = os.path.abspath(os.path.curdir)
        self.working_directory = ''
        self.path_pdf_to_transform = ''
        self.file_name = ''
        self.images = ''
        self.image_name = ''
        self.images_saved = []

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="transform a PDF file to an image file")
        parser.add_argument("-fp", "--file_path", required=True, type=str,
                            help="Enter the path of the PDF to transform")

        self.args = parser.parse_args()
        self.working_directory = self.args.file_path[::-1][self.args.file_path[::-1].find('/')+1:]
        self.working_directory = self.working_directory[::-1]
        self.file_name = self.args.file_path[::-1][:self.args.file_path[::-1].find('/')]
        self.file_name = self.file_name[::-1]
        self.image_name = self.file_name[:self.file_name.find('.')]

    def __convert(self):
        self.images = convert_from_path(self.file_name)

    def __save(self):
        for ind,image in enumerate(self.images):
            name = self.image_name + str(ind+1) + ".png"
            self.images_saved.append(name)
            image.save(name)


    def start(self):
        self.__parse_arguments()
        os.chdir(self.working_directory)
        self.__convert()
        self.__save()

if __name__ == "__main__":
    TransformToImage().start()