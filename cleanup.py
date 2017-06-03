
# coding: utf-8

# In[1]:

import json_lines


# In[2]:

import re


# In[3]:

data = []
with open('items.jl', 'r') as f:
    for item in json_lines.reader(f):
        data.append(item)


# In[4]:

topics = {}
for i in data:
    for t in i['topic']:
        if t not in topics:
            topics[t] = 1
        else:
            topics[t] += 1


# In[5]:

for i in sorted(topics, key=topics.get, reverse=True)[:50]:
    print(i+': ', str(topics[i]))


# In[6]:

noaq = re.compile('\?$')
noacom = re.compile('\.{3}$')


# In[7]:

data = data[1:]


# In[8]:

def cleanup(data):
    # data = list(set(data))
    for i in data:
        i['q'] = i['q'][0]
        arr = []
        for a in i['a']:
            if not noaq.match(a) and not noacom.match(a):
                arr.append(a)
        i['a'] = ' '.join(arr)
    return data


# In[9]:

data = cleanup(data)


# In[10]:

clean = open('clean.json', 'w')


# In[11]:

import json


# In[12]:

json.dump(data, clean, indent=4)


# In[ ]:




# In[ ]:



