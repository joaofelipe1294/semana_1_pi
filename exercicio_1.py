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
#constantes

MEAN = 'mean'
MEDIAN = 'median'
MODE = 'mode'


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
	
	def __init__(self , proportion , image , method):
		self.proportion = proportion 
		self.image = image
		self.method = method

	def apply(self):
		if self.proportion == 100:
			return self.image
		elif self.proportion < 100:
			height , width = self.image.shape #recupera as dimensoes da imagem
			kernel_size = int(100.0 / self.proportion) #calcula o tamanho do kernel
			re_sized_image = np.zeros(( self.image.shape[0] / kernel_size, self.image.shape[1] / kernel_size) , np.uint8) #calcula as medidas da nova imagem
			kernel_values = [] #lista que ira conter os valores preenxidos de cada kernel
			for x in xrange(0 , self.image.shape[0] , kernel_size): #loop que varre as linhas
				for y in xrange(0 , self.image.shape[1] , kernel_size): #loop que varre as colunas
					values = [] #lista com os valores referentes a um kernel
					for kernel_x in xrange(x , x + kernel_size): #loop que que varre as linhas do kernel
						for kernel_y in xrange(y , y + kernel_size): #loop que varre as colunas do kernel
							if kernel_x < self.image.shape[0] and kernel_y < self.image.shape[1]: #verifica se o indice eh valido
								values.append(self.image.item(kernel_x , kernel_y)) #pega valor da imagem original
					kernel_values.append(values) #adiciona o kernel na lista que contem os kernels
			index = 0 
			for x in xrange(0 , re_sized_image.shape[0]): #loop que varre as linhas da imagem redimensionada
				for y in xrange(0 , re_sized_image.shape[1]): #loop que varre as colunas da imagem redimensionada
					if self.method == MEAN: #define valor usado para imagem rescalonada
						re_sized_image.itemset(x , y , self.mean(kernel_values[index])) 
					elif self.method == MEDIAN:
						re_sized_image.itemset(x , y , self.median(kernel_values[index]))
					elif self.method == MODE:
						re_sized_image.itemset(x , y , self.mode(kernel_values[index]))
					index += 1
				#corrige o desvio gerado			
			if (width * 0.75) > height and self.proportion < 100: #or ((width * 0.75) > height and self.proportion == 100):  #self.proportion < 100: #o redimensionamento gera uma distorcao que deve ser corrigida
				norm_lines = [] #lista com as linhas corrigidas
				for line_index in xrange(0 , re_sized_image.shape[0]): #loop que itera sobre as linhas da imagem redimensionada
					line = re_sized_image[line_index , :] #recupera uma linha completa da imagem redimensionada
					start = list(line[line_index:]) #recupera os elementos posicionados errado na nova imagem
					end = list(line[:line_index]) #seleciona os elementos corretos da linha
					norm_line = np.array((start + end) , np.uint8) #cria um novo np.array com o desvio corrigido
					norm_lines.append(norm_line) 
				re_sized_image = np.array(norm_lines , np.uint8) #recria a imagem redimensionada com o desvio corrigido
			return re_sized_image
		elif self.proportion > 100:
			height , width = self.image.shape #recupera as dimensoes da imagem
			re_sized_image = cv2.resize( self.image , (int(((float(self.proportion) / 100) * width)) , int((float(self.proportion) / 100) * height )) , interpolation = cv2.INTER_CUBIC)
			return re_sized_image

	def mean(self , values):
		values = np.array( values, np.uint8)
		return int(np.mean(values))

	def median(self , values):
		values = np.array(values , np.uint8)
		return int(np.median(values))

	def mode(self , values):
		a = np.array(values , np.uint8)
		counts = np.bincount(a)
		return np.argmax(counts)		


#######################################################################


#try:
image = cv2.imread(sys.argv[1] , 0)	
re_scale_proportion = int(sys.argv[2])
gray_values = int(sys.argv[3])
re_scale_method = sys.argv[4]
normalized_image = Quantization(image , gray_chanels = gray_values).apply() #binary_normalization(image)
re_scaled_image = Sampling(re_scale_proportion , normalized_image , re_scale_method).apply()
cv2.imshow('original_image' , image)
#cv2.imshow('normalized_image' , normalized_image)
cv2.imshow('re_caled' , re_scaled_image)
cv2.waitKey(0)
#except Exception as e:
#	print('Numero errado de parametros.')
#	print('Parametros : image_path resize_proportion gray_values re_scale_method')
#	raise e
	


'''
test_image = np.array(([ 0 , 15 , 23 , 15 , 30 , 120] ,
					   [ 42 , 80 , 35 , 172 , 200 , 255] , 
					   [ 255 , 120 , 40 , 15 , 35 , 180] , 
					   [ 100 , 20 , 30 , 40 , 45 , 85 ] , 
					   [ 70 , 10 , 8 , 16 , 45 , 120 ] ,
					   [ 35 , 45 , 70 , 85 , 88 , 0]) ,
					   np.uint8)
'''
