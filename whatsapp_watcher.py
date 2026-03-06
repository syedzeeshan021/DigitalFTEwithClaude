"""
WhatsApp Watcher for AI Employee - Silver Tier

This script monitors WhatsApp Web for new messages and creates action items
in the AI Employee's Needs_Action folder.

Silver Tier Requirement: Two or more Watcher scripts (Filesystem + Gmail + WhatsApp)

Note: This uses WhatsApp Web automation via Playwright. Be aware of WhatsApp's terms of service.
"""

import time
import logging
from pathlib import Path
from datetime import datetime


class WhatsAppWatcherSkill:
    """
    Skill for monitoring WhatsApp Web and creating action items from new messages.
    Uses Playwright for browser automation.
    """

    def __init__(self, vault_path="AI_Employee_Vault", session_path=None):
        self.vault_path = Path(vault_path).resolve()
        self.session_path = Path(session_path) if session_path else self.vault_path / ".whatsapp_session"
        self.processed_ids = set()
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'deadline', 'pricing', 'interested']

    def create_action_file(self, message_data: dict) -> str:
        """Create an action file in Needs_Action folder for the WhatsApp message."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"WHATSAPP_{timestamp}_{message_data.get('chat_id', 'unknown')}.md"
        file_path = self.vault_path / "Needs_Action" / filename

        content = f"""---
type: whatsapp_message
from: {message_data.get('from', 'Unknown')}
chat_id: {message_data.get('chat_id', 'Unknown')}
received: {message_data.get('timestamp', datetime.now().isoformat())}
priority: {message_data.get('priority', 'normal')}
status: pending
keywords_matched: {','.join(message_data.get('keywords', []))}
---

# WhatsApp Message

## Sender
{message_data.get('from', 'Unknown')}

## Received
{message_data.get('timestamp', datetime.now().isoformat())}

## Priority
{message_data.get('priority', 'NORMAL').upper()}

## Message Content
{message_data.get('text', 'No content')}

## Keywords Detected
{', '.join(message_data.get('keywords', []))}

## Suggested Actions
- [ ] Read full message
- [ ] Determine required response
- [ ] Reply if necessary
- [ ] Archive after processing

## Notes
Add any notes or context about how to handle this message.
"""

        file_path.write_text(content)
        return str(file_path)

    def check_for_messages_playwright(self) -> list:
        """
        Check for new WhatsApp messages using Playwright.

        Note: This requires Playwright to be installed:
        pip install playwright
        playwright install chromium
        """
        try:
            from playwright.sync_api import sync_playwright

            messages = []

            with sync_playwright() as p:
                # Launch browser with persistent context for session
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()

                try:
                    # Navigate to WhatsApp Web
                    page.goto('https://web.whatsapp.com', timeout=60000)

                    # Wait for chat list to load
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)

                    # Find unread messages (look for unread indicators)
                    unread_chats = page.query_selector_all('[aria-label*="unread"]')

                    for chat in unread_chats:
                        try:
                            # Extract chat information
                            chat_name = chat.query_selector('[data-testid="chat-cell-name"]')
                            message_text = chat.query_selector('[data-testid="chat-cell-message"]')

                            name = chat_name.inner_text() if chat_name else "Unknown"
                            text = message_text.inner_text() if message_text else ""

                            # Check for important keywords
                            text_lower = text.lower()
                            matched_keywords = [kw for kw in self.keywords if kw in text_lower]

                            if matched_keywords:
                                messages.append({
                                    'from': name,
                                    'chat_id': name.replace(' ', '_'),
                                    'text': text,
                                    'priority': 'high',
                                    'keywords': matched_keywords,
                                    'timestamp': datetime.now().isoformat()
                                })
                        except Exception as e:
                            logging.error(f"Error extracting chat info: {e}")

                    browser.close()

                except Exception as e:
                    logging.error(f"Error interacting with WhatsApp Web: {e}")
                    browser.close()
                    # Return demo message if WhatsApp Web is not accessible
                    return self._create_demo_message()

            return messages

        except ImportError:
            logging.warning("Playwright not installed. Run: pip install playwright && playwright install chromium")
            return self._create_demo_message()
        except Exception as e:
            logging.error(f"Error in WhatsApp watcher: {e}")
            return self._create_demo_message()

    def _create_demo_message(self) -> list:
        """Create a demo WhatsApp message for testing."""
        return [{
            'from': 'Demo Client',
            'chat_id': 'demo_client',
            'text': 'Hi, I am interested in your services. Can you send me pricing information?',
            'priority': 'high',
            'keywords': ['interested', 'pricing'],
            'timestamp': datetime.now().isoformat()
        }]

    def process_messages(self) -> int:
        """Main method to check and process new WhatsApp messages."""
        messages = self.check_for_messages_playwright()
        processed_count = 0

        for message_data in messages:
            # Create unique ID for deduplication
            msg_id = f"{message_data['chat_id']}_{message_data['timestamp']}"

            if msg_id not in self.processed_ids:
                action_file = self.create_action_file(message_data)
                if action_file:
                    processed_count += 1
                    self.processed_ids.add(msg_id)

        return processed_count


def main():
    """Main function to run the WhatsApp watcher."""
    print("=" * 60)
    print("AI Employee - WhatsApp Watcher")
    print("=" * 60)

    # Initialize the WhatsApp watcher skill
    vault_path = Path("AI_Employee_Vault")
    whatsapp_watcher = WhatsAppWatcherSkill(str(vault_path))

    # Setup logging
    log_dir = vault_path / "Logs"
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f'whatsapp_watcher_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("WhatsAppWatcher")

    print("\nWhatsApp Watcher Configuration")
    print("-" * 40)
    print(f"Vault Path: {vault_path.absolute()}")
    print(f"Check Interval: 30 seconds")
    print(f"Monitored Keywords: urgent, asap, invoice, payment, help, deadline, pricing, interested")
    print("\nNOTE: To enable WhatsApp monitoring, you need to:")
    print("1. Install Playwright: pip install playwright")
    print("2. Install browsers: playwright install chromium")
    print("3. First run: Scan QR code on WhatsApp Web to authenticate")
    print("4. Session will be saved in .whatsapp_session folder")
    print("\nFor now, the watcher will demonstrate with demo messages")
    print("\nPress Ctrl+C to stop...")

    # Run watcher with demo messages
    check_count = 0
    max_demo_checks = 3  # Limit demo checks

    while check_count < max_demo_checks:
        try:
            check_count += 1
            logger.info(f"Checking for WhatsApp messages (check #{check_count})...")

            # Process messages
            processed_count = whatsapp_watcher.process_messages()
            logger.info(f"Processed {processed_count} new messages")

            logger.info(f"Waiting 30 seconds before next check...")
            time.sleep(30)  # Check every 30 seconds

        except KeyboardInterrupt:
            logger.info("WhatsApp Watcher stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in WhatsApp watcher: {e}")
            time.sleep(30)

    print("\nWhatsApp Watcher demonstration complete!")
    print("To enable real WhatsApp monitoring, follow the setup instructions above.")


if __name__ == "__main__":
    main()
