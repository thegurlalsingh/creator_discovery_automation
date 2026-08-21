import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from app.config.constants import USER_AGENT


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

INSTAGRAM_USERNAME = os.getenv(
    "INSTAGRAM_USERNAME"
)

INSTAGRAM_PASSWORD = os.getenv(
    "INSTAGRAM_PASSWORD"
)


# ============================================================
# INSTAGRAM BROWSER
# ============================================================

class InstagramBrowser:

    def __init__(self):

        self.playwright = None

        self.browser = None

        self.context = None

        self.page = None


    # ========================================================
    # START BROWSER
    # ========================================================

    def start(self):

        self.playwright = (
            sync_playwright()
            .start()
        )

        # ----------------------------------------------------
        # Launch Chromium
        # ----------------------------------------------------

        self.browser = (
            self.playwright.chromium.launch(
                headless=True
            )
        )

        # ----------------------------------------------------
        # Create ONE browser context
        #
        # All pages created later will use this
        # same authenticated context.
        # ----------------------------------------------------

        self.context = (
            self.browser.new_context(
                user_agent=USER_AGENT
            )
        )

        # ----------------------------------------------------
        # Create initial page
        # ----------------------------------------------------

        self.page = (
            self.context.new_page()
        )

        # ----------------------------------------------------
        # Login to Instagram
        # ----------------------------------------------------

        self.login()

        return self.page


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        if not INSTAGRAM_USERNAME:

            raise ValueError(
                "INSTAGRAM_USERNAME "
                "is not set in .env"
            )

        if not INSTAGRAM_PASSWORD:

            raise ValueError(
                "INSTAGRAM_PASSWORD "
                "is not set in .env"
            )

        print(
            "\n"
            + "=" * 70
        )

        print(
            "INSTAGRAM AUTHENTICATION"
        )

        print(
            "=" * 70
        )

        # ----------------------------------------------------
        # Open Instagram login
        # ----------------------------------------------------

        self.page.goto(
            "https://www.instagram.com/accounts/login/",
            wait_until="domcontentloaded",
            timeout=60_000
        )

        self.page.wait_for_timeout(
            3000
        )

        # ----------------------------------------------------
        # Check whether already logged in
        # ----------------------------------------------------

        if (
            "/accounts/login"
            not in self.page.url
        ):

            print(
                "Instagram session already active."
            )

            return

        print(
            "Logging into Instagram..."
        )

        # ----------------------------------------------------
        # Username
        # ----------------------------------------------------

        self.page.locator(
            'input[name="username"]'
        ).fill(
            INSTAGRAM_USERNAME
        )

        # ----------------------------------------------------
        # Password
        # ----------------------------------------------------

        self.page.locator(
            'input[name="password"]'
        ).fill(
            INSTAGRAM_PASSWORD
        )

        # ----------------------------------------------------
        # Login button
        # ----------------------------------------------------

        self.page.locator(
            'button[type="submit"]'
        ).click()

        # ----------------------------------------------------
        # Wait for login
        # ----------------------------------------------------

        self.page.wait_for_timeout(
            5000
        )

        print(
            f"After login URL: "
            f"{self.page.url}"
        )

        # ----------------------------------------------------
        # Handle possible "Save login info"
        # ----------------------------------------------------

        try:

            save_button = self.page.get_by_role(
                "button",
                name="Not now"
            )

            if save_button.is_visible(
                timeout=3000
            ):

                save_button.click()

                self.page.wait_for_timeout(
                    1500
                )

        except Exception:
            pass

        # ----------------------------------------------------
        # Handle possible notification popup
        # ----------------------------------------------------

        try:

            not_now = self.page.get_by_text(
                "Not Now",
                exact=True
            )

            if not_now.is_visible(
                timeout=3000
            ):

                not_now.click()

                self.page.wait_for_timeout(
                    1000
                )

        except Exception:
            pass

        # ----------------------------------------------------
        # Verify authentication
        # ----------------------------------------------------

        if "/accounts/login" in self.page.url:

            raise RuntimeError(
                "Instagram login failed. "
                "Still on login page."
            )

        print(
            "Instagram authentication successful."
        )

        print(
            "=" * 70
            + "\n"
        )


    # ========================================================
    # CREATE PAGE
    # ========================================================

    def create_page(self):

        if not self.context:

            return None

        # IMPORTANT:
        #
        # This page belongs to the SAME context
        # that was authenticated in start().
        #

        return self.context.new_page()


    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        if self.context:

            self.context.close()

        if self.browser:

            self.browser.close()

        if self.playwright:

            self.playwright.stop()
