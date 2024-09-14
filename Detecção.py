import cv2
import numpy as np
import random




FILE = "001_01.PNG"
CAP = 1


SAMPLES = 3


#parametros de circulo
DP = 1.2
MINDIST = 10
PARAM1 = 50
PARAM2 = 20
MINRADIUS_DEFAULT = 10
MAXRADIUS_DEFAULT = 150
MINRAD_CEILING = 100
MAXRAD_CEILING = 100
RAD_PACE = 10
MINRAD_MAXVALUE = 6


#Parametros de linha
LIMITEMINHOUGH = 50
LIMITEMAXHOUGH = 120
PACEHOUGH = 5


#contador para label de imagens
contador = 0


def Identificação(imagens):
   
    titulos = {}
    linhas = {}
    param_linhas = {}
    param_circulos = {}
    circulos = {}
    imagens_finais = {}
    eixo_x_linhas = {}
    eixo_x_circulos = {}
    for conjunto_imagens in imagens:
       
        eixo_x_linhas[conjunto_imagens] = {}
        eixo_x_circulos[conjunto_imagens] = {}
        titulos[conjunto_imagens] = {}
        linhas[conjunto_imagens] = {}
        param_linhas[conjunto_imagens] = {}
        param_circulos[conjunto_imagens] = {}
        circulos[conjunto_imagens] = {}
        imagens_finais[conjunto_imagens] = {}


        for indice_imagem_original in imagens[conjunto_imagens]:
           
            try:
                teste = eixo_x_linhas[conjunto_imagens][indice_imagem_original]
            except:
                eixo_x_linhas[conjunto_imagens][indice_imagem_original] = {}
                eixo_x_circulos[conjunto_imagens][indice_imagem_original] = {}
                titulos[conjunto_imagens][indice_imagem_original] = {}
                linhas[conjunto_imagens][indice_imagem_original] = {}
                param_linhas[conjunto_imagens][indice_imagem_original] = {}
                param_circulos[conjunto_imagens][indice_imagem_original] = {}
                circulos[conjunto_imagens][indice_imagem_original] = {}
                imagens_finais[conjunto_imagens][indice_imagem_original] = {}


            contador = 0
            for img_tratada in imagens[conjunto_imagens][indice_imagem_original]:
                eixo_x_linhas[conjunto_imagens][indice_imagem_original][contador] = []
                eixo_x_circulos[conjunto_imagens][indice_imagem_original][contador] = []
                titulos[conjunto_imagens][indice_imagem_original][contador] = {'linhas':[], 'circulos':[]}
                titulos[conjunto_imagens][indice_imagem_original][contador]['circulos'] = []
                linhas[conjunto_imagens][indice_imagem_original][contador] = []
                param_linhas[conjunto_imagens][indice_imagem_original][contador] = []
                param_circulos[conjunto_imagens][indice_imagem_original][contador] = []
                circulos[conjunto_imagens][indice_imagem_original][contador] = []
                imagens_finais[conjunto_imagens][indice_imagem_original][contador] = {'linhas':[], 'circulos':[]}


                for parametroHough in range (LIMITEMINHOUGH, LIMITEMAXHOUGH+1, PACEHOUGH):
                   
                    eixo_x_linhas[conjunto_imagens][indice_imagem_original][contador] += [parametroHough]
                    titulos[conjunto_imagens][indice_imagem_original][contador]['linhas'],imagens_finais[conjunto_imagens][indice_imagem_original][contador]['linhas'],linhas[conjunto_imagens][indice_imagem_original][contador], param_linhas[conjunto_imagens][indice_imagem_original][contador] = detect_lines(titulos[conjunto_imagens][indice_imagem_original][contador]['linhas'],
                                                                                                                                                                                                                        imagens_finais[conjunto_imagens][indice_imagem_original][contador]['linhas'],
                                                                                                                                                                                                                        linhas[conjunto_imagens][indice_imagem_original][contador],
                                                                                                                                                                                                                        param_linhas[conjunto_imagens][indice_imagem_original][contador],
                                                                                                                                                                                                                        parametroHough,image_raw= imagens[conjunto_imagens][indice_imagem_original][img_tratada],
                                                                                                                                                                                                                        image_or_path=False)
                for minrad in range(5, MINRAD_CEILING+1, RAD_PACE):
                    vetor_minrad = []
                    for i in range(1, MINRAD_MAXVALUE+1):
                        vetor_minrad.append(minrad*i)
                    for maxrad in range(minrad, MAXRAD_CEILING+1, RAD_PACE):
                        for dist in vetor_minrad:
                            label_eixo_X = [int(dist/minrad), minrad, maxrad]
                            eixo_x_circulos[conjunto_imagens][indice_imagem_original][contador] += [label_eixo_X]
                            titulos[conjunto_imagens][indice_imagem_original][contador]['circulos'],imagens_finais[conjunto_imagens][indice_imagem_original][contador]['circulos'],circulos[conjunto_imagens][indice_imagem_original][contador], param_circulos[conjunto_imagens][indice_imagem_original][contador] = detect_circulos(titulos[conjunto_imagens][indice_imagem_original][contador]['circulos'],
                                                                                                                                                                                                                    imagens_finais[conjunto_imagens][indice_imagem_original][contador]['circulos'],
                                                                                                                                                                                                                    circulos[conjunto_imagens][indice_imagem_original][contador],
                                                                                                                                                                                                                    param_circulos[conjunto_imagens][indice_imagem_original][contador],
                                                                                                                                                                                                                    circleparams=[dist, minrad, maxrad], image_raw= imagens[conjunto_imagens][indice_imagem_original][img_tratada],
                                                                                                                                                                                                                    image_or_path=False)
                contador += 1
   
    output = {}
    output["titulos"] = titulos
    output["linhas"] = linhas
    output["param_linhas"] = param_linhas
    output["param_circulos"] = param_circulos
    output["circulos"] = circulos
    output["imagens"] = imagens
    output["imagens_finais"] = imagens_finais
    output["Param_Hough_linhas"] = eixo_x_linhas
    output["param_Hough_circulos"] = eixo_x_circulos


    return output


   
