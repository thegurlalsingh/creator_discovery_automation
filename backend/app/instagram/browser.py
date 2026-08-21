from playwright.sync_api import sync_playwright

from app.config.constants import CHROME_EXECUTABLE_PATH, USER_AGENT


class InstagramBrowser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True, executable_path=(CHROME_EXECUTABLE_PATH)
        )

        self.page = self.browser.new_page(user_agent=USER_AGENT)

        return self.page

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()
