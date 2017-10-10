
# coding: utf-8

# In[79]:


import os
import pandas as pd
paper_directory = "../2014/papers_text"

#paper_array = names of all papers in dataset ordered lexically
paper_array = []
for filename in os.listdir(paper_directory):
    if filename.endswith(".txt"): 
        #print(os.path.join(directory, filename))
        paper_array.append(filename[:-4])
paper_array = sorted(paper_array)


incite = {} #dict of all incites of every paper
outcite = {} #dict of all outcites of every paper
for name in paper_array:
    incite[name] = []
    outcite[name] = []

acl_address = "../2014/acl.txt"
acl = open(acl_address, "r")
lines = acl.readlines()
for data in lines:
    a = data[:8]
    b = data[-9:-1]
    if(b in paper_array and a in paper_array):
        incite[b].append(a)
        outcite[a].append(b)
        
dict_to_write = {}

for (key, value) in incite.items():
    temp = ""
    if (value == []):
        dict_to_write[key] = [temp]
    for x in value:
        temp = temp+","+x
    dict_to_write[key] = [temp[1:]]
for (key, value) in outcite.items():
    temp = ""
    for x in value:
        temp = temp+","+x
    dict_to_write[key].append(temp[1:])
    
network = pd.DataFrame.from_dict(dict_to_write, orient='index')
network.to_csv("network.csv")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




