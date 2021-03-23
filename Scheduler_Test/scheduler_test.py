import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from scipy.interpolate import interp1d
############################################
#Separação de dados para realizar os testes#
############################################

#Função que separa a a utilidade dos arquivos
#Recebe uma coluna do arquivo e a quantidade de dados  não nulos da coluna
#Retorna uma lista de cojunto de utilidades que somadas resultam em uma utilidade do sistema
def Seleciona_conjunto(coluna,qtd):
    conjunto = []
    for ind in range(qtd): #itera na coluna e separa a utilidades para uma lista de dados
        aux = coluna[ind]
        valor = ""
        #por ter três valores de dados o pandas reconhceu como string fazndo necessário uma manipulação
        i = aux.find(',') + 1
        while aux[i] != ',':
            valor = valor + aux[i]
            i = i + 1
        conjunto.append(float(valor))
    return conjunto

#Função que cria uma matriz com os dados de uma coluna
#A posição 0 comtém o período, a 1 a utilidade e a 2 o tempo de execução
#Recebe uma coluna do arquivo e a quantidade de dados  não nulos da coluna
#Retorna a Matriz de Valores
def Seleciona_conjunto_RTA(coluna,qtd):
    conjunto = np.zeros([qtd,3])
    for ind in range(qtd):
        aux = coluna[ind]
        valor = ""
        i = 1
        while aux[i] != ',':
             valor = valor + aux[i]
             i = i + 1
        conjunto[ind][0] = float(valor)
        i = i + 1
        valor = ""
        while aux[i] != ',':
            valor = valor + aux[i]
            #print(aux[i])
            i = i + 1
        conjunto[ind][1] = float(valor)
        i = i + 1
        valor = ""
        while aux[i] != ')':
            valor = valor + aux[i]
            #print(aux[i])
            i = i + 1
        conjunto[ind][2] = float(valor)
   # print(conjunto)
    return conjunto

############################################
#          Teste Suficiente                #
############################################

#Calcula a utilização máxima pelo RM
def calcUB(num_tasks):
    return num_tasks*(2**(1/num_tasks)-1)

#Função para calcular o teste suficiente das utilidades de sistema de
def teste_suficiente(file_name):
    Retorno_suficiente = []
    file_utilidade = pd.read_csv('arquivos/'+file_name)
    for i in range(len(file_utilidade.columns)-1):
        coluna_name = 'conjunto' + str(i)
        qtd_dados = file_utilidade[coluna_name].count()
        coluna = file_utilidade[coluna_name]
        conjunto = Seleciona_conjunto(coluna, qtd_dados)
        soma = 0
        for i in range(len(conjunto)):
            soma = soma + conjunto[i]
       # print(soma)
       # print(calcUB(qtd_dados))
        if(soma <= calcUB(qtd_dados)):
            Retorno_suficiente.append(1)
           # print("passou")

        else:
            Retorno_suficiente.append(0)
          #  print("falhou")
    return Retorno_suficiente

############################################
#          Teste Hyperbolic Bound          #
############################################
def teste_hyperbolic_bound(file_name):
    Retorno_HB = []
    file_utilidade = pd.read_csv('arquivos/'+file_name)
    for i in range(len(file_utilidade.columns)-1):
        coluna_name = 'conjunto' + str(i)
        qtd_dados = file_utilidade[ coluna_name].count()
        coluna = file_utilidade[coluna_name]
        conjunto = Seleciona_conjunto(coluna, qtd_dados)
        produto = 1
        for i in range(len(conjunto)):
            #print(conjunto[i] + 1)
            produto = produto*(conjunto[i] +1)
           # print(produto)
        if(produto <= 2):
            Retorno_HB.append(1)
           # print("passou")

        else:
            Retorno_HB.append(0)
           # print("falhou")
    return Retorno_HB

def rate_monotonic(lista):
    lista_ordenada = sorted(lista, key=lambda periodo: periodo[0])
    return lista_ordenada


def teste_RTA(file_name):
    file_utilidade = pd.read_csv('arquivos/'+file_name)
    Resultado = []
    for k in range(len(file_utilidade.columns)-1):
      #  print('primeiro for')
        coluna_name = 'conjunto' + str(k)
        qtd_dados = file_utilidade[coluna_name].count()
        coluna = file_utilidade[coluna_name]
        conjunto = Seleciona_conjunto_RTA(coluna, qtd_dados)
        r = np.zeros(len(conjunto))  # matriz para tempos de resposta
        tasks = rate_monotonic(conjunto)
        verifica = 0
       # print(conjunto)
        for i in range(0, len(tasks)):  # para cada tarefa, avalia-se o tempo de resposta
            # tempo de resposta inicial
            # r[i] = tasks [:, :, i]
            r[i] = tasks[i][2]
            j = i
            while j > 0:  # enquanto houver tarefas de maior prioridade
                # r[i]=r[i]+tasks[:, :, j]
                j = j - 1
                r[i] = r[i] + tasks[j][2]


            # tempo de resposta na k-esima interação
            r_k = 0
            r_aux = 0
            cont = 0
            while r[i] != r_k:  # enquanto não convergir
                if (r[i] > tasks[i][0] or cont>100):

                    Resultado.append(0)
                    verifica = 1
                    break;
                j = i
                r_k = r[i]  # Tempo de resposta da interação anterior
                r[i] = tasks[i][2]
                while j > 0:  # enquanto houver tarefas de maior prioridade
                    j = j - 1

                    r_aux = math.ceil(r_k / tasks[j][0]) * (tasks[j][2]) # ceil faz arredondamento para cima
                    r[i] = r[i]+r_aux
                cont=cont+1



        for i in range(0, len(tasks)):  # para cada tarefa, avalia-se a escanolabilidade
            if r[i] > tasks[i][0] and verifica == 0:
                print("Errado")
                Resultado.append(0)
                verifica = 1
                break;

        if( verifica == 0):
            Resultado.append(1)



    return Resultado



############################################
#    Calculo da porcentagem  e gráficos    #
############################################
def calcula_porcentagem(Retorno_testes):
    soma_passaram = 0
    for i in range(len(Retorno_testes)):
        if(Retorno_testes[i] == 1):
            soma_passaram = soma_passaram + 1
    porcetagem_passaram = (soma_passaram/len(Retorno_testes))*100
    return porcetagem_passaram

#Função que calcula todas a porcetagens de todos os testes
def cria_lista_resutados(tipo_teste, combinacao):
    Resultados = []
    for i in range(1, 11):
        numero = i/10
        if(i == 10):
            numero = int(numero)
        nome_file = str(numero) + combinacao +'.csv'
        if(tipo_teste == 'suficiente'):
            Resultados.append(calcula_porcentagem(teste_suficiente(nome_file)))
        if(tipo_teste == 'HB'):
            Resultados.append(calcula_porcentagem(teste_hyperbolic_bound(nome_file)))
        if(tipo_teste == 'RTA'):
            Resultados.append(calcula_porcentagem(teste_RTA(nome_file)))
    print(Resultados)
    return Resultados

def plota_graficos(resutado_suficiente, resultado_HB, resultado_RTA,combincao):
        utilizacoes = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    #utilizacoes = np.array(range(len(resutado_suficiente)))
        plt.plot(utilizacoes,resutado_suficiente, label= 'Suficiente')
        plt.plot(utilizacoes,resultado_HB,  label= 'Hyperbolic Bound')
        plt.plot(utilizacoes, resultado_RTA,  label= 'RTA')
        label_x = 'Utilização do sistema ' + combincao
        plt.xlabel(label_x)
        plt.ylabel('% de sistemas que passaram nos testes')
        plt.title('Comparação Testes de escalonabilidade')
        plt.legend()
        plt.show()

#cria_lista_resutados("suficiente")
#cria_lista_resutados("HB")
plota_graficos(cria_lista_resutados("HB",'HH'), cria_lista_resutados("suficiente","HH"), cria_lista_resutados("RTA", "HH"), 'HH')
plota_graficos(cria_lista_resutados("HB",'HM'), cria_lista_resutados("suficiente","HM"), cria_lista_resutados("RTA", "HM"), "HM")
plota_graficos(cria_lista_resutados("HB",'HL'), cria_lista_resutados("suficiente","HL"), cria_lista_resutados("RTA", "HL"), 'HL' )
plota_graficos(cria_lista_resutados("HB",'LH'), cria_lista_resutados("suficiente","LH"), cria_lista_resutados("RTA", "LH"), 'LH')
plota_graficos(cria_lista_resutados("HB",'LM'), cria_lista_resutados("suficiente","LM"), cria_lista_resutados("RTA", "LM"), 'LM')
plota_graficos(cria_lista_resutados("HB",'LL'), cria_lista_resutados("suficiente","LL"), cria_lista_resutados("RTA", "LL"), 'LL')
plota_graficos(cria_lista_resutados("HB",'ML'), cria_lista_resutados("suficiente","ML"), cria_lista_resutados("RTA", "ML"), 'ML')
plota_graficos(cria_lista_resutados("HB",'MM'), cria_lista_resutados("suficiente","MM"), cria_lista_resutados("RTA", "MM"), 'MM')
plota_graficos(cria_lista_resutados("HB",'MH'), cria_lista_resutados("suficiente","MH"), cria_lista_resutados("RTA", "MH"), 'MH')

