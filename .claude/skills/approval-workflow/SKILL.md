---
name: approval-workflow
description: |
  Human-in-the-loop approval system for sensitive actions. Creates approval request
  files that require human review before executing payments, emails, file operations,
  and other sensitive actions. Ensures AI Employee operates with proper oversight.
---

# Approval Workflow Skill - Human-in-the-Loop

Manage approval requests for sensitive AI Employee actions.

## Quick Start

### Create Approval Request

```bash
python -c "from skills_silver import ApprovalWorkflowSkill; a = ApprovalWorkflowSkill(); print(a.create_approval_request('payment', {'amount': '$500', 'recipient': 'Vendor'}, 'Payment exceeds threshold'))"
```

### Approval File Location
Approval requests are created in: `AI_Employee_Vault/Pending_Approval/`

## Approval File Structure

```markdown
---
type: approval_request
action_type: payment
created: 2026-03-03T00:00:00
expires: 2026-03-04T00:00:00
status: pending
reason: Payment exceeds $100 threshold
---

# Approval Request: Payment

## Request Details
- **Amount:** $500.00
- **Recipient:** Vendor ABC
- **Purpose:** Software subscription

## Reason for Approval
Payment exceeds $100 threshold

## Expires
2026-03-04T00:00:00

## Instructions

### To Approve
Move this file to the `/Approved` folder.

### To Reject
Move this file to the `/Rejected` folder with a comment explaining why.

### To Request More Information
Add a comment to this file and move it back to `/Needs_Action`.

## Audit Trail
- Created: 2026-03-03T00:00:00
- Status: Pending Approval
```

## Usage Patterns

### Pattern 1: Payment Approval

```python
from skills_silver import ApprovalWorkflowSkill

approval = ApprovalWorkflowSkill()
approval_path = approval.create_approval_request(
    action_type="payment",
    details={
        "amount": "$500.00",
        "recipient": "Vendor ABC",
        "purpose": "Monthly software subscription",
        "is_new_recipient": False
    },
    reason="Payment exceeds $100 threshold"
)
```

### Pattern 2: Email Approval

```python
from skills_silver import ApprovalWorkflowSkill

approval = ApprovalWorkflowSkill()
approval_path = approval.create_approval_request(
    action_type="email_send",
    details={
        "to": "client@example.com",
        "subject": "Project Proposal",
        "body_preview": "Dear Client, Please find attached..."
    },
    reason="Email to new client requires review"
)
```

### Pattern 3: Check Approval Status

```python
from skills_silver import ApprovalWorkflowSkill

approval = ApprovalWorkflowSkill()
status = approval.check_approval_status("APPROVAL_PAYMENT_20260303_120000.md")
print(f"Status: {status}")  # 'pending', 'approved', or 'rejected'
```

### Pattern 4: List Pending Approvals

```python
from skills_silver import ApprovalWorkflowSkill

approval = ApprovalWorkflowSkill()
pending = approval.get_pending_approvals()
print(f"Pending approvals: {len(pending)}")
for item in pending:
    print(f"  - {item}")
```

### Pattern 5: Check If Action Requires Approval

```python
from skills_silver import ApprovalWorkflowSkill

approval = ApprovalWorkflowSkill()

# Payment over $100 requires approval
needs_approval = approval.requires_approval(
    action_type="payment",
    details={"amount": 500, "is_new_recipient": False}
)
print(f"Needs approval: {needs_approval}")  # True
```

## Approval Thresholds

| Action Type | Threshold | Auto-Approval |
|-------------|-----------|---------------|
| Payment | > $100 | No |
| Payment | New recipient | Never (always approve) |
| Email | > 10 recipients | No |
| Email | New contact | Recommended |
| File Delete | Any | Always |
| File Move | Outside vault | Always |

## Approval Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    APPROVAL WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. AI Employee detects action needed                       │
│                                                              │
│  2. Check if approval required                              │
│     ┌──────────────────────────────────────────┐            │
│     │ requires_approval(action_type, details)  │            │
│     └──────────────────────────────────────────┘            │
│                    │                                         │
│         ┌──────────┴──────────┐                             │
│         │                     │                             │
│         ▼                     ▼                             │
│    Needs Approval        No Approval                         │
│         │                     │                             │
│         │                     ▼                             │
│         │            Execute action                          │
│         │                     │                             │
│         ▼                     │                             │
│  3. Create approval file      │                             │
│     Pending_Approval/         │                             │
│         │                     │                             │
│         │                     │                             │
│         ▼                     │                             │
│  4. Human reviews             │                             │
│         │                     │                             │
│    ┌────┴────┐                │                             │
│    │         │                │                             │
│    ▼         ▼                │                             │
│  Approve   Reject             │                             │
│    │         │                │                             │
│    │         │                │                             │
│    ▼         ▼                │                             │
│  /Approved  /Rejected         │                             │
│    │                          │                             │
│    │                          │                             │
│    ▼                          │                             │
│  5. Execute action ◄──────────┘                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Human Actions

### Approve an Action
```bash
# Move file from Pending_Approval to Approved
mv AI_Employee_Vault/Pending_Approval/APPROVAL_*.md AI_Employee_Vault/Approved/
```

### Reject an Action
```bash
# Move file from Pending_Approval to Rejected
mv AI_Employee_Vault/Pending_Approval/APPROVAL_*.md AI_Employee_Vault/Rejected/
```

### Add Comment to Approval Request
```bash
# Edit the file to add comments, then move to Needs_Action
echo "## Comment\nNeed more information about..." >> AI_Employee_Vault/Pending_Approval/APPROVAL_*.md
mv AI_Employee_Vault/Pending_Approval/APPROVAL_*.md AI_Employee_Vault/Needs_Action/
```

## Integration with AI Employee

### Email Approval Flow

```python
from skills_silver import EmailMCPSkill, ApprovalWorkflowSkill

email = EmailMCPSkill()
approval = ApprovalWorkflowSkill()

# Check if approval needed
if approval.requires_approval("email", {"recipients": ["client@example.com"]}):
    # Create approval request
    approval_path = approval.create_approval_request(
        action_type="email_send",
        details={"to": "client@example.com", "subject": "Proposal"},
        reason="New client communication"
    )
    print(f"Approval required: {approval_path}")
else:
    # Send directly
    email.send_email("client@example.com", "Proposal", "Body text")
```

### Payment Approval Flow

```python
from skills_silver import ApprovalWorkflowSkill

approval = ApprovalWorkflowSkill()

# Large payment requires approval
payment_details = {"amount": 500, "recipient": "Vendor", "is_new_recipient": False}

if approval.requires_approval("payment", payment_details):
    approval.create_approval_request(
        action_type="payment",
        details=payment_details,
        reason="Payment exceeds $100 threshold"
    )
```

## Commands

### View All Pending Approvals
```bash
python -c "from skills_silver import ApprovalWorkflowSkill; a = ApprovalWorkflowSkill(); print('\n'.join(a.get_pending_approvals()))"
```

### Check Specific Approval Status
```bash
python -c "from skills_silver import ApprovalWorkflowSkill; a = ApprovalWorkflowSkill(); print(a.check_approval_status('APPROVAL_PAYMENT_20260303_120000.md'))"
```

### Process Approved Actions
```bash
python -c "from skills_silver import ApprovalWorkflowSkill; a = ApprovalWorkflowSkill(); print(a.process_approved_actions())"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Approval file not created | Check vault path and permissions |
| Can't check status | Verify filename is correct |
| Approval not processed | Ensure file was moved to /Approved folder |
| Expired approvals | Review and clean up old approval files manually |

## Related Skills

- `planning-skill` - For plans requiring approval
- `email-mcp` - For email approval workflow
- `linkedin-posting` - For social media approval
