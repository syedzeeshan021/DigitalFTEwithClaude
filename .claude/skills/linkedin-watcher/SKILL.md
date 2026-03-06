---
name: linkedin-watcher
description: |
  Monitor and automate LinkedIn interactions using Playwright browser automation.
  Posts content to LinkedIn, checks notifications, and manages your LinkedIn presence.
  Uses persistent session to maintain login state across runs.
---

# LinkedIn Watcher Skill

Automate LinkedIn interactions using Playwright browser automation.

## Quick Start

### Post to LinkedIn Directly

```bash
python -c "from linkedin_watcher import LinkedInWatcherSkill; l = LinkedInWatcherSkill(); l.post_to_linkedin('Your post content here')"
```

### Process Approved Posts

```bash
python linkedin_watcher.py
```

### Check Profile Info

```bash
python -c "from linkedin_watcher import LinkedInWatcherSkill; l = LinkedInWatcherSkill(); print(l.get_profile_info())"
```

## How LinkedIn Watcher Works with Your Profile

### Session-Based Authentication

The LinkedIn Watcher uses **persistent browser sessions** to maintain your LinkedIn login:

1. **First Run**:
   - Browser opens to LinkedIn login page
   - You log in manually with your credentials
   - Session is saved to `AI_Employee_Vault/.linkedin_session/`

2. **Subsequent Runs**:
   - Uses saved session cookies
   - No login required (unless session expires)
   - Direct access to your LinkedIn profile

3. **Your Profile Connection**:
   - Operates on YOUR LinkedIn account
   - Posts appear from YOUR profile
   - Notifications are from YOUR account
   - All actions reflect YOUR identity

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              LINKEDIN WATCHER WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. LinkedInWatcherSkill initialized                        │
│     - Loads session from .linkedin_session/                  │
│     - Launches Chromium via Playwright                       │
│                                                              │
│  2. Navigate to LinkedIn Feed                               │
│     - Checks if logged in                                    │
│     - If not, waits for manual login (first run only)        │
│                                                              │
│  3. For posting:                                            │
│     - Clicks "Start a post" button                           │
│     - Types content (mimics human typing)                    │
│     - Attaches images if provided                            │
│     - Clicks "Post" button                                   │
│                                                              │
│  4. For notifications:                                      │
│     - Navigates to /notifications/                           │
│     - Reads notification cards                               │
│     - Returns list of recent activity                        │
│                                                              │
│  5. Session saved for future runs                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Usage Patterns

### Pattern 1: Post Text Update

```python
from linkedin_watcher import LinkedInWatcherSkill

linkedin = LinkedInWatcherSkill()

success = linkedin.post_to_linkedin("""
Excited to announce our new AI Employee system!

This autonomous digital assistant helps businesses:
- Monitor Gmail 24/7
- Track WhatsApp messages
- Automate task management
- Manage approvals seamlessly

The future of work is here.

#AI #Automation #BusinessGrowth
""")

print(f"Post successful: {success}")
```

### Pattern 2: Post with Image

```python
from linkedin_watcher import LinkedInWatcherSkill

linkedin = LinkedInWatcherSkill()

success = linkedin.post_to_linkedin(
    content="Our team reached a major milestone!",
    image_path="F:/path/to/image.jpg"
)
```

### Pattern 3: Process Approved Posts

```python
from linkedin_watcher import LinkedInWatcherSkill

linkedin = LinkedInWatcherSkill()

# Move posts from Needs_Action to Approved first
# Then process them
processed = linkedin.process_pending_posts()
print(f"Published {processed} posts")
```

### Pattern 4: Check Notifications

```python
from linkedin_watcher import LinkedInWatcherSkill

linkedin = LinkedInWatcherSkill()

notifications = linkedin.check_notifications()

for n in notifications[:5]:
    print(f"Notification: {n['text']}")
    print(f"Time: {n['timestamp']}")
```

### Pattern 5: Get Profile Info

```python
from linkedin_watcher import LinkedInWatcherSkill

linkedin = LinkedInWatcherSkill()

profile = linkedin.get_profile_info()

if profile:
    print(f"Logged in as: {profile['name']}")
    print(f"Session valid: {profile['session_valid']}")
else:
    print("Not logged in - please log in manually")
```

