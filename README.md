# TechNews

A small Flask app that shows the latest headlines for a chosen NDTV section, with a random
background photo from Unsplash.

## How it works

- Fetches the selected NDTV section page (Latest, India, Cities, World News, Education,
  Science, People) and extracts the first eight article blurbs with BeautifulSoup.
- Requests a random photo from the Unsplash API and falls back to a static image if the
  request fails.
- Renders both with a Jinja template (`templates/index.html`, assets in `static/`).

## Setup

Requires Python 3.10+ and a free [Unsplash developer key](https://unsplash.com/developers).

```bash
git clone https://github.com/sachin2967/TECHNEWS-App.git
cd TECHNEWS-App
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env        # then put your key in unsplash_api_key
flask --app app run
```

Open http://127.0.0.1:5000.

## Configuration

| Variable | Purpose |
| --- | --- |
| `unsplash_api_key` | Unsplash access key, read from `.env`. Never commit this file. |

## Limitations

- Scrapes a third-party site whose HTML can change without notice, which would break the
  parser. Respect the site's terms of use; this is a learning project, not a news product.
- No caching, retries or error handling for failed network calls.

## License

MIT
