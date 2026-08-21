import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from app.config.constants import USER_AGENT, CHROME_EXECUTABLE_PATH

load_dotenv()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

class InstagramBrowser:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True,
            executable_path=CHROME_EXECUTABLE_PATH
        )

        # One context = shared authentication
        self.context = self.browser.new_context(
            user_agent=USER_AGENT
        )

        self.page = self.context.new_page()

        self.login()

        return self.page

    def login(self):

        if not INSTAGRAM_USERNAME:
            raise ValueError(
                "INSTAGRAM_USERNAME is not set in environment variables."
            )

        if not INSTAGRAM_PASSWORD:
            raise ValueError(
                "INSTAGRAM_PASSWORD is not set in environment variables."
            )

        print("\n" + "=" * 70)
        print("INSTAGRAM AUTHENTICATION")
        print("=" * 70)

        self.page.goto(
            "https://www.instagram.com/accounts/login/",
            wait_until="domcontentloaded",
            timeout=60_000
        )

        self.page.wait_for_timeout(5000)

        if "/accounts/login" not in self.page.url:

            print("Instagram session already active.")
            return

        print("Instagram login page loaded.")

        username_selectors = [
            'input[name="username"]',
            'input[name="email"]',
            'input[autocomplete="username"]',
            'input[type="text"]',
        ]

        username_input = None

        for selector in username_selectors:

            try:
                locator = self.page.locator(selector).first

                if locator.is_visible(timeout=2000):
                    username_input = locator
                    break

            except Exception:
                continue

        if username_input is None:
            raise RuntimeError(
                "Could not find Instagram username input."
            )


        password_selectors = [
            'input[name="password"]',
            'input[name="pass"]',
            'input[autocomplete="current-password"]',
            'input[type="password"]',
        ]

        password_input = None

        for selector in password_selectors:

            try:
                locator = self.page.locator(selector).first

                if locator.is_visible(timeout=2000):
                    password_input = locator
                    break

            except Exception:
                continue

        if password_input is None:
            raise RuntimeError(
                "Could not find Instagram password input."
            )

        username_input.fill(INSTAGRAM_USERNAME)
        password_input.fill(INSTAGRAM_PASSWORD)

        login_button = self.page.locator(
            '[role="button"][aria-label="Log In"]'
        ).first

        if not login_button.count():
            raise RuntimeError(
                "Could not find Instagram login button."
            )

        login_button.wait_for(
            state="visible",
            timeout=10_000
        )

        login_button.click()

        print("Instagram login submitted.")

        self.page.wait_for_timeout(10_000)

        if "/accounts/login" in self.page.url:

            try:
                page_text = self.page.locator("body").inner_text()

            except Exception:
                page_text = ""

            if "incorrect" in page_text.lower():
                raise RuntimeError(
                    "Instagram login failed: incorrect credentials."
                )

            if "suspicious" in page_text.lower():
                raise RuntimeError(
                    "Instagram requires additional verification."
                )

            raise RuntimeError(
                "Instagram login did not complete."
            )

        print("Instagram authentication successful.")

    def create_page(self):

        if not self.context:
            return None

        return self.context.new_page()

    def close(self):

        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()
