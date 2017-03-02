import numpy as np
import cv2


image_1 = cv2.imread('wdg4.png' , 0) #le a imagem 1
image_2 = cv2.imread('wdg5.png' , 0) #le a imagem 2
rows , cols = image_1.shape #pega as medidas de altura e largura da imagem 1


rotation_affine_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), 172 , 1) #otem matriz que ira rotacionar a imagem 1 em 180 graus para que fiquem no mesmo sentido
rotated_image = cv2.warpAffine(image_1 , rotation_affine_matrix ,(cols,rows)) #aplica a matriz affine rotacionando a imagem 1
image_2 = np.delete(image_2 , 1, 0) #remove uma linha da imagem 2, por ela ter mais linhas do que a imagem 2 nao eh permitido fazer operacoes aritmeticas em imagens com dimensoes diferentes

#thresh1 = cv2.threshold(image_1 ,120,255,cv2.THRESH_BINARY)[1]
#thresh2 = cv2.threshold(image_2 ,120,255,cv2.THRESH_BINARY)[1]
#M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 172 , 1)
#thresh_dst = cv2.warpAffine(thresh1 , M ,(cols,rows))

pairing_affine_matrix = np.float32([[1,0,41],[0,1, -14 ]])
paired_image = cv2.warpAffine(rotated_image , pairing_affine_matrix , (cols,rows))
#thresh_dst = cv2.warpAffine(thresh_dst , M , (cols,rows))


binary_image_2 = cv2.threshold(image_2 ,120,255,cv2.THRESH_BINARY)[1]
binary_paired_image = cv2.threshold(paired_image ,120,255,cv2.THRESH_BINARY)[1]
sum_image = binary_image_2 + binary_paired_image

result_image = sum_image.copy()
for x in xrange(0 , rows):
	for y in xrange(0 , cols):
		if sum_image.item(x , y) > 0:
			sum_image.itemset(x , y , 255)


subtracted_image = sum_image - binary_image_2
count = 0
for x in xrange(0 , rows):
	for y in xrange(0 , cols):
		if subtracted_image.item(x , y) == 255:
			count += 1

print('aproximated diference : ' + str(count))

#cv2.imshow('1' , image_1)
#cv2.imshow('2' , image_2)
#cv2.imshow('dist' , rotated_image)
#cv2.imshow('result' , result_image)
#cv2.imshow('image_2_th' , binary_image_2)
#cv2.imshow('image_paired_th' , binary_paired_image)
#cv2.imshow('result' , sum_image - binary_image_2)
#cv2.imshow('multi' ,  paired_image)
#cv2.waitKey(0)