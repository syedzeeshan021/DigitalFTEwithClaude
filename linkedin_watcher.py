"""
LinkedIn Watcher for AI Employee - Silver Tier

This script uses Playwright to automate LinkedIn interactions:
- Post content to LinkedIn automatically
- Check notifications and engagement
- Monitor messages and connection requests

Silver Tier Requirement: Automatically Post on LinkedIn about business to generate sales

Note: Requires Playwright browsers installed. Run: playwright install chromium
"""

import time
import logging
from pathlib import Path
from datetime import datetime


class LinkedInWatcherSkill:
    """
    Skill for automating LinkedIn interactions using Playwright.
    Posts content, monitors engagement, and manages LinkedIn presence.
    """

    def __init__(self, vault_path="AI_Employee_Vault", session_path=None):
        self.vault_path = Path(vault_path).resolve()
        self.session_path = Path(session_path) if session_path else self.vault_path / ".linkedin_session"
        self.processed_posts = set()
        self.logger = logging.getLogger(self.__class__.__name__)

    def post_to_linkedin(self, content: str, image_path: str = None) -> bool:
        """
        Post content to LinkedIn using Playwright automation.

        Args:
            content: The post content to share
            image_path: Optional path to an image to attach

        Returns:
            True if post was successful, False otherwise
        """
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                # Launch browser with persistent context (keeps login session)
                context = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Set to True for production
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )

                page = context.pages[0] if context.pages else context.new_page()

                # Go to LinkedIn
                self.logger.info("Navigating to LinkedIn...")
                page.goto("https://www.linkedin.com/feed/", timeout=60000)

                # Wait for page to load and check if logged in
                try:
                    page.wait_for_selector('[data-id="gh-home"]', timeout=10000)
                    self.logger.info("Already logged in to LinkedIn")
                except:
                    self.logger.info("Login required - please log in manually")
                    # Wait for user to log in (max 2 minutes)
                    try:
                        page.wait_for_selector('[data-id="gh-home"]', timeout=120000)
                        self.logger.info("Login successful")
                    except:
                        self.logger.error("Login timeout - please try again")
                        context.close()
                        return False

                # Start creating a post
                self.logger.info("Starting post creation...")
                try:
                    # Click on the "Start a post" button
                    start_post_btn = page.locator('button[aria-label="Start a post"]').first
                    start_post_btn.click(timeout=5000)
                    self.logger.info("Clicked 'Start a post' button")
                except Exception as e:
                    self.logger.warning(f"Could not find start post button: {e}")
                    # Try alternative selector
                    try:
                        start_post_btn = page.locator('.share-box-feed-entry__trigger').first
                        start_post_btn.click(timeout=5000)
                        self.logger.info("Clicked alternative start post button")
                    except Exception as e2:
                        self.logger.error(f"Could not start post: {e2}")
                        context.close()
                        return False

                # Wait for post dialog to appear
                page.wait_for_selector('div[role="dialog"]', timeout=5000)

                # Find the text editor and type content
                self.logger.info("Entering post content...")
                editor = page.locator('div[contenteditable="true"][role="textbox"]').first

                # Clear any existing content and type new content
                editor.fill("")

                # Type content in chunks to avoid detection
                self._type_slowly(editor, content[:1000])  # LinkedIn has character limits

                # Add image if provided
                if image_path and Path(image_path).exists():
                    self.logger.info(f"Attaching image: {image_path}")
                    try:
                        # Click on media/photo button
                        media_btn = page.locator('button[aria-label*="photo" i], button[aria-label*="media" i], button[aria-label*="image" i]').first
                        media_btn.click(timeout=3000)

                        # Wait for file input and upload
                        file_input = page.locator('input[type="file"]').first
                        file_input.set_input_files(str(image_path), timeout=5000)

                        # Wait for upload to complete
                        page.wait_for_timeout(3000)
                        self.logger.info("Image attached successfully")
                    except Exception as e:
                        self.logger.warning(f"Could not attach image: {e}")

                # Click Post button
                self.logger.info("Publishing post...")
                try:
                    post_btn = page.locator('button[aria-label*="Post"], button:has-text("Post")').first
                    post_btn.click(timeout=5000)

                    # Wait for confirmation
                    page.wait_for_timeout(3000)
                    self.logger.info("Post published successfully!")

                    context.close()
                    return True

                except Exception as e:
                    self.logger.error(f"Could not publish post: {e}")
                    # Try alternative: press Enter or find another post button
                    try:
                        post_btn = page.locator('button.sharing-create-post-send-button').first
                        post_btn.click(timeout=5000)
                        page.wait_for_timeout(3000)
                        self.logger.info("Post published successfully (alternative method)!")
                        context.close()
                        return True
                    except Exception as e2:
                        self.logger.error(f"Alternative post method also failed: {e2}")
                        context.close()
                        return False

        except ImportError:
            self.logger.error("Playwright not installed. Run: pip install playwright && playwright install chromium")
            return False
        except Exception as e:
            self.logger.error(f"Error posting to LinkedIn: {e}")
            return False

    def _type_slowly(self, element, text: str, delay: int = 50):
        """Type text with small delays to mimic human behavior."""
        # Split into paragraphs and type them
        paragraphs = text.split('\n\n')
        for i, para in enumerate(paragraphs):
            if i > 0:
                element.press('Enter')
                element.press('Enter')
            element.type(para, delay=delay)

    def get_profile_info(self) -> dict:
        """
        Get current LinkedIn profile information.

        Returns:
            Dict with profile info or None if failed
        """
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={"width": 1280, "height": 720}
                )

                page = context.pages[0] if context.pages else context.new_page()
                page.goto("https://www.linkedin.com/feed/", timeout=60000)

                # Wait for page load
                try:
                    page.wait_for_selector('[data-id="gh-home"]', timeout=10000)
                except:
                    self.logger.warning("Not logged in to LinkedIn")
                    context.close()
                    return None

                # Get profile name from top nav
                try:
                    name_elem = page.locator('div[aria-label="You have 1 new notification"]').locator('..').locator('img').first
                    name = name_elem.get_attribute('alt', timeout=5000) or "Unknown"
                except:
                    name = "Unknown"

                context.close()
                return {
                    'name': name,
                    'session_valid': True,
                    'profile_url': 'https://www.linkedin.com/in/your-profile'
                }

        except Exception as e:
            self.logger.error(f"Error getting profile info: {e}")
            return None

    def check_notifications(self) -> list:
        """
        Check recent LinkedIn notifications.

        Returns:
            List of notification items
        """
        notifications = []
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                context = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    viewport={"width": 1280, "height": 720}
                )

                page = context.pages[0] if context.pages else context.new_page()
                page.goto("https://www.linkedin.com/notifications/", timeout=60000)

                # Wait for notifications page
                try:
                    page.wait_for_selector('.notification-card', timeout=10000)
                except:
                    self.logger.warning("No notifications found or not logged in")
                    context.close()
                    return []

                # Get notification cards
                cards = page.locator('.notification-card').all()
                for card in cards[:10]:  # Get last 10 notifications
                    try:
                        text = card.inner_text(timeout=3000)
                        notifications.append({
                            'text': text[:200],  # Truncate long text
                            'timestamp': datetime.now().isoformat()
                        })
                    except:
                        continue

                context.close()

        except Exception as e:
            self.logger.error(f"Error checking notifications: {e}")

        return notifications

    def process_pending_posts(self) -> int:
        """
        Process pending LinkedIn posts from Needs_Action folder.
        Moves approved posts to Done folder after posting.

        Returns:
            Number of posts processed
        """
        needs_action = self.vault_path / "Needs_Action"
        approved = self.vault_path / "Approved"
        done = self.vault_path / "Done"

        # Ensure folders exist
        needs_action.mkdir(exist_ok=True)
        approved.mkdir(exist_ok=True)
        done.mkdir(exist_ok=True)

        processed = 0

        # Check Approved folder for posts ready to publish
        if approved.exists():
            for post_file in approved.glob("LINKEDIN_POST_*.md"):
                self.logger.info(f"Processing approved post: {post_file.name}")

                # Read post content
                content = post_file.read_text(encoding='utf-8')

                # Extract post content from markdown
                post_content = self._extract_post_content(content)

                if post_content:
                    # Post to LinkedIn
                    success = self.post_to_linkedin(post_content)

                    if success:
                        # Move to Done folder
                        done_file = done / post_file.name
                        post_file.rename(done_file)
                        self.logger.info(f"Post published and moved to Done: {done_file}")
                        processed += 1
                    else:
                        self.logger.error(f"Failed to publish post: {post_file.name}")
                else:
                    self.logger.warning(f"Could not extract content from: {post_file.name}")

        return processed

    def _extract_post_content(self, markdown_content: str) -> str:
        """Extract the actual post content from markdown file."""
        lines = markdown_content.split('\n')
        in_content = False
        content_lines = []
        hashtags = []

        for line in lines:
            if line.startswith('## Content'):
                in_content = True
                continue
            if in_content:
                if line.startswith('##'):
                    break
                if line.startswith('#') and not line.startswith('##'):
                    # This is a hashtag
                    hashtags.append(line)
                elif line.strip():
                    content_lines.append(line)

        # Combine content and hashtags
        full_content = '\n\n'.join(content_lines)
        if hashtags:
            full_content += '\n\n' + ' '.join(hashtags)

        return full_content.strip()

    def create_demo_post(self) -> str:
        """Create a demo post file for testing."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"LINKEDIN_POST_{timestamp}_demo.md"
        file_path = self.vault_path / "Needs_Action" / filename

        content = f"""---
