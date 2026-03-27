import json
import os
import xml.etree.ElementTree as ET

import requests
from dotenv import load_dotenv
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

load_dotenv()


class GoogleIndexer:
    """
    A tool to batch submit URLs to Google Indexing API.
    Used for accelerating page indexing for static sites.
    """

    def __init__(self, service_account_file):
        """
        Initialize the indexer with service account credentials.
        """
        self.endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        self.scopes = ["https://www.googleapis.com/auth/indexing"]
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=self.scopes
        )
        self.session = AuthorizedSession(self.credentials)

    def fetch_urls_from_sitemap(self, sitemap_url):
        """
        Extract all <loc> tags from a given sitemap.xml URL.
        """
        response = requests.get(sitemap_url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        # Handle XML namespaces usually present in sitemaps
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        urls = [loc.text for loc in root.findall(".//ns:loc", namespace)]
        return urls

    def notify_url(self, url, action="URL_UPDATED"):
        """
        Notify Google about a specific URL update or creation.
        """
        payload = {"url": url, "type": action}

        response = self.session.post(self.endpoint, data=json.dumps(payload))
        return response.status_code, response.json()

    def batch_index(self, sitemap_url):
        """
        Orchestrate the fetching and submission of all URLs in a sitemap.
        """
        print(f"Starting discovery: {sitemap_url}")
        urls = self.fetch_urls_from_sitemap(sitemap_url)
        print(f"Found {len(urls)} URLs. Starting submission...")

        for url in urls:
            status, result = self.notify_url(url)
            if status == 200:
                print(f"Successfully notified: {url}")
                print(f"result: {result}")
            else:
                print(f"Failed to notify {url}: {result}")


if __name__ == "__main__":
    KEY_FILE = os.environ.get("KEY_FILE")
    SITEMAP_URL = "https://zts0hg.github.io/codexspec/sitemap.xml"

    indexer = GoogleIndexer(KEY_FILE)
    indexer.batch_index(SITEMAP_URL)
