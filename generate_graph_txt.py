
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os

#reading data
network = pd.read_csv("network.csv")


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

paper_directory = "../2014/papers_text"

#paper_array = names of all papers in dataset ordered lexically
paper_array = []
for filename in os.listdir(paper_directory):
    if filename.endswith(".txt"): 
        #print(os.path.join(directory, filename))
        paper_array.append(filename[:-4])
paper_array = sorted(paper_array)


# In[17]:


def cos_sim(p1, p2):
    index = paper_array.index(p1)
    file_index = index//100
    cosinefile = "cos_sim/cosine_similarity_"+str(file_index)+".csv"
    index = index%100
    cosine = open(cosinefile, "r")
#    print index
    #lines = cosine.readlines()
    for i in range(0,index):
        #print(i)
        line = cosine.readline()
    line = cosine.readline()
    similarity_p1 = line.split(',')
    return similarity_p1[paper_array.index(p2)]
    


# In[5]:


## generates induced graph...
   
def gen_ind_graph(paper_id, out_net, in_net):       
   nodes = []
   out_1 = out_net[paper_id]
   in_1 = in_net[paper_id]
   nodes=nodes+out_1+in_1                           ## adds all 1-hop papers...
   
                               
   for paper in out_1:                              ## adds all 2-hop papers...
       nodes=nodes+out_net[paper]
       nodes=nodes+in_net[paper]
   for paper in in_1:
       nodes=nodes+out_net[paper]
       nodes=nodes+in_net[paper]

   node_set = set(nodes)                            ## takes unique values only...
   nodes = list(node_set)

   graph = []
   for i in nodes:
       for j in nodes:
           if j in outcite[i]:
               if(i<j):
                   graph.append([i, j, cos_sim(i,j)])   ## cos_sim needs to be defined...       
               else:
                   graph.append([i, j, cos_sim(j,i)])   ## cos_sim needs to be defined...       
   return graph    


# In[15]:


## For storing graph as 'paper_id_graph.txt' :

def get_graph_txt(paper_id, out_net, in_net):
    g = gen_ind_graph(paper_id, out_net, in_net)

	total=0
	for i in g:
		total += float(i[2])

    name = "graph/" + paper_id + '_graph.txt'
    file = open(name, 'w')
    for item in g:
        item_str = item[0]+'\t'+item[1]+'\t'+str(float(item[2])/total)+'\n'
        print item_str
        file.write(item_str)
    file.close()


# In[18]:


get_graph_txt('A00-1005', outcite, incite)


# In[ ]:




