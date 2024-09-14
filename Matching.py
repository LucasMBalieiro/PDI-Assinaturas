TAXARHO = 0.20
TAXATHETA = 0.20
TAXAX = 70
TAXAY = 70
TAXAR = 70




def matching(params_base_linha, params_base_circulo, params_alvo_linha, params_alvo_circulo):
       
    taxa_matches = {'linhas':{}, 'circulos':{}}


    for tipo in params_base_linha:
        taxa_matches['linhas'][tipo] = {}
        taxa_matches['circulos'][tipo] = {}
        for imagem_base in params_base_linha[tipo]:
                taxa_matches['linhas'][tipo][imagem_base] = {}
                taxa_matches['circulos'][tipo][imagem_base] = {}


                for imagem_alvo in params_alvo_linha[tipo]:
                    taxa_matches['linhas'][tipo][imagem_base][imagem_alvo] = matching_linhas(params_base_linha[tipo][imagem_base],params_alvo_linha[tipo][imagem_alvo])
                    taxa_matches['circulos'][tipo][imagem_base][imagem_alvo] = matching_circulos(params_base_circulo[tipo][imagem_base],params_alvo_circulo[tipo][imagem_alvo])


    #print(taxa_matches)


    return taxa_matches            
       


def matching_linhas(linhas_base, linhas_alvo):
    #print ('matching sendo realizdo')


   
    taxa = []    
    for linha_alvo in linhas_alvo[0]:
        if linha_alvo is not None:
            resultado = 0
            for targetline in linha_alvo:
                qtd_linhas = len(linha_alvo)
                rho_alvo, theta_alvo = targetline[0]
                contador_match = 0
                for linha_base in linhas_base[0]:
                    if linha_base is not None:
                        for baseline in linha_base:
                            rho_base, theta_base = baseline[0]
                            erro_rho = TAXARHO*rho_base
                            erro_theta = TAXATHETA*theta_base
                           
                            if ((rho_base - erro_rho <= rho_alvo and rho_alvo <= rho_base + erro_rho) and
                                (theta_base - erro_theta <= theta_alvo and theta_alvo <= theta_base + erro_theta)):
                               
                                    contador_match += 1


                if contador_match > 0:
                    resultado += 1
           
            taxa.append(round(resultado/qtd_linhas, 4))


    output_sum = 0
    for i in taxa:
        output_sum += i
    try:
         return round(output_sum/len(taxa),4)
    except:
        return 0


def matching_circulos(circulos_base, circulos_alvo):
    #print ('matching sendo realizdo')


   
    taxa = []    
    for circulo_alvo in circulos_alvo[0]:
        if circulo_alvo is not None:
            resultado = 0
            for targetcircle in circulo_alvo:
                qtd_circulos = len(circulo_alvo)
                x_alvo, y_alvo, r_alvo = targetcircle
                contador_match = 0
                for circulo_base in circulos_base[0]:
                    if circulo_base is not None:
                        for basecircle in circulo_base:
                            x_base, y_base, r_base = basecircle
                            erro_x = TAXAX
                            erro_y = TAXAY
                            erro_r = TAXAR
                           
                            if ((x_base - erro_x <= x_alvo and x_alvo <= x_base + erro_x) and
                                (y_base - erro_y <= y_alvo and y_alvo <= y_base + erro_y) and
                                (r_base - erro_r <= r_alvo and r_alvo <= r_base + erro_r)
                                ):
                               
                                    contador_match += 1


                if contador_match > 0:
                    resultado += 1
           
            taxa.append(round(resultado/qtd_circulos, 4))


    output_sum = 0
    for i in taxa:
        output_sum += i
    try:
         return round(output_sum/len(taxa), 4)
    except:
        return 0


if __name__ == "__main__":
    matching()