## Commands

### Run LinkedIn Watcher

```bash
# Full watcher with all features
python linkedin_watcher.py
```

### Quick Post

```bash
python -c "from linkedin_watcher import LinkedInWatcherSkill; l = LinkedInWatcherSkill(); l.post_to_linkedin('Quick update from AI Employee!')"
```

### Check Session Status

```bash
python -c "from linkedin_watcher import LinkedInWatcherSkill; l = LinkedInWatcherSkill(); print('Logged in:', l.get_profile_info() is not None)"
```

## Setup Requirements

### 1. Install Playwright

```bash
pip install playwright
playwright install chromium
```

### 2. First-Time Login

Run the watcher once to log in:

```bash
python linkedin_watcher.py
```

A browser window will open:
1. Log in to LinkedIn with your credentials
2. Wait for the feed to load
3. Browser closes automatically
4. Session saved for future runs

### 3. Session Location

Your LinkedIn session is stored in:
- `AI_Employee_Vault/.linkedin_session/`

This folder contains:
- Browser cookies
- Local storage
- Login tokens

**Do not delete this folder** unless you want to re-authenticate.

## Integration with AI Employee

### Automated Posting Workflow

```
1. AI creates post → linkedin_posting.py creates draft
2. Draft saved → Needs_Action/LINKEDIN_POST_*.md
3. Human reviews → Move to Approved/ folder
4. Watcher runs → linkedin_watcher.py publishes
5. Post live → File moved to Done/ folder
```

### With Approval Workflow

```python
from pathlib import
import shutil

# After AI creates post in Needs_Action/
# Human moves it to Approved/
shutil.move(
    "AI_Employee_Vault/Needs_Action/LINKEDIN_POST_*.md",
    "AI_Employee_Vault/Approved/"
)

# Then run watcher
from linkedin_watcher import LinkedInWatcherSkill
linkedin = LinkedInWatcherSkill()
linkedin.process_pending_posts()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Browser doesn't open | Run `playwright install chromium` |
| Login required every time | Check session folder exists and has write permissions |
| Post button not found | LinkedIn may have updated UI - wait for page to fully load |
| Session expired | Delete `.linkedin_session/` and re-authenticate |
| Character limit error | LinkedIn limits posts to 3000 characters - content is auto-truncated |
| Image upload fails | Ensure image path is absolute and file exists |

## Security Considerations

1. **Protect Session Data**: The `.linkedin_session/` folder contains login cookies - keep it secure
2. **Don't Share Session**: Never share your session folder with others
3. **Rate Limiting**: Avoid posting too frequently (LinkedIn may flag as spam)
4. **Human Oversight**: Always review posts before approving for automation
5. **Compliance**: Follow LinkedIn's Terms of Service for automated posting

## Best Practices

### Posting Frequency
- **Optimal**: 1-2 posts per day maximum
- **Minimum**: 3-5 posts per week for visibility
- **Avoid**: More than 5 posts per day (may trigger spam filters)

### Content Guidelines
- Keep posts professional and valuable
- Use 3-5 relevant hashtags
- Include engagement questions
- Respond to comments within 24 hours

### Session Management
- Run watcher regularly to keep session active
- Re-authenticate if session expires
- Use same machine for consistent sessions

## Related Skills

- `linkedin-posting` - For creating post drafts
- `approval-workflow` - For post approval decisions
- `scheduling-skill` - For scheduling posts
- `browsing-with-playwright` - General browser automation

## API Reference

### `post_to_linkedin(content, image_path=None)`
Post content to LinkedIn.

**Args:**
- `content`: String content to post
- `image_path`: Optional path to image file

**Returns:** Boolean indicating success

### `get_profile_info()`
Get current profile information.

**Returns:** Dict with name, session_valid, profile_url or None

### `check_notifications()`
Get recent notifications.

**Returns:** List of notification dicts with text and timestamp

### `process_pending_posts()`
Publish approved posts from Approved/ folder.

**Returns:** Number of posts processed
