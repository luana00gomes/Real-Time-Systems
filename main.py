import random
import string
import pandas as pd
import numpy as np


# taskSet2 = []
# taskSet3 = []
# taskSet4 = []
# taskSet5 = []
# taskSet6 = []
# taskSet7 = []
# taskSet8 = []
# taskSet9 = []

def gera_tarefas(utilidade_sistema, p_min, p_max, util_min, util_max, combinacao):
     soma = 0
     name_coluna = 'conjunto' + str(0)
     coluna_dumm = []
     for t in range(250):
          coluna_dumm.append(0)
     file = pd.DataFrame()
     file['coluna0'] = pd.Series(coluna_dumm)
     for i in range(101):
          taskSet1 = []
          while soma <= utilidade_sistema:
               t = random.uniform(p_min, p_max)
               u = random.uniform(util_min, util_max)
               c = t * u
               task = t, u, c
               taskSet1.append(task)
               soma = u + soma
          file[name_coluna] = pd.Series(taskSet1)
          soma = 0
          name_coluna = 'conjunto' + str(i)
     name_arquivo = str(utilidade_sistema) + combinacao + ".csv"
     file.to_csv('arquivos/'+name_arquivo, index=False)

def gera_arquivos( p_min, p_max, util_min, util_max,combinaçao):
     for i in range(1,11):
          numero = i / 10
          if (i == 10):
               numero = int(numero)
          p_min = p_min*pow(10,-3)
          p_max = p_max*pow(10,-3)
          gera_tarefas(numero,p_min, p_max, util_min, util_max,combinaçao)

gera_arquivos(3, 33, 0.0001, 0.01,'LL')
gera_arquivos(3, 33, 0.001, 0.09,'LM')
gera_arquivos(3, 33, 0.09, 0.1,'LH')
gera_arquivos(10, 100, 0.0001, 0.01,'ML')
gera_arquivos(10, 100, 0.001, 0.09,'MM')
gera_arquivos(10, 100, 0.09, 0.1,'MH')
gera_arquivos(50, 250, 0.0001, 0.01,'HL')
gera_arquivos(50, 250, 0.001, 0.09,'HM')
gera_arquivos(50, 250, 0.09, 0.1,'HH')