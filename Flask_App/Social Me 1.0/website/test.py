import requests
from bs4 import BeautifulSoup

username = "instagram_username"
url = f"https://www.instagram.com/justanotherv700/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Look for the meta tag containing followers
meta = soup.find("meta", attrs={"name": "description"})
content = meta["content"]
followers = content.split(",")[0]  # Extract followers
print(f"Followers: {followers}")
