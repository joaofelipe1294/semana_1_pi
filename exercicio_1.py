# -*- coding: utf-8 -*-
'''
    1-Implemente um programa que realize uma amostragem de quantização em uma imagem monocromática.
        O programa deve receber como parâmetros o nome da imagem, o porcentual de amostragem, os níveis de cinza e a técnica de quantização (média, mediana ou moda.)
        A saída do programa deve ser a imagem amostrada.
'''

import numpy as np
import cv2
import sys


image = cv2.imread(sys.argv[1] , 0)
min_value = sys.argv[2]
max_value = sys.argv[3]
cv2.imshow('image' , image)
cv2.waitKey(0)

#print(sys.argv)