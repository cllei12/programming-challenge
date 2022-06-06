'''
Collect 10 most recent articles from https://www.aljazeera.com/where/mozambique/ 

Include collected articles as a JSON file in your submission repository. 

The format of the file is up to you, describe this format in your summary (see step 6).
'''

from typing import List
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path


def fetch_article_links(link: str, num_articles: int) -> List[str]:
    r = requests.get(link)
    
    print(f"Status code: {r.status_code}")
    print(f"Content type: {r.headers['content-type']}")
    print(f"Encoding: {r.encoding}")  # utf-8
    
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # find all <article> tags
    article_tags = soup.find_all(
        lambda tag: tag.name=="article" and 'gc--type-episode' not in tag.get("class")  # remove video post
    )
    assert num_articles <= len(article_tags)
    
    # find all <article> links
    article_links = []
    for i in range(num_articles):
        article_links.append(article_tags[i].a['href'])  # <article> -> <a href= "">
    
    return article_links

def collect_articles(article_links: List[str]):
    
    for i, article_link in enumerate(article_links):
        print(article_link)
        home_link = "https://www.aljazeera.com"
        r = requests.get(( home_link + article_link))
        
        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')
        main_content = soup.find(id='main-content-area')
        
        header = main_content.find("header", class_="article-header").h1.text
        sub_header = main_content.find("header", class_="article-header").p.text
        img_link = home_link + soup.find("img")['src']
        img_cap = main_content.find("figcaption").text
        date = main_content.find("div", class_="article-dates").span.text
        
        raw_content = main_content.find("div", class_="wysiwyg wysiwyg--all-content css-1ck9wyi")
        content = []
        for p in raw_content.find_all('p'):
            content.append(p.text)
        content = "\n".join(content)
        
        dictionary = {
            "header": header,
            "sub_header": sub_header,
            "img_link": img_link,
            "img_cap": img_cap,
            "date": date,
            "content": content
        }
        
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 4)
  
        # Writing to sample.json
        out_dir = "./articles/"
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        with open(out_dir + f"article_{i}.json", "w") as outfile:
            outfile.write(json_object)

if __name__ == "__main__":
    home = 'https://www.aljazeera.com/where/mozambique/'
    num_articles = 10
    article_links = fetch_article_links(home, num_articles)
    # print(article_links)
    
    collect_articles(article_links)
    