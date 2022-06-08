import json
from tqdm import tqdm
from scraper import fetch_article_links, collect_articles

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

import pandas as pd
import plotly.graph_objects as go

import argparse
import pprint


def preprocess(num_articles = 10, out_path = "articles.json"):
    # collect articles
    article_links = fetch_article_links(num_articles)
    collect_articles(article_links, out_path)
    
    with open(out_path, "r") as f:
        articles = json.load(f)
        
    return articles
        
def sentiment_analysis_vader(articles: dict, res_path="sentiment_analysis.json"):
    # nltk and VADER
    nltk.download('vader_lexicon')
    
    sentiment_results = {}
    sia = SentimentIntensityAnalyzer()
    for key in tqdm(articles, desc="Sentiment Analysis"):
        content = articles[key]["content"]
        sentiment_results[key] = sia.polarity_scores(content)
        compound_score = sentiment_results[key]['compound']
        # positive sentiment: compound score >= 0.05
        if compound_score >= 0.05:
            sentiment_results[key]['label'] = "positive"
        # neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
        elif compound_score > -0.05 and compound_score < 0.05:
            sentiment_results[key]['label'] = "neutral"
        # negative sentiment: compound score <= -0.05
        elif compound_score <= -0.05:
            sentiment_results[key]['label'] = "negative"
            
    json_object = json.dumps(sentiment_results, indent = 4)
    with open(res_path, "w") as out_file:
        out_file.write(json_object)
         
    return sentiment_results

def sentiment_analysis_bert(articles: dict, res_path="sentiment_analysis.json"):
    # Hugging Face pipeline: DistilBERT
    sentiment_results = {}
    pipe = pipeline("sentiment-analysis")
    for key in tqdm(articles, desc="Sentiment Analysis"):
        content = articles[key]["content"]
        try:
            sentiment_results[key] = pipe(content)[0]  # output is List[dict]
        except:
            print("Too many tokens (> 512) for DistilBERT, so only the 1/3 article is used.")
            sentiment_results[key] = pipe(content[:len(content)//3])[0]
        
    json_object = json.dumps(sentiment_results, indent = 4)
    with open(res_path, "w") as out_file:
        out_file.write(json_object)
         
    return sentiment_results

def visualize_vader(sentiment_results):
    df = pd.DataFrame(sentiment_results).T

    x_labels = []
    for i in range(0, 10):
        x_labels.append(f'article_{i}')
        
    fig = go.Figure()
    fig.add_trace(go.Bar(x = x_labels, y = df['neg'], name = 'Negative'))
    fig.add_trace(go.Bar(x = x_labels, y = df['neu'], name = 'Neutral'))
    fig.add_trace(go.Bar(x = x_labels, y = df['pos'], name= 'Positive'))
    fig.add_trace(go.Bar(x = x_labels, y = df['compound'], name= "Compound",))
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode = 'group', xaxis_tickangle = -45)
    fig.show()
    
def visualize_bert(sentiment_results):
    df = pd.DataFrame(sentiment_results).T
    df['score'] = df['score'].where(df['label']=='POSITIVE', -df['score'])
    
    x_labels = []
    for i in range(0, 10):
        x_labels.append(f'article_{i}')
        
    fig = go.Figure()
    fig.add_trace(go.Bar(x = x_labels, y = df['score'], name = 'score'))
    fig.update_layout(barmode = 'group', xaxis_tickangle = -45)
    fig.show()
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_articles", type=int, default=10, 
                        help="input the number of articles you want collect")
    parser.add_argument("--out_path", type=str, default='articles.json', 
                        help="json path to store scraped articles")
    parser.add_argument("--method", type=str, default='VADER', choices=['VADER', 'DistilBERT'],
                        help="choose one method to analyze sentiment")
    parser.add_argument("--res_path", type=str, default='sentiment_analysis.json', 
                        help="json path to store the results fo sentiment analysis")
    args = parser.parse_args()
    
    articles = preprocess(args.num_articles, args.out_path)
    
    if args.method == "VADER":
        sentiment_results = sentiment_analysis_vader(articles, args.res_path)
        visualize_vader(sentiment_results)
    if args.method == "DistilBERT":
        sentiment_results = sentiment_analysis_bert(articles, args.res_path)
        visualize_bert(sentiment_results)
    
    pprint.pprint(sentiment_results)
    
        
    
