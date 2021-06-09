# Project-Cymopolea
Natural disasters are major adverse events resulting from natural processes of the Earth and have plagued us for centuries. Fortunately, we've gotten better in mitigating and created tools that allow us to detect these events in advance which has aided us in taking proactive measures to prepare for the event.  
The project name was inspired from the greek goddess of violent storm waves, Cymopolea (kee-mo-po-laya) ([source](https://greekmythology.wikia.org/wiki/Kymopoleia)) 

#### Quick start guide
All of the work related to the text processing and modeling was done in an Ipython notebook
To view the notebook:
[Notebook View](https://nbviewer.jupyter.org/github/yepterence/Project-Cymopolea/blob/main/text-processing.ipynb)

If you would like to play around with it you can: 
- download all the requirements in requirements.txt file by using: 

<span>pip install -r requirements.txt</span>

- Download the [notebook](https://github.com/yepterence/Project-Cymopolea/blob/main/text-processing.ipynb)
- Download the best model and use that instead. 

## Business case

- Monetary reasons: Global disasters caused losses world-wide in 2020 that totaled $210 billion dollars which is up by 26% from 2019 to $166 billion with $82 billion worth of damage insured last year up by 44% from 2019. (source: [Insurance Information Institute](https://www.iii.org/fact-statistic/facts-statistics-global-catastrophes))
- Preventable loss of human life: Last year’s natural disasters claimed approximately 8,200 lives (source: [Investopedia](https://www.investopedia.com/natural-disasters-cost-usd210-billion-worldwide-in-2020-5094629))
- Protecting against insurance fraud: A catastrophe greatly magnifies the opportunity for fraud and abuse. Providing real time feedback to insurance agencies can help prevent this. [NICB](https://www.nicb.org/disaster-tips)
- Twitter: 
    - Real-time microblogging platform
    - 186 million daily active users as of 2020
    - 150 million users worldwide, including 36 million from US
    - Ubiquitous presence of smartphones 
    [Twitter stats source](https://www.businessofapps.com/data/twitter-statistics/)

## Objectives
- Quick identification of natural disaster occurrences from tweets 
- Incorporate image classification for any pictures that were included with tweet

## Methodology 

- Using Python to 
- Determine best classifier for use case.
- Optimize hyperparamters using RandomSearch cross validation.

## Data sources

- [Kaggle (NLP getting started)](https://www.kaggle.com/c/nlp-getting-started/overview) : For hand labeled tweets. 
- [Kaggle (Disaster image dataset)](https://www.kaggle.com/mikolajbabula/disaster-images-dataset-cnn-model): For images of natural disasters that were divided into disaster specific folders.

## Pre-processing 

Text corpus was preprocessed to remove any english stop words, punctuations, hyperlinks and symbols. In addition, any words that did not constitute as natural disaster were also muted that would have potentially skewed our classifier.

## Visualization 

![disaster-wordcloud](images/disaster_wordcloud.jpg?raw=true "Disaster Tweet wordcloud")
Above: Word cloud image that shows frequency of words that are classified as natural disaster tweets in the cleaned training dataset

## Modeling and evaluation 

Bag-of-words and TF-IDF model was used to generate ngram vectors from the corpus and then used linear regression as well as ensemble classifiers such as RandomForest and GradientBoost to classify the tweets.  
The best results were from our uni-bigram Bag-of-Words model with RandomForest classifier had an accuracy of ~78\%. It had the lowest false positive rate and better performance in detecting true positives. 

## Limitations of study

- Class imbalance 
- Bias introduced during pre-processing steps

## Future directions
- Improve accuracy of model (95% target)
- Word embeddings and deep learning (LSTM) 
- Web application to send notifications to subscriber 

