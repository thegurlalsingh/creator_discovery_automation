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

        self.playwright = sync_playwright().start()
    
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
            ]
        )
    
        self.context = self.browser.new_context(
            user_agent=USER_AGENT
        )
    
        self.page = self.context.new_page()
    
        self.login()
    
        return self.page


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        if not INSTAGRAM_USERNAME:
            raise ValueError(
                "INSTAGRAM_USERNAME is not set in .env"
            )
    
        if not INSTAGRAM_PASSWORD:
            raise ValueError(
                "INSTAGRAM_PASSWORD is not set in .env"
            )
    
        print("\n" + "=" * 70)
        print("INSTAGRAM AUTHENTICATION")
        print("=" * 70)
    
        # ========================================================
        # OPEN INSTAGRAM LOGIN
        # ========================================================
    
        self.page.goto(
            "https://www.instagram.com/accounts/login/",
            wait_until="domcontentloaded",
            timeout=60_000
        )
    
        print(
            f"\nLogin page URL: {self.page.url}"
        )
    
        # ========================================================
        # WAIT FOR INSTAGRAM PAGE TO ACTUALLY RENDER
        # ========================================================
    
        username_input = None
    
        username_selectors = [
            'input[name="username"]',
            'input[name="email"]',
            'input[autocomplete="username"]',
            'input[type="text"]',
        ]
    
        # Give Instagram up to 30 seconds to render the form.
        for _ in range(30):
    
            for selector in username_selectors:
    
                try:
    
                    locator = self.page.locator(
                        selector
                    ).first
    
                    if locator.count() > 0 and locator.is_visible():
    
                        username_input = locator
    
                        print(
                            f"\nUsername selector found: {selector}"
                        )
    
                        break
    
                except Exception:
                    pass
    
            if username_input:
                break
    
            self.page.wait_for_timeout(1000)
    
        # ========================================================
        # DEBUG IF LOGIN FORM WAS NOT FOUND
        # ========================================================
    
        if username_input is None:
    
            print(
                "\nInstagram login form did not appear."
            )
    
            print(
                f"Current URL: {self.page.url}"
            )
    
            try:
    
                print(
                    "\n========== PAGE TITLE ==========\n"
                )
    
                print(
                    self.page.title()
                )
    
            except Exception:
                pass
    
            try:
    
                print(
                    "\n========== PAGE TEXT ==========\n"
                )
    
                text = self.page.locator(
                    "body"
                ).inner_text(
                    timeout=5000
                )
    
                print(
                    text[:5000]
                )
    
            except Exception as e:
    
                print(
                    f"Could not read page text: {e}"
                )
    
            try:
    
                self.page.screenshot(
                    path="/tmp/instagram_login_failed.png",
                    full_page=True
                )
    
                print(
                    "\nFailure screenshot saved."
                )
    
            except Exception as e:
    
                print(
                    f"Could not save screenshot: {e}"
                )
    
            raise RuntimeError(
                "Could not find Instagram username input. "
                "Instagram login page did not render correctly."
            )
    
        # ========================================================
        # PASSWORD INPUT
        # ========================================================
    
        password_input = None
    
        password_selectors = [
            'input[name="password"]',
            'input[name="pass"]',
            'input[autocomplete="current-password"]',
            'input[type="password"]',
        ]
    
        for selector in password_selectors:
    
            try:
    
                locator = self.page.locator(
                    selector
                ).first
    
                if locator.count() > 0 and locator.is_visible():
    
                    password_input = locator
    
                    print(
                        f"Password selector found: {selector}"
                    )
    
                    break
    
            except Exception:
                pass
    
        if password_input is None:
    
            raise RuntimeError(
                "Could not find Instagram password input."
            )
    
        # ========================================================
        # FILL CREDENTIALS
        # ========================================================
    
        username_input.fill(
            INSTAGRAM_USERNAME
        )
    
        password_input.fill(
            INSTAGRAM_PASSWORD
        )
    
        print(
            "\nLogin credentials filled."
        )
    
        # ========================================================
        # FIND REAL LOGIN BUTTON
        # ========================================================
    
        login_button = None
    
        login_selectors = [
            '[role="button"][aria-label="Log In"]',
            'button:has-text("Log in")',
            '[role="button"]:has-text("Log in")',
        ]
    
        for selector in login_selectors:
    
            try:
    
                locator = self.page.locator(
                    selector
                ).first
    
                if locator.count() > 0 and locator.is_visible():
    
                    login_button = locator
    
                    print(
                        f"Login button found: {selector}"
                    )
    
                    break
    
            except Exception:
                pass
    
        if login_button is None:
    
            raise RuntimeError(
                "Could not find Instagram login button."
            )
    
        # ========================================================
        # CLICK LOGIN
        # ========================================================
    
        login_button.click(
            force=True
        )
    
        print(
            "Login button clicked."
        )
    
        # ========================================================
        # WAIT FOR LOGIN RESULT
        # ========================================================
    
        self.page.wait_for_timeout(5000)
    
        print(
            f"\nAfter login URL: {self.page.url}"
        )
    
        # Give Instagram additional time to finish authentication.
        self.page.wait_for_timeout(5000)
    
        # ========================================================
        # CHECK LOGIN RESULT
        # ========================================================
    
        current_url = self.page.url
    
        print(
            f"\nFinal login URL: {current_url}"
        )
    
        # --------------------------------------------------------
        # Read body text for authentication errors/challenges.
        # --------------------------------------------------------
    
        try:
    
            body_text = self.page.locator(
                "body"
            ).inner_text(
                timeout=5000
            )
    
        except Exception:
    
            body_text = ""
    
        lower_text = body_text.lower()
    
        # ========================================================
        # LOGIN FAILED
        # ========================================================
    
        if "/accounts/login" in current_url:
    
            print(
                "\n========== INSTAGRAM LOGIN RESPONSE ==========\n"
            )
    
            print(
                body_text[:5000]
            )
    
            # ----------------------------------------------------
            # Detect common login failures.
            # ----------------------------------------------------
    
            if (
                "incorrect" in lower_text
                or "login information" in lower_text
            ):
    
                raise RuntimeError(
                    "Instagram rejected the login credentials."
                )
    
            if (
                "challenge" in lower_text
                or "suspicious" in lower_text
                or "confirm" in lower_text
            ):
    
                raise RuntimeError(
                    "Instagram requires an additional "
                    "verification/challenge."
                )
    
            raise RuntimeError(
                "Instagram login did not complete. "
                f"Current URL: {current_url}"
            )
    
        # ========================================================
        # SUCCESS
        # ========================================================
    
        print(
            "\nInstagram authentication successful."
        )
    
        print(
            f"Authenticated URL: {current_url}"
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
