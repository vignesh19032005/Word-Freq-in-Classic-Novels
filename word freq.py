import requests
from bs4 import BeautifulSoup
import nltk
import random
from collections import Counter

# Get top 10 popular books
url = 'https://www.gutenberg.org/ebooks/search/?sort_order=downloads'
response = requests.get(url)

if response.status_code == 200:
  soup = BeautifulSoup(response.text, 'html.parser')
  popular_books = [
      {'id': book.find('a', class_='link')['href'].split('/')[-1],
       'title': book.find('span', class_='title').text.strip()}
      for book in soup.find_all('li', class_='booklink')[:10]
  ]
else:
  print(f"Error retrieving popular books: {response.status_code}")

# Choose a random book and download its text
chosen_book = random.choice(popular_books)
book_url = f"https://www.gutenberg.org/files/{chosen_book['id']}/{chosen_book['id']}-h/{chosen_book['id']}-h.htm"
book_response = requests.get(book_url)

if book_response.status_code == 200:
  # Process book text
  html = book_response.text
  soup = BeautifulSoup(html, 'html.parser')
  text = soup.get_text()

  # Tokenize, lowercase, and remove stopwords
  tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
  tokens = tokenizer.tokenize(text.lower())
  words = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]

  # Count word frequencies
  word_counts = Counter(words)

  # Print the 20 most frequent words
  print("Top 20 Most Frequent Words:")
  print(word_counts.most_common(20))
else:
  print(f"Error downloading book: {book_response.status_code}")