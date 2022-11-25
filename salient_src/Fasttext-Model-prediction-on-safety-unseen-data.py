
# @author sebastiano panichella

import csv
import numpy as np
import pandas as pd
# pip install fasttext==0.9.1 #required version
import fasttext # pip uninstall fasttext 
import nltk
nltk.download('stopwords')

#### functions
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt')
import re

def stemSentence(sentence, stemmer):
    token_words=word_tokenize(sentence)
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(stemmer.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


import sys
import json
import argparse
#python3 -m spacy download en_core_web_sm
#pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
import spacy
import pysbd
from pysbd.utils import PySBDFactory
#if we are reading arguments from command line..
if len(sys.argv) > 1:
    UAV_config_file = sys.argv[1]
    print(UAV_config_file)
    #parsing JSON file..
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', nargs=1, help="JSON file to be processed", type=argparse.FileType('r'))
    arguments = parser.parse_args()
    # Loading a JSON object returns a dict.
    data = json.load(arguments.infile[0])
    profileInfo = {} #necessary command to load json file
    # Overwrite the profileInfo dict
    #profileInfo.update(data)
    #print(data["path_model"])
    #print(data["path_test_set"])
    #print(data["path_text_issue"])
    #print(data["path_fasttext_predicted_labels_test_dataset"])
    #print(data)
    print("Parsed json file.")

#usage xample -> x=stemSentence(sentence,stemmer)
####end functions

#path_model = "/Users/spanichella/Desktop/Zurich-applied-Science/Projects/EU-PROJECTS/APPROVED/COSMOS/GITLAB--project-Repositories/WP6.1-dev/Safety-Bugs/Tf-idf-pipeline/R-solution/Resources/R-scripts-safety/TOOL-DEMO-2023/trained_model.bin"
path_model = data["path_model"]
#path_text_issue = "/Users/spanichella/Desktop/Zurich-applied-Science/Projects/EU-PROJECTS/APPROVED/COSMOS/GITLAB--project-Repositories/WP6.1-dev/Safety-Bugs/Tf-idf-pipeline/R-solution/Resources/R-scripts-safety/TOOL-DEMO-2023/text_issue.txt"
path_text_issue = data["path_text_issue"]

#path_fasttext_predicted_labels_test_dataset = "/Users/spanichella/Desktop/Zurich-applied-Science/Projects/EU-PROJECTS/APPROVED/COSMOS/GITLAB--project-Repositories/WP6.1-dev/Safety-Bugs/Tf-idf-pipeline/R-solution/Resources/R-scripts-safety/TOOL-DEMO-2023/fasttext_predicted_labels_test_dataset.txt" 
path_fasttext_predicted_labels_test_dataset = data["path_fasttext_predicted_labels_test_dataset"]

#path_test_set = "/Users/spanichella/Desktop/Zurich-applied-Science/Projects/EU-PROJECTS/APPROVED/COSMOS/GITLAB--project-Repositories/WP6.1-dev/Safety-Bugs/Tf-idf-pipeline/R-solution/Resources/R-scripts-safety/TOOL-DEMO-2023/test-set.csv"
path_test_set = data["path_test_set"]

#text_as_input = "AP_Arming: pre-arm check if compass1 is disabled but 2 or 3 are enabled. This PR adds a pre-arm check to reduce the chance of users accidentally disabling all compasses when they only intended to disable the first one."
text_as_input = data["text_as_input"]

#we load the model
model = fasttext.load_model(path_model)

# CASE 1: if we are givin in input (also) a structured test set
if path_test_set != "":
    test_set  = pd.read_csv(path_test_set)
    test_set = test_set.rename(columns={'IS_SAFETY_FINAL': 'Predicted_Label'})
    #test_set.loc['Probability_of_Predicted_Label'] = 0
    #test_set.loc['ID'] = IDs
    IDs = test_set.loc[:,'ID']
    i = 0
    # prediction on test data
    for i in np.arange(test_set['Sentence'].size):
        index = test_set.index[i]
        results = model.predict( str(test_set.loc[ index ,'Sentence']))
        test_set.loc[index,'Predicted_Label'] = str(results[0])
        test_set.loc[index,'Probability_of_Predicted_Label'] = float(results[1])
    start = (IDs.index.size-test_set.index.size)
    end = (IDs.index.size)
    test_set.index = IDs[start: end]
    print(test_set)
    test_set.to_csv(path_fasttext_predicted_labels_test_dataset,sep=",")
    
# CASE 2: if we are givin in input (also) the text of an issue
if path_text_issue != "":
    with open(path_text_issue) as f:
        text_issue = f.readlines()
    #we remove empty lines.. (i.e., having only "\n")
    text_issue = pd.DataFrame(text_issue)
    text_issue = text_issue[0].astype(str)
    text_issue = text_issue[ text_issue != "\n"]

    # we extract sentences missed in the previous preprocessing step
    text_issue = text_issue.astype(str)
    text_issue.index =  list(range(0, text_issue.size))
    #text_issue[0:text_issue.size]
    seg = pysbd.Segmenter(language="en", clean=False)
    #text = "First Jennifer is learning quantitative analysis. Second. Third. Five (3)."
    #seg.segment(text)
    sentences = []
    i = 0
    for i in np.arange(text_issue.size):
        sentences = sentences  + seg.segment(text_issue[i])
    #If you want to remove \n from all the elements, use this:
    #we remove "\n" from the text
    sentences = [x[:-1] for x in sentences]
    sentences = pd.DataFrame(sentences)
    sentences = sentences.rename(columns={0: 'Sentence'})
    #sentences[0].replace("\n", "")
    #sentences['Sentence'] 
    sentences['Predicted_Label'] = ""
    sentences['Probability_of_Predicted_Label'] = 0
    i = 0
    # prediction on test data
    for i in np.arange(sentences['Sentence'].size):
        results = model.predict( sentences["Sentence"][i] )
        sentences.loc[i,'Predicted_Label'] = str(results[0])
        sentences.loc[i,'Probability_of_Predicted_Label'] = float(results[1])
    #sentences.loc[0,:]
    print(sentences)
    sentences.to_csv(path_fasttext_predicted_labels_test_dataset,sep=",")
    sentences1 = sentences

# CASE 3: if we are givin in input a string of the issue
if text_as_input != "":
    sentences = []
    #text_issue[0:text_issue.size]
    seg = pysbd.Segmenter(language="en", clean=False)
    sentences = sentences  + seg.segment(text_as_input)
    #If you want to remove \n from all the elements, use this:
    #we remove "\n" from the text
    sentences = [x[:-1] for x in sentences]
    sentences = pd.DataFrame(sentences)
    sentences = sentences.rename(columns={0: 'Sentence'})
    #sentences[0].replace("\n", "")
    #sentences['Sentence'] 
    sentences['Predicted_Label'] = ""
    sentences['Probability_of_Predicted_Label'] = 0
    i = 0
    # prediction on test data
    for i in np.arange(sentences['Sentence'].size):
        results = model.predict( sentences["Sentence"][i] )
        sentences.loc[i,'Predicted_Label'] = str(results[0])
        sentences.loc[i,'Probability_of_Predicted_Label'] = float(results[1])
    #sentences.loc[0,:]
    print(sentences)
    sentences.to_csv(path_fasttext_predicted_labels_test_dataset,sep=",")
    sentences2 = sentences

# CASE 4: if more than one parameter was used (as input) we then merge the results
if(int(text_as_input != "") + int(path_text_issue != "") + int(path_test_set != "")) >1:
    new_Probability_of_Predicted_Label = []
    new_Sentence= []
    new_Predicted_Label= []
    #new_Probability_of_Predicted_Label = new_Probability_of_Predicted_Label + test_set.loc[:,'Probability_of_Predicted_Label'].to_list()  + sentences1.loc[:,'Probability_of_Predicted_Label'].to_list()+ sentences2.loc[:,'Probability_of_Predicted_Label'].to_list()
    #new_Predicted_Label = new_Predicted_Label + test_set.loc[:,'Predicted_Label'].to_list()  + sentences1.loc[:,'Predicted_Label'].to_list()+ sentences2.loc[:,'Predicted_Label'].to_list()
    #new_Sentence = new_Sentence + test_set.loc[:,'Sentence'].to_list()  + sentences1.loc[:,'Sentence'].to_list()+ sentences2.loc[:,'Sentence'].to_list()
    
    if (int(path_test_set != "")):
        new_Probability_of_Predicted_Label = new_Probability_of_Predicted_Label + test_set.loc[:,'Probability_of_Predicted_Label'].to_list()  
        new_Predicted_Label = new_Predicted_Label + test_set.loc[:,'Predicted_Label'].to_list()  
        new_Sentence = new_Sentence + test_set.loc[:,'Sentence'].to_list()  
      
    if(int(path_text_issue != "")):
       new_Probability_of_Predicted_Label = new_Probability_of_Predicted_Label  + sentences1.loc[:,'Probability_of_Predicted_Label'].to_list()
       new_Predicted_Label = new_Predicted_Label + sentences1.loc[:,'Predicted_Label'].to_list()
       new_Sentence = new_Sentence + sentences1.loc[:,'Sentence'].to_list()
        
    if(int(text_as_input != "")):
        new_Probability_of_Predicted_Label = new_Probability_of_Predicted_Label + sentences2.loc[:,'Probability_of_Predicted_Label'].to_list()
        new_Predicted_Label = new_Predicted_Label + sentences2.loc[:,'Predicted_Label'].to_list()
        new_Sentence = new_Sentence + sentences2.loc[:,'Sentence'].to_list()
         
    #we put in a single dataframe all results...
    new_dataframe = pd.DataFrame(list(zip(new_Sentence, new_Predicted_Label, new_Probability_of_Predicted_Label)), columns =['Sentence','Predicted_Label','Probability_of_Predicted_Label'])
    new_dataframe.to_csv(path_fasttext_predicted_labels_test_dataset,sep=",")
    print("\n\n STORED DATA:\n")
    print(new_dataframe)








