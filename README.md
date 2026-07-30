# Multimodal Clickbait Detection System Using Deep Learning 

## Project Overview
This research project focuses on detecting clickbait in both article headlines and YouTube videos using deep learning models.

The system combines:
- Text analysis (BiLSTM)
- Thumbnail image analysis (CNN)
- Video metadata features

In this repository, we have uploaded the samples of our articles headline and youtube videos datasets, since they are large in size and cannot be viewed. They are saved in the Datasets folder. The python scripts used to manually extract the attributes of the youtube videos and label them through ruled-based labelling are also uploaded to the Video Data Collection Scripts folder. We have uploaded our Literature Review in the Literature Review folder, which can be downloaded from there.

## Research Objectives
- Build a multimodal clickbait detection model
- Develop a browser extension for real-time detection
- Evaluate performance using accuracy, F1-score, and ROC

## Current Progress
- Literature review completed on clickbait detection 
- Dataset collection in progress for youtube videos (2000 rows created till now, our goal is 10,000)
- YouTube API data collection scripts developed  

## Dataset
The text dataset contains:
- Article headlines and their labels
- contains almost 32,000 rows
- We have taken this dataset that contains the headines of various articles, from an online source
  
The youtube video dataset contains:
- YouTube video ids
- video title
- video description
- Thumbnails
- Engagement metrics
- Comments and tags
- contains almost 2000 rows (till now)
- We have manually constructed the whole dataset. Collected youtube videos, extracted their attributes through the YouTube Data API v3 and auto-labelled them through a heuristic approach.

## Next Steps (Future Work)
- Data preprocessing
- Feature engineering
- BiLSTM text model implementation for headlines
- Hybrid Multimodal deep learning model for videos
- Browser extension development

## Tools
Python, TensorFlow/Keras, FastAPI, Chrome Extension APIs
