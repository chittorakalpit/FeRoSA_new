
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import os
import pickle
import timeit


# In[6]:

# Loading network from csv file
print '.....Loading network from csv file.....'
network = pd.read_csv("network.csv")

# Loading cos-sim-array from cos_mat.npy
print '.....Loading cos-sim-array from cos_mat.npy.....'
cos_sim_array = np.load("cos/cos_mat.npy")

# Min cos_sim value to consider similar
COS_LIMIT = 0.49


# In[3]:

#Creating incite and outcite dictionary
incite = {}
outcite = {}
for row in network.iterrows():
    if(type(row[1][1])!=str):
        incite[row[1][0]] = []
    else:
        incite[row[1][0]] = row[1][1].split(',')
    if(type(row[1][2])!=str):
        outcite[row[1][0]] = []
    else:
        outcite[row[1][0]] = row[1][2].split(',')


# In[ ]:

## Loading/Creating paper_array 

paper_dir = "../2014/papers_text"
paper_array_path = 'pickled/paper_array.txt'
#paper_array = names of all papers in dataset ordered lexically
if os.path.isfile(paper_array_path):
    with open(paper_array_path, "rb") as array_file:
        paper_array = pickle.load(array_file)
else:
    paper_array = []
    for filename in os.listdir(paper_dir):
        if filename.endswith(".txt"): 
            #print(os.path.join(directory, filename))
            paper_array.append(filename[:-4])
    paper_array = sorted(paper_array)
    with open(paper_array_path, "wb") as array_file:
        pickle.dump(paper_array, array_file)


# In[17]:

# Function to compute cos_sim for given paper_id's p1 and p2:
def cos_sim(p1, p2):
    return cos_sim_array[paper_array.index(p1), paper_array.index(p2)]
    


# In[ ]:

# Function to compute top 100 similar papers for given paper_id p1:
def cos_sim_top(p1):
    similarity_p1 = cos_sim_array[paper_array.index(p1)]
    top = [paper_array[i] for (i,j) in enumerate(similarity_p1) if j> COS_LIMIT]
    if(len(top)>100):
        return top[:100]
    else:
        return top


# In[5]:

# Function to generate induced graph for given paper_id, outcite_network, incite_network and facet:
def gen_ind_graph(paper_id, out_net, in_net,facet):
    
    nodes = []
    out_1 = out_net[paper_id][facet]
    in_1 = in_net[paper_id][facet]
    nodes=nodes+out_1+in_1                           ## adds all 1-hop papers...
   
                               
    for paper in out_1:                              ## adds all 2-hop papers...
        nodes=nodes+out_net[paper][facet]
        nodes=nodes+in_net[paper][facet]
    for paper in in_1:
        nodes=nodes+out_net[paper][facet]
        nodes=nodes+in_net[paper][facet]
    
    nodes = nodes + cos_sim_top(paper_id)            ## adds papers above COS_LIMIT

    node_set = set(nodes)                            ## takes unique values only...
    nodes = list(node_set)
    
    tpm = np.zeros((len(nodes),len(nodes)))
    graph = []
    
    for i in range(1,len(nodes)):
        for j in range(0,i):
            p1 = nodes[i]
            p2 = nodes[j]
            if (p1 in out_net[p2][facet]) or (p2 in out_net[p1][facet]) or (cos_sim(p1,p2)>COS_LIMIT):
                tpm[i][j] = cos_sim(p1,p2)
                tpm[j][i] = tpm[i][j]
    for i in xrange(len(nodes)):
        tpm[i] = tpm[i]/float(np.sum(tpm[i]))*0.9 
        tpm[i]+= (1-np.sum(tpm[i]))/len(nodes)
        
    for i in range(0,len(nodes)):
        for j in range(0,len(nodes)):    
            graph.append([nodes[i], nodes[j], tpm[i,j]])
                
    return graph


# In[15]:

## Function for storing graph as 'paper_id_graph.txt' :

def get_graph_txt(paper_id, out_net, in_net,facet):
    g = gen_ind_graph(paper_id, out_net, in_net,facet)
    name = "graph/" + paper_id + '_graph.txt'
    file = open(name, 'w')
    for item in g:
        item_str = item[0]+'\t'+item[1]+'\t'+str(item[2])+'\n'
        file.write(item_str)
    file.close()


# In[ ]:

# Loading dict_out_cit_facet  and dict_in_cit_facet
print '....loading dict_out_cit_facet in pickled.....'
with open("pickled/dict_out_cit_facet.txt", "rb") as dict_file:
    outcite_2 = pickle.load(dict_file)

print '....loading dict_in_cit_facet in pickled.....'
with open("pickled/dict_in_cit_facet.txt", "rb") as dict_file:
    incite_2 = pickle.load(dict_file)


# In[18]:

get_graph_txt('A00-1005', outcite_2, incite_2, 'M')
get_graph_txt('A00-1009', outcite_2, incite_2, 'C')



# In[ ]:



