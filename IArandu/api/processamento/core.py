import cv2
import numpy as np
import utlis
import os
from PIL import Image


# Corpo do programa
def scanner(img):
    # TRATAMENTO PARA DETECTAR CONTORNOS
    heightImg = img.shape[0]
    widthImg = img.shape[1]
    img = cv2.resize(img, (widthImg, heightImg))   # ALTERAR TAMANHO
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERTE ESCALA DE CINZA
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)  # ADICIONA GAUSS
    kernel = np.ones((5, 5))
    imgPrep1 = cv2.erode(imgBlur, kernel)  # ADICIONA DILATACAO
    imgPrep2 = cv2.morphologyEx(imgPrep1, cv2.MORPH_OPEN, kernel)
    imgPrep3 = cv2.morphologyEx(imgPrep2, cv2.MORPH_CLOSE, kernel)
    # imgThreshold = cv2.erode(imgDial, kernel, iterations=10)  # ADICIONA EROSAO
    # cv2.imwrite(f'{pathfiles}/{imagefiles}_{outcount}_thresh.jpg', imgThreshold)
    # Acha Contornos
    imgContours = img.copy()  # COPIA PARA DEBUG
    imgBigContour = img.copy()  # COPIA PARA DEBUG
    imgPrep4 = cv2.Canny(imgPrep3, 20, 240)  # ADICIONA Cannyi
    imgPrepFinal = cv2.dilate(imgPrep4, kernel)  # ADICIONA DILATACAO
    contours, hierarchy = cv2.findContours(imgPrepFinal, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # ACHA TODOS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DESENHA CONTORNOS
    # ACHA O MAIOR CONTORNO
    biggest, maxArea = utlis.biggestContour(contours)  # FIND THE BIGGEST CONTOUR
    if biggest.size != 0:
        biggest = utlis.reorder(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
        imgBigContour = utlis.drawRectangle(imgBigContour, biggest, 2)
        pts1 = np.float32(biggest)  # PREPARAR PONTOS PARA MUDANÇA PERSPECTIVA
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARA OS SEGUNDOS PONTOS PARA MUDANÇA
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        print(biggest)
        print('----------------------------------------')
        print(pts1)
        img = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        # Convert the image to grayscale
    imagemFinal = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # imagemFinal = cv2.equalizeHist(img)
    # Apply thresholding to the image
    # _, imagemFinal = cv2.threshold(imagemFinal, 200, 255, cv2.THRESH_BINARY)
    # Binarizacao OTSU
    # _, imagemFinal = cv2.threshold(imagemFinal, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Threshold adaptativo
    imagemFinal = cv2.adaptiveThreshold(imagemFinal, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 8)


    # imagemFinal = cv2.morphologyEx(imagemFinal, cv2.MORPH_OPEN, kernel, iterations=1)
    # Adaptativo com gauss
    # imagemFinal = cv2.adaptiveThreshold(imagemFinal, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 8)
    imagemFinal = cv2.medianBlur(imagemFinal, 5)
    return imagemFinal


if __name__ == "__main__":
    pass
