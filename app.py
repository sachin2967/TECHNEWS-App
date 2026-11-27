import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for

load_dotenv()

app = Flask(__name__)

BASE_URL = "https://www.ndtv.com"
SECTIONS = ["LATEST", "INDIA", "CITIES", "WORLD-NEWS", "EDUCATION", "SCIENCE", "PEOPLE"]
REQUEST_TIMEOUT = (5, 15)


def fetch_headlines(section):
    """Fetch up to eight article blurbs from the selected NDTV section."""
    if section not in SECTIONS:
        raise ValueError("Unsupported news section")

    response = requests.get(
        f"{BASE_URL}/{section}",
        headers={"User-Agent": "TechNewsPortfolioDemo/1.0"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("div", class_="news_Itm", limit=8)
    blurbs = []
    for article in articles:
        description = article.select_one(".news_Itm-cont p")
        if description:
            blurb = description.get_text(" ", strip=True)
            if blurb:
                blurbs.append(blurb)

    return "\n".join(blurbs) if blurbs else "No headlines were found for this section."


def get_random_image():
    """Use Unsplash when configured; otherwise serve the bundled fallback image."""
    fallback = url_for("static", filename="images/download.jpg")
    api_key = os.getenv("UNSPLASH_ACCESS_KEY") or os.getenv("unsplash_api_key")
    if not api_key:
        return fallback

    try:
        response = requests.get(
            "https://api.unsplash.com/photos/random",
            params={"client_id": api_key},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        image_url = response.json().get("urls", {}).get("regular")
        return image_url or fallback
    except (requests.RequestException, ValueError, TypeError):
        return fallback


@app.route("/", methods=["GET", "POST"])
def index():
    raw_section = request.form.get("section_number", "0") if request.method == "POST" else "0"
    try:
        section_index = int(raw_section)
    except (TypeError, ValueError):
        section_index = 0

    if not 0 <= section_index < len(SECTIONS):
        section_index = 0

    selected_section = SECTIONS[section_index]
    try:
        news = fetch_headlines(selected_section)
    except requests.RequestException:
        news = "Headlines are temporarily unavailable. Please try again later."

    return render_template(
        "index.html",
        News=news,
        header=selected_section,
        image_url=get_random_image(),
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG") == "1",
    )
