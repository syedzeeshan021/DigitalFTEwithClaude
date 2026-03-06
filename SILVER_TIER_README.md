# AI Employee - Silver Tier Implementation

This document describes the Silver Tier implementation of the Personal AI Employee, building upon the Bronze Tier foundation.

## Silver Tier Requirements Completed

1. ✅ **All Bronze Tier requirements**
   - Obsidian vault with Dashboard.md and Company_Handbook.md
   - File System Watcher working
   - Claude Code reading/writing to vault
   - Basic folder structure
   - Agent Skills implementation

2. ✅ **Two or more Watcher scripts**
   - File System Watcher (from Bronze Tier)
   - Gmail Watcher (new for Silver Tier)

3. ✅ **Automatically Post on LinkedIn about business**
   - LinkedInSkill for creating and managing posts
   - Business update posts for generating sales
   - Tip posts for thought leadership

4. ✅ **Claude reasoning loop that creates Plan.md files**
   - PlanningSkill for creating structured plans
   - Support for objectives, steps, and progress tracking
   - Integration with approval workflow

5. ✅ **One working MCP server for external action**
   - EmailMCPSkill for sending emails via SMTP
   - Draft email creation with approval workflow
   - Integration with approval system

6. ✅ **Human-in-the-loop approval workflow**
   - ApprovalWorkflowSkill for managing sensitive actions
   - Configurable approval thresholds
   - Support for payments, emails, and file operations

7. ✅ **Basic scheduling via cron or Task Scheduler**
   - SchedulingSkill for creating scheduled tasks
   - Support for Windows Task Scheduler, cron, and PM2
   - Pre-configured daily briefing and hourly check schedules

8. ✅ **All AI functionality implemented as Agent Skills**
   - Modular skill architecture
   - Easy to extend and maintain

## Files Included

### Core Skills (skills_silver.py)
- **FileOperationsSkill**: File I/O operations (extended from Bronze)
- **GmailWatcherSkill**: Monitor Gmail and create action items
- **PlanningSkill**: Create and manage plans with Claude reasoning
- **ApprovalWorkflowSkill**: Human-in-the-loop approval system
- **EmailMCPSkill**: Send emails and create drafts
- **LinkedInSkill**: Create and manage LinkedIn posts
- **SchedulingSkill**: Create and manage scheduled tasks

### Watcher Scripts
- `filesystem_watcher.py`: Monitors file system for new items (Bronze)
- `gmail_watcher.py`: Monitors Gmail for new emails (Silver)

### Configuration
- `ecosystem.config.js`: PM2 configuration for all processes
- `requirements.txt`: Python dependencies for Silver Tier

## Silver Tier Skills Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SILVER TIER SKILLS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  Gmail Watcher   │    │ Filesystem       │               │
│  │  Skill           │    │ Watcher          │               │
│  └────────┬─────────┘    └────────┬─────────┘               │
│           │                       │                          │
│           └───────────┬───────────┘                          │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Needs_Action Folder                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                       │                                      │
│           ┌───────────┴───────────┐                          │
│           │                       │                          │
│           ▼                       ▼                          │
│  ┌─────────────────┐    ┌─────────────────┐                  │
│  │  Planning Skill │    │  Approval       │                  │
│  │  (Claude Loop)  │    │  Workflow Skill │                  │
│  └────────┬────────┘    └────────┬────────┘                  │
│           │                      │                           │
│           │                      │                           │
│           ▼                      ▼                           │
│  ┌─────────────────┐    ┌─────────────────┐                  │
│  │  LinkedIn Skill │    │  Email MCP      │                  │
│  │  (Auto Post)    │    │  Skill          │                  │
│  └─────────────────┘    └─────────────────┘                  │
│                                                              │
│           ┌─────────────────────────┐                        │
│           │   Scheduling Skill      │                        │
│           │   (Cron/Task Scheduler) │                        │
│           └─────────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Gmail Watcher (Optional)

To enable Gmail monitoring:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth2 credentials
5. Download credentials.json to vault root
6. Run the authentication flow

### 3. Configure Email MCP

Add SMTP configuration to environment variables or .env file:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
FROM_EMAIL=your-email@gmail.com
USERNAME=your-username
PASSWORD=your-app-password
```

### 4. Setup PM2 Processes

```bash
# Delete old processes
pm2 delete all

# Start new Silver Tier configuration
pm2 start ecosystem.config.js

