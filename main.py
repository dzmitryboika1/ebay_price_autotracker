import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv


# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'prcIsum'}).get_text()
        price = float(price.split('$')[1].replace(',', '.'))

    except AttributeError:
        price = ""

    return price


# Function to extract Product Price
def get_title(soup):
    try:
        title = soup.select_one('#LeftSummaryPanel > div.vi-swc-lsp > div:nth-child(1) > '
                                'div > h1 > span.ux-textspans.ux-textspans--BOLD').get_text()
    except AttributeError:
        title = ""

    return title


# Function to send notification email if price lower than set
def send_email(email, password, recipient, title, price, url):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        msg = f"Subject:EBAY Price Alert\n\n{title} is now ${format(price, '.2f')}\n{url}"
        connection.sendmail(
            from_addr=email,
            to_addrs=recipient,
            msg=msg.encode("utf8")
        )


if __name__ == '__main__':

    load_dotenv()
    # sign in and recipient emails data
    my_email = os.environ["MY_EMAIL"]
    password = os.environ["PASSWORD"]
    recipient = os.environ["RECIPIENT"]
    # set expected price
    SET_PRICE = 250

    # The webpage URL
    URL = "https://www.ebay.com/itm/354213929437?epid=" \
          "2323899370&hash=item5278cba1dd%3Ag%3AAgUAAOSwAB9i8hQY&LH_BIN=1&LH_ItemCondition=1000"

    # HTTP Request
    webpage = requests.get(URL)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    current_price = get_price(soup)
    title = get_title(soup)
    print(f"{title} - {current_price}")

    if current_price <= SET_PRICE:
        send_email(email=my_email, password=password, recipient=recipient,
                   title=title, price=current_price, url=URL)
