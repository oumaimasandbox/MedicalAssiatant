from selenium import webdriver
from bs4 import BeautifulSoup
import json

# Set up Selenium WebDriver (requires a browser driver like ChromeDriver)
driver = webdriver.Chrome()  # Make sure ChromeDriver is installed and in PATH
driver.get("https://www.who.int/news-room/questions-and-answers")

# Wait for the page to load fully
driver.implicitly_wait(10)

# Use BeautifulSoup on the page source
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Update scraping logic based on the page structure
questions = soup.find_all("h3")
answers = soup.find_all("div", class_="answer")

medical_data = []
for q, a in zip(questions, answers):
    medical_data.append({"content": f"{q.text.strip()} {a.text.strip()}"})

# Save the data as JSON
with open("medical_data.json", "w") as file:
    json.dump(medical_data, file, indent=4)