type: linkedin_post
post_type: business_update
created: {datetime.now().isoformat()}
status: draft
---

# LinkedIn Post Draft

## Content

Excited to share our latest AI Employee update!

Our autonomous digital assistant now includes:
- Gmail monitoring with OAuth2 authentication
- WhatsApp message tracking
- Automated task management
- Human-in-the-loop approvals

This is the future of business automation.

#AI #Automation #BusinessGrowth #Innovation

## Post Type
business_update
"""

        file_path.write_text(content, encoding='utf-8')
        return str(file_path)


def main():
    """Main function to run the LinkedIn Watcher."""
    print("=" * 60)
    print("AI Employee - LinkedIn Watcher")
    print("=" * 60)

    vault_path = Path("AI_Employee_Vault")
    vault_path.mkdir(exist_ok=True)

    # Check if Playwright browsers are installed
    try:
        from playwright.sync_api import sync_playwright
        browsers_installed = True
    except ImportError:
        browsers_installed = False
        print("\n[WARNING] Playwright not installed. Run: pip install playwright")
        print("Then run: playwright install chromium")

    linkedin = LinkedInWatcherSkill(str(vault_path))

    print("\nLinkedIn Watcher Configuration")
    print("-" * 40)
    print(f"Vault Path: {vault_path.absolute()}")
    print(f"Session Path: {linkedin.session_path}")
    print(f"Playwright Available: {'YES' if browsers_installed else 'NO'}")

    if not browsers_installed:
        print("\nTo enable LinkedIn automation:")
        print("  1. pip install playwright")
        print("  2. playwright install chromium")
        print("\nFor now, running in demo mode...")

        # Create demo post
        demo_post = linkedin.create_demo_post()
        print(f"\nCreated demo post: {demo_post}")
        print("Move this file to Approved/ folder to test posting when Playwright is installed")
        return

    # Get profile info
    print("\nChecking LinkedIn profile...")
    profile = linkedin.get_profile_info()
    if profile:
        print(f"Logged in as: {profile['name']}")
        print(f"Session valid: {'YES' if profile['session_valid'] else 'NO'}")

        # Only process if logged in successfully
        # Check for pending posts
        print("\nChecking for pending posts...")
        processed = linkedin.process_pending_posts()
        print(f"Processed {processed} posts")

        # Check notifications
        print("\nChecking notifications...")
        notifications = linkedin.check_notifications()
        if notifications:
            print(f"Found {len(notifications)} recent notifications")
            for n in notifications[:3]:
                print(f"  - {n['text'][:50]}...")
        else:
            print("No new notifications")
    else:
        print("Not logged in - first run will require manual login")
        print("Run 'python linkedin_watcher.py' interactively to log in to LinkedIn")
        print("Once logged in, the session will be saved for future automated runs")

    print("\n" + "=" * 60)
    print("LinkedIn Watcher ready!")
    print("\nUsage:")
    print("  1. Create posts with: python linkedin_posting.py")
    print("  2. Move posts to Approved/ folder")
    print("  3. Run this watcher to auto-publish")
    print("  4. Or use: python -c \"from linkedin_watcher import LinkedInWatcherSkill; l = LinkedInWatcherSkill(); l.post_to_linkedin('Your post content')\"")
    print("=" * 60)


if __name__ == "__main__":
    main()
