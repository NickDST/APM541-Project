import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import imageio ## this one is only necessary for creating GIFs


### loading in the graph data and parsing it
with open("data/graph_social.txt","r") as details:
            payload=[]
            for line in details:
                edge = line.strip()
                edge = edge.split()
                payload.append((int(edge[0]), int(edge[1])))    #put the entire file into a list line by line 

## creating the graph and adding edges and nodes
G = nx.Graph()
for e in payload:
    G.add_edge(*e)


## helper function to convert 1 2 3 to colors for creating GIFs
def getcolormap(colors):
    cm = []
    size = []
    for color in colors:
        if(color == 0):
            cm.append("blue")
            size.append(0.5)
        elif(color == 1):
            cm.append("red")
            size.append(3)
        else:
            cm.append("limegreen")
            size.append(3)
    return cm, size

def sel_neighbor(site):
    adj = list(G.adj[site])
    pick_neighbor_idx = np.random.randint(len(adj))
    y = adj[pick_neighbor_idx]
    return y


## initial conditions
initial_count = 1
## grabbing the most and least connected
neighbor_count = []
for i in range(len(G.nodes)):
    neighbor_count.append({"node" : i , "count": len(G.adj[i]) })
        
ndf = pd.DataFrame(neighbor_count)

tdf = ndf.sort_values(by=['count'], ascending = False)
ldf = ndf.sort_values(by=['count'], ascending = True)

top_connected = list(tdf.iloc[:initial_count]["node"])
least_connected = list(ldf.iloc[:initial_count]["node"])



## The process

colors = np.zeros((len(G.nodes)))
infected = []
normal = []
alerted = []

N = len(colors) ## number of nodes
bI = 1 ## birthrate of the Infected
dI = 1 ## deathrate of the Infected -> becomes an Alerted
bA = 1 ## birthrate of an Alerted
dA = 1 ## deathrate of an Alerted

t = 0
t_arr = []
max_time = 1000
history = [np.copy(colors)]

best_connected_nodes = False

if best_connected_nodes:
    init_config = top_connected
    str_connected = "most-connected"
else:
    init_config = least_connected
    str_connected = "least-connected"

### setting one site to be infected
for i in init_config:
    colors[i] = 1
    
### starting off entirely infected
for i in range(N):
    colors[i] = 1

while(t < 1000):
    
    time_rate = 1/(bI + dI + bA + dA) * N
    t += np.random.exponential(1/time_rate)
    t_arr.append(t)

    
    site = int(np.random.rand() * N)
    
    if(colors[site] == 1): ## if it is infected
        U = np.random.rand() * (bI + dI)
        
        if(U < dI): ## death
            colors[site] = 2 ## set the infected to an alerted
        else:
            ## choose one of the neighbors
            y = sel_neighbor(site)
            
            if(colors[y] == 2): ## if the site is the alerted
                colors[site] = 2 ## then we set the current site to be alerted
            else:
                colors[y] = 1 ## otherwise we set it to be infected (normal or infected anyways)
    
    elif(colors[site] == 2):
        U = np.random.rand() * (bA + dA)
        
        if(U < dA):
            colors[site] = 0 ## set the alerted site to be normal
        else:
            ## choose one of the neighbors
            y = sel_neighbor(site)
            colors[y] = 2
            
    infected.append(len(colors[colors == 1]))
    alerted.append(len(colors[colors == 2]))
    normal.append(len(colors[colors == 0]))
    
    history.append(np.copy(colors))

print("finished")
hist = np.array(history)


# red dashes, blue squares and green triangles
plt.title("Entirely Filled Init" +  str(initial_count) + " | bI:" + str(bI) + " dI:" + str(dI) + "bA:" + str(bA) + " dA:" + str(dA))
# plt.title("Init: " + str_connected + " " + str(initial_count) + " | bI:" + str(bI) + " dI:" + str(dI) + "bA:" + str(bA) + " dA:" + str(dA))
plt.plot(t_arr, infected, 'r')
plt.plot(t_arr, normal, 'b')
plt.plot(t_arr, alerted, 'g')
plt.show()

print("infected: ", infected[-1])
print("normal: ", normal[-1])
print("alerted: ", alerted[-1])



#### THIS IS FOR CREATING GIFS
parse_step = int(hist.shape[0] / 100)
ds_hist = hist[::100] ## rule of thumb do it based on time


## putting all the pictures into a folder called gifs, make sure to make it!
for i in range(50): #ds_hist.shape[0]-50
    # this is for graphing the particular
    print(i)
    cmap, node_size = getcolormap(ds_hist[i])
    # plt.title("Facebook Network Graph -> Very Infectious Virus")
    plt.figure(figsize=(10,5))
    ax = plt.gca()
    ax.set_title("Facebook Network Graph -> Full Infected, 1111")
    nx.draw_networkx(G, pos, node_color=cmap, with_labels=False, node_size = node_size) # node lables
    plt.savefig("gifs/" + str(i) + '.png', bbox_inches='tight')
    plt.close()



## creating the gif by stiching all the pictures together
images = []
for i in range(50):
    images.append(imageio.imread("gifs/" + str(i) + ".png"))
imageio.mimsave('movie3.gif', images)