# NewScraper

Is a web crawler focused on scraping the content of a famous news website from Brazil.

- globo.com: is a general news channel
- ge.com: is focused in sports news

The goal is to go to the main page that has some infinit scrolling (lazy loading) of content and do it until we reach a considerable amount of data.

## Process

1. Go to the webpage
2. Scroll down until reached a critical amount of data
3. Get the links for the news content
4. Go to the news content webpage
5. Extract all the text from there

## Installing

**Don't** forget to start your virtual environment first

**venv** - `python -m venv venv`
To activate the virtual environment
`source venv/bin/activate`

After installing the requirements.txt `pip install -r requirements.txt` run on your terminal`playwright install`
