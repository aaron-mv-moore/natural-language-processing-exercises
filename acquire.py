# imports 
import pandas
from requests import get
import re
from bs4 import BeautifulSoup

def get_blog_links():
    '''
    Gets a list of article links from the codeup blog
    Modules:
    import pandas as pd
    from requests import get
    from bs4 import BeautifulSoup
    '''
    # getting a response
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the pyhon-requests default user-agent
    response = get(url, headers=headers)
    response
    
    # getting soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # checking out the headers
    all_h2 = soup.find_all(['h2'])

    # creating list to hold the 'a'
    all_a = []

    # for each header2 in list of header2's
    for h2 in all_h2:

        # find the 'a' and add it to the list of all_s
        all_a.append(h2.find('a'))

    # show me the list of all_a
    all_a.remove(None)

    # initialize link lis
    links_from_blog = []

    # for each element in the list of a
    for i in range(len(all_a)-1):

        # add the links to a list for links
        links_from_blog.append(all_a[i]['href'])

    # show me the links from the main blog page
    return links_from_blog 

def get_title_article_text(url):
    '''
    Takes a url for the codeup blog and returns the title and article in string format
    Modules:
    from requests import get
    from bs4 import BeautifulSoup
    '''
    # set headers
    headers = {'User-Agent': 'Codeup Data Science'}
    
    # get the url responses
    response = get(url, headers=headers)
    
    # get soup from response
    soup = BeautifulSoup(response.text)
    
    # get the article
    article = soup.find('div', id='main-content')
    
    # get the title
    title = soup.find('title')

    # exti function and return title and article text
    return title.text, article.text

def get_blog_articles():
    '''
    Gets a list of blog links, creates dictionary of dictionaries that hold blog tiltles and blog articles
    Modules:
    from acquire import get_blog_links
    from acquire import get_title_article_text
    '''
    # get blog links from main codeup blog page
    blog_links = get_blog_links()
    
    # intialize the dictionary
    blog_articles = {}

    # for each url in the blog links, along with an index
    for i, url in enumerate(blog_links):

        # create a new entry in the dictionary that corresponds with the index
        blog_articles[i] = {'title': get_title_article_text(url)[0], # call function to get the title text (0th item returned) store it as the title value 
         'content': get_title_article_text(url)[1]} # call the function to get the main content text (1st item returns) and store it as the content value

    # exit functyion and returns dictionary of dictionaries 
    return blog_articles


def root_url_to_future():
    '''
    Goes from root url page to read now page with 
    '''

    # getting response
    root_url = 'https://inshorts.com'
    response = get(root_url)

    # getting soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # getting the ending to the url
    url_end = soup.find_all('a')[1]['href']

    # getting the new url
    url = (root_url + url_end)

    # getting new response
    response = get(url)

    # new soup for new response
    soup = BeautifulSoup(response.content, 'html.parser')
    
    return soup



def get_category_url(category):
    '''
    takes in one category and returns a url for webscraping
    '''
    # set the root url
    root_url = 'https://inshorts.com'
    
    # get soup from root url to main page
    soup = root_url_to_future()
    
    # for each item in the 'a' of soup
    for i, k in enumerate(soup.find_all('a')):

        # if 'business' is in the webpage ending 
        if category in soup.find_all('a')[i]['href']:

            # save that webpage ending here (its always the first)
            url_end = soup.find_all('a')[i]['href']

            # break from the loop
            break
            
    # add the url ending to the root url to makle th new url
    url = root_url + url_end
    
    return url


def get_title_content_category(category, url):
    '''
    Takes in a category/topic and a url for the matching page and returns a list of dictionaries for that one category
    
    '''
    # check the reposnse for the new url
    response = get(url)

    # get the soup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # get all the headlines as titles
    titles = soup.find_all('span', itemprop='headline')

    # get all the contents in one variables
    contents =  soup.find_all('div', itemprop='articleBody')

    # intialize a new list
    new_articles = []

    # for each title and content
    for t, c in zip(titles, contents):
        
        # add them to the list as string values in a dictionary
        new_articles.append({'title': t.text,
        'content': c.text,
        'category': category})
    
    # return the list
    return new_articles


def get_news_articles():
    '''
    Gets all ews articles from the website and returns a list of duictionaries with the titles, contents, and categorys
    '''
    # create list of news topics
    topics = ['business', 'sports', 'technology', 'entertainment']
    
    # initialize blank list
    all_articles = []
    
    # for each topic in news topics
    for topic in topics:
        
        # get the topic url from the main page, get the title and contents, and add it to list to combine all resutls into a large list
        all_articles = all_articles + get_title_content_category(topic, get_category_url(topic))
     
    # return all news articles as a list of dictionaries
    return all_articles