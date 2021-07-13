# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 16:11:15 2021

@author: domini4
"""

from selenium import webdriver
import matplotlib.pyplot as plt
import numpy as np

# replace with valid path
driver = webdriver.Chrome(executable_path=r'C:\Users\domini4\Downloads\chromedriver_win32\chromedriver.exe')

user_n = []
dictionary = {}

# repeat for every page
for page_n in range(1,39):
    page_url = 'https://www.reef2reef.com/threads/10-winners-hanna-instruments-great-summer-giveaway-win-a-brand-new-nitrate-checker.835887/page-' + str(page_n)
    
    driver.get(page_url)    
    
    # save all unique comment ids
    ids = driver.find_elements_by_xpath("//*[contains(@id,'js-post')]")
    comment_ids = []
    for i in ids:
        comment_ids.append(i.get_attribute('id'))
        
    # remove op and entries after cutoff
    if page_n == 1:
        del comment_ids[0]
    if page_n == 38:
        del comment_ids[4:20]

        
    for x in comment_ids:
        # extract data using the unique id
        userid_element = driver.find_elements_by_xpath('//*[@id="' + x +'"]')[0]
        userid = userid_element.text
        # adding data to dict
        if len(userid.splitlines()[2]) > 1:
            if userid.splitlines()[2] in dictionary.keys():
                dictionary[userid.splitlines()[2]]+=1
            else:
                dictionary[userid.splitlines()[2]]=1
        else:
            if userid.splitlines()[3] in dictionary.keys():
                dictionary[userid.splitlines()[3]]+=1
            else:
                dictionary[userid.splitlines()[3]]=1

# check if all data is collected
sum_d = 0

for key in dictionary:
    sum_d += dictionary[key]
    
print(sum_d)

# sort dict by number of entries
key_n = {}
for i in dictionary:
    if dictionary[i] in key_n.keys():
        key_n[dictionary[i]]+=1
    else:
        key_n[dictionary[i]]=1
        
# prepare data for plotting
key_s = sorted(key_n.items())
x, y = zip(*key_s)

#adding entry for 9
x = list(x)
x.insert(8,9)
y = list(y)
y.insert(8,0)

# plot the data
ind = np.arange(len(x))
width = 0.60

fig, ax = plt.subplots()

ax.set_ylabel('Number of reefers')
ax.set_xlabel('Number of entries')
ax.set_title('Number of entries per reefer')

ax.set_xticks(ind)
ax.set_xticklabels(x)

pps = ax.bar(ind-width/2, y, width, label='y')
for p in pps:
   height = p.get_height()
   ax.annotate('{}'.format(height),
      xy=(p.get_x() + p.get_width() / 2, height),
      xytext=(0, 0), # 3 points vertical offset
      textcoords="offset points",
      ha='center', va='bottom')
    
plt.show()