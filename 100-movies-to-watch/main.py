import requests
from bs4 import BeautifulSoup

url = "https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

all_films = soup.findAll('h2')

#creating a list of movies and remove the first item, that was a topic text.
films = [text.getText() for text in all_films]
films.pop(0)
reversed_list = films[::-1]

# creating a new .txt file with the list of movies
with open("output.txt", "w") as file:
    for item in reversed_list:
        file.write(f"{item}\n")  # Escreve cada elemento em uma nova linha
print(reversed_list)