def detect_lines(titulos, imagens, linhas, param_linhas, parametroHough, image_raw = FILE, image_or_path = True):
    # Carregar a imagem
   
    global contador
    gray_image, image = leitura_imagem(image_raw, image_or_path)
   
    #detecção de linhas
    edges = cv2.Canny(gray_image, 50, 150)


    mask = np.ones_like(edges) * 255  # Criar uma máscara branca


    height, width = edges.shape
    lenght = 10
    roi_top_left = (lenght, lenght)          # Coordenadas do canto superior esquerdo
    roi_bottom_right = (width-lenght, height-lenght)  # Coordenadas do canto inferior direito


    # Desenhar um retângulo preto na máscara para a área a ser ignorada (bordas)
    mask[0:roi_top_left[1], :] = 0
    mask[roi_bottom_right[1]:, :] = 0
    mask[:, 0:roi_top_left[0]] = 0
    mask[:, roi_bottom_right[0]:] = 0
   
    # Aplicar a máscara à imagem de bordas
    masked_edges = cv2.bitwise_and(edges, mask)
   
    # Aplicar a Transformada de Hough para linhas
    lines = cv2.HoughLines(masked_edges, 1, np.pi / 180, parametroHough)
   
    # Desenhar as linhas detectadas na imagem original
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
   
    try:
        linhas.append(len(lines))
    except:
        linhas.append(0)
   
    param_linhas.append(lines)
    contador += 1
    titulos.append("Imagem"+str(contador)+" Hough = "+str(parametroHough))
    imagens.append(image)


    return titulos, imagens, linhas, param_linhas
   
def detect_circulos(titulos, imagens, circulos,param_circulos, circleparams = [MINDIST, MINRADIUS_DEFAULT, MAXRADIUS_DEFAULT], image_raw = FILE, image_or_path = True):
    # Carregar a imagem
   
    global contador


    gray_image, image = leitura_imagem(image_raw, image_or_path)
       
       
    circles = cv2.HoughCircles(
    gray_image,
    cv2.HOUGH_GRADIENT,
    dp=DP,
    minDist= circleparams[0] ,
    param1=PARAM1,
    param2=PARAM2,
    minRadius=circleparams[1],
    maxRadius=circleparams[2]
)


# Verificar se foram encontrados círculos
    if circles is not None:
        # Convertendo as coordenadas dos círculos para inteiros
        circles = np.round(circles[0, :]).astype("int")
   
        # Desenhar os círculos na imagem original
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 0, 255), 4)  # Círculo verde
            cv2.rectangle(image, (x - 1, y - 1), (x + 1, y + 1), (0, 0, 255), -1)  # Centro do círculo
    try:
        circulos.append(len(circles))
    except:
        circulos.append(0)
    param_circulos.append(circles)
    contador += 1
    titulos.append("Imagem"+str(contador) + " MINDIST = " +str(circleparams[0]) + " MINRAD = " +str(circleparams[1]) + " MAXRAD = " +str(circleparams[2]))
    imagens.append(image)


    return titulos, imagens, circulos, param_circulos    


def detect_linhas_e_circulos(titulos, imagens, linhas, circulos, parametroHough, circleparams = [MINDIST, MINRADIUS_DEFAULT, MAXRADIUS_DEFAULT], image_raw = FILE, image_or_path = True):


    global contador
    gray_image, image = leitura_imagem(image_raw, image_or_path)
   
    #detecção de linhas
    edges = cv2.Canny(gray_image, 50, 150)


    mask = np.ones_like(edges) * 255  # Criar uma máscara branca


    height, width = edges.shape
    lenght = 10
    roi_top_left = (lenght, lenght)          # Coordenadas do canto superior esquerdo
    roi_bottom_right = (width-lenght, height-lenght)  # Coordenadas do canto inferior direito


    # Desenhar um retângulo preto na máscara para a área a ser ignorada (bordas)
    mask[0:roi_top_left[1], :] = 0
    mask[roi_bottom_right[1]:, :] = 0
    mask[:, 0:roi_top_left[0]] = 0
    mask[:, roi_bottom_right[0]:] = 0
   
    # Aplicar a máscara à imagem de bordas
    masked_edges = cv2.bitwise_and(edges, mask)
   
    # Aplicar a Transformada de Hough para linhas
    lines = cv2.HoughLines(masked_edges, 1, np.pi / 180, parametroHough)
   
    # Desenhar as linhas detectadas na imagem original
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
   
    #detecção de circulos
    circles = cv2.HoughCircles(
    gray_image,
    cv2.HOUGH_GRADIENT,
    dp=DP,
    minDist= circleparams[0] ,
    param1=PARAM1,
    param2=PARAM2,
    minRadius=circleparams[1],
    maxRadius=circleparams[2]
)


