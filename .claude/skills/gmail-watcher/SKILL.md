---
name: gmail-watcher
description: |
  Monitor Gmail for new emails and create action items in the AI Employee vault.
  Uses Gmail API with OAuth2 authentication (credentials.json) to fetch unread emails,
  identify important messages, and create structured action files for processing.
  Use for email automation and triage.
---

# Gmail Watcher Skill

Monitor Gmail and create action items for the AI Employee.

## Quick Start

### Start Gmail Watcher

```bash
python gmail_watcher.py
```

### Create Action File from Email

```bash
python -c "
from gmail_watcher import GmailWatcherSkill
g = GmailWatcherSkill()
email = {'id': 'demo', 'from': 'client@example.com', 'to': 'you@company.com', 'subject': 'Project Inquiry', 'snippet': 'Interested in your services', 'priority': 'high', 'timestamp': '2026-03-03T00:00:00'}
print(g.create_action_file(email))
"
```

## Action File Structure

```markdown
---
type: email
from: client@example.com
to: you@company.com
subject: Project Inquiry
received: 2026-03-03T00:00:00
priority: high
status: pending
email_id: abc123
---

# Email: Project Inquiry

## Sender
client@example.com

## Received
2026-03-03T00:00:00

## Priority
HIGH

## Content
Interested in your services...

## Suggested Actions
- [ ] Read full email
- [ ] Determine required response
- [ ] Reply if necessary
- [ ] Archive after processing

## Notes
Add any notes or context about how to handle this email.
```

## Setup Requirements

### 1. Credentials Setup (Already Configured)

The project already has `credentials.json` configured:

```
Project: digitalhackathonftewithclaude
Client ID: 947085388053-ouooch65p5ru7jnqnelqh6s8iga0pcas.apps.googleusercontent.com
```

The `credentials.json` file is located in the project root folder.

### 2. Install Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. First-Time Authentication

Run the Gmail watcher - it will automatically open a browser for OAuth2 authentication:

```bash
python gmail_watcher.py
```

This will:
1. Open browser for OAuth consent
2. Sign in with your Google account
3. Grant Gmail API permissions (read-only)
4. Save `token.pickle` in `AI_Employee_Vault/` for future use

### 4. Token Storage

After first authentication, the token is saved in:
- `AI_Employee_Vault/token.pickle`

This token is used for subsequent runs without re-authentication.

## Usage Patterns

### Pattern 1: Run Gmail Watcher

```python
from gmail_watcher import GmailWatcherSkill

gmail = GmailWatcherSkill()

# Authenticate (first time only - opens browser)
gmail.authenticate()

# Check and process new emails
processed_count = gmail.process_emails()
print(f"Processed {processed_count} new emails")
```

### Pattern 2: Check for New Emails

```python
from gmail_watcher import GmailWatcherSkill

gmail = GmailWatcherSkill()
gmail.authenticate()  # Ensure authenticated

emails = gmail.check_for_new_emails(max_results=5)

for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Priority: {email['priority']}")
```

### Pattern 3: Get Email Details

```python
from gmail_watcher import GmailWatcherSkill

gmail = GmailWatcherSkill()
email_data = gmail._get_email_details('message_id_here')

if email_data:
    print(f"From: {email_data['from']}")
    print(f"Subject: {email_data['subject']}")
    print(f"Snippet: {email_data['snippet']}")
```

### Pattern 4: Create Action File

```python
from gmail_watcher import GmailWatcherSkill

gmail = GmailWatcherSkill()

email_data = {
    'id': 'email_id',
    'from': 'client@example.com',
    'subject': 'Urgent: Project Deadline',
    'priority': 'high'
}

action_file = gmail.create_action_file(email_data)
print(f"Created: {action_file}")
```

## Important Keywords

Emails containing these keywords are marked as high priority:

```python
important_keywords = [
    'urgent',
    'asap',
    'invoice',
    'payment',
    'deadline',
    'meeting',
    'client',
    'project'
]
```

## Integration with AI Employee

### Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    GMAIL WATCHER WORKFLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Gmail Watcher runs (every 60 seconds)                   │
│                                                              │
│  2. Authenticate with Gmail API                             │
│     - Uses credentials.json (project root)                   │
│     - Uses token.pickle (AI_Employee_Vault/)                 │
│                                                              │
│  3. Fetch unread emails from Gmail                          │
│     - Uses Gmail API                                         │
│     - Filters by keywords for priority                       │
│                                                              │
│  4. For each new email:                                     │
│     - Extract sender, subject, snippet                       │
│     - Determine priority                                     │
│     - Create action file in Needs_Action/                    │
│                                                              │
│  5. Orchestrator processes action files                     │
│     - Reads email details                                    │
│     - Determines required action                             │
│     - Creates plan if needed                                 │
│     - Sends reply via EmailMCPSkill                          │
│                                                              │
│  6. Mark email as processed                                 │
│     - Add to processed_ids set                               │
│     - Won't process again                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Continuous Monitoring

```bash
# Run Gmail watcher continuously
python gmail_watcher.py
```

The watcher will:
- Check for new emails every 60 seconds
- Create action files for new emails
- Log all activity to Logs/ folder
- Handle errors gracefully
- Fall back to demo mode if authentication fails

### PM2 Process Management

```bash
# Start Gmail watcher with PM2
pm2 start gmail_watcher.py --name ai-employee-gmail-watcher --interpreter python

# Save PM2 configuration
pm2 save

# View logs
pm2 logs ai-employee-gmail-watcher
```

## Email Priority Rules

| Condition | Priority |
|-----------|----------|
| Subject contains urgent/asap | HIGH |
| Subject contains invoice/payment | HIGH |
| Subject contains deadline | HIGH |
| Subject contains client/meeting | HIGH |
| All other emails | NORMAL |

## Commands

### Check Gmail Status

```bash
python -c "
from gmail_watcher import GmailWatcherSkill
gmail = GmailWatcherSkill()
gmail.authenticate()
emails = gmail.check_for_new_emails()
print(f'Found {len(emails)} new emails')
"
```

### View Gmail Watcher Logs

```bash
# View today's log
cat AI_Employee_Vault/Logs/gmail_watcher_$(date +%Y%m%d).log

# Or via PM2
pm2 logs ai-employee-gmail-watcher --lines 50
```

### Re-authenticate (if token expires)

```bash
# Delete existing token
rm AI_Employee_Vault/token.pickle

# Run watcher to re-authenticate
python gmail_watcher.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Delete token.pickle and re-run gmail_watcher.py |
| Browser doesn't open | Manually open the localhost URL shown in terminal |
| No emails found | Check if emails are marked as unread in Gmail |
| API quota exceeded | Wait 24 hours or request quota increase |
| Token expired | Delete AI_Employee_Vault/token.pickle and re-authenticate |
| Module not found | Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib |
| Credentials not found | Ensure credentials.json exists in project root |

## Security Considerations

1. **Protect credentials.json** - Already in project root, never commit to version control
2. **Secure token.pickle** - Stored in AI_Employee_Vault/, contains OAuth tokens
3. **Limit API scope** - Only requests Gmail read-only access (`gmail.readonly`)
4. **Review logs regularly** - Check Logs/ folder for unusual activity
5. **Rotate credentials** - Update OAuth credentials periodically if needed

## Demo Mode

If authentication fails or credentials are not available, the watcher runs in demo mode:
- Creates sample email action files
- Tests the file creation workflow
- Logs "Demo Email" entries

## Credentials Information

The project uses the following Google Cloud project:

| Setting | Value |
|---------|-------|
| Project ID | digitalhackathonftewithclaude |
| Client ID | 947085388053-ouooch65p5ru7jnqnelqh6s8iga0pcas.apps.googleusercontent.com |
| Auth URI | https://accounts.google.com/o/oauth2/auth |
| Token URI | https://oauth2.googleapis.com/token |

## Related Skills

- `email-mcp` - For sending email replies
- `approval-workflow` - For email approval decisions
- `planning-skill` - For creating email response plans
- `whatsapp-watcher` - For alternative communication channel
