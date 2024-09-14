import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
import cv2
import scipy




PATH = "./"
FILE = "001_01.PNG"


#parametros de tratamento gaussiano, binarização e morfologia
MINSIZEGAUSSIAN = 5
MAXSIZEGAUSSIAN = 5
MINSIZEOFESTRUTURANTE = 5
MAXSIZEOFESTRUTURANTE = 5
PACEESTRUTURANTE = 4
BINARIZACAO = 234




def gaussian_filter_2d(filter_size):
    # Note que o desvio padrão está sendo definido com base no tamanho do filtro
    sigma = filter_size/6.


    # Definição as coordenadas do matriz
    x_vals = np.linspace(-3*sigma, 3*sigma, filter_size)
    y_vals = x_vals.copy()


    # Cria o filtro Gaussino
    z = np.zeros((filter_size, filter_size))
    for row in range(filter_size):
        x = x_vals[row]
        for col in range(filter_size):
            y = y_vals[col]
            z[row, col] = np.exp(-(x**2+y**2)/(2*sigma**2))
    z = z/np.sum(z)


    return z


def tratamento_imagem(path = PATH, files = [FILE]):
    imgs ={}
    for file in files:
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
        imgs[file] = img
    #tratamento de imagens com filtro gaussiano
    gaussian_images = {}
    binary_images = {}
    erode_images = {}
    open_images = {}


    for img_id in imgs:
        gaussian_images[img_id] = {}
        binary_images[img_id] = {}
        erode_images[img_id] = {}
        open_images[img_id] = {}


        for i in range(MINSIZEGAUSSIAN, MAXSIZEGAUSSIAN+1, 2):
            gaussian_images[img_id][i] = scipy.signal.convolve(imgs[img_id], gaussian_filter_2d(i**2), mode='same')


        #binarização de imagens pós filtro
        for i in gaussian_images[img_id]:
            _, binary_images[img_id][i] = cv2.threshold(gaussian_images[img_id][i], BINARIZACAO, 255, cv2.THRESH_BINARY)




        #Tratamento morfologico (erosão)
        counter = 1
        for i in binary_images[img_id]:
            for j in range(MINSIZEOFESTRUTURANTE, MAXSIZEOFESTRUTURANTE+1, PACEESTRUTURANTE):
                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (j, j))
                erode_images[img_id][counter] = cv2.morphologyEx(binary_images[img_id][i],cv2.MORPH_ERODE, kernel, iterations=1)
                counter += 1


        #Tratamento morfologico (abertura)
        counter = 1
        for i in binary_images[img_id]:
            for j in range(MINSIZEOFESTRUTURANTE, MAXSIZEOFESTRUTURANTE+1, PACEESTRUTURANTE):
                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (j, j))
                open_images[img_id][counter] = cv2.morphologyEx(binary_images[img_id][i],cv2.MORPH_OPEN, kernel, iterations=1)
                counter += 1


    return imgs, gaussian_images, binary_images, erode_images, open_images
