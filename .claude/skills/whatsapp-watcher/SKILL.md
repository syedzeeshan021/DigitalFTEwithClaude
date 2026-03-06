---
name: whatsapp-watcher
description: |
  Monitor WhatsApp Web for new messages and create action items in the AI Employee vault.
  Uses Playwright for browser automation to detect unread messages with important keywords.
  Use for real-time communication monitoring and lead capture from WhatsApp.
---

# WhatsApp Watcher Skill

Monitor WhatsApp Web and create action items for the AI Employee.

## Quick Start

### Start WhatsApp Watcher

```bash
python whatsapp_watcher.py
```

### Create Action File from Message

```bash
python -c "
from whatsapp_watcher import WhatsAppWatcherSkill
w = WhatsAppWatcherSkill()
msg = {'from': 'Client Name', 'chat_id': 'client_name', 'text': 'Interested in pricing', 'priority': 'high', 'keywords': ['interested', 'pricing'], 'timestamp': '2026-03-03T00:00:00'}
print(w.create_action_file(msg))
"
```

## Action File Structure

```markdown
---
type: whatsapp_message
from: Client Name
chat_id: client_name
received: 2026-03-03T00:00:00
priority: high
status: pending
keywords_matched: interested,pricing
---

# WhatsApp Message

## Sender
Client Name

## Received
2026-03-03T00:00:00

## Priority
HIGH

## Message Content
Interested in pricing

## Keywords Detected
interested, pricing

## Suggested Actions
- [ ] Read full message
- [ ] Determine required response
- [ ] Reply if necessary
- [ ] Archive after processing

## Notes
Add any notes or context about how to handle this message.
```

## Setup Requirements

### 1. Install Playwright

```bash
pip install playwright
playwright install chromium
```

### 2. First-Time Authentication

```bash
python whatsapp_watcher.py
```

On first run:
1. WhatsApp Web will open in the browser
2. Scan the QR code with your WhatsApp mobile app
3. Session will be saved in `.whatsapp_session` folder
4. Subsequent runs will use the saved session

### 3. Configure Monitored Keywords

Default keywords that trigger high priority:
```python
keywords = [
    'urgent',
    'asap',
    'invoice',
    'payment',
    'help',
    'deadline',
    'pricing',
    'interested'
]
```

## Usage Patterns

### Pattern 1: Run WhatsApp Watcher

```python
from whatsapp_watcher import WhatsAppWatcherSkill

whatsapp = WhatsAppWatcherSkill()

# Process messages
processed_count = whatsapp.process_messages()
print(f"Processed {processed_count} new messages")
```

### Pattern 2: Create Action File Manually

```python
from whatsapp_watcher import WhatsAppWatcherSkill

whatsapp = WhatsAppWatcherSkill()

message_data = {
    'from': 'John Doe',
    'chat_id': 'john_doe',
    'text': 'Hi, I need help with your product urgently!',
    'priority': 'high',
    'keywords': ['help', 'urgently'],
    'timestamp': '2026-03-03T00:00:00'
}

action_file = whatsapp.create_action_file(message_data)
```

### Pattern 3: Check for Messages Only

```python
from whatsapp_watcher import WhatsAppWatcherSkill

whatsapp = WhatsAppWatcherSkill()

messages = whatsapp.check_for_messages_playwright()
for msg in messages:
    print(f"From: {msg['from']}")
    print(f"Text: {msg['text']}")
    print(f"Keywords: {msg['keywords']}")
```

## Integration with AI Employee

### Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              WHATSAPP WATCHER WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. WhatsApp Watcher runs (every 30 seconds)                │
│                                                              │
│  2. Connect to WhatsApp Web via Playwright                  │
│     - Uses saved session if available                        │
│     - Opens headless browser                                 │
│     - Navigates to web.whatsapp.com                          │
│                                                              │
│  3. Scan for unread messages                                │
│     - Looks for [aria-label*="unread"]                       │
│     - Extracts sender name and message text                  │
│                                                              │
│  4. Filter by keywords                                      │
│     - Checks message against keyword list                    │
│     - Marks as high priority if match                        │
│                                                              │
│  5. Create action file in Needs_Action/                     │
│     - Formats message as markdown                            │
│     - Includes metadata (sender, time, keywords)             │
│                                                              │
│  6. Orchestrator processes action files                     │
│     - Reads message details                                  │
│     - Determines required response                           │
│     - Creates reply draft                                    │
│                                                              │
│  7. Mark as processed                                       │
│     - Adds to processed_ids set                              │
│     - Won't process same message again                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Continuous Monitoring

```bash
# Run WhatsApp watcher continuously
python whatsapp_watcher.py
```

The watcher will:
- Check for new messages every 30 seconds
- Create action files for messages with keywords
- Log all activity to Logs/ folder
- Handle errors gracefully

### PM2 Process Management

```bash
# Start WhatsApp watcher with PM2
pm2 start whatsapp_watcher.py --name ai-employee-whatsapp-watcher --interpreter python

# Save PM2 configuration
pm2 save

# View logs
pm2 logs ai-employee-whatsapp-watcher
```

## Keyword Priority Rules

| Keyword | Priority | Use Case |
|---------|----------|----------|
| urgent, asap | HIGH | Immediate attention needed |
| invoice, payment | HIGH | Financial matters |
| help | HIGH | Customer needs assistance |
| deadline | HIGH | Time-sensitive |
| pricing, interested | HIGH | Sales lead |
| Other | NORMAL | General messages |

## Commands

### Check WhatsApp Status

```bash
python -c "
from whatsapp_watcher import WhatsAppWatcherSkill
w = WhatsAppWatcherSkill()
messages = w.check_for_messages_playwright()
print(f'Found {len(messages)} messages')
"
```

### View WhatsApp Watcher Logs

```bash
# View today's log
cat AI_Employee_Vault/Logs/whatsapp_watcher_$(date +%Y%m%d).log

# Or via PM2
pm2 logs ai-employee-whatsapp-watcher --lines 50
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Playwright not found | Run: pip install playwright && playwright install chromium |
| Session expired | Delete .whatsapp_session folder and re-scan QR code |
| No messages detected | Ensure WhatsApp Web is showing unread messages |
| Browser won't launch | Check if Chromium is installed: playwright install chromium |
| QR code not showing | Try running with headless=False temporarily |

## Security Considerations

1. **Protect session data** - `.whatsapp_session` contains authentication tokens
2. **Don't commit session** - Add `.whatsapp_session` to .gitignore
3. **Monitor usage** - WhatsApp may flag automated access
4. **Respect terms of service** - Use responsibly for business purposes
5. **Rate limit checks** - Don't poll too frequently (30s minimum recommended)

## Example Output

```
============================================================
AI Employee - WhatsApp Watcher
============================================================

WhatsApp Watcher Configuration
----------------------------------------
Vault Path: F:\DigitalFTEwithClaude\AI_Employee_Vault
Check Interval: 30 seconds
Monitored Keywords: urgent, asap, invoice, payment, help, deadline, pricing, interested

NOTE: To enable WhatsApp monitoring, you need to:
1. Install Playwright: pip install playwright
2. Install browsers: playwright install chromium
3. First run: Scan QR code on WhatsApp Web to authenticate
4. Session will be saved in .whatsapp_session folder

For now, the watcher will demonstrate with demo messages

Press Ctrl+C to stop...

2026-03-03 00:00:00 - WhatsAppWatcher - INFO - Checking for WhatsApp messages (check #1)...
2026-03-03 00:00:01 - WhatsAppWatcher - INFO - Processed 1 new messages
2026-03-03 00:00:01 - WhatsAppWatcher - INFO - Created action file: F:\DigitalFTEwithClaude\AI_Employee_Vault\Needs_Action\WHATSAPP_20260303_000001_demo_client.md
2026-03-03 00:00:01 - WhatsAppWatcher - INFO - Waiting 30 seconds before next check...
```

## Related Skills

- `gmail-watcher` - For email monitoring
- `email-mcp` - For sending email replies to WhatsApp leads
- `approval-workflow` - For message response approval
- `linkedin-posting` - For alternative communication channel
