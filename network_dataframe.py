
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import os
import pickle
import distance
import re
import ezodf
import timeit


# In[2]:

## Functions to normalize string
def to_normal(a1):
    a1 = re.sub(r'\d+', '', a1)    # removes int
    a1 = re.sub(r'\W+', '', a1)    # removes non-alphanumeric
    #a1 = re.sub(r'[^\w\s]','',a1)  # removes non-alphanumeric(retains whitespaces)
    a1 = re.sub('\n', '', a1)
    a1 = a1.strip()
    a1 = a1.lower()
    return a1

#Function to find match for str(a1) in list_of_strings(a2)
def find_match(a1,a2):
    match_limit = 0.1
    a1 = to_normal(a1)
    dis = 1
    paper = None
    
    for elem in a2: 
        #Not applying to_normal to elem in a2(will make code very slow)
        #to_normal must be applied to every element of a2 before passing in the function 
    
        score = distance.nlevenshtein(a1, elem)
        if score<dis:
            paper = elem
            dis = score
    if dis<match_limit:
        return paper
    return False


# In[4]:

## Loading/Creating paper_array 
## paper_array = names of all papers in dataset ordered lexically
print '.....Loading/Creating paper_array..... '

paper_dir = "../2014/papers_text"
paper_array_path = 'pickled/paper_array.txt'

if os.path.isfile(paper_array_path):
    with open(paper_array_path, "rb") as array_file:
        paper_array = pickle.load(array_file)
else:
    paper_array = []
    for filename in os.listdir(paper_dir):
        if filename.endswith(".txt"): 
            paper_array.append(filename[:-4])
    paper_array = sorted(paper_array)
    with open(paper_array_path, "wb") as array_file:
        pickle.dump(paper_array, array_file)


# In[5]:

# Generating dict from section-mapping-file:
print '.....Generating dict from section-mapping-file....'

doc = ezodf.opendoc('section_mapping.ods')
sheet = doc.sheets[0]
f_dict = {}
for i, row in enumerate(sheet.rows()):
    key=to_normal(str(row[0].value))
    val=str(row[1].value)
    f_dict[key]=val
    
facets = list(set(f_dict.values()))
print facets


# In[6]:

#Loading dict_cit_head
print '.....loading dict_cit_head from pickled..... '
import pickle
with open("pickled/dict_cit_head.txt", "rb") as dict_file:
    outcite_1 = pickle.load(dict_file)


# In[7]:

#Initializing dict_cit_facet (outcite_2 and incite_2)
print '.....Initializing dict_cit_facet (outcite_2 and incite_2).....'

start_time = timeit.default_timer()
loop_count = -1

outcite_2 = {}
for paper_id in paper_array:
    outcite_2[paper_id] = {}
    for val in facets:
        outcite_2[paper_id][val]=[] 
        
incite_2 = {}
for paper_id in paper_array:
    incite_2[paper_id] = {}
    for val in facets:
        incite_2[paper_id][val]=[] 
        


# In[8]:

#Generating dict_cit_facet (outcite_2 and incite_2)
print 'Generating dict_cit_facet (outcite_2 and incite_2)..... '

for paper_id in outcite_1.keys():
    loop_count+=1
    if loop_count%10 ==0:
        elapsed = timeit.default_timer() - start_time
        print '---- time taken for last batch '+str(loop_count-9)+'--to--'+str(loop_count)+' = ' +str(elapsed)
    for entry in outcite_1[paper_id]:
        matched = find_match(entry[1],f_dict.keys())
        if matched:
            outcite_2[paper_id][f_dict[matched]].append(entry[0])
            incite_2[entry[0]][f_dict[matched]].append(paper_id)
    if loop_count%10 ==0:
        start_time = timeit.default_timer()
         


# In[9]:

# Saving dict_out_cit_facet and dict_in_cit_facet

print '....saving dict_out_cit_facet in pickled.....'
with open("pickled/dict_out_cit_facet.txt", "wb") as dict_file:
    pickle.dump(outcite_2, dict_file)
print '.....saved dict_out_cit_facet in pickled.....'

print '....saving dict_in_cit_facet in pickled.....'
with open("pickled/dict_in_cit_facet.txt", "wb") as dict_file:
    pickle.dump(incite_2, dict_file)
print '.....saved dict_in_cit_facet in pickled.....'


# In[ ]:

###....code ends here.....###


# In[ ]:




# In[ ]:




# In[ ]:



