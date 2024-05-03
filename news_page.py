import requests
from bs4 import BeautifulSoup, Tag
import json
from json.decoder import JSONDecodeError

# existing JSON file content
existing_data = []

with open('links.txt', 'r') as links:
    for link in links:
        url = link.strip()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get title
        title_element = soup.select_one('h1.content-head__title')
        if title_element is None:
            continue # Skip this URL

        title = title_element.text
        print(title)

        # Get Subtitle
        subtitle_element = soup.select_one('h2.content-head__subtitle')
        if subtitle_element is None:
            subtitle = ""
        else:
            subtitle = subtitle_element.text
        #print(subtitle)

        # Get content publication data
        info_element = soup.select_one('p.content-publication-data__from')
        if info_element is None:
            info = "Sem informações"
        else:
            info = info_element.text
        #print(info)

        # datetime to metadata
        time_element = soup.select_one('time[itemprop="datePublished"]')
        if time_element is None:
            datetime = "Sem data de publicação"
        datetime = time_element.get('datetime')  # Get the value of the datetime attribute
        #print(datetime)

        # Find the <article> tag
        article_tag = soup.find('article')

        # Get its children elements
        article_contents = article_tag.contents

        # Loop through the children elements and print their text content
        article_content = ""
        for child in article_contents:
            # concatenate the content
            article_content += child.get_text(strip=True)

        # join title, subtitle, info, datetime and article_content
        full_content = title + "\n" + subtitle + "\n" + info + "\n" + datetime + "\n" + article_content

        # Read existing data from saida.json
        try:
            with open('news_content.json', 'r', encoding="utf-8") as file:
                existing_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            pass

        len(existing_data)
        # save the content to a json file
        new_data = {
            'content': full_content,
            'metadata': {
                'source': url,
                'title': title,
                'subtitle': subtitle,
                'info': info,
                'datetime': datetime,
            }    
        }

        # Append the new data to the existing data
        existing_data.append(new_data)

        # Write all data to saida.json
        with open('news_content.json', 'w', encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
