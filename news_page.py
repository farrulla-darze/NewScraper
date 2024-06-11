import requests
from bs4 import BeautifulSoup, Tag
import json
from json.decoder import JSONDecodeError
from tqdm import tqdm


with open('links.txt', 'r') as links_file:
    links = links_file.readlines()
    total_links = len(links)
    print(f"Total links: {total_links}")

# Process each link
data = []

for link in tqdm(links, total=total_links, leave=False):
        url = link.strip()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get title
        title_element = soup.select_one('h1.content-head__title')
        if title_element is None:
            print(f"Title not found in {url}")
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
            continue
        else:
            datetime = time_element.get('datetime')  # Get the value of the datetime attribute
        #print(datetime)

        # Find the <article> tag and get its content
        article_tag = soup.find('article')
        if article_tag is None:
            print(f"Article tag not found in {url}")
            continue  # Skip this URL if the article tag is not found

        article_content = "".join([child.get_text(strip=True) for child in article_tag.contents])

        # join title, subtitle, info, datetime and article_content
        full_content = title + "\n" + subtitle + "\n" + info + "\n" + datetime + "\n" + article_content

               
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
        data.append(new_data)

# Write all data to saida.json
with open('news_content.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

