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

        self.browser = self.playwright.chromium.launch( headless=True )

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
                "INSTAGRAM_USERNAME is not set in .env"
            )
    
        if not INSTAGRAM_PASSWORD:
            raise ValueError(
                "INSTAGRAM_PASSWORD is not set in .env"
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
    
        print(
            f"\nLogin page URL: {self.page.url}"
        )
    
        # ========================================================
        # DEBUG: PRINT INPUTS
        # ========================================================
    
        inputs = self.page.locator("input").all()
    
        print(
            f"\nInputs found: {len(inputs)}"
        )
    
        for i, input_element in enumerate(inputs):
    
            try:
    
                print(
                    f"INPUT {i}: "
                    f"type={input_element.get_attribute('type')} "
                    f"name={input_element.get_attribute('name')} "
                    f"placeholder={input_element.get_attribute('placeholder')}"
                )
    
            except Exception:
                pass
    
        # ========================================================
        # DEBUG: SCREENSHOT
        # ========================================================
    
        try:
    
            self.page.screenshot(
                path="/tmp/instagram_login.png",
                full_page=True
            )
    
            print(
                "\nLogin screenshot saved."
            )
    
        except Exception as e:
    
            print(
                f"\nCould not save screenshot: {e}"
            )
    
        # ========================================================
        # CHECK WHETHER INSTAGRAM ACTUALLY SHOWED LOGIN
        # ========================================================
    
        if "/accounts/login" not in self.page.url:
    
            print(
                "Instagram session already active."
            )
    
            return
    
        # ========================================================
        # TRY MULTIPLE USERNAME SELECTORS
        # ========================================================
    
        username_selectors = [
    
            'input[name="username"]',
    
            'input[autocomplete="username"]',
    
            'input[type="text"]',
    
            'input[aria-label*="username" i]',
    
            'input[placeholder*="username" i]',
    
        ]
    
        username_input = None
    
        for selector in username_selectors:
    
            try:
    
                locator = self.page.locator(
                    selector
                ).first
    
                if locator.is_visible(
                    timeout=2000
                ):
    
                    username_input = locator
    
                    print(
                        f"\nUsername selector found: "
                        f"{selector}"
                    )
    
                    break
    
            except Exception:
                continue
    
        if username_input is None:
    
            raise RuntimeError(
                "Could not find Instagram "
                "username input. "
                "Check the login screenshot/logs."
            )
    
        # ========================================================
        # PASSWORD
        # ========================================================
    
        password_selectors = [
    
            'input[name="password"]',
    
            'input[autocomplete="current-password"]',
    
            'input[type="password"]',
    
        ]
    
        password_input = None
    
        for selector in password_selectors:
    
            try:
    
                locator = self.page.locator(
                    selector
                ).first
    
                if locator.is_visible(
                    timeout=2000
                ):
    
                    password_input = locator
    
                    print(
                        f"Password selector found: "
                        f"{selector}"
                    )
    
                    break
    
            except Exception:
                continue
    
        if password_input is None:
    
            raise RuntimeError(
                "Could not find Instagram "
                "password input."
            )
    
        # ========================================================
        # FILL LOGIN
        # ========================================================
    
        username_input.fill(
            INSTAGRAM_USERNAME
        )
    
        password_input.fill(
            INSTAGRAM_PASSWORD
        )
    
        print(
            "Login credentials filled."
        )
    
        # ========================================================
        # LOGIN BUTTON
        # ========================================================

        # Find the REAL Instagram "Log in" button
        login_button = self.page.locator('[role="button"][aria-label="Log In"]').first

        if not login_button.count():
            raise Exception("Could not find Instagram login button")

        print("Real Instagram login button found")

        # Wait until it is actually visible
        login_button.wait_for(state="visible", timeout=10_000)

        print("Login button is visible")

        # Click the real button
        login_button.click()

        print("Login button clicked")

        # Give Instagram time to process the login
        self.page.wait_for_timeout(5000)

        print(f"After login URL: {self.page.url}")

        # ========================================================
        # WAIT FOR INSTAGRAM RESPONSE
        # ========================================================

        self.page.wait_for_timeout(10_000)

        print(
            f"\nAfter login URL: {self.page.url}"
        )


        # ========================================================
        # DEBUG PAGE CONTENT
        # ========================================================

        print("\n========== LOGIN PAGE TEXT ==========\n")

        try:

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


        # ========================================================
        # DEBUG INPUTS AFTER SUBMISSION
        # ========================================================

        print(
            "\n========== INPUTS AFTER LOGIN ==========\n"
        )

        inputs = self.page.locator(
            "input"
        ).all()

        print(
            f"Inputs found: {len(inputs)}"
        )

        for i, element in enumerate(inputs):

            try:

                print(
                    f"INPUT {i}: "
                    f"type={element.get_attribute('type')} "
                    f"name={element.get_attribute('name')} "
                    f"value={element.get_attribute('value')}"
                )

            except Exception:
                pass


        # ========================================================
        # SCREENSHOT
        # ========================================================

        try:

            self.page.screenshot(
                path="/tmp/instagram_after_login.png",
                full_page=True
            )

            print(
                "\nAfter-login screenshot saved."
            )

        except Exception as e:

            print(
                f"Could not save screenshot: {e}"
            )


        # ========================================================
        # CURRENT URL
        # ========================================================

        print(
            f"\nFinal login URL: {self.page.url}"
        )
    
        # ========================================================
        # WAIT
        # ========================================================
    
        self.page.wait_for_timeout(
            7000
        )
    
        print(
            f"\nAfter login URL: "
            f"{self.page.url}"
        )
    
        # ========================================================
        # VERIFY
        # ========================================================
    
        if "/accounts/login" in self.page.url:
    
            raise RuntimeError(
                "Instagram login did not complete. "
                f"Current URL: {self.page.url}"
            )
    
        print(
            "\nInstagram authentication successful."
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