# Verificar se foram encontrados círculos
    if circles is not None:
        # Convertendo as coordenadas dos círculos para inteiros
        circles = np.round(circles[0, :]).astype("int")
   
        # Desenhar os círculos na imagem original
        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 0, 255), 4)  # Círculo verde
            cv2.rectangle(image, (x - 1, y - 1), (x + 1, y + 1), (0, 0, 255), -1)  # Centro do círculo
    try:
        linhas.append(len(lines))
        try:
            circulos.append(len(circles))
            contador += 1
            titulos.append("Imagem"+str(contador)+" Hough = "+str(parametroHough) + "MINDIST = " +str(circleparams[0]) + "MINRAD = " +str(circleparams[1]) + "MAXRAD = " +str(circleparams[2]))
            imagens.append(image)
        except:
            circulos.append(0)
            contador += 1
            titulos.append("Imagem"+str(contador)+" Hough = "+str(parametroHough) + "MINDIST = " +str(circleparams[0]) + "MINRAD = " +str(circleparams[1]) + "MAXRAD = " +str(circleparams[2]))
            imagens.append(image)
    except:
        try:
            linhas.append(0)
            circulos.append(len(circles))
            contador += 1
            titulos.append("Imagem"+str(contador)+" Hough = "+str(parametroHough) + "MINDIST = " +str(circleparams[0]) + "MINRAD = " +str(circleparams[1]) + "MAXRAD = " +str(circleparams[2]))
            imagens.append(image)
        except:
            pass
   
    return titulos, imagens, linhas, circulos


def leitura_imagem(image_raw, image_or_path):
    global contador


    if(image_or_path):
        image = cv2.imread(image_raw)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    else:
        #imagem ja tratada
        gray_image = image_raw
        gray_image = np.uint8(gray_image)
        image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        image = np.uint8(image)


    return gray_image, image    


def exibir_imagens(titulos, imagens, linhas, circulos, samples = SAMPLES):
    for indice_tema in titulos:
        for indice_img_original in titulos[indice_tema]:
            #para linhas
            if samples > len(titulos[indice_tema][indice_img_original][0]['linhas']):
                size = len(titulos[indice_tema][indice_img_original][0]['linhas'])
                for i in range(size):
                    indice = i
                    titulo = str(titulos[indice_tema][indice_img_original][0]['linhas'][indice])+ " - "+str(indice_tema)+" "+str(linhas[indice_tema][indice_img_original][0][indice])+" linhas"
                    cv2.imshow(titulo, imagens[indice_tema][indice_img_original][0]['linhas'][indice])
            else:
                size = samples
                for i in range(size):
                    indice = random.randrange(1,len(titulos[indice_tema][indice_img_original][0]['linhas']))
                    titulo = str(titulos[indice_tema][indice_img_original][0]['linhas'][indice])+ " - "+str(indice_tema)+" "+str(linhas[indice_tema][indice_img_original][0][indice])+" linhas"
                    cv2.imshow(titulo, imagens[indice_tema][indice_img_original][0]['linhas'][indice])
           
            if samples > len(titulos[indice_tema][indice_img_original][0]['circulos']):
                size = len(titulos[indice_tema][indice_img_original][0]['circulos'])
                for i in range(size):
                    indice = i
                    titulo = str(titulos[indice_tema][indice_img_original][0]['circulos'][indice])+ " - "+str(indice_tema)+" "+str(circulos[indice_tema][indice_img_original][0][indice])+" Circulos"
                    cv2.imshow(titulo, imagens[indice_tema][indice_img_original][0]['circulos'][indice])
            else:
                size = samples
                for i in range(size):
                    indice = random.randrange(1,len(titulos[indice_tema][indice_img_original][0]['circulos']))
                    titulo = str(titulos[indice_tema][indice_img_original][0]['circulos'][indice])+ " - "+str(indice_tema)+" "+str(circulos[indice_tema][indice_img_original][0][indice])+" Circulos"
                    cv2.imshow(titulo, imagens[indice_tema][indice_img_original][0]['circulos'][indice])
           
    cv2.waitKey(0)
    cv2.destroyAllWindows()




   


if __name__ == "__main__":
    detect_linhas_e_circulos([""], [""])
