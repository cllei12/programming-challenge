from typing import List
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse


def fetch_article_links(num_articles: int):
    """Fetch the most recent {num_articles} news article URLs.

    Args:
        num_articles (int): the number of collected articles

    Returns:
        List[str]: a list of news article URLs
    """
    home_link = "https://www.aljazeera.com/where/mozambique"
    r = requests.get(home_link)
    print(f"Status code: {r.status_code}")
    print(f"Content type: {r.headers['content-type']}")
    
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
  
    # find all <article> tags, ignoring video posts
    article_tags = soup.find_all(
        lambda tag: tag.name=="article" and 'gc--type-episode' not in tag.get("class")  
    )
    assert num_articles <= len(article_tags)
   
    # find all <article> links
    article_links = []
    for i in range(num_articles):
        article_links.append(article_tags[i].a['href'])  # <article> -> <a href= "">
  
    return article_links

def collect_articles(article_links: List[str], out_path="articles.json"):
    """Scrape news articles by the URLs in the list {article_links}.

    Args:
        article_links (List[str]): a list of news article URLs
        out_path (str, optional): the JSON file path for storing scraped articles. 
                                  Defaults to "articles.json".
    """
    home_link = "https://www.aljazeera.com"
    articles = {}
  
    for i, article_link in tqdm(enumerate(article_links), 
                                desc="Collecting articles", 
                                total=len(article_links)):
        r = requests.get((home_link + article_link))
        
        # Parsing the HTML
        soup = BeautifulSoup(r.content, 'html.parser')
        main_content = soup.find(id='main-content-area')
        
        # article info
        header = main_content.find("header", class_="article-header").h1.text
        sub_header = main_content.find("header", class_="article-header").p.text
        img_link = home_link + soup.find("img")['src']
        img_cap = main_content.find("figcaption").text
        date = main_content.find("div", class_="article-dates").span.text
        
        # article content
        raw_content = main_content.find(
            lambda tag: tag.name=="div" and 'wysiwyg' in tag.get("class")
        )
        content = []
        for p in raw_content.find_all('p'):
            content.append(p.text)
        content = "\n".join(content)
        
        dictionary = {
            "article_link": home_link + article_link,
            "header": header,
            "sub_header": sub_header,
            "img_link": img_link,
            "img_cap": img_cap,
            "date": date,
            "content": content
        }
            
        articles[f'article_{i}'] = dictionary
       
    json_object = json.dumps(articles, indent=4)
    with open(out_path, "w") as out_file:
        out_file.write(json_object)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_articles", type=int, default=10, 
                        help="input the number of articles you want collect")
    parser.add_argument("--out_path", type=str, default='articles.json', 
                        help="json path to store scraped articles")
    args = parser.parse_args()
    
    article_links = fetch_article_links(args.num_articles)
    collect_articles(article_links)
    