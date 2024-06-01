#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 22:33:58 2021

@author: oliviersamin
"""
import os
import img2pdf
from PIL import Image
import argparse


class ImageToPDF():
    def __init__(self):
        self.args = ''
        self.starting_working_directory = os.path.abspath(os.path.curdir)
        self.working_directory = ''
        self.fichierImages = []  # liste de fichiers images
        self.images = []
        self.imageFinale = ''
        self.pdf_name = ''

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="transform one image to one PDF files")
        parser.add_argument("-i", "--image", required=True, type=str,
                            help="Enter the full path of the image with its extension")

        self.args = parser.parse_args()
        dico = self.__get_directory_and_pdf_name(self.args.image)
        self.working_directory = dico['directory']
        self.pdf_name = dico['pdf_name']
        self.image_name = dico['image_name']
        # self.image_name = self.file_name[:self.file_name.find('.')]
        # self.images = self.args.images.split(', ')
        # self.pdf_name = self.args.pdf_name + ".pdf"

    def __get_directory_and_pdf_name(self, image):
        """ image is an attribute of Ticket in models.py of base_app """
        image_name = image[::-1][:image[::-1].find('/')]
        directory = image[::-1][image[::-1].find('/')+1:]
        image_name = image_name[::-1]
        pdf_name = image_name[:image_name.find('.')] + '.pdf'
        return {'pdf_name': pdf_name, 'directory': directory[::-1], 'image_name': image_name}

    def detecterFormatImage(self,image):
        ext=['.png','.jpg','.jpeg']
        for elem in ext:
            if elem in image:
                self.extension=elem
                break

    def enleverAlpha(self, image):
        im=Image.open(image)
        newI=Image.new('RGB',(im.size[0],im.size[1]),(255,0,255))
        cmpI=Image.composite(im,newI,im).quantize(colors=256,method=2)
        cmpI.save(image)
    
    def collerImagesVertical(self):
        hauteurs=[0]
        largeur=100000
        # print (self.fichierImages)
        for ind,elem in enumerate(self.fichierImages):
            # print ('dans for ',elem)
            im=Image.open(elem)
            if (im.width < largeur):
                largeur=im.width
            hauteurs.append(hauteurs[ind]+im.height)
        # print ('hauteurs = ',hauteurs)
        for ind,elem in enumerate(self.fichierImages):
            im=Image.open(elem)
            if (im.width > largeur):
                print (im.width,largeur)
                im=im.crop((0,0,largeur,im.height))
                # print (im.width)
            # im.show()
            dico={'image':im,'hdebut':hauteurs[ind],'hfin':hauteurs[ind+1],'l':im.width}
            # print ('dico = ',dico)
            self.images.append(dico)
            # print (hauteurs,hauteurs[ind],im.height,im.width)
        # print (hauteurs,hauteurs[:-1])
        params=(largeur,hauteurs[-1])
        # print (params,self.images)
        dst = Image.new('RGB', params)
        for ind,elem in enumerate(self.images):
            # print ('indice = ',ind,elem['image'],elem['l'],elem['hdebut'],elem['hfin'])
            dst.paste(elem['image'],(0,elem['hdebut'],elem['l'],elem['hfin']))
        self.imageFinale=self.nomPDF[:-3]+'png'
        dst.save(self.imageFinale)

    def convertir(self):
        with open(self.pdf_name,"wb") as f:
            f.write(img2pdf.convert(self.image_name))
            # f.write(img2pdf.convert(self.listeImages))

    def lancer(self):
        self.__parse_arguments()
        os.chdir(self.working_directory)
        # self.choisirDossierTravail()
        # self.initialiser()
        # self.collerImagesVertical()
        try:
            self.enleverAlpha(self.image_name)
        except ValueError:
            pass
        self.convertir()


if __name__ == "__main__":
    ImageToPDF().lancer()
