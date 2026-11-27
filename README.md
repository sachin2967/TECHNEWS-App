# TechNews

A small Flask application that presents headline blurbs from selected NDTV sections, with an optional random Unsplash background image.

**Project type:** learning/demo application. It scrapes a third-party website; it is not an official NDTV product or a production news aggregator.

## Features

- Select Latest, India, Cities, World News, Education, Science or People
- Extracts up to eight visible article blurbs from the selected section using BeautifulSoup
- Uses a random Unsplash image when an access key is configured
- Uses a bundled local image when Unsplash is not configured or unavailable
- Displays a simple shareable news-card layout

## Local setup

Requires Python 3.10+.

```bash
git clone https://github.com/sachin2967/TECHNEWS-App.git
cd TECHNEWS-App
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
flask --app app run
```

Open http://127.0.0.1:5000. The app works without an Unsplash key and will use the bundled fallback image.

## Configuration

| Variable | Purpose |
| --- | --- |
| `UNSPLASH_ACCESS_KEY` | Optional Unsplash access key. Store it in local `.env`; never commit the real value. |
| `FLASK_DEBUG` | Set to `1` only for local debugging. Debug mode is off by default. |
| `PORT` | Optional local server port; defaults to `5000`. |

The legacy `unsplash_api_key` variable name is still accepted for existing local `.env` files.

## Limitations and responsible use

- NDTV page structure may change at any time and break the parser.
- External requests use timeouts and display a fallback message when NDTV is unavailable.
- There is no caching; repeated requests may fetch the same section multiple times.
- Respect the source website's terms and robots policy. This is a learning project, not a commercial feed or an official news API.
- The random Unsplash image is decorative and is not necessarily related to the news stories.

## License

MIT
