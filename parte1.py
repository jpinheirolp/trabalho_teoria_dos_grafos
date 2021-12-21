import numpy as np
import argparse
import statistics
from queue import Queue

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile", help = "Path Input File") 
parser.add_argument("-k", "--kind", help = "Representacao das arestas em  matriz de adjacencia(1) ou lista de adjacencia(2) ")
parser.add_argument("-o", "--outputfile", help = "Path Output File") 
args = parser.parse_args()


## Processar Arquivo Entrada
'''
Sua biblioteca deve ser capaz de ler um grafo de um arquivo texto. O formato do
grafo no arquivo sera o seguinte. 
A primeira linha informa o numero de vertices do grafo.
Cada linha subsequente informa as arestas. Um exemplo de um grafo e seu respectivo arquivo
'''
def processarArquivoEntrada(arquivoentrada):
    f = open(arquivoentrada, "r")
    nvertices=f.readline() # primeira linha
    arestas=[]
    while(1):
        line = f.readline()
        if (line != ''):
            line=line.replace('\n',"")
            line=line.replace('\r',"")
            aresta=line.split(" ", 1)
            aresta=[int(aresta[0])-1,int(aresta[1])-1]
            arestas.append(aresta)
        else:
            break
    f.close()
    return arestas,int(nvertices)
## Processar arquivo Saida
'''
Saıda. Sua biblioteca deve ser capaz de gerar um arquivo texto com as seguintes informacoes
sobre o grafo: numero de vertices, numero de arestas, grau minimo, grau maximo, grau medio,
e mediana de grau. Alem disso, imprimir informacoes sobre as componentes conexas (ver
abaixo).
'''
# def processarArquivoSaida(arquivosaida):
#     f = open(arquivosaida, "wr")
#     f.write(str(nvertices))
#     f.write(str(narestas))
#     f.close()

# Cli OUTPUT
# print("Numero de Vertices: "+str(nvertices))
# print("Numero de arestas: "+str(narestas))
# print("Grau Maximo: " +str(matriz.calcula_maior_grau))
# print("Grau Minimo: " +str(matriz.calcula_menor_grau))
# print("Grau Medio:  " +str(matriz.calcula_media_grau))
# print("Mediana de Grau : "+str(matriz.calcula_mediana_grau))    
#

class grafo_generico():
    def __init__(self,arestas,numero_vertices):
        self.vetor_nome_vertices = np.zeros(numero_vertices)   
        self.numero_vertices = numero_vertices
        self.lista_graus = np.zeros(numero_vertices)
        

    def adjacencia_vertices(self,vertice1,vertice2):
        return True
        
    def calcula_maior_grau(self):
        return max(self.lista_graus)

    def calcula_menor_grau(self):
        return min(self.lista_graus)

    def calcula_media_grau(self):
        return statistics.mean(self.lista_graus)

    def calcula_mediana_grau(self):
        return statistics.median(self.lista_graus)

    def gera_arvore_largura(self, vertice_raiz):  
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.full(self.numero_vertices,None)
        vetor_pai_vertice[vertice_raiz] = None
        def funcao_auxiliar(vertice_filho, vertice_pai):
            vetor_pai_vertice[vertice_filho] = vertice_pai
            vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
            return None
        self.busca_largura( vertice_raiz, funcao_auxiliar)
        # onde tiver 0 e nao for raiz = none em vetor nivel arvore
        for vertice in range(self.numero_vertices):
            if vetor_nivel_arvore[vertice] == 0 and vertice != vertice_raiz:
                vetor_nivel_arvore[vertice] = None
        return list(vetor_pai_vertice), list(vetor_nivel_arvore)

    def busca_largura(self, vertice_raiz, funcao_auxiliar = lambda x,y:0, condicao_parada = False):
        vetor_explorados = np.zeros(self.numero_vertices)#vetor nivel do vertice    
        vetor_explorados[vertice_raiz] = 1
        fila = Queue(maxsize=self.numero_vertices)
        fila.put(vertice_raiz)
        retorno_func_auxiliar = None
        while (not fila.empty()) and ((retorno_func_auxiliar == None) or (not condicao_parada)):
            vertice_sendo_explorado = fila.get()
            for vertice_adjacente in range(self.numero_vertices):
                if self.adjacencia_vertices(vertice_sendo_explorado,vertice_adjacente) == 1 and vetor_explorados[vertice_adjacente] == 0:
                        retorno_func_auxiliar = funcao_auxiliar(vertice_adjacente,vertice_sendo_explorado)
                        vetor_explorados[vertice_adjacente] = 1
                        fila.put(vertice_adjacente)                          
                if retorno_func_auxiliar != None and condicao_parada:
                    break

        return retorno_func_auxiliar
        
    def busca_profundidade(self,vertice_raiz):
        #retorna árvore no arquivo de saída
        return 0

    def calcula_distancia_vertices(self,vertice1,vertice2):
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.full(self.numero_vertices,None)
        def funcao_auxiliar(vertice_filho, vertice_pai):
            vetor_pai_vertice[vertice_filho] = vertice_pai
            vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
            if vertice_filho == vertice2:
                return vetor_nivel_arvore[vertice_filho]
            return None

        distancia = self.busca_largura(vertice1, funcao_auxiliar,True)
        return distancia
        

    def calcula_diametro_grafo(self):
        diametro = [0]
        for vertice_raiz in range(self.numero_vertices):
            vetor_nivel_arvore = np.zeros(self.numero_vertices)
            vetor_pai_vertice = np.full(self.numero_vertices,None)
            
            def funcao_auxiliar(vertice_filho, vertice_pai):
                vetor_pai_vertice[vertice_filho] = vertice_pai
                vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
                diametro[0] = max(vetor_nivel_arvore[vertice_filho],diametro[0])
                return None
            self.busca_largura(vertice_raiz, funcao_auxiliar,False)

        return diametro[0]
        
    def descobre_componentes_conexas(self):
        '''
        Componentes conexos. Sua biblioteca deve ser capaz descobrir as componentes conexas
        de um grafo. O numero de componentes conexos, assim como o tamanho (em vertices) de
        cada componente e a lista de vertices pertencentes a componente. Os componentes devem
        estar listados em ordem decrescente de tamanho (listar primeiro o componente com o maior
        numero de vertices, etc).
        '''
        vertices_conhecidos = np.zeros(self.numero_vertices)
        lista_componentes = [[-1]] # o '-1' e so pra corrigir o problema do ultimo for n rodar por a lista estar vazia
        componente_conexa = [0]
        def funcao_auxiliar(vertice_filho,vertice_pai):
            componente_conexa[0] += 1
            componente_conexa.append(vertice_filho)
            vertices_conhecidos[vertice_filho] = 1
            return None
        for vertice_raiz in range(self.numero_vertices):
            if vertices_conhecidos[vertice_raiz] == 0:
                self.busca_largura(vertice_raiz,funcao_auxiliar)
                componente_conexa[0] += 1  #acrescentando e contabilizando a raiz que faltava  
                componente_conexa.append(vertice_raiz)

                for index in range(len(lista_componentes)):
                    if componente_conexa[0] >= lista_componentes[index][0]:
                        lista_componentes.insert(index,componente_conexa)
                        break
                componente_conexa = [0]

        lista_componentes.pop() # remove 0 '[-1]' pois ele sempre sera o ultimo elemento
        return lista_componentes 


class grafo_matriz_adjacencia():
    def __init__(self,arestas,numero_vertices):
        self.vetor_nome_vertices = np.zeros(numero_vertices)   
        self.numero_vertices = numero_vertices
        self.matriz = np.zeros([numero_vertices, numero_vertices])
        self.lista_graus = np.zeros(numero_vertices)
        for aresta in arestas:
            if (self.matriz[aresta[0]][aresta[1]] == 1 or self.matriz[aresta[1]][aresta[0]] == 1):
                print("Aresta "+str(aresta)+"já existe no grafo")
                return 1
            self.matriz[aresta[0]][aresta[1]] = 1
            self.matriz[aresta[1]][aresta[0]] = 1
            
            self.lista_graus[aresta[1]]+= 1
            self.lista_graus[aresta[0]]+= 1

    def adjacencia_vertices(self,vertice1,vertice2):
        return self.matriz[vertice1][vertice2] == 1

    def calcula_grau_vertice(self,vertice):
        grau = np.sum(self.matriz[vertice])
        return grau
        
    def calcula_maior_grau(self):
        return max(self.lista_graus)

    def calcula_menor_grau(self):
        return min(self.lista_graus)

    def calcula_media_grau(self):
        return statistics.mean(self.lista_graus)

    def calcula_mediana_grau(self):
        return statistics.median(self.lista_graus)

    def gera_arvore_largura(self, vertice_raiz):  
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.full(self.numero_vertices,None)
        vetor_pai_vertice[vertice_raiz] = None
        def funcao_auxiliar(vertice_filho, vertice_pai):
            vetor_pai_vertice[vertice_filho] = vertice_pai
            vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
            return None
        self.busca_largura( vertice_raiz, funcao_auxiliar)
        # onde tiver 0 e nao for raiz = none em vetor nivel arvore
        for vertice in range(self.numero_vertices):
            if vetor_nivel_arvore[vertice] == 0 and vertice != vertice_raiz:
                vetor_nivel_arvore[vertice] = None
        return list(vetor_pai_vertice), list(vetor_nivel_arvore)

    def busca_largura(self, vertice_raiz, funcao_auxiliar = lambda x,y:0, condicao_parada = False):
        vetor_explorados = np.zeros(self.numero_vertices)#vetor nivel do vertice    
        vetor_explorados[vertice_raiz] = 1
        fila = Queue(maxsize=self.numero_vertices)
        fila.put(vertice_raiz)
        retorno_func_auxiliar = None
        while (not fila.empty()) and ((retorno_func_auxiliar == None) or (not condicao_parada)):
            vertice_sendo_explorado = fila.get()
            for vertice_adjacente in range(self.numero_vertices):
                if self.adjacencia_vertices(vertice_sendo_explorado,vertice_adjacente) == 1 and vetor_explorados[vertice_adjacente] == 0:
                        retorno_func_auxiliar = funcao_auxiliar(vertice_adjacente,vertice_sendo_explorado)
                        vetor_explorados[vertice_adjacente] = 1
                        fila.put(vertice_adjacente)                          
                if retorno_func_auxiliar != None and condicao_parada:
                    break

        return retorno_func_auxiliar
        
    def busca_profundidade(self,vertice_raiz):
        #retorna árvore no arquivo de saída
        return 0

    def calcula_distancia_vertices(self,vertice1,vertice2):
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.full(self.numero_vertices,None)
        def funcao_auxiliar(vertice_filho, vertice_pai):
            vetor_pai_vertice[vertice_filho] = vertice_pai
            vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
            if vertice_filho == vertice2:
                return vetor_nivel_arvore[vertice_filho]
            return None

        distancia = self.busca_largura(vertice1, funcao_auxiliar,True)
        return distancia
        

    def calcula_diametro_grafo(self):
        diametro = [0]
        for vertice_raiz in range(self.numero_vertices):
            vetor_nivel_arvore = np.zeros(self.numero_vertices)
            vetor_pai_vertice = np.full(self.numero_vertices,None)
            
            def funcao_auxiliar(vertice_filho, vertice_pai):
                vetor_pai_vertice[vertice_filho] = vertice_pai
                vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
                diametro[0] = max(vetor_nivel_arvore[vertice_filho],diametro[0])
                return None
            self.busca_largura(vertice_raiz, funcao_auxiliar,False)

        return diametro[0]
        
    def descobre_componentes_conexas(self):
        '''
        Componentes conexos. Sua biblioteca deve ser capaz descobrir as componentes conexas
        de um grafo. O numero de componentes conexos, assim como o tamanho (em vertices) de
        cada componente e a lista de vertices pertencentes a componente. Os componentes devem
        estar listados em ordem decrescente de tamanho (listar primeiro o componente com o maior
        numero de vertices, etc).
        '''
        vertices_conhecidos = np.zeros(self.numero_vertices)
        lista_componentes = [[-1]] # o '-1' e so pra corrigir o problema do ultimo for n rodar por a lista estar vazia
        componente_conexa = [0]
        def funcao_auxiliar(vertice_filho,vertice_pai):
            componente_conexa[0] += 1
            componente_conexa.append(vertice_filho)
            vertices_conhecidos[vertice_filho] = 1
            return None
        for vertice_raiz in range(self.numero_vertices):
            if vertices_conhecidos[vertice_raiz] == 0:
                self.busca_largura(vertice_raiz,funcao_auxiliar)
                componente_conexa[0] += 1  #acrescentando e contabilizando a raiz que faltava  
                componente_conexa.append(vertice_raiz)

                for index in range(len(lista_componentes)):
                    if componente_conexa[0] >= lista_componentes[index][0]:
                        lista_componentes.insert(index,componente_conexa)
                        break
                componente_conexa = [0]

        lista_componentes.pop() # remove 0 '[-1]' pois ele sempre sera o ultimo elemento
        return lista_componentes 

class grafo_lista_adjacencia(grafo_generico): 
    def __init__(self,arestas,numero_vertices):
        self.vetor_nome_vertices = np.zeros(numero_vertices)   
        self.numero_vertices = numero_vertices
        self.lista_adjacencias = []
        for lista in range(self.numero_vertices):self.lista_adjacencias.append([])
        self.lista_graus = np.zeros(numero_vertices)
        for aresta in arestas:
            if aresta[0] == aresta[1]:
                print("aresta não pode ir de um grafo para ele mesmo")
            if (aresta[1] in self.lista_adjacencias[aresta[0]] or aresta[0] in self.lista_adjacencias[aresta[1]]):
                print("Aresta "+str(aresta)+"já existe no grafo")
                return 1
            self.lista_adjacencias[aresta[0]].append(aresta[1])
            self.lista_adjacencias[aresta[1]].append(aresta[0])
            
            self.lista_graus[aresta[1]]+= 1
            self.lista_graus[aresta[0]]+= 1

    def adjacencia_vertices(self,vertice1,vertice2):
        return vertice2 in self.lista_adjacencias[vertice1]
    

### Debug
arg1,arg2 = processarArquivoEntrada(args.inputfile)
matrizteste=grafo_matriz_adjacencia(arg1,arg2)
listateste = grafo_lista_adjacencia(arg1,arg2)
# # print(matrizteste.matriz)
# print(matrizteste.gera_arvore_largura(3))
# print(matrizteste.calcula_distancia_vertices(1,5))
#print(matrizteste.calcula_diametro_grafo())
print(listateste.calcula_diametro_grafo())
print(matrizteste.descobre_componentes_conexas())
# print(matrizteste.calcula_maior_grau())
# print(matrizteste.calcula_menor_grau())
# print(matrizteste.calcula_mediana_grau())
# print(matrizteste.calcula_media_grau())
