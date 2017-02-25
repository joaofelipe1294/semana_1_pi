# -*- coding: utf-8 -*-
'''
    1-Implemente um programa que realize uma amostragem de quantização em uma imagem monocromática.
        O programa deve receber como parâmetros o nome da imagem, o porcentual de amostragem, os níveis de cinza e a técnica de quantização (média, mediana ou moda.)
        A saída do programa deve ser a imagem amostrada.
'''

import numpy as np
import cv2
import sys
import math


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


class Sampling(object):
	
	def __init__(self , proportion , image):
		self.proportion = proportion
		self.image = image

	def apply(self):
		height , width = self.image.shape
		kernel_size = int(100.0 / self.proportion)
		normalized_image = np.zeros(( self.image.shape[0] / kernel_size, self.image.shape[1] / kernel_size) , np.uint8)
		#print('image_shape : ' + str(self.image.shape) + '  |  rescaled_shape : ' + str(normalized_image.shape))
		#print(kernel_size)
		kernel_values = []
		for x in xrange(0 , self.image.shape[0] , kernel_size):
			for y in xrange(0 , self.image.shape[1] , kernel_size):
				values = []
				for kernel_x in xrange(x , x + kernel_size):
					for kernel_y in xrange(y , y + kernel_size):
						if kernel_x < self.image.shape[0] and kernel_y < self.image.shape[1]:
							values.append(self.image.item(kernel_x , kernel_y))
				kernel_values.append(values)
		#print(kernel_values)

		#print(kernel_values)
		index = 0
		for x in xrange(0 , normalized_image.shape[0]):
			for y in xrange(0 , normalized_image.shape[1]):
				#print('original : ' + str(self.image.item(x , y)) + '  |  re_scaled : ' + str(self.mean(kernel_values[index])) + '  |  x : ' + str(x) + '  |  y : ' + str(y))
				#print('x : ' + str(x) + '  |  y : ' + str(y))
				normalized_image.itemset(x , y , self.mean(kernel_values[index]))
				index += 1
		#	print()
		#print(normalized_image)
		#print(normalized_image.shape)
		#print(self.image.shape)
		#print(normalized_image)
		
		#normalized_image.itemset(0,45,255)
		#normalized_image.itemset(0,46,255)
		#normalized_image.itemset(0,47,255)
		#normalized_image.itemset(0,48,255)
		#normalized_image.itemset(0,49,255)
		#var = self.image[0 , :]
		#print(var[:2])
		#end = list(var[:2])
		#start = list(var[2:])
		#norm = np.array((start + end) , np.uint8)
		#np.array( end + start, np.uint8)
		#print(var)
		#print(norm)
		#print(var.pop(0))
		

		#corrige o desvio gerado
		if self.proportion < 100:
			norm_lines = []
			for line_index in xrange(0 , normalized_image.shape[0]):
				line = normalized_image[line_index , :]
				start = list(line[line_index:])
				end = list(line[:line_index])
				norm_line = np.array((start + end) , np.uint8)
				norm_lines.append(norm_line)
			normalized_image = np.array(norm_lines , np.uint8)


		return normalized_image

	def mean(self , values):
		values = np.array( values, np.uint8)
		#print('values : ' + str(values) + '  |  mean : ' + str(int(np.mean(values))))
		return int(np.mean(values))


#######################################################################


image = cv2.imread(sys.argv[1] , 0)
re_scale_proportion = int(sys.argv[2])
gray_values = int(sys.argv[3])
normalized_image = Quantization(image , gray_chanels = gray_values).apply() #binary_normalization(image)

test_image = np.array(([ 0 , 15 , 23 , 15 , 30 , 120] ,
					   [ 42 , 80 , 35 , 172 , 200 , 255] , 
					   [ 255 , 120 , 40 , 15 , 35 , 180] , 
					   [ 100 , 20 , 30 , 40 , 45 , 85 ] , 
					   [ 70 , 10 , 8 , 16 , 45 , 120 ] ,
					   [ 35 , 45 , 70 , 85 , 88 , 0]) ,
					   np.uint8)



re_scaled_image = Sampling(re_scale_proportion , image).apply()








cv2.imshow('original_image' , image)
cv2.imshow('normalized_image' , normalized_image)
cv2.imshow('re_caled' , re_scaled_image)
cv2.waitKey(0)

#print(sys.argv)