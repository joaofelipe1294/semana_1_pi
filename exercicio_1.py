# -*- coding: utf-8 -*-
'''
    1-Implemente um programa que realize uma amostragem de quantização em uma imagem monocromática.
        O programa deve receber como parâmetros o nome da imagem, o porcentual de amostragem, os níveis de cinza e a técnica de quantização (média, mediana ou moda.)
        A saída do programa deve ser a imagem amostrada.
'''

import numpy as np
import cv2
import sys

#######################################################################

class Quantization(object):
	#classe usada para manipular a quantizacao de uma imagem em tons de cinza

	def __init__(self , image , gray_chanels = 256):
		self.gray_chanels = gray_chanels #novo valor de tons de cinza disponiveis
		self.image = image #imagem usada como base para mudanca de quantizacao
		self.normalized_image = np.zeros(image.shape[:2] , np.uint8) #imagem resultante da troca da quantizacao da imagem

	def apply(self):
		if self.gray_chanels == 2: 
			self.binary_normalization() #gera uma imagem binaria
		else:
			self.standard_normalization() #gera uma imagem com mais de dois tons de cinza
		return self.normalized_image

	def standard_normalization(self):
		for x in xrange(0 , self.image.shape[0]):
			for y in xrange(0 , self.image.shape[1]):
				original_px_value = self.image.item(x , y) #pega valor do px atual da imagem
				new_px_value = (float(original_px_value) / 255) * self.gray_chanels #converte o valor do px atual para float para que o resultado da divisao por 255 tambem seja um float, o valor do px atual eh dividido por 255 para que se tenha um range de valores de 0 - 1 , depois multiplica-se pelo numero de tons de cinza disponiveis para que o numero resultante varia entre 0 e NOVO_NUMERO_DE_TONS_DE_CINZA 
				new_px_value = round(new_px_value) * (256 / gray_values) #o round arredonda o valor de new_px_value, o resultado da multiplicacao eh o novo valor do px ,255 / gray_chanesl resulta no intervalo entre cada um dos tons disponiveis 
				if new_px_value == 256:
					new_px_value -= 1 #o valor maximo de um px eh 255 (branco absoluto)
				self.normalized_image.itemset(x , y , new_px_value) #aplica o novo valor no px x , y da imagem normalizada
			

	def binary_normalization(self):
		for x in xrange(0 , self.image.shape[0]):
			for y in xrange(0 , self.image.shape[1]):
				original_px_value = self.image.item(x , y)
				new_px_value = (float(original_px_value) / 255) #resulta em um numero float presente no intervalo de 0 - 1
				new_px_value = round(new_px_value) * 255 #a funcao round() retorna 0 ou 1 nesse caso
				self.normalized_image.itemset(x , y , new_px_value)

#######################################################################


image = cv2.imread(sys.argv[1] , 0)
gray_values = int(sys.argv[2])
normalized_image = Quantization(image , gray_chanels = gray_values).apply() #binary_normalization(image)

cv2.imshow('original_image' , image)
cv2.imshow('normalized_image' , normalized_image)
cv2.waitKey(0)

#print(sys.argv)