"""
Gmail Watcher for AI Employee - Silver Tier

This script monitors Gmail for new emails and creates action items
in the AI Employee's Needs_Action folder.

Silver Tier Requirement: Two or more Watcher scripts

Credentials: Uses credentials.json in project root for Gmail API authentication
"""

import time
import logging
import pickle
from pathlib import Path
from datetime import datetime


class GmailWatcherSkill:
    """
    Skill for monitoring Gmail and creating action items from new emails.
    Uses Gmail API with OAuth2 authentication.
    """

    def __init__(self, vault_path="AI_Employee_Vault", credentials_path="credentials.json"):
        self.vault_path = Path(vault_path).resolve()
        self.credentials_path = Path(credentials_path)
        self.token_path = self.vault_path / "token.pickle"
        self.processed_ids = set()
        self.important_keywords = ['urgent', 'asap', 'invoice', 'payment',
                                   'deadline', 'meeting', 'client', 'project']
        self.gmail_service = None

    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth2 credentials.

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            # If token exists, load it
            if self.token_path.exists():
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
                if creds and creds.valid:
                    self.gmail_service = build('gmail', 'v1', credentials=creds)
                    logging.info("Successfully loaded existing token")
                    return True

            # Check if credentials file exists
            if not self.credentials_path.exists():
                logging.error(f"Credentials file not found: {self.credentials_path}")
                return False

            # Run OAuth2 flow
            SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

            # Save the token for future use
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

            # Build the Gmail service
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            logging.info("Successfully authenticated with Gmail API")
            return True

        except ImportError:
            logging.error("Gmail API libraries not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return False
        except Exception as e:
            logging.error(f"Authentication error: {e}")
            return False

    def check_for_new_emails(self, max_results: int = 10) -> list:
        """Check for new unread emails."""
        if not self.gmail_service:
            logging.error("Gmail service not initialized")
            return []

        try:
            results = self.gmail_service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            new_emails = []

            for message in messages:
                if message['id'] not in self.processed_ids:
                    email_data = self._get_email_details(message['id'])
                    if email_data:
                        new_emails.append(email_data)
                        self.processed_ids.add(message['id'])

            return new_emails

        except Exception as e:
            logging.error(f"Error checking emails: {e}")
            return []

    def _get_email_details(self, message_id: str) -> dict:
        """Get detailed information about an email."""
        try:
            message = self.gmail_service.users().messages().get(
                userId='me', id=message_id, format='full'
            ).execute()

            headers = {h['name']: h['value'] for h in message['payload']['headers']}

            # Determine priority based on keywords
            subject = headers.get('Subject', '').lower()
            from_email = headers.get('From', '').lower()
            priority = 'high' if any(kw in subject for kw in self.important_keywords) else 'normal'

            return {
                'id': message_id,
                'from': headers.get('From', 'Unknown'),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', 'No Subject'),
                'date': headers.get('Date', ''),
                'snippet': message.get('snippet', ''),
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"Error getting email details: {e}")
            return None

    def create_action_file(self, email_data: dict) -> str:
        """Create an action file in Needs_Action folder for the email."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"EMAIL_{timestamp}_{email_data['id']}.md"
        file_path = self.vault_path / "Needs_Action" / filename

        content = f"""---
type: email
from: {email_data['from']}
to: {email_data['to']}
subject: {email_data['subject']}
received: {email_data['timestamp']}
priority: {email_data['priority']}
status: pending
email_id: {email_data['id']}
---

# Email: {email_data['subject']}

## Sender
{email_data['from']}

## Received
{email_data['timestamp']}

## Priority
{email_data['priority'].upper()}

## Content
{email_data['snippet']}

## Suggested Actions
- [ ] Read full email
- [ ] Determine required response
- [ ] Reply if necessary
- [ ] Archive after processing

## Notes
Add any notes or context about how to handle this email.
"""

        file_path.write_text(content, encoding='utf-8')
        return str(file_path)

    def process_emails(self) -> int:
        """Main method to check and process new emails."""
        # Try to authenticate if not already done
        if not self.gmail_service:
            if not self.authenticate():
                logging.warning("Authentication failed, using demo mode")
                return self._process_demo_emails()

        emails = self.check_for_new_emails()
        processed_count = 0

        for email_data in emails:
            action_file = self.create_action_file(email_data)
            if action_file:
                processed_count += 1
                logging.info(f"Created action file: {action_file}")

        return processed_count

    def _process_demo_emails(self) -> int:
        """Process demo emails when Gmail API is not available."""
        demo_emails = [{
            'id': f'demo_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'from': 'demo@example.com',
            'to': 'you@yourcompany.com',
            'subject': 'Demo Email - Gmail API Not Connected',
            'snippet': 'This is a demo email. To enable real Gmail monitoring, ensure credentials.json is valid and run authentication.',
            'priority': 'normal',
            'timestamp': datetime.now().isoformat()
        }]

        processed_count = 0
        for email_data in demo_emails:
            if email_data['id'] not in self.processed_ids:
                action_file = self.create_action_file(email_data)
                if action_file:
                    processed_count += 1
                    self.processed_ids.add(email_data['id'])

        return processed_count


def main():
    """Main function to run the Gmail watcher."""
    print("=" * 60)
    print("AI Employee - Gmail Watcher")
    print("=" * 60)

    # Initialize the Gmail watcher skill
    vault_path = Path("AI_Employee_Vault")

    # Check for credentials file
    credentials_path = Path("credentials.json")
    if credentials_path.exists():
        print("\n[SUCCESS] Found credentials.json")
        print("Project: digitalhackathonftewithclaude")
        print("Client ID: 947085388053-ouooch65p5ru7jnqnelqh6s8iga0pcas.apps.googleusercontent.com")
    else:
        print("\n[WARNING] credentials.json not found - will use demo mode")

    gmail_watcher = GmailWatcherSkill(str(vault_path), str(credentials_path))

    # Setup logging
    log_dir = vault_path / "Logs"
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f'gmail_watcher_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("GmailWatcher")

    print("\nGmail Watcher Configuration")
    print("-" * 40)
    print(f"Vault Path: {vault_path.absolute()}")
    print(f"Check Interval: 60 seconds")
    print(f"Important Keywords: urgent, asap, invoice, payment, deadline, meeting, client, project")

    if credentials_path.exists():
        print("\n[INFO] First run will open browser for OAuth2 authentication")
        print("[INFO] Subsequent runs will use saved token in AI_Employee_Vault/token.pickle")

    print("\nPress Ctrl+C to stop...")

    # Run watcher
    check_count = 0

    while True:
        try:
            check_count += 1
            logger.info(f"Checking for new emails (check #{check_count})...")

            # Process emails
            processed_count = gmail_watcher.process_emails()

            if processed_count > 0:
                logger.info(f"Processed {processed_count} new emails")
            else:
                logger.info("No new emails")

            logger.info(f"Waiting 60 seconds before next check...")
            time.sleep(60)

        except KeyboardInterrupt:
            logger.info("Gmail Watcher stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in Gmail watcher: {e}")
            time.sleep(60)

    print("\nGmail Watcher stopped!")


if __name__ == "__main__":
    main()
