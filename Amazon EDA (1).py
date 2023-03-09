#!/usr/bin/env python
# coding: utf-8

# This is an EDA project. Dataset and questions are provided by Mr Abhishek Agarrwal in his youtube video. Link: https://www.youtube.com/watch?v=_DAwaQAAG2U&list=PL6_D9USWkG1CuKTolr0FoZMjG91PMiCKp&index=25
# 
# Questions: 
# 1. Import the dataset into the system
# 2. Show how many rows and columns are present
# 3. What is a datatype of each column
# 4. If datatype is different then expected then change it
# 5. Check for missing values in the dataset
# 6. Show missing values % in each column
# 7. Divide the column duration into duration_movie and duration_season
# 8. Divide column 'listed_in' by genre1, genre2...
# 9. What is the time period range of this dataset (hint: release_year)
# 10. How many movies and tv shows are present. Show both count and % of total
# 11. What type of movies are generally based on according to Genre1
# 12. What type of TV shows are generally based on according to Genre1
# 13. Clean the new duration column and remove min and season from numbers
# 14. What is average time of movie by Genre1
# 15. What is the average seasons of tv shows by genre1
# 16. Highest movies and tv shows by Director
# 17. Which type of genre generally have highest and smallest duration in both movie and tv show
# 18. Each year how many movie and tv show released
# 19. Which type ('Movie' or 'TV Show') is releasing more for Genre1
# 20. How many kids movies and tv shows are released each year
# 21. Are you seeing a trend change in Genre1 based on movie and tv shows released each year
# 22. How do you create new column based on hit movie or hit tv show vs average vs flop (base on rating)(create on your own)
# 23. Which Genre1 has most hit movies
# 24. Does the Genre1 of hit movies show a trend change
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


#1. Import the dataset into the system
dataset = pd.read_csv('amazon_prime_titles.csv')
dataset.head()


# In[3]:


#2. Show how many rows and columns are present
dataset.shape


# In[4]:


#3. What is a datatype of each column
dataset.info()


# In[5]:


#4. If datatype is different then expected then change it

#4a. Change show_id to integer by removing letter 's'

dataset['show_id']=dataset['show_id'].str.replace('s', '').astype(int)

#4b. Date_added should be in date format

dataset['date_added']=pd.to_datetime(dataset['date_added'])
dataset['year_added'] = dataset['date_added'].dt.year
dataset['month_added']= dataset['date_added'].dt.month


# In[6]:


#5. Check for missing values in the dataset. #Missing Data: Director, Cast, Country, Date_added, rating
dataset.info()


# In[7]:


dataset.type.unique()


# In[8]:


#6. Show missing values % in each column
percent_missing = dataset.isnull().sum() * 100 / len(dataset)
missing_value_dataset = pd.DataFrame({'column_name': dataset.columns,
                                 'percent_missing': percent_missing})
print(percent_missing)


# In[9]:


#7. Divide the column duration into duration_movie and duration_season

dataset['duration_season'] = dataset.apply(lambda x : x['duration'].split(" ")[0] if "Season" in x['duration'] else 0, axis = 1)
dataset['duration_movie'] = dataset.apply(lambda x : x['duration'].split(" ")[0] if "Season" not in x['duration'] else 0, axis = 1)


# In[10]:


dataset.head()


# In[11]:


#8. Divide column 'listed_in' by genre1, genre2...

dataset['Genre1'] = dataset['listed_in'].str.split(',', expand=True)[0]
dataset['Genre2'] = dataset['listed_in'].str.split(',', expand=True)[1]
dataset['Genre3'] = dataset['listed_in'].str.split(',', expand=True)[2]
dataset['Genre4'] = dataset['listed_in'].str.split(',', expand=True)[3]
dataset['Genre5'] = dataset['listed_in'].str.split(',', expand=True)[4]


# In[12]:


#9. What is the time period range of this dataset (hint: release_year)

dataset_range = range(max(dataset.release_year), min(dataset.release_year))
print(dataset_range)


# In[13]:


#10. How many movies and tv shows are present. Show both count and % of total

dataset.type.value_counts()


# In[14]:


#10. How many movies and tv shows are present. Show both count and % of total
dataset.type.value_counts(normalize=True)*100


# In[15]:


#11. What type of movies are generally based on according to Genre1

print(dataset[dataset['type']=='Movie']['Genre1'].value_counts())


# In[16]:


#12. What type of TV shows are generally based on according to Genre1

print(dataset[dataset['type']=='TV Show']['Genre1'].value_counts())


# In[17]:


#13. Clean the new duration column and remove min and season from numbers

dataset['duration_movie'] = dataset['duration_movie'].astype(int)
dataset['duration_season'] = dataset['duration_season'].astype(int)


# In[18]:


#14. What is average time of movie by Genre1

dataset.groupby('Genre1').agg({'duration_movie':('mean')})


# In[19]:


#15. What is the average seasons of tv shows by genre1
dataset.groupby('Genre1').agg({'duration_season':('mean')})


# In[20]:


#16. Highest movies and tv shows by Director
dire = dataset[dataset['type']=='Movie']['director'].value_counts()
print(dire)


# In[21]:


markk = dataset['director'].str.startswith('Mark')
print(markk)


# In[22]:


#16. Highest movies and tv shows by Director ANS: NONE
tvs = dataset[dataset['type']=='TVShow']['director'].value_counts()
print(tvs)


# In[23]:


import seaborn as sns
fig = plt.figure(figsize=(20,10))
sns.countplot(y='Genre1', data=dataset)


# In[24]:


#17. Which type of genre generally have highest and smallest duration in movie
movie1 = dataset.sort_values('duration_movie', ascending = False)
movie1[['title', 'duration_movie']][:1]


# In[25]:


movie2 = dataset.sort_values('duration_movie', ascending = True)
movie2 = movie2[movie2['duration_movie'] >= 10]
movie2[['title', 'duration_movie']]


# In[26]:


#18. Each year how many movie and tv show released
dataset[dataset['type']=='Movie'].release_year.value_counts()


# In[27]:


#18. Each year how many movie and tv show released

dataset[dataset['type']=='TV Show'].release_year.value_counts()


# In[28]:


#19. Which type ('Movie' or 'TV Show') is releasing more for Genre1
dataset.groupby('Genre1')['type'].value_counts()


# In[29]:


#20. How many kids movies and tv shows are released each year
dataset[dataset['Genre1']=='Kids'].groupby('type').size().reset_index()


# In[31]:


#21. Are you seeing a trend change in Genre1 based on movie and tv shows released each year

df = dataset.groupby(['release_year', 'type']).count()['Genre1']

df.unstack().plot(figsize=(20,10))
plt.show()


# In[32]:


#22. How do you create new column based on hit movie or hit tv show vs average vs flop (base on rating)(create on your own)

dataset['Rating'].unique()


# In[33]:


#22. How do you create new column based on hit movie or hit tv show vs average vs flop (base on rating)(create on your own)

def successtype(value):
    if value <= 3:
        return "Flop"
    if value >= 7:
        return "Hit"
    else:
        return "Average"

dataset['successtype'] = dataset['Rating'].map(successtype)
dataset.head()


# In[34]:


#23. Breakdown of TV Shows and Movies 

dataset.groupby(['successtype', 'type']).size()


# In[35]:


#23. Which Genre1 has most hit movies and Tv shows

df1 = dataset[['type','successtype','Genre1']].groupby(['type','successtype','Genre1']).size().reset_index().rename(columns={0:'Count'})

df1[df1['successtype']=='Hit'].sort_values('Count', ascending=False).reset_index()
#dataset[dataset['successtype']=='Hit']['Genre1'].value_counts()


# In[36]:


#24. Does the Genre1 of hit movies show a trend change

dataset[dataset['successtype']=='Hit']['Genre1'].value_counts().plot(kind='bar', figsize=(20,10))


# In[37]:


#25. What is the average duration of hit movies by Genre1

df2 = dataset[['duration_movie','successtype','Genre1']].groupby(['duration_movie','successtype','Genre1']).size().reset_index().rename(columns={0:'Count'})
df2[df2['successtype']=='Hit'].duration_movie.mean()


# In[38]:


#26. IS this differ by Country? 22,23,24,25.. Missing values in Country column
df2 = dataset[['duration_movie','successtype','country']].groupby(['duration_movie','successtype','country']).size().reset_index().rename(columns={0:'Count'})
df2[df2['successtype']=='Hit'].duration_movie.mean()


# In[42]:


dataset.isnull().sum()


# In[40]:


dataset[['Genre1','successtype']].groupby('Genre1').value_counts().plot(kind='bar', figsize=(20,20))


# In[41]:


dataset[dataset['successtype']=='Hit']['country'].value_counts()

