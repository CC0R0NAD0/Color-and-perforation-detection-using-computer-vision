# -*- coding: utf-8 -*-
"""Copia de CodFin.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H9b1jTbNtpJDuO4UpbnwLPuKBF5jxGqC
"""

#importar los archivos en carpeta gzip
###############################################################
#                      Authors:                               #
#                  Carlos Coronado                            #
#                  Adrián Monge                               #
#                   ITCR MT 8004                              #
#   Red neuronal convolucional: Clasificacion de caracteres   #
###############################################################


# Importante mencionar que para que este script funcione se debe correr
# en google Colab, pues se hizo uso de un parche de dicha plataforma para
# hacer correr una función de la librería cv2, que se requería.


# Inicialización del entonrno e importación de librerías

from google.colab import drive  #Librería para accesar a archivos drive
import os  #Librería manejo del sistema

# Montar el archivo del drive (con previa autorización del usuario)
drive.mount('/content/drive', force_remount=True)

# Abrir el documento con la ruta de acceso personal predeterminada.
#os.chdir("/content/drive/MyDrive/Sistemas_V/Mini_Proyecto")  #Cuenta carlos

os.chdir("/content/drive/MyDrive/TEC/XIII Semestre/Sistemas_V/Mini_Proyecto") #Cuenta Adrián

from PIL import Image #Librería para trabajo de imagenes

import numpy as np  # Librearía manejo arreglos
import matplotlib.pyplot as plt  # Libreria para mostrar imagenes
import matplotlib.image as mpimg  #manejo imagen


from skimage.color import rgb2gray # se pasa a escala de gris

import cv2  # libreria trabajo con imagenes

from google.colab.patches import cv2_imshow # Se utiliza este parche para 
                                            # poder mostrar las imágenes en
                                            # pantalla

# Funciones de binarización planteadas

# Función que encuentra automáticamente el umbral de binarización, mediante
# una aproximación.
# Se debe ingresar la imagen en escala de grises.
# Retorna la imagen ya binarizada.
def threshold_demo(image):
    ret, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    print('threshold value %s' % ret)
    #cv2_imshow(binary)
    return binary
 
# Umbral adaptativo: Obtiene el umbral calculando la media de la Funcion de 
# distribución del histograma.
# Se debe ingresar la imagen en escala de grises.
# Retorna la imagen ya binarizada.
def custom_threshold(image):
    h, w = image.shape[:2]
    m = np.reshape(image, [1, w*h])
         # Mean
    mean = (m.sum() / (w*h))  #
    print('mean:', mean)
    ret, binary = cv2.threshold(image, mean, 255, cv2.THRESH_BINARY)
    #cv2_imshow(binary)
    return binary
 
# Establecer manualmente el umbral. La función pide al usuario el valor umbral
# de binarización. Para esto, antes se tiene que conocer el histograma
# de la imagen correspondiente.
# Se debe ingresar la imagen en escala de grises
# Retorna la imagen ya binarizada
def threshold_demo_1(image):
    X=int(input("Ingrese el valor umbral (0 - 255): "))
    ret, binary = cv2.threshold(image, X, 255, cv2.THRESH_BINARY)
    print('threshold value %s' % ret)
    #cv2_imshow(binary)
    return binary,ret

# Función que encuentra el valor umbral de binarización cuando en el histograma 
# se identifican claramente dos picos.
# Se debe ingresar la imagen en escala de grises
# Retorna la imagen ya binarizada
def threshold_demo_2(image):
    ret, binary = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY)
    print('threshold value %s' % ret)
    #cv2_imshow(binary)
    return binary, ret

#Carga imagen en variable
original = cv2.imread("Imagenes/Azul/4.jpg")
#original = cv2.imread("Imagenes/pruebas_color/foto_gris.jpg")



#Cambiar tamaño imagen para procesado
new_original = cv2.resize(original,(320,240))


plt.subplots(figsize=(16, 4)) # tamaño de imagen
plt.subplot(1,3,1) # tamaño 1 fila,2 columnas, columna 1
# Muestra la imagen con el nuevo tamaño
cv2_imshow(new_original) # se imprime la imagen en formato cv2


#se cambia el formato a PIL para representar las imagenes juntas
convert_color = cv2.cvtColor(new_original, cv2.COLOR_BGR2RGB)
im_pil = Image.fromarray(convert_color)
#plt.title("Imagen con cambio de tamaño")
plt.xlabel("Posición en X (pixel)")
plt.ylabel("Posición en Y (pixel)")
plt.imshow(im_pil)

# Se pasa la imagen a escala de grises con valores de 0 a 255
gris = cv2.cvtColor(new_original, cv2.COLOR_BGR2GRAY)
# Se muestra la imagen en escala de grises

plt.subplot(1,3,2) # tamaño 1 fila,2 columnas, columna 1
plt.imshow(gris, cmap=plt.cm.gray)
#plt.title("Imagen en escala de grises")
plt.xlabel("Posición en X (pixel)")
plt.ylabel("Posición en Y (pixel)")
#plt.savefig("ObjetoGrises.png")


# Se obtine el histograma de la imagen en escala de grises
plt.subplot(1,3,3) # tamaño 1 fila,2 columnas, columna 3
hist_orig = cv2.calcHist([gris], [0], None, [256], [0, 255])

#plt.title("Histograma sin binarizar",)
#plt.figure()
plt.plot(hist_orig)
plt.xlabel("Nivel de gris")
plt.ylabel("Cantidad de píxeles")
#plt.savefig("histograma_SinBina2_EG_P1.png")

plt.show()

# Se aplica un filtro Gauss a la imagen, para que las transiciones sean más suaves
gauss = cv2.GaussianBlur(gris, (5,5), 2) # el último parámetro de esta función
                                         # determina que tanto se difunina la imagen                                  
plt.subplots(figsize=(15, 4)) # tamaño de imagen
plt.subplot(1,2,1) # tamaño 1 fila,2 columnas, columna 1
plt.imshow(gauss, cmap=plt.cm.gray)     # Muestra la imagen
#plt.title("Imagen filtrada")
plt.xlabel("Posición en X (pixel)")
plt.ylabel("Posición en Y (pixel)")


# Se obtine el histograma de la imagen luego del filtro Gauss
plt.subplot(1,2,2) # tamaño 1 fila,2 columnas, columna 2
histo_gauss = cv2.calcHist([gauss], [0], None, [256], [0, 256])
# Se muestra el histograma
#plt.figure()
plt.plot(histo_gauss)
plt.xlabel("Nivel de gris")
plt.ylabel("Cantidad de píxeles")

plt.show()

MetBina = input("Ingrese un 1 para método de valor de umbral para binarización automático (Recomendado para cuando se aprecian los 2 picos en el histograma antes de aplicar el filtro gaussiano), o bien, ingrese cualquier otro número o letra para poner el valor de umbral para binarización de manera manual (viendo el histograma)")

# Se asigna a una variable la imagene binarizada
# según el método que se escoja. Se varió
# entre threshold_demo_2 y threshold_demo_1

if (MetBina=="1"):   
  bina, ret = threshold_demo_2(gauss) 
else:
  bina, ret = threshold_demo_1(gauss)


plt.subplots(figsize=(15, 4)) # tamaño de imagen
plt.subplot(1,2,1) # tamaño 1 fila,2 columnas, columna 1
plt.imshow(bina, cmap=plt.cm.gray)     # Muestra la imagen
plt.xlabel("Posición en X (pixel)")
plt.ylabel("Posición en Y (pixel)")


# Histograma de la imagen binarizada.
plt.subplot(1,2,2) # tamaño 1 fila,2 columnas, columna 2
histo_bina = cv2.calcHist([bina], [0], None, [256], [0, 256])
# Se muestra el histograma
#plt.figure()
plt.plot(histo_bina)
plt.xlabel("Nivel de gris")
plt.ylabel("Cantidad de píxeles")


plt.show()

# Buscamos los contornos

# Variable que guarda los contornos que encuentra con la función "findContours"
# Con cv2.RETR_TREE y cv2.CHAIN_APPROX_SIMPLE, se debe ingresar la imagen binarizada
# y retorna las posiciones que conforman a cada uno de los contornos que esta encuentra
(contornos,_) = cv2.findContours(bina, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
# Variable con el número de perforaciones encontradas
# Se le resta 2, porque la función siempre encuentra un contorno exterior y además,
# en contorno de la figura, y lo que nos interesa es obtener los contornos de las
# perforaciones que tiene cada figura
Num_Perf = len(contornos)-2

# Mostramos el número de perforaciones por figura
print("Se han encontrado {} perforaciones".format(Num_Perf))

Img_ConCont = new_original

# Se dibujan los contornos encontrados en la imagen original con la el reescalado
cv2.drawContours(Img_ConCont,contornos,-1,(0,0,255), 1)
cv2_imshow(new_original)  # Se muestra la imagen resultante

cv2.waitKey(0)

#################################################################

# Una vez obtenidos contornos se realiza un postprocesado para poder determinar
# cuales perforaciones hacen falta. Para esto se determina una posión en la 
# cual se encuentre el centro de la perforación. Luego con el contorno de la figura
# se divide, la misma, en regiones. Luego mediate condicionales (if's) se determina
# en qué posición se encuentra la perforación que se está analizando. Finalmente,
# cuando se analiza en contorno de cada perforación, se muestra en pantalla pediante un
# "False" cuales perforaciones hacen falta.

# Función para obtener la posición en "x" del centro de la perforación
# Se obtine mediante el valor promedio de las posciones en "x"
# Recibe a la variable con las posiciones del contorno de la perforación
def ValorMed_Cir_X(contor):
  suma = 0
  promed = 0
  for i in range(len(contor)):
    suma = contor[i][0][0] + suma
  promed = suma/len(contor)
  return int(round(promed))

# Función para obtener la posición en "y" del centro de la perforación
# Se obtine mediante el valor promedio de las posciones en "y"
# Recibe a la variable con las posiciones del contorno de la perforación
def ValorMed_Cir_Y(contor):
  suma = 0
  promed = 0
  for i in range(len(contor)):
    suma = contor[i][0][1] + suma
  promed = suma/len(contor) 
  return int(round(promed))

# Función para determinar la posición más a la derecha del contorno de la figura
# A partir de una posición en "x" inicial del contorno, comienza analizar el resto de
# posiciones hasta encontrar a la que está más a la derecha (valor más grande en "x")
# Recibe a la variable con las posiciones del contorno de la figura
def BordeDerecha(ContorFig):
  Dere = ContorFig[0][0][0]
  for i in range(len(ContorFig)):
    if ContorFig[i][0][0] > Dere:
      Dere = ContorFig[i][0][0]
    else:
      Dere = Dere
  return Dere

# Función para determinar la posición más a la izquierda del contorno de la figura
# A partir de una posición en "x" inicial del contorno, comienza analizar el resto de
# posiciones hasta encontrar a la que está más a la izquierda (valor más pequeño en "x")
# Recibe a la variable con las posiciones del contorno de la figura
def BordeIzquierda(ContorFig):
  Izq = ContorFig[0][0][0]
  for i in range(len(ContorFig)):
    if ContorFig[i][0][0] < Izq:
      Izq = ContorFig[i][0][0]
    else:
      Izq = Izq
  return Izq

# Función para determinar la posición más hacia arriba del contorno de la figura
# Apartir de una posición en "y" inicial del contorno, comienza analizar el resto de
# posiciones hasta encontrar a la que está más hacia arriba (valor más pequeño en "y")
# Recibe a la variable con las posiciones del contorno de la figura
def BordeArriba(ContorFig):
  Arri = ContorFig[0][0][1]
  for i in range(len(ContorFig)):
    if ContorFig[i][0][1] < Arri:
      Arri = ContorFig[i][0][1]
    else:
      Arri = Arri
  return Arri

# Función para determinar la posición más hacia abajo del contorno de la figura
# Apartir de una posición en "y" inicial del contorno, comienza analizar el resto de
# posiciones hasta encontrar a la que está más hacia abajo (valor más grande en "y")
# Recibe a la variable con las posiciones del contorno de la figura
def BordeAbajo(ContorFig):
  Aba = ContorFig[0][0][1]
  for i in range(len(ContorFig)):
    if ContorFig[i][0][1] > Aba:
      Aba = ContorFig[i][0][1]
    else:
      Aba = Aba
  return Aba

#############################################

# Variables que almacenan si se encuentra o no la perforación correspondiente
Perf_Arriba = False
Perf_Abajo = False
Perf_Centro = False
Perf_Izquierda = False
Perf_Derecha = False

# Bordes estimados de la figura
BorArriba = BordeArriba(contornos[1])
BorAbajo = BordeAbajo(contornos[1])
BorIzquierda = BordeIzquierda(contornos[1])
BorDerecha = BordeDerecha(contornos[1])

# Ciclo for que recorre cada uno de los contrornos de las perforaciones para
# determinar en qué posición se encuente. Se descartan los dos primeros contornos,
# pues estos corresponden al borde exterior y al de la figura en cualquier caso 
# (Siempre y cuando  se haya podido binarizar bien la imagen)
for i in range(2,len(contornos)):
  # Posiciones en "x" y "y" de la perforación
  Cen_Perf_X = ValorMed_Cir_X(contornos[i])
  Cen_Perf_Y = ValorMed_Cir_Y(contornos[i])
  # Se determinan las dimensiones (en pixeles) de la figura, tanto en "x" como en "y"
  LongitudX = BorDerecha - BorIzquierda
  LongitudY = BorAbajo - BorArriba
  # Divisiones creadas para determinar las posiciones de la perforación
  # Se crea una cuadrícula de 3 x 3
  A = BorDerecha - round(LongitudX*(1/3))     #Division vertical derecha
  B = BorIzquierda + round(LongitudX*(1/3))   #Division vertical izquierda
  C = BorArriba + round(LongitudY*(2/5))      #Division horizontal superior 
  D = BorAbajo - round(LongitudY*(2/5))       #Division horizontal inferior
  
  # Se plantean las condicones para determinar en qué posición se encuentra cada 
  # perforación, de acuerdo con la posición del centro de la perforación.
  if ( C > Cen_Perf_Y ):
    Perf_Arriba = True
  elif ( D >= Cen_Perf_Y ):
    if ( A < Cen_Perf_X ):
      Perf_Derecha = True
    elif ( B < Cen_Perf_X ):
      Perf_Centro = True
    else:
      Perf_Izquierda = True
  else:
    Perf_Abajo = True

# Se muestra en pantalla el resultado del análisis de presencia de perforaciones
# print("¿Hay perforacion abajo?: ", Perf_Abajo)
# print("¿Hay perforacion arriba?: ", Perf_Arriba)
# print("¿Hay perforacion a la derecha?: ", Perf_Derecha)
# print("¿Hay perforacion a la izquerda?: ", Perf_Izquierda)
# print("¿Hay perforacion en el centro?: ", Perf_Centro)

#Se imprime la relación de tamaño de la imagen
print("\nRelación de tamaño de la tarjeta respecto al fondo: ",((BorDerecha - BorIzquierda)/320)*100 ," %")
print("Valor de Threshold: ", ret)

#Se indican las perforaciones bastantes según el analisis
if Perf_Abajo == False:
  print("\nFalta la perforación de abajo")
if Perf_Arriba == False:
  print("Falta la perforación de arriba")
if Perf_Derecha == False:
  print("Falta la perforación de la derecha")
if Perf_Izquierda == False:
  print("Falta la perforación de la izquierda")
if Perf_Centro == False:
  print("Falta la perforación del centro")
if Num_Perf == 5:
  print("No hace falta ninguna perforación")

#//////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////
# DETECCIÓN DE COLOR EN LA IMAGEN
import matplotlib.colors as colors #libreria necesaria para histogramas hsv

#se recarga la imagen para operar los histogramas de color
# image = Image.open("Imagenes/Cafe_largo/4.jpg") #Carga imagen en variable
# new_image = image.resize((320, 240))   #Cambiar tamaño imagen
# img_objeto = np.array(new_image)  # Se convierte imagen a arreglo



# img_objeto = np.asarray(img_objeto)  # Se convierte imagen a arreglo
# img = cv2.cvtColor(img_objeto, cv2.COLOR_RGB2BGR) #se invierte el color
# img  = img_objeto #Se copia la variable

img = new_original

plt.subplots(figsize=(18, 5)) #Se establece el tamaño del conjunto de imagenes



plt.subplot(1,3,1) #Primera imagen RGB
b, g, r = img[:,:,0], img[:,:,1], img[:,:,2] #se extraen los array de cada canal

#Se muestran los 3 histogramas en 1 con la etiqueta de cada canal
hist_b = cv2.calcHist([b],[0],None,[255],[0,256])
hist_g = cv2.calcHist([g],[0],None,[255],[0,256])
hist_r = cv2.calcHist([r],[0],None,[255],[0,256])
plt.plot(hist_r, color='r', label="r")
plt.plot(hist_g, color='g', label="g")
plt.plot(hist_b, color='b', label="b")
#plt.title("Histograma RGB")
plt.xlabel("Valor")    
plt.ylabel("Frecuencia")
plt.legend()

#Segunda imagen se convierte de RGB a HSV
plt.subplot(1,3,2)
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#Se muestran los histogramas
h, s, v = img2[:,:,0], img2[:,:,1], img2[:,:,2]
hist_h = cv2.calcHist([h],[0],None,[256],[0,256])
hist_s = cv2.calcHist([s],[0],None,[256],[0,256])
hist_v = cv2.calcHist([v],[0],None,[256],[0,256])
plt.plot(hist_h, color='c', label="h")
plt.plot(hist_s, color='m', label="s")
plt.plot(hist_v, color='y', label="v")
#plt.title("Histograma HSV")
plt.xlabel("Valor")    
plt.ylabel("Frecuencia")
plt.legend()
#///////////////////////////////////////////////////////////////////////////////

#Se imprime la saturacion de la imagen sola, para mejor analisis
#arr=(img_objeto.astype(float))/255.0 # Se normaliza el valor de 0 a 1
arr=(img.astype(float))/255.0 # Se normaliza el valor de 0 a 1
img_hsv = colors.rgb_to_hsv(arr[...,:3]) # Se convierten los 3 canales a hsv

lu=img_hsv[...,1].flatten() # Se aplana el arreglo

#Se determina el histograma de los datos suministrados de forma lineal
plt.subplot(1,3,3)                  
# Se define rango, cantidad de columnas y color
plt.hist(lu,bins=100,range=(0.0,1.0),histtype='stepfilled', color='m', label='Saturacion')
#plt.title("Saturación")
plt.xlabel("Valor")    
plt.ylabel("Frecuencia")
plt.legend()
plt.show()

h = bina.shape[0] # dimension de alto
w = bina.shape[1] # dimension de ancho

#print(h,w)

#Se generan dos imagnes vacias
est_image = np.ones((h,w))
pix_color = np.ones((h,w))

#print(BorArriba,BorAbajo, BorIzquierda, BorDerecha)

# Se toman lis limites correcpondientes a la posicion de la tarjeta
est_image[BorArriba:BorAbajo, BorIzquierda:BorDerecha] = 0

#print(est_image[BorArriba-1:BorAbajo+1, BorIzquierda-1:BorDerecha+1])

# print(BorIzquierda)
# print(BorDerecha)
# print(BorArriba)
# print(BorAbajo)



#array para agregar las posiciones a analizar
posic_object = []

#convertida = cv2.cvtColor(new_original, cv2.COLOR_BGR2HSV)


#ciclo que recorre la imagen si el pixel está dentro del recuadro y es de color
#negro se agrega a una nueva imagen para visulizar los pixeles analizados
#y se agrega el pixel a la lista para analizar su saturacion
for i in range(h):
    for j in range(w):
        if((bina[i,j] == 0) and (est_image[i,j] == 0)):
          pix_color[i,j] = 0
          posic_object.append(img2[i,j,1])



#Se imprime el recuadro de la posicion de la imagen
plt.subplots(figsize=(18, 5))

plt.subplot(1,3,1)
imgplot_BN=plt.imshow(est_image, cmap=plt.cm.gray)
plt.xlabel("Posición en X (pixel)")
plt.ylabel("Posición en Y (pixel)")



# Se imprime la imagen con los pixeles a analizar
plt.subplot(1,3,2)
imgplot_BN=plt.imshow(pix_color, cmap=plt.cm.gray)
plt.xlabel("Posición en X (pixel)")
plt.ylabel("Posición en Y (pixel)")



# se convierte la imagen y lista a arreglo
pix_color = np.array(pix_color)
posic_object = np.array(posic_object)

print (posic_object)


#se imprime el histograma de saturacion unicamente de los pixeles analizados
plt.subplot(1,3,3)
hist_s = cv2.calcHist([posic_object],[0],None,[256],[0,256.0])
plt.axvline(x=0.2 * 256, color='r', label='Sat 20%-División color')
plt.plot(hist_s, color='m', label="s")
#plt.title("Histograma S")
plt.xlabel("Valor")    
plt.ylabel("Frecuencia")
plt.legend()
plt.show()




# Analisis de saturación de los pixeles de la tarjeta

porcen_v = 0.2  #umbral de 20% de saturacion para definir
cont = 0        # contador de pixeles
#ciclo que cuenta cuantos pixeles tienen un valor de S menor a 20% (de 256)
for i in range(len(posic_object)):
  if(int(posic_object[i]) < (porcen_v * 256)):
    cont = cont +1


# Se imprimem los resultados
#print(pix_color)


#Se imprimen los resultados de las cantidades de pixeles de las imagenes y el analisis
print("Cantidad total de pixeles en la imagen: ", h*w )
print("Cantidad de pixeles en el recuadro:", (BorArriba - BorAbajo) * (BorIzquierda - BorDerecha))
print("Cantidad de pixeles correspondientes a la tarjeta:", len(posic_object))
print("Cantidad pixeles con saturación menor a 20%: ",cont)

# Se toma la condicion de que si el 80% está por debajo de 20% es Monocromatica
# si no es cromatica (Criterio Pareto)
if cont > (0.80 * len(pix_color)):
  print("Resultado: Imagen Monocromática")
else:
  print("\nResultado: Imagen Cromática")

#Se recrea el resultado final en un solo bloque para mostrar

plt.subplots(figsize=(12, 4)) #Se establece el tamaño del conjunto de imagenes
# Se dibujan los contornos encontrados en la imagen original con la el reescalado
plt.subplot(1,2,1)
cv2.drawContours(new_original,contornos,-1,(0,0,255), 1)
#cv2_imshow(new_original)  # Se muestra la imagen resultante

#se cambia el formato a PIL para representar las imagenes juntas
convert_color2 = cv2.cvtColor(new_original, cv2.COLOR_BGR2RGB)
im_pil = Image.fromarray(convert_color2)
plt.title("(a) Detección de Contornos", y=-0.25 )
plt.imshow(im_pil)

#se imprime el histograma de saturacion unicamente de los pixeles analizados
plt.subplot(1,2,2)

hist_s = cv2.calcHist([posic_object],[0],None,[256],[0,256.0])
plt.axvline(x=0.2 * 256, color='r', label='Sat 20%-División color')
plt.plot(hist_s, color='m', label="s")
plt.title("(b) Histograma Saturación", y=-0.25)
plt.xlabel("Valor")    
plt.ylabel("Frecuencia")
plt.legend()

plt.show()




#Se imprime la relación de tamaño de la imagen
print("   Relación de tamaño de la tarjeta respecto al fondo: ",((BorDerecha - BorIzquierda)/320)*100 ," %")
print("   Valor de Threshold: ", ret)

#Se indican las perforaciones bastantes según el analisis
if Perf_Abajo == False:
  print("\n   Falta la perforación de abajo")
if Perf_Arriba == False:
  print("   Falta la perforación de arriba")
if Perf_Derecha == False:
  print("   Falta la perforación de la derecha")
if Perf_Izquierda == False:
  print("   Falta la perforación de la izquierda")
if Perf_Centro == False:
  print("   Falta la perforación del centro")
if Num_Perf == 5:
  print("   No hace falta ninguna perforación")




#Se imprimen los resultados de las cantidades de pixeles de las imagenes y el analisis
print("\n   Cantidad total de pixeles en la imagen: ", h*w )
print("   Cantidad de pixeles en el recuadro:", (BorAbajo-BorArriba) * (BorDerecha-BorIzquierda))
print("   Cantidad de pixeles correspondientes a la tarjeta:", len(posic_object))
print("   Cantidad pixeles con saturación menor a 20%: ",cont)

# Se toma la condicion de que si el 80% está por debajo de 20% es Monocromatica
# si no es cromatica (Criterio Pareto)
if cont > (0.80 * len(posic_object)):
  print("   Resultado: Imagen Acromática")
else:
  print("\n   Resultado: Imagen Cromática")