import numpy as np
import argparse
from queue import Queue

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--Input", help = "Path Input File") 
parser.add_argument("-r", "--representacao", help = "Representacao das arestas em lista de adjacencia(1) ou matriz de adjacencia(2) ou Vetor de Adjacencia(3) ")
parser.add_argument("-o", "--Output", help = "Path Output File") 
args = parser.parse_args()


## Processar Arquivo Entrada
'''
Sua biblioteca deve ser capaz de ler um grafo de um arquivo texto. O formato do
grafo no arquivo sera o seguinte. 
A primeira linha informa o numero de vertices do grafo.
Cada linha subsequente informa as arestas. Um exemplo de um grafo e seu respectivo arquivo
'''
f = open(args.Input, "r")
nvertices=f.readline() # primeira linha
narestas=0
while(1):
    line = f.readline()
    if (line != ''):
        line=line.replace('\n',"")
        line=line.replace('\r',"")
        aresta=line.split(" ", 1)
        aresta=[int(aresta[0]),int(aresta[1])]
        narestas+=1
        print(aresta)
    else:   
        break
f.close()   

## Processar arquivo Saida
'''
Saıda. Sua biblioteca deve ser capaz de gerar um arquivo texto com as seguintes informacoes
sobre o grafo: numero de vertices, numero de arestas, grau minimo, grau maximo, grau medio,
e mediana de grau. Alem disso, imprimir informacoes sobre as componentes conexas (ver
abaixo).
'''
# Arquivo
f = open(args.Output, "wr")
f.write(str(nvertices))
f.write(str(narestas))
f.close()

# Cli OUTPUT
print("Numero de Vertices: "+str(nvertices))
print("Numero de arestas: "+str(narestas))
print("Grau Maximo: "+str(matriz.calcula_maior_grau))
print("Grau Minimo: "+str(matriz.calcula_menor_grau))
print("Grau Medio: "+str(matriz.calcula_media_grau))
print("Grau mediana: "+str(matriz.calcula_mediana_grau))    
#

class grafo_matriz_adjacencia():
    def __init__(self,arestas,numero_vertices):
        self.numero_vertices = numero_vertices
        self.matriz = np.zeros(numero_vertices, numero_vertices)
        self.lista_graus = np.zeros(numero_vertices)
        for aresta in arestas:
            if (self.matriz[aresta[0]][aresta[1]] == 1 or self.matriz[aresta[1]][aresta[0]] == 1):
                print("Aresta "+str(aresta)+"já existe no grafo")
                return 1
            self.matriz[aresta[0]][aresta[1]] = 1
            self.matriz[aresta[1]][aresta[0]] = 1
            
            self.lista_graus[aresta[1]]+= 1
            self.lista_graus[aresta[0]]+= 1

        return 0

    def calcula_grau_vertice(self,vertice):
        grau = np.sum(self.matriz[vertice])
        return grau
        
    def calcula_maior_grau(self):
        return max(self.lista_graus)

    def calcula_menor_grau(self):
        return min(self.lista_graus)

    def gera_arvore_largura(self, vertice_raiz):  
        vetor_nivel_arvore = np.zeros(self.numero_vertices)
        vetor_pai_vertice = np.zeros(self.numero_vertices)
        vetor_pai_vertice[vertice_raiz] = np.void
        def funcao_auxiliar(vertice_filho, vertice_pai):
            vetor_pai_vertice[vertice_filho] = vertice_pai
            vetor_nivel_arvore[vertice_filho] = vetor_nivel_arvore[vertice_pai] + 1
            return 0
        self.busca_largura( vertice_raiz, funcao_auxiliar)
        return vetor_pai_vertice, vetor_nivel_arvore

    def busca_largura(self, vertice_raiz, funcao_auxiliar = lambda x:0):
        vetor_explorados = np.zeros(self.numero_vertices)#vetor nivel do vertice    
        fila = Queue(maxsize=self.numero_vertices)
        fila.put(vertice_raiz)
        
        while not fila.empty():
            vertice_sendo_explorado = fila.get()
            for vertice_adjacente in range(self.numero_vertices):
                if self.matriz[vertice_sendo_explorado][vertice_adjacente] == 1 and vetor_explorados[vertice_adjacente] == 0:
                        funcao_auxiliar(vertice_adjacente,vertice_sendo_explorado)
                        vetor_explorados[vertice_adjacente] == 1
                        fila.put(vertice_adjacente)                          

        #retorna árvore no arquivo de saída
        return 0

    def busca_profundidade(self,vertice):
        #retorna árvore no arquivo de saída
        return 0

    def calcula_distancia_vertices(self,vertice1,vertice2):
        return 0

    def calcula_diametro_grafo(self):
        #chama distancia_vertices
        return 0
    def descobre_componentes_conexas(self):
        #chama BFS
        return 0 # lista ordenada de componentes

class grafo_lista_adjacencia():
    def __init__(self,arestas):
        return 0

    def busca_largura(self,vertice):
        #retorna árvore no arquivo de saída
        return 0

    def busca_profundidade(self,vertice):
        #retorna árvore no arquivo de saída
        return 0
    def distancia_vertices(self,vertice1,vertice2):
        return 0

    def diametro(self):
        return 0
    
    def componentes_conexas(self):
        #chama BFS
        return 0 # lista ordenada de componentes