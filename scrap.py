from itertools import zip_longest
from bs4 import BeautifulSoup
import requests
import lxml
import csv

# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3",
# }

##Downloading HTML from website (In case site blocks us, because of scraping)

# for page in range(1, 12):
#     response = requests.get(f"https://www.trustpilot.com/review/food.bolt.eu?page={page}", headers=headers)

#     soup = BeautifulSoup(response.text, "lxml").prettify()

#     with open(f"review_site_{page}.html", "w", encoding="utf-8") as file:
#         file.write(soup)

for i in range(1,12):
    with open(f"review_site_{i}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    main = soup.find('section', class_="styles_reviewListContainer__2bg_p")

    # Names
    block_reviewer_name = main.find_all('span', class_="typography_heading-xs__osRhC typography_appearance-default__t8iAq")
    reviewers_names = [ i.text.strip() for i in block_reviewer_name ]

    # rating
    block_rating = main.find_all('div', class_="star-rating_starRating__sdbkn star-rating_medium__Oj7C9")
    reviewers_rating = [ i.find('img').get('alt').strip() for i in block_rating ]

    # Headers
    block_reviewer_header = main.find_all('h2', class_="typography_heading-xs__osRhC typography_appearance-default__t8iAq")
    reviewers_headers = [ i.text.strip() for i in block_reviewer_header ]

    # Comments
    block_comment = main.find_all('p', class_="typography_body-l__v5JLj typography_appearance-default__t8iAq")
    reviewers_comments = [ i.text.strip() for i in block_comment ] 

    # Date
    block_date = main.find_all('div', class_="styles_reviewContent__tuXiN")
    reviewers_dates = [ i.find('span', class_="typography_body-m__k2UI7 typography_appearance-subtle__PYOVM").text.strip() for i in block_date ]

    rows = zip_longest(
        reviewers_names,
        reviewers_rating,
        reviewers_headers,
        reviewers_comments,
        reviewers_dates,
        fillvalue="N/A"
    )

    # CSV
    with open("reviews.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Rating", "Header", "Comment", "Date"])
        writer.writerows(rows)

