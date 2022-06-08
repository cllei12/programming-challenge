# programming-challenge
Summer 2022 Programming Challenge

The specific task will be to create a pipeline that collects and analyzes news articles from the web. Given a short list of curated websites, your script should be able to collect the latest news articles (via web scraping) and run them through some basic sentiment analysis.

## Create a enviroment

Created by conda with Python 3.8+

```python
conda create -n text python=3.8
conda activate text
```


## Collect latest news via web scraping

Collect 10 most recent articles from https://www.aljazeera.com/where/mozambique/ Include collected articles as a JSON file in your submission repository. The format of the file is up to you, describe this format in your summary (see step 6).


### format of the file
- [x] collect articles as a JSON file in your submission repository. The format of the file is up to you, describe this format in your summary (see step 6).

```
{
    "article_0":{
        "article_link": home_link + article_link,
        "header": header,
        "sub_header": sub_header,
        "img_link": img_link,
        "img_cap": img_cap,
        "date": date,
        "content": contents
    },
    "article_1":{
        ...
    },
    ...
}
```

## Pre-process
Pre-process the data. Remove anything that is not part of the article itself, e.g. comments, publishing date, images, etc. Make sure the articles are in English and can be processed by the sentiment analysis library. Use the tqdm package to display progress on the terminal. Use PEP8 Style Guide for your python code.

## Requirements

Create a GitHub repo with a Python 3.8+ environment for this project and start a requirements.txt file to capture the external libraries/packages required to run your code. 

If you use a virtual environment such as conda, specify that in the summary (see step 6). This repository is where you can upload all the files pertaining to your submission.
