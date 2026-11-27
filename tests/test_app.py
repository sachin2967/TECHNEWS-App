"""Offline tests for TechNews request validation and fallbacks."""

import unittest
from unittest.mock import patch

from app import app, fetch_headlines


class TechNewsTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_home_page_uses_latest_by_default(self):
        with patch("app.fetch_headlines", return_value="Example headline"), patch(
            "app.get_random_image", return_value="/static/images/download.jpg"
        ) as image:
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Example headline", response.data)
        image.assert_called_once()

    def test_invalid_section_value_falls_back_to_latest(self):
        with patch("app.fetch_headlines", return_value="Latest headline") as fetch, patch(
            "app.get_random_image", return_value="/static/images/download.jpg"
        ):
            response = self.client.post("/", data={"section_number": "999"})

        self.assertEqual(response.status_code, 200)
        fetch.assert_called_once_with("LATEST")

    def test_scraper_uses_a_timeout_and_parses_article_blurbs(self):
        html = b'<div class="news_Itm"><div class="news_Itm-cont"><p>Example story</p></div></div>'
        response_obj = type("Response", (), {"content": html, "raise_for_status": lambda self: None})()
        with patch("app.requests.get", return_value=response_obj) as get:
            result = fetch_headlines("LATEST")

        self.assertEqual(result, "Example story")
        self.assertEqual(get.call_args.kwargs["timeout"], (5, 15))

    def test_invalid_section_is_rejected(self):
        with self.assertRaises(ValueError):
            fetch_headlines("UNKNOWN")


if __name__ == "__main__":
    unittest.main()
