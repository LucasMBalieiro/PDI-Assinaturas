import matplotlib.pyplot as plt
import numpy as np
from Detecções import detect_lines, exibir_imagens, detect_circulos, detect_linhas_e_circulos, Identificação
from Tratamentos import tratamento_imagem
from Matching import matching




"""
Projeto final de Processamento Digital de Imagens
Grupo 9 - Verificação de assinaturas
Membros:
- Lucas Maciel Balieiro - 800534
- Marciel Silva de Almeida - 628069


base de dados referencia: http://www.iapr-tc11.org/mediawiki/index.php/ICDAR_2011_Signature_Verification_Competition_(SigComp2011)


"""




PATH_BASE = "./"
PATH_ALVO = "./"
IMAGENS_BASE = ["001_01.PNG","001_02.PNG"]
IMAGEM_ALVO = ["001_03.PNG", "001_01.PNG", "Assinatura diferente.png"]
DEPARA_TIPO = {"imagens_orignais": "ORIGINAL", "gaussianas":"Tratada com filtro gaussiano", "binarias": "Binarizada e suavizada", "erodidas": "aplicada erosão", "abertas": "aplicada abertura"}




FATOR_LINHAS = 0.8
FATOR_CIRCULOS = 0.2


PESO_PADRAO = {'gaussianas': 0.1, 'binarias': 0.3, 'erodidas':0.3, 'abertas':0.3}


# files precisam ser o relative path
# pastas precisam ser o restante do caminho que levam aos files. Apenas uma por entidade (base ou alvo)
def main(pasta_base = PATH_BASE, files_base = IMAGENS_BASE, pasta_alvo = PATH_ALVO, files_alvo = IMAGEM_ALVO):


   
    identidade_base = {}
    identidade_alvo = {}


    #Realização de diferentes tratamentos (aplicação de filtro gaussiano, binarização e morfologia matemática) a fim de preparar diferentes abordagens para cada imagem
    _, identidade_base["gaussianas"], identidade_base["binarias"], identidade_base["erodidas"], identidade_base["abertas"] = tratamento_imagem(path= pasta_base, files=files_base)
    _, identidade_alvo["gaussianas"], identidade_alvo["binarias"], identidade_alvo["erodidas"], identidade_alvo["abertas"] = tratamento_imagem(path= pasta_alvo, files=files_alvo)
   
 
    #Processo de identificação de linhas e circulos utilizando-se transformadas de Hough
    identidade_base["Hough"] = Identificação(identidade_base)
    identidade_alvo["Hough"] = Identificação(identidade_alvo)


    #Amostra de imagens
    exibir_imagens(identidade_base["Hough"]['titulos'], identidade_base["Hough"]['imagens_finais'], identidade_base["Hough"]['linhas'], identidade_base["Hough"]['circulos'])
    exibir_imagens(identidade_alvo["Hough"]['titulos'], identidade_alvo["Hough"]['imagens_finais'], identidade_alvo["Hough"]['linhas'], identidade_alvo["Hough"]['circulos'])
   
   
    #Graficos de influencia das parametrizações na identificação de linhas e circulos
    grafico_quantidades(identidade_base["Hough"]["linhas"],identidade_base["Hough"]["circulos"], identidade_base["Hough"]["Param_Hough_linhas"], identidade_base["Hough"]["param_Hough_circulos"], "Base")
    grafico_quantidades(identidade_alvo["Hough"]["linhas"],identidade_alvo["Hough"]["circulos"], identidade_alvo["Hough"]["Param_Hough_linhas"], identidade_alvo["Hough"]["param_Hough_circulos"], "Alvo")
   
    #processo de matching e expressão de resultado
    resultado_matches = matching(identidade_base['Hough']['param_linhas'],identidade_base['Hough']['param_circulos'], identidade_alvo['Hough']['param_linhas'], identidade_alvo['Hough']['param_circulos'])
    result_output(resultado_matches, files_base, files_alvo)


 
def result_output(resultados, bases, alvos):
    result_por_tratamento = {}
    for tipo in resultados['linhas']:
        result_por_tratamento[tipo] = {}
           
    result_geral = {}
    for alvo in alvos:
        result_geral[alvo] = 0
        for tipo in resultados['linhas']:
            result_por_tratamento[tipo][alvo] = 0
            for base in bases:
                result_por_tratamento[tipo][alvo] += round((resultados['linhas'][tipo][base][alvo]*FATOR_LINHAS+resultados['circulos'][tipo][base][alvo]*FATOR_CIRCULOS)/len(bases),3)
   
    for tipo in result_por_tratamento:
        for alvo in alvos:
            result_geral[alvo] += round(result_por_tratamento[tipo][alvo]*PESO_PADRAO[tipo], 3)


    print(result_por_tratamento)
    print(result_geral)


   
