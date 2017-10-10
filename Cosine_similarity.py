
# coding: utf-8

# In[2]:


from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


paper_directory = "../2014/papers_text/"

#paper_array = names of all papers in dataset ordered lexically
paper_array = []
for filename in os.listdir(paper_directory):
    if filename.endswith(".txt"): 
        #print(os.path.join(directory, filename))
        paper_array.append(filename[:-4])
paper_array = sorted(paper_array)

filenames = [paper_directory + x + ".txt" for x in paper_array]
documents = [open(f).read() for f in filenames]

raw_matrix = TfidfVectorizer(stop_words = 'english')
matrix = raw_matrix.fit_transform(documents)


# In[3]:


output_matrix = cosine_similarity(matrix)


# In[14]:


#ready_to_write = np.asarray(output_matrix)
for i in range(0,len(paper_array)//100):
    np.savetxt("cos_sim/cosine_similarity_"+str(i)+".csv", output_matrix[i*100:(i+1)*100], delimiter=",")


# In[16]:


i = i+1
np.savetxt("cos_sim/cosine_similarity_"+str(i)+".csv", output_matrix[i*100:], delimiter=",")


# In[ ]:





# In[ ]:




