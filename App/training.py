
# !!!!!!!! --- Emotion Classifier --- !!!!!!!!
# Core Packages
import streamlit as st
import altair as alt

# EDA Packages 
import pandas as pd
import numpy as np

# Utilities 
import joblib

# Importing Pipeline
pipeline = joblib.load(open("models/emotion_classifier_pipeline.pkl","rb"))

# Other Functions 

# Function - Predicting Emotions
def predict_emotions(docx):
    results = pipeline.predict([docx]) #.lower()
    return results[0]

# Function - Predicting Probability
def get_prediction_proba(docx):
    results = pipeline.predict_proba([docx])
    return results 


# Emoji - Dictionary
emotions_emoji_dict = {"anger":"😠","disgust":"🤮", 
                       "fear":"😨😱", "happy":"🤗",
                       "joy":"😂", "neutral":"😐", 
                       "sad":"😔", "sadness":"😔",
                       "shame":"😳", "surprise":"😮"}

#emotions_emoji_dict = emotions_emoji_dict.lower()


# !!!!!!!! --- Chat Assist --- !!!!!!!!
# Imported Chat Assist Functions
# # Importing Libraries
import numpy as np
import random
import json

import nltk
#nltk.download('punkt')
#nltk.download('wordnet')

import torch 
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# # Tokenizing Sentences
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# # Stemming Sentences
def stem(word):
    return stemmer.stem(word.lower())

# # Feature Engineering
def bag_of_words(tokenized_sentence, words):
    # stem each word 
    sentence_words = [stem(word) for word in tokenized_sentence]
    
    # initialize bag with 0 for each word 
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1
            
    return bag 

# # Loading Dataset
with open('intents.json', 'r') as f:
    intents = json.load(f)
    
# # Text Cleaning
all_words = []
tags = []
xy = []

for intent in intents["intents"]:
    tag = intent['tag']
    tags.append(tag)
    
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))
        
        
ignore_words = ['?', '.', ',', '!']

all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# print(len(all_words), 'unique stemmed words')

# # Labelling the Dataset
X_train= []
y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    
    y_train.append(label)
    
X_train = np.array(X_train)
y_train = np.array(y_train)

# # Creating the Pytorch Model
# Creating the Model

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)        
        # no activation and no softmax at the end
        return out 
    
# class ChatDataset(Dataset):
#     def __init__(self):
#         self.n_samples = len(X_train)
#         self.x_data = X_train 
#         self.y_data = y_train
        
#     # support indexing such that dataset[i] can be used to get i-th sample
#     def __getitem__(self, index):
#         return self.x_data[index], self.y_data[index]
    
#     # we call len(dataset) to return the size
#     def __len__(self):
#         return self.n_samples 
    
    
# num_epochs = 1000
# batch_size = 8
# learning_rate= 0.001
# input_size = len(X_train[0])
# hidden_size = 8
# output_size = len(tags)

# # print(input_size, output_size)
# # print(output_size)

# dataset = ChatDataset()
# train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# model = NeuralNet(input_size, hidden_size, output_size).to(device)

# criterion = nn.CrossEntropyLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)



## Training the Pytorch Model
# Train the model 
# for epoch in range(num_epochs):
#     for (words, labels) in train_loader:
#         words = words.to(device)
#         labels = labels.to(dtype=torch.long).to(device)
        
#         # forward pass
#         outputs = model(words)
#         # if y would be one-bot, we must apply 
#         # labels = torch.max(labels, 1)[1]
#         loss = criterion(outputs, labels)
        
#         # backward and optimize
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
        
#     if (epoch+1) % 100 == 0:
#         #pass
#         print(f'Epoch [{epoch+1}/{num_epochs}], loss: {loss.item():.4f}')
        
# print(f'final loss: {loss.item():.4f}')

# data = {
# "model_state": model.state_dict(),
# "input_size": input_size,
# "hidden_size": hidden_size,
# "output_size": output_size,
# "all_words": all_words,
# "tags": tags  
# }

# File = "data.pth"
# torch.save(data, File)

# # Saving the Model
#File = "data.pth"
#torch.save(data, File)



# # Loading the Trained Model
# Loading the saved model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)
    
FILE = "data.pth"
data = torch.load(FILE)

input_size = data['input_size']
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model =NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()