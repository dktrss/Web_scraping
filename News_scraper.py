import requests
from bs4 import BeautifulSoup

url = 'https://thehackernews.com/'
response = requests.get(url)


soup = BeautifulSoup(response.content, 'html.parser')

titles = soup.find_all(class_='home-title')
descriptions = soup.find_all(class_='home-desc')
story_links = soup.find_all(class_='story-link')


for i, (title, desc) in enumerate(zip(titles, descriptions), 1):
    print(f"{i}. {title.text.strip()}")
    print(f"   {desc.text.strip()}\n")


try:
    choice = int(input("Enter the number of the article to extract text from (0 to exit): "))
    if choice > 0 and choice <= len(story_links):
        link = story_links[choice - 1]['href']

        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')

        title = titles[choice - 1].text.strip()
        print("\n" + title.upper() + "\n")

        article_body = article_soup.find('div', class_='articlebody')

        if article_body:
            for tag in article_body.find_all(['p', 'strong']):
                print(tag.text.strip())
            
            for ul in article_body.find_all('ul'):
                for li in ul.find_all('li'):
                    print(f"- {li.text.strip()}")
        else:
            print("Article body not found.")
    elif choice == 0:
        print("Exiting...")
    else:
        print("Invalid input. Exiting...")
except ValueError:
    print("Please enter a valid number.")