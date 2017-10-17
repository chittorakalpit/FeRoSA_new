
# coding: utf-8

# In[2]:

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import numpy as np
import os

tokenizer = RegexpTokenizer(r'\w+')


# In[3]:

# create English stop words list
en_stop = get_stop_words('en')


# In[4]:

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    


# In[5]:

paper_directory = "../2014/papers_text/"

#paper_array = names of all papers in dataset ordered lexically
paper_array = []
for filename in os.listdir(paper_directory):
    if filename.endswith(".txt"): 
        #print(os.path.join(directory, filename))
        paper_array.append(filename[:-4])
paper_array = sorted(paper_array)

filenames = [paper_directory + x + ".txt" for x in paper_array]
doc_list = [open(f).read() for f in filenames]


# In[6]:

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_list:
    if i%1000 ==0:
        print 'preprocessing paper_num: ' +str(paper_array[i]) 
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)
    

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # removing words of length < 3 (some integers were interfering in topics otherwise)
    filtered_tokens = [i for i in stemmed_tokens if len(i)>2]
    
    # add tokens to list
    texts.append(filtered_tokens)


# In[7]:

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)


# In[13]:

# convert tokenized documents into a document-term matrix
print 'building corpus (bag of words format).....'
corpus = [dictionary.doc2bow(text) for text in texts]
print 'corpus_size: ' + str(len(corpus))


# In[44]:

# generate LDA model
print '\n generating LDA model.....\n'
ldamodel = models.ldamulticore.LdaMulticore(corpus, num_topics=7, id2word = dictionary, passes=20)


# In[ ]:

print '\n saving LDA model.....\n'
ldamodel.save('lda/lda.model')


# In[14]:

print '\n printing LDA model.....\n'
for entry in ldamodel.print_topics(num_topics=7, num_words=5):
    print entry


# In[16]:

def get_doc_topics(lda, bow):
    gamma, _ = lda.inference([bow])
    
    topic_dist = gamma[0] / sum(gamma[0])  # normalize distribution
    return topic_dist
    #return [(topicid, topicvalue) for topicid, topicvalue in enumerate(topic_dist)]


# In[17]:

topic_dist = []
for j in xrange(len(corpus)):
    topic_dist.append(get_doc_topics(ldamodel, corpus[j]))
print '\n printing topic_dist for 1st paper: \n'
print topic_dist[0]


# In[52]:

#JSDiv_0
from scipy.stats import entropy
from numpy.linalg import norm
#import numpy as np

def JSDiv(P, Q):
    _P = P / norm(P, ord=1)
    _Q = Q / norm(Q, ord=1)
    _M = 0.5 * (_P + _Q)
    return 0.5 * (entropy(_P, _M) + entropy(_Q, _M))


# In[66]:

print '\n printing JSD for 1st paper and 1st paper: (must be 0.0) \n'
print m.sqrt(JSDiv(topic_dist[0],topic_dist[0]))


# In[ ]:

print '\n printing JSD for 1st paper and 2nd paper: \n'
print m.sqrt(JSDiv(topic_dist[0],topic_dist[1]))


# In[63]:

print '\n Building JSD_mat to replace cosine_mat.....\n'
JSD_mat = np.zeros((50,50))
for i in xrange(50):
    for j in xrange(50):
        JSD_mat[i][j] = m.sqrt(JSD(pd[i],pd[j]))
print 'JSD_mat done! \n'        


# In[ ]:

#ready_to_write = np.asarray(output_matrix)
print 'Saving JSD_mat to file....'
for i in range(0,len(paper_array)//100):
    np.savetxt("lda/jsd/jsd_"+str(i)+".csv", output_matrix[i*100:(i+1)*100], delimiter=",")


# In[ ]:

i = i+1
np.savetxt("lda/jsd/jsd_"+str(i)+".csv", output_matrix[i*100:], delimiter=",")


# In[ ]:



