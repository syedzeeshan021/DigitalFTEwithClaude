---
name: email-mcp
description: |
  Send emails via SMTP or create draft emails with approval workflow. Supports HTML
  emails, attachments, CC/BCC, and integration with the approval system for sensitive
  communications. Use for all email-related operations in the AI Employee.
---

# Email MCP Skill

Send emails and manage email drafts for the AI Employee.

## Quick Start

### Send Email (with SMTP config)

```bash
python -c "from skills_silver import EmailMCPSkill; e = EmailMCPSkill(smtp_config={'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 'from_email': 'you@gmail.com', 'username': 'you@gmail.com', 'password': 'app-password'}); e.send_email('recipient@example.com', 'Subject', 'Body text')"
```

### Create Draft Email

```bash
python -c "from skills_silver import EmailMCPSkill; e = EmailMCPSkill(); print(e.create_draft('recipient@example.com', 'Subject', 'Body text'))"
```

### Send with Approval

```bash
python -c "from skills_silver import EmailMCPSkill; e = EmailMCPSkill(); print(e.send_with_approval('recipient@example.com', 'Subject', 'Body text'))"
```

## Email Draft Structure

```markdown
---
type: email_draft
to: recipient@example.com
subject: Email Subject
created: 2026-03-03T00:00:00
status: draft
---

# Email Draft: Subject

## To
recipient@example.com

## Subject
Email Subject

## Body
Email body content here...

---
*This is a draft email. Review and move to /Approved to send.*
```

## Usage Patterns

### Pattern 1: Send Email via SMTP

```python
from skills_silver import EmailMCPSkill

email = EmailMCPSkill(smtp_config={
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'from_email': 'you@gmail.com',
    'username': 'you@gmail.com',
    'password': 'your-app-password'
})

success = email.send_email(
    to='client@example.com',
    subject='Project Update',
    body='<h1>Update</h1><p>Project is on track.</p>',
    cc='manager@company.com'
)
```

### Pattern 2: Send Email with Attachments

```python
from skills_silver import EmailMCPSkill

email = EmailMCPSkill(smtp_config=smtp_config)

email.send_email(
    to='client@example.com',
    subject='Invoice',
    body='Please find attached invoice.',
    attachments=['Invoices/invoice_001.pdf']
)
```

### Pattern 3: Create Draft for Review

```python
from skills_silver import EmailMCPSkill

email = EmailMCPSkill()

draft_path = email.create_draft(
    to='client@example.com',
    subject='Project Proposal',
    body='Dear Client,\n\nPlease find our proposal attached...',
    draft_name='PROPOSAL_ClientX.md'
)
```

### Pattern 4: Send with Approval Workflow

```python
from skills_silver import EmailMCPSkill

email = EmailMCPSkill()

# Creates approval request in Pending_Approval/
approval_path = email.send_with_approval(
    to='newclient@example.com',
    subject='Partnership Opportunity',
    body='We would like to propose...'
)
```

## SMTP Configuration

### Gmail

```python
smtp_config = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'from_email': 'you@gmail.com',
    'username': 'you@gmail.com',
    'password': 'your-16-char-app-password'
}
```

### Outlook/Hotmail

```python
smtp_config = {
    'smtp_server': 'smtp.office365.com',
    'smtp_port': 587,
    'from_email': 'you@outlook.com',
    'username': 'you@outlook.com',
    'password': 'your-password'
}
```

### Custom SMTP

```python
smtp_config = {
    'smtp_server': 'mail.yourcompany.com',
    'smtp_port': 587,
    'from_email': 'you@yourcompany.com',
    'username': 'you@yourcompany.com',
    'password': 'your-password'
}
```

## Environment Variables (Recommended)

Instead of hardcoding credentials, use environment variables:

```bash
# .env file (add to .gitignore)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FROM_EMAIL=you@gmail.com
USERNAME=you@gmail.com
PASSWORD=your-app-password
```

```python
import os
from skills_silver import EmailMCPSkill

smtp_config = {
    'smtp_server': os.getenv('SMTP_SERVER'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'from_email': os.getenv('FROM_EMAIL'),
    'username': os.getenv('USERNAME'),
    'password': os.getenv('PASSWORD')
}

email = EmailMCPSkill(smtp_config=smtp_config)
```

## Integration with AI Employee

### Email from Gmail Watcher

```
Gmail Watcher detects email
       ↓
Creates action file in Needs_Action/
       ↓
Orchestrator processes
       ↓
EmailMCPSkill creates reply draft
       ↓
Pending_Approval/ (if new contact)
       ↓
Human approves (moves to Approved/)
       ↓
Email sent via SMTP
       ↓
Logged and moved to Done/
```

### Automated Email Responses

```python
from skills_silver import EmailMCPSkill, ApprovalWorkflowSkill

email = EmailMCPSkill(smtp_config=smtp_config)
approval = ApprovalWorkflowSkill()

# Check if recipient is known
known_contacts = ['client1@example.com', 'client2@example.com']
is_known = recipient_email in known_contacts

if is_known:
    # Send directly for known contacts
    email.send_email(recipient_email, subject, body)
else:
    # Require approval for new contacts
    email.send_with_approval(recipient_email, subject, body)
```

## Email Templates

### Invoice Email

```python
template = """
Dear {name},

Please find attached invoice #{invoice_number} for ${amount}.

Payment is due within {days} days.

Thank you for your business!

Best regards,
Your Company
"""
```

### Follow-up Email

```python
template = """
Hi {name},

Following up on my previous email regarding {topic}.

Have you had a chance to review?

Looking forward to hearing from you.

Best regards,
Your Company
"""
```

### Meeting Request

```python
template = """
Hi {name},

I would like to schedule a meeting to discuss {topic}.

Are you available on {date_option1} or {date_option2}?

Please let me know what works best.

Best regards,
Your Company
"""
```

## Commands

### Send Test Email

```bash
python -c "
from skills_silver import EmailMCPSkill
import os

smtp_config = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': 587,
    'from_email': os.getenv('FROM_EMAIL'),
    'username': os.getenv('USERNAME'),
    'password': os.getenv('PASSWORD')
}

email = EmailMCPSkill(smtp_config=smtp_config)
email.send_email('test@example.com', 'Test Subject', 'Test body')
"
```

### List Email Drafts

```bash
python -c "from skills_silver import EmailMCPSkill; e = EmailMCPSkill(); print('\n'.join(e.file_ops.list_files('Pending_Approval')))"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Use app-specific password for Gmail |
| Connection timeout | Check SMTP server and port |
| Email not sent | Verify SMTP credentials are correct |
| Attachments fail | Ensure file paths are relative to vault |

## Security Best Practices

1. **Never commit credentials** - Use environment variables or .env file
2. **Use app-specific passwords** - Don't use main account password
3. **Enable 2FA** - Required for Gmail app passwords
4. **Review before sending** - Use approval workflow for new contacts
5. **Log all sends** - Check Logs/ folder for audit trail

## Related Skills

- `approval-workflow` - For email approval requests
- `gmail-watcher` - For processing incoming emails
- `linkedin-posting` - For alternative communication channel