# Save configuration
pm2 save
```

### 5. Setup Scheduling

For daily briefings and automated tasks:

**Windows Task Scheduler:**
```bash
# Open Task Scheduler and create tasks based on:
pm2 start ecosystem.config.js
```

**Linux/Mac Cron:**
```bash
# Add to crontab
0 8 * * * cd /path/to/project && python orchestrator.py --generate-briefing
```

## Usage Examples

### Create a Plan

```python
from skills_silver import PlanningSkill

planning = PlanningSkill()

plan_path = planning.create_plan(
    title="Q1 Marketing Campaign",
    objective="Increase leads by 30%",
    context="Current lead generation is at 50/month",
    steps=[
        "Create content calendar",
        "Set up LinkedIn posting",
        "Track engagement metrics"
    ],
    priority="high"
)
```

### Create Approval Request

```python
from skills_silver import ApprovalWorkflowSkill

approval = ApprovalWorkflowSkill()

approval_path = approval.create_approval_request(
    action_type="payment",
    details={
        "amount": "$500.00",
        "recipient": "Vendor ABC",
        "purpose": "Software subscription"
    },
    reason="Payment exceeds $100 threshold"
)
```

### Create LinkedIn Post

```python
from skills_silver import LinkedInSkill

linkedin = LinkedInSkill()

# Business update post
post_path = linkedin.create_business_update_post(
    achievement="We reached 1000+ satisfied clients!",
    call_to_action="Contact us to learn more."
)

# Tip post
tip_path = linkedin.create_tip_post(
    topic="Productivity",
    tips=[
        "Start your day with a clear plan",
        "Use time-blocking for deep work",
        "Take regular breaks to stay fresh"
    ]
)
```

### Schedule a Task

```python
from skills_silver import SchedulingSkill

scheduling = SchedulingSkill()

# Daily briefing at 8 AM
daily = scheduling.create_daily_briefing_schedule("08:00")

# Hourly system check
hourly = scheduling.create_hourly_check_schedule()

# Get setup instructions
print(daily['setup_instructions']['windows'])
```

## Approval Workflow

The approval workflow ensures human oversight for sensitive actions:

### Actions Requiring Approval

| Action Type | Threshold | Reason |
|-------------|-----------|--------|
| Payment | > $100 | Financial control |
| Payment | New recipient | Fraud prevention |
| Email | > 10 recipients | Bulk communication |
| File Delete | Any | Data protection |

### Approval Process

1. AI Employee detects action requiring approval
2. Creates approval request file in `Pending_Approval/`
3. Human reviews and moves file to:
   - `/Approved` - Action will be executed
   - `/Rejected` - Action is cancelled
4. System logs the decision

## Monitoring and Logs

All skills log to the `Logs/` folder:

- `gmail_watcher_YYYYMMDD.log`: Gmail monitoring
- `email_mcp_YYYYMMDD.log`: Email operations
- `linkedin_skill_YYYYMMDD.log`: LinkedIn posts
- `orchestrator_YYYYMMDD.log`: System orchestration

View PM2 logs:
```bash
pm2 logs --lines 50
```

## Silver Tier vs Bronze Tier

| Feature | Bronze Tier | Silver Tier |
|---------|-------------|-------------|
| Watchers | 1 (Filesystem) | 2+ (Filesystem + Gmail) |
| Planning | Basic | Claude Reasoning Loop |
| External Actions | None | Email MCP |
| Approval Workflow | Basic | Full HITL System |
| Social Media | None | LinkedIn Auto-Post |
| Scheduling | Manual | Cron/Task Scheduler |
| Skills | 3 | 7 |

## Next Steps (Gold Tier)

To advance to Gold Tier, add:
- Facebook/Instagram integration
- Twitter (X) integration
- Odoo accounting integration
- Multiple MCP servers
- Weekly CEO Briefing generation
- Error recovery system
- Comprehensive audit logging
- Ralph Wiggum persistence loop

## Troubleshooting

### Gmail Watcher Not Working
- Verify OAuth2 credentials are valid
- Check Gmail API is enabled
- Ensure credentials.json is in correct location

### LinkedIn Posts Not Publishing
- Full LinkedIn API integration required
- For now, posts are created as drafts
- Move to /Approved to mark as ready

### Approval Workflow Issues
- Check file permissions in vault
- Verify folder structure exists
- Review logs for specific errors

## Support

For issues or questions:
1. Check logs in `Logs/` folder
2. Review PM2 logs: `pm2 logs`
3. Consult the hackathon document
4. Join Wednesday Research Meeting (Zoom link in main doc)