
# @author sebastiano panichella

from tkinter import * #https://tkdocs.com/tutorial/text.html
from tkinter import filedialog

from pathlib import Path
import os
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

#python -m pip install -U matplotlib
#import matplotlib

if os.environ.get('DISPLAY','') == '':
    print('no display found.')
    #print('no display found. Using :0.0')
    #os.environ.__setitem__('DISPLAY', ':0.0')

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

#usage xample -> x=stemSentence(sentence,stemmer)
####end functions

# functions 
def openFile():
    #we delete the current text.. in the form..
    txtarea.delete("1.0","end")
    tf = filedialog.askopenfilename(
        initialdir="/", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),)
        )
    pathh.insert(END, tf)
    tf = open(tf)
    file_cont = tf.read()
    print("CONTENT TYPE: ",type(file_cont), "\n")
    #print(file_cont)
    #text_issue = text_issue + "" +file_cont.atype(str)
    txtarea.insert(END, file_cont)
    global text_issue
    text_issue = txtarea.get(1.0, "end-1c")
    #with open(path_text_issue) as f:
        #text_issue = f.readlines()
    tf.close()
    return text_issue

global sentences

def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    lbl.config(text = "Provided Input: "+inp)

def saveFile():
    try:
        #if sentences is "empty" of not "defined" the following line will generate an exception
        print(sentences)
        print(sentences['Sentence'])
        #base_path = os.getcwd()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # in case of issues we use pathlib (https://github.zhaw.ch/gann/dockerizing-python/wiki/Best-Practices)
        #__location__ = os.path.realpath(os.path.join(os.getcwd(), Path(__file__).parent))
        path_fasttext_predicted_labels_test_dataset = __location__
        #we replace the name of the current python script with the model name
        path_fasttext_predicted_labels_test_dataset = path_fasttext_predicted_labels_test_dataset.replace(os.path.basename(__file__), "trained_model.bin")
        path_fasttext_predicted_labels_test_dataset = path_fasttext_predicted_labels_test_dataset + "/fasttext_predicted_labels_test_dataset.csv"
        file = filedialog.asksaveasfilename(filetypes=[("csv file", ".csv")], defaultextension=".csv")
        #we try to take the name and location of the csv file from the GUI
        if file:
            sentences.to_csv(file,index=False) # store as CSV file
            print("CSV file saved as ", file)
        else:
            sentences.to_csv(path_fasttext_predicted_labels_test_dataset,sep=",")
            print("CSV file saved as ", path_fasttext_predicted_labels_test_dataset)
        
        print("Done.")
    except:
        print("Open a text file or write some more text. Then click on ''Read and Classify the Text'' for classifying the text. Then save the results by clicking on ''Save Classification Results'' ")
        
        
def classifyText():
    #if no file or text was entered..
    original_text = txtarea.get(1.0, "end+1c")
    temp_text = original_text+ " "
    #print(temp_text)
    # we remove extra spaces based on the fact that we are in front of a string OR a list of strings
    if type(temp_text) == list:
        temp_text = [x.strip(' ') for x in temp_text]
    elif type(temp_text) == str: 
        temp_text = " ".join(temp_text.split())
    #after removing extra spaces, we check if the text makes sense or not for the classification process
    print(temp_text)
    if  temp_text == "" or temp_text == " ":
        #temp_text
        print("Open a text file or write some more text. Then click on ''Read and Classify the Text'' for classifying the text. Then save the results by clicking on ''Save Classification Results'' ")
    else:
        #temp_text = "AP_Arming: pre-arm check if compass1 is disabled but 2 or 3 are enabled. This PR adds a pre-arm check to reduce the chance of users accidentally disabling all compasses when they only intended to disable the first one.\n Hello."
        #temp_text = ['AP_Arming: pre-arm check if compass1 is disabled but 2 or 3 are enabled. This PR adds a pre-arm check to reduce the chance of users accidentally disabling all compasses when they only intended to disable the first one. \n Hello. ',' Hello2.']
        # we reninizalize the text
        temp_text = original_text+ " "
        #if there is any "\n", we remove it from the list
        if any("\n" in s for s in temp_text) and type(temp_text) == list:
            temp = []
            for s in temp_text:
                temp = temp + s.splitlines()
            temp_text = temp
        #elif  there is any "\n", we remove it from the string
        elif "\n" in temp_text and type(temp_text) == str:
            temp = []
            temp = temp + temp_text.splitlines()
            temp_text = temp
        text_as_input = temp_text
        print(text_as_input)
        # we make the list global
        global sentences
        #and we inizialize it
        sentences = []
        #text_issue[0:text_issue.size]
        seg = pysbd.Segmenter(language="en", clean=False)
        if type(temp_text) == list:
            i = 0
            for i in np.arange(len(text_as_input)):
                sentences = sentences  + seg.segment(text_as_input[i])
        elif type(temp_text) == str:
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
        #we load the model
        #base_path = os.getcwd()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        path_model = __location__
        #we replace the name of the current python script with the model name
        path_model = path_model.replace(os.path.basename(__file__), "trained_model.bin")
        path_model = path_model + "/trained_model.bin"
        print(path_model)
        model = fasttext.load_model(path_model)
        for i in np.arange(sentences['Sentence'].size):
            results = model.predict( sentences["Sentence"][i] )
            sentences.loc[i,'Predicted_Label'] = str(results[0])
            sentences.loc[i,'Probability_of_Predicted_Label'] = float(results[1])
        #sentences.loc[0,:]
        print(sentences)
        print(sentences['Sentence'])
        #we delete the current text.. in the form..
        txtarea.delete("1.0","end")
        #we update the text in the textarea
        #string_collapsed = ' \n\n '.join(sentences['Sentence'])
        #string_collapsed = ' \n\n '+string_collapsed+' \n\n '
        #Selection Color Setting in Tkinter Entry Widget
        #txtarea.insert(END,string_collapsed)
        #txtarea.insert('end', 'first text', ('important'))
        #txtarea.tag_configure('important', background="orange", foreground="black")
        i = 0
        for i in np.arange(sentences['Sentence'].size):
            sentence_to_add = sentences["Sentence"][i]
            if "label__YES" in sentences["Predicted_Label"][i]:
                txtarea.insert('end', ' \n ')
                txtarea.insert('end', sentence_to_add, ('important'))
                background_to_set = color_classified_elements.get()
                #background_to_set = "orange"
                txtarea.tag_configure('important', background=background_to_set, foreground="black")
                txtarea.insert('end', ' \n ')
            else:
                txtarea.insert('end', ' \n ')
                txtarea.insert('end', sentence_to_add)
                txtarea.insert('end', ' \n ')
        #txtarea.insert('end', ' ')
    
ws = Tk()

# SALIENT (SAfety-criticaL IssuE ideNTifier), which automatically identifies safety-related sentences in the titles and descriptions of UAV-reported issues.
ws.title("SALIENT (SAfety-criticaL IssuE ideNTifier)")
ws.geometry("1250x750")
ws['bg']='#2a636e'

# adding frame
frame = Frame(ws)
frame.pack(pady=20)

# adding scrollbars 
ver_sb = Scrollbar(frame, orient=VERTICAL )
ver_sb.pack(side=RIGHT, fill=BOTH)

hor_sb = Scrollbar(frame, orient=HORIZONTAL)
hor_sb.pack(side=BOTTOM, fill=BOTH)

# adding writing space
txtarea = Text(frame, width=240, height=30,padx=10,font=16)#,bg='blue',fg='white')
txtarea.pack(side=LEFT)

# binding scrollbar with text area
txtarea.config(yscrollcommand=ver_sb.set)
ver_sb.config(command=txtarea.yview)

txtarea.config(xscrollcommand=hor_sb.set)
hor_sb.config(command=txtarea.xview)

# adding path showing box
pathh = Entry(ws)
pathh.pack(expand=True, fill=X, padx=5)

color_classified_elements = StringVar(ws)
color_classified_elements.set("orange") # default value

# the label for user_name
coloring = Label(ws, text = "Select a color to highlight classified elements:",background='#2a636e', foreground="white").place(x = 250,y = 680) 

w = OptionMenu(ws, color_classified_elements, "orange", "yellow","grey","cyan","magenta","red","blue", "green")
#w.place(x = 150,y = 520) 

w.pack()

# adding buttons 
open_f = Button(
    ws, 
    text="Open File", 
    command=openFile
    ).pack(side=LEFT, expand=True, fill=X, padx=5)

Button(
    ws, 
    text="Read and Classify the Text", 
    command=classifyText
    ).pack(side=LEFT, expand=True, fill=X, padx=5)


Button(
    ws, 
    text="Save Classification Results", 
    command=saveFile
    ).pack(side=LEFT, expand=True, fill=X, padx=5)

Button(
    ws, 
    text="Exit", 
    command=lambda:ws.destroy()
    ).pack(side=LEFT, expand=True, fill=X, padx=5, pady=5)

ws.mainloop()