def on_key(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)




def grafico_quantidades(linhas, circulos, x_linhas, x_circulos, base_or_target = "Base"):
   
    fig_linha = {}
    contador_linhas = 1
    for tipo in linhas:
        ax_linhas = []
        ay_linhas = []
        ax_circulos = []
        ay_circulos = []
        for imagem in linhas[tipo]:
            subplot = int("22"+str(contador_linhas))
            try:
                teste = fig_linha[imagem]
            except:
                fig_linha[imagem] = plt.figure()
           
            axs_linha = fig_linha[imagem].add_subplot(subplot)
            for i in linhas[tipo][imagem]:
                ax_linhas += x_linhas[tipo][imagem][i]
                ay_linhas += linhas[tipo][imagem][i]
           
            conjunto = str(DEPARA_TIPO[tipo])
            if base_or_target == "Base":
                titulo = "Linhas imagem base " + str(imagem) + " ("+str(tipo)+")"
            else:
                titulo = "Linhas imagem alvo " + str(imagem) + " ("+str(tipo)+")"
                 
            # Gráfico: Linhas
            axs_linha.scatter(ax_linhas, ay_linhas, color = np.random.rand(3,), label = conjunto)
            axs_linha.set_title(titulo)
            axs_linha.set_xlabel('Parametro de Hough')
            axs_linha.set_ylabel('Quantidade de linhas identificadas')
            axs_linha.legend(loc='upper right')


        contador_linhas += 1
    for i in fig_linha:
        fig_linha[i].canvas.mpl_connect('key_press_event', on_key)
   
    plt.show()


    for tipo in circulos:    
        for imagem in circulos[tipo]:
            fig_1 = plt.figure()  # 2 linha e 2 colunas
   
            axs_circulo_dist = fig_1.add_subplot(221)
            axs_circulo_Minrad = fig_1.add_subplot(222)
            axs_circulo_Maxrad = fig_1.add_subplot(223)
           
            for i in circulos[tipo][imagem]:
                ax_circulos += x_circulos[tipo][imagem][i]
                ay_circulos += circulos[tipo][imagem][i]
           
             
                # Primeiro gráfico: circulos (dist)
                conjunto = str(DEPARA_TIPO[tipo])
                if base_or_target == "Base":
                    titulo = "Circulos imagem base " + str(imagem)
                else:
                    titulo = "Circulos imagem alvo " + str(imagem)


                dists = [linha[0] for linha in ax_circulos]
                axs_circulo_dist.scatter(dists, ay_circulos, color = np.random.rand(3,), label = conjunto)
                axs_circulo_dist.set_title(titulo + "(Dist)")
                axs_circulo_dist.set_xlabel('Dist')
                axs_circulo_dist.set_ylabel('Quantidade de circulos identificadas')
                axs_circulo_dist.legend(loc='upper right')


                #Segundo grafico: circulos (Minrad)
                mins = [linha[1] for linha in ax_circulos]
                axs_circulo_Minrad.scatter(mins, ay_circulos, color = np.random.rand(3,), label = conjunto)
                axs_circulo_Minrad.set_title(titulo + "(Minrad)")
                axs_circulo_Minrad.set_xlabel('Minrad')
                axs_circulo_Minrad.set_ylabel('Quantidade de circulos identificadas')
                axs_circulo_Minrad.legend(loc='upper right')


                #Terceiro grafico: circulos (maxrad)
                maxs = [linha[2] for linha in ax_circulos]
                axs_circulo_Maxrad.scatter(maxs, ay_circulos, color = np.random.rand(3,), label = conjunto)
                axs_circulo_Maxrad.set_title(titulo + "(Maxrad)")
                #ax_caxs_circulo_Maxrad].set_xticks([])
                axs_circulo_Maxrad.set_xlabel('Maxrad')
                axs_circulo_Maxrad.set_ylabel('Quantidade de circulos identificadas')
                axs_circulo_Maxrad.legend(loc='upper right')
           


            # Ajustar o layout para que os gráficos não se sobreponham
            plt.tight_layout()
   
        fig_1.canvas.mpl_connect('key_press_event', on_key)
        plt.show()


if __name__ == "__main__":
    main()
