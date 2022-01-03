### NLP On Steam Player Comments
This is a standard NLP tutorial,Which includes text collection, text data analysis, and emotional analysis of text by establishing a deep learning model.  

## Steam Crawler Based on Selenium
I wrote a crawler specifically for steam platform,which based on selenium.This crawler will analyze the page source of steam website and collecting the following data:Game Title,Review Text,Recommendation,hour played,whether this review is helpful and whether this review is funny. And I applied I used multithreading to speed up data collection. 

## Data Analyze
I read the data and import some necessary components,Then I did some basic analyze of data and draw the graph.At last I Preprocessed the data,which includes text cleaning,text tokenizing and padding. 

## Data Moodeling
I established two deep learning models to analyze the data,one is GRU Model and another is LSTM Model,one is based on GPU and another is based on CPU,I used these two models to do sentiment analyze respectively,finally I compared the difference between speed and accuracy between two models. 