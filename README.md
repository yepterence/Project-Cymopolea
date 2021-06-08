# Project-Cymopolea
Natural disasters are major adverse events resulting from natural processes of the Earth and have plagued us for centuries. Fortunately, we've gotten better in mitigating and created tools that allow us to detect these events in advance which has aided us in taking proactive measures to prepare for the event.  
The project name was inspired from the greek goddess of violent storm waves, Cymopolea (kee-mo-po-laya) ([source](https://greekmythology.wikia.org/wiki/Kymopoleia)) 
With twitter 
1. How do you identify what is relevant information for emergency response personnel? 
2. What sort of implementation would be valuable? 

## Why Bother? 

- Monetary reasons: Global disasters caused losses world-wide in 2020 that totaled $210 billion dollars which is up by 26% from 2019 to $166 billion with $82 billion worth of damage insured last year up by 44% from 2019. (source: [Insurance Information Institute](https://www.iii.org/fact-statistic/facts-statistics-global-catastrophes))
- Preventable loss of human life: Last year’s natural disasters claimed approximately 8,200 lives (source: [Investopedia](https://www.investopedia.com/natural-disasters-cost-usd210-billion-worldwide-in-2020-5094629))
- Protecting against insurance fraud: A catastrophe greatly magnifies the opportunity for fraud and abuse. Providing real time feedback to insurance agencies can help prevent this. [NICB](https://www.nicb.org/disaster-tips)

## Methodology 

- Using Python NLTK package to tokenize, lemmatize and then vectorize the words using Bag-of-words model 
- Determine best classifier for use case.
- Optimize hyperparamters using RandomSearch cross validation.

## Data sources

- [Kaggle (NLP getting started)](https://www.kaggle.com/c/nlp-getting-started/overview) : For hand labeled tweets. 
- [Kaggle (Disaster image dataset)](https://www.kaggle.com/mikolajbabula/disaster-images-dataset-cnn-model): For images of natural disasters that were divided into disaster specific folders.

## Pre-processing 

Text corpus was preprocessed to remove any english stop words, punctuations, hyperlinks and symbols. In addition, any words that did not constitute as natural disaster were also muted that would have potentially skewed our classifier.

## Visualization 

Below is a word cloud image that shows frequency of words that are classified as natural disaster tweets in the cleaned training dataset
![disaster-wordcloud](images/disaster_wordcloud.jpg?raw=true "Disaster Tweet wordcloud")

## Modeling and evaluation 

Bag-of-words and TF-IDF model was used to generate ngram vectors from the corpus and then used linear regression as well as ensemble classifiers such as RandomForest and GradientBoost to classify the tweets.  
The best results were from our uni-bigram Bag-of-Words model with RandomForest classifier had an accuracy of ~78\%. It had the lowest false positive rate and better performance in detecting true positives. 

## Limitations and Future directions

- Class imbalance 
