import spacy
import requests
from Stock_Purchase import *

# Sample sentence
def stockfinder(sentence):
    ticker_list = []
    # Load spaCy's English model
    nlp = spacy.load("en_core_web_sm")

    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Extract named entities (companies are often labeled as "ORG" in spaCy)
    stock_names = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

    # Delete duplicate tickers that are mentioned more than once
    stock_names = list(set(stock_names))

    found_ticker = False  # Track if any stock was valid

    print("Stock names found:", stock_names)
    for x in stock_names:
        if get_ticker(x): # If a valid ticker is found
            found_ticker = True

    return found_ticker
            
# Find ticker off company name
def get_ticker(company_name):
    yfinance_url = "https://query2.finance.yahoo.com/v1/finance/search"
    USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    ]

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    try:
        res = requests.get(url=yfinance_url, params=params, headers=headers)
        res.raise_for_status() # Raise an error for HTTP issues (e.g., 404, 500)
        data = res.json()

        #If no ticker was found return that information to the user
        if "quotes" not in data or not data["quotes"]:
            print(f"No ticker found for: {company_name}")
            return False

        #If a ticker is found let the user know and procced
        company_code = data['quotes'][0]['symbol']
        print(f"Ticker found for: {company_name}")
        return Stock_info(company_code)
    
        #Different error catchers
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching data: {e}")
        return False
    except KeyError:
        print("⚠️ Unexpected response format.")
        return False