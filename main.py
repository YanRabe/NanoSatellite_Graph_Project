from csv_handler import avg, low, high
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

## Visualiser

# viz = plt.figure().add_subplot(projection='3d')
# viz.plot(avg[:, 0], avg[:, 1], avg[:, 2], 'ro')
# plt.title("Représentation de l'essaim dans la configuration moyenne")

# viz = plt.figure().add_subplot(projection='3d')
# viz.plot(low[:, 0], low[:, 1], low[:, 2], 'bo')
# plt.title("Représentation de l'essaim dans la configuration faible")

# viz = plt.figure().add_subplot(projection='3d')
# viz.plot(high[:, 0], high[:, 1], high[:, 2], 'yo')
# plt.title("Représentation de l'essaim dans la configuration forte")

# plt.show()

### études des graphes

essaim = nx.Graph()

# 1 - pour chaque satellite : créer un noeud
for i,cord in enumerate(avg):
    essaim.add_node(i,coord=cord)


PORTEE = 20000 #portée des satellite
NOMBRE_SAT = 100 #nombre de satellite


# fonction pour calculer la distance entre deux points
def calc_distance(x1,y1,z1,x2,y2,z2):
    p1 = np.array([x1,y1,z1])
    p2 = np.array([x2,y2,z2])
    return np.linalg.norm(p1 - p2)

# 2 - pour chaque satellite, calculer sa distance à tous les autres, ajouter un edge si distance < portée
mat_distance = np.zeros((NOMBRE_SAT,NOMBRE_SAT))
for i,c1 in enumerate(avg):
    for j,c2 in enumerate(avg):
        # c1 = essaim.nodes[i]["pos"]
        # c2 = essaim.nodes[j]["pos"]
        mat_distance[i][j] = calc_distance(c1[0],c1[1],c1[2],c2[0],c2[1],c2[2])
        if mat_distance[i][j] < PORTEE :
            essaim.add_edge(i,j)

# DEGREE_MOYEN

deg_moyen = 0
for i in essaim.nodes:
    deg_moyen += essaim.degree(i)

deg_moyen = deg_moyen / essaim.number_of_nodes()
DEGREE_MOYEN = deg_moyen

# REPARTITION
essaim_degree = np.zeros((1))
for i in essaim.nodes:
    essaim_degree = np.append(essaim_degree,essaim.degree(i))

res = plt.hist(essaim_degree)
plt.xlabel("satellites")
plt.ylabel("degrés")
plt.title("Distribution du degree par satellite")
# plt.show()


#DEGREE DE CLUSTERING
# CLUSTERING MOYEN
clustering_moyen = nx.average_clustering(essaim)
CLUSTERING_MOYEN = clustering_moyen
print("Clustering moyen :", clustering_moyen)


# DISTRIBUTION
clustering_nodes = nx.clustering(essaim)
clustering_values = np.array(list(clustering_nodes.values()))
plt.figure()
plt.hist(clustering_values, bins=20)
plt.xlabel("Coefficient de clustering")
plt.ylabel("Nombre de satellites")
plt.title("Distribution du coefficient de clustering")
# plt.show()


#CLIQUE
clique_by_node = nx.find_cliques(essaim)
NOMBRE_CLIQUE = len(list(clique_by_node))
print("Nombre de clique : " +str(NOMBRE_CLIQUE))


#COMPOSANTS CONNEXE
composant_connexe = nx.connected_components(essaim)
NOMBRE_CONNEXE = len(list(composant_connexe))
print("nombre connexe : " + str(NOMBRE_CONNEXE))