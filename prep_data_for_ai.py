# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:12:12 2023

@author: kacem
"""

import pandas as pd
import glob
import nltk

from nltk.stem import PorterStemmer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


nltk.download('stopwords')
nltk.download('punkt')



file_list = glob.glob("OneDrive/Bureau/D/data/*")

df_list = []
for file in file_list:
    df = pd.read_csv(file)
    df_list.append(df)
    

df = pd.concat(df_list, axis=0, ignore_index=True)

df = pd.concat([pd.read_csv(file) for file in file_list], ignore_index=True)

df.columns

df = df[['date', 'source', 'title', 'discreption']]



def fixe_date(original_date):
    month_dict = {
        'jan': '1', 'fév': '2', 'mar': '3', 'av': '4', 'mai': '5', 'juin': '6',
        'juil': '7', 'ao': '8', 'sep': '9', 'oct': '10', 'nov': '11', 'dec': '12', 'déc': '12'
    }
    
    splited_date = original_date.split()
    month = month_dict.get(splited_date[1].lower(), '')  # Get the month abbreviation in lowercase
    
    if month:  # If a valid month abbreviation is found
        splited_date[1] = month
    
    return '/'.join(splited_date)


df['date'] = df['date'].apply(fixe_date) 


mask = df['date'].str.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
filtered_df = df[mask]

df = df[mask]

df['date'] = pd.to_datetime(df['date'])




def remove_stop_words(string) :
    
    stop_words = set(stopwords.words('english'))
    
    lemmatizer = WordNetLemmatizer()
    
    string = string.replace('.' , '').replace(',' , '').replace(':', '').replace('\n','')
      
    word_tokens = word_tokenize(string)
    # converts the words in word_tokens to lower case and then checks whether 
    #they are present in stop_words or not
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    #with no lower case conversion
    filtered_sentence = []
      
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence

    
def steeming(filtered_sentence):
       
    ps = PorterStemmer()
    return list(map(ps.stem , filtered_sentence ))
    

def processing_one_str(string):
    
    filtered_sentence =  remove_stop_words(string)
    
    filtered_sentence = steeming(filtered_sentence)
    return filtered_sentence





from textblob import TextBlob


def word_sentiment(word):
    word_blob = TextBlob(word)
    sentiment = word_blob.sentiment.polarity
    return sentiment

def num_des(string_list):
    return list(map(word_sentiment, string_list ))


df['des_trt'] = df['discreption'].apply(processing_one_str)
    
df['num_des'] = df['des_trt'].apply(num_des)  

df['title_trt'] = df['title'].apply(processing_one_str)
     
df['num_title'] = df['title_trt'].apply(num_des)   


from statistics import mean


def avg_des(num_list):
    num_list = list(filter(lambda num: num != 0, num_list))
    
    return 0 if len(num_list) == 0 else mean(num_list)


df['avg_des'] = df['num_des'].apply(avg_des)

df['avg_title'] = df['num_title'].apply(avg_des)





file_y = "OneDrive/Bureau/D/diff_data/BTCUSD"



df_y = pd.read_csv(file_y)

df_y = df_y.rename(columns={'time': 'date'})

df_y['date'] = pd.to_datetime(df_y['date'])

merged_df = pd.merge(df, df_y, on='date')


merged_df = merged_df.set_index('date')



corr = merged_df['avg_des'].corr(merged_df['diff'])

# Print the correlation coefficient
print(corr)


