---
name: scheduling-skill
description: |
  Create and manage scheduled tasks via cron, Windows Task Scheduler, or PM2.
  Supports daily briefings, hourly checks, and custom scheduled operations.
  Use for automating recurring AI Employee tasks.
---

# Scheduling Skill

Schedule and manage recurring tasks for the AI Employee.

## Quick Start

### Create Daily Briefing Schedule

```bash
python -c "from skills_silver import SchedulingSkill; s = SchedulingSkill(); print(s.create_daily_briefing_schedule('08:00'))"
```

### Create Hourly Check Schedule

```bash
python -c "from skills_silver import SchedulingSkill; s = SchedulingSkill(); print(s.create_hourly_check_schedule())"
```

### Create Custom Schedule

```bash
python -c "from skills_silver import SchedulingSkill; s = SchedulingSkill(); print(s.create_scheduled_task('weekly_report', 'orchestrator.py --weekly-report', '0 9 * * 1', 'Generate weekly report every Monday'))"
```

## Usage Patterns

### Pattern 1: Daily Briefing at 8 AM

```python
from skills_silver import SchedulingSkill

scheduling = SchedulingSkill()

result = scheduling.create_daily_briefing_schedule("08:00")

print(f"Task: {result['task']['name']}")
print(f"Schedule: {result['task']['schedule']}")
print("\nSetup Instructions:")
print(result['setup_instructions']['windows'])
```

### Pattern 2: Hourly System Check

```python
from skills_silver import SchedulingSkill

scheduling = SchedulingSkill()

result = scheduling.create_hourly_check_schedule()

print(f"Task: {result['task']['name']}")
print(f"Schedule: {result['task']['schedule']}")
```

### Pattern 3: Custom Scheduled Task

```python
from skills_silver import SchedulingSkill

scheduling = SchedulingSkill()

result = scheduling.create_scheduled_task(
    name="weekly_report",
    command="orchestrator.py --generate-weekly-report",
    schedule="0 9 * * 1",  # Every Monday at 9 AM
    description="Generate weekly business report"
)

print(result['setup_instructions']['windows'])
```

### Pattern 4: List All Scheduled Tasks

```python
from skills_silver import SchedulingSkill

scheduling = SchedulingSkill()

tasks = scheduling.list_scheduled_tasks()
for task in tasks:
    print(f"Name: {task['name']}")
    print(f"Schedule: {task['schedule']}")
    print(f"Enabled: {task['enabled']}")
    print("---")
```

### Pattern 5: Enable/Disable Task

```python
from skills_silver import SchedulingSkill

scheduling = SchedulingSkill()

# Disable a task
scheduling.disable_task("daily_briefing")

# Enable a task
scheduling.enable_task("daily_briefing")
```

## Cron Expressions

### Format
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, Sunday=0 or 7)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

### Common Schedules

| Description | Cron Expression |
|-------------|-----------------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every hour | `0 * * * *` |
| Every hour at 30 min | `30 * * * *` |
| Daily at midnight | `0 0 * * *` |
| Daily at 8 AM | `0 8 * * *` |
| Daily at 5:30 PM | `30 17 * * *` |
| Every Monday 9 AM | `0 9 * * 1` |
| Every Friday 5 PM | `0 17 * * 5` |
| 1st of every month | `0 0 1 * *` |
| Weekdays 9 AM | `0 9 * * 1-5` |

## Setup Instructions by Platform

### Windows Task Scheduler

```
1. Open Task Scheduler (taskschd.msc)
2. Click "Create Basic Task" in the right panel
3. Name: {task_name}
4. Description: {description}
5. Trigger: Choose your schedule
6. Action: "Start a program"
7. Program/script: python
8. Add arguments: {command}
9. Start in: {vault_path}
10. Finish and test the task
```

### Linux/Mac Cron

```bash
# Open crontab editor
crontab -e

# Add line in format:
{schedule} cd {vault_path} && python {command} >> {vault_path}/Logs/{task_name}.log 2>&1

# Example: Daily briefing at 8 AM
0 8 * * * cd /path/to/AI_Employee_Vault && python orchestrator.py --generate-briefing >> /path/to/AI_Employee_Vault/Logs/daily_briefing.log 2>&1

# Save and exit
# Verify: crontab -l
```

### PM2 (Cross-Platform)

```bash
# Install PM2
npm install -g pm2

# Start task with cron schedule
pm2 start {command} --name {task_name} --cron "{schedule}"

# Save PM2 configuration
pm2 save

# Setup PM2 startup (run once)
pm2 startup

# View logs
pm2 logs {task_name}
```

## Pre-configured Tasks

### Daily Briefing

Generates CEO briefing every morning.

```python
scheduling.create_daily_briefing_schedule("08:00")
```

**Schedule:** `0 8 * * *` (Daily at 8 AM)

**Output:** `Briefings/YYYY-MM-DD_Briefing.md`

### Hourly Check

Runs system health check every hour.

```python
scheduling.create_hourly_check_schedule()
```

**Schedule:** `0 * * * *` (Every hour)

**Checks:**
- Orchestrator status
- Watcher status
- Queue lengths
- Error logs

## Integration with AI Employee

### Scheduled Task Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              SCHEDULING WORKFLOW                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SchedulingSkill creates task configuration              │
│                                                              │
│  2. Platform-specific setup                                 │
│     - Windows: Task Scheduler                               │
│     - Linux/Mac: Cron                                       │
│     - Cross-platform: PM2                                   │
│                                                              │
│  3. At scheduled time, task executes                        │
│     - Python script runs                                    │
│     - Output logged to Logs/                                │
│                                                              │
│  4. AI Employee processes results                           │
│     - Creates files in vault                                │
│     - Updates Dashboard                                     │
│     - Sends notifications if needed                         │
│                                                              │
│  5. Task status tracked                                     │
│     - Last run time recorded                                │
│     - Next run time calculated                              │
│     - Errors logged                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Daily Briefing Content

When scheduled, daily briefing generates:

```markdown
---
generated: 2026-03-03T08:00:00Z
period: 2026-03-02 to 2026-03-03
---

# Monday Morning CEO Briefing

## Executive Summary
Brief overview of business status.

## Revenue
- **This Week**: $X,XXX
- **MTD**: $X,XXX
- **Trend**: On track / Behind / Ahead

## Completed Tasks
- [x] Task 1
- [x] Task 2

## Bottlenecks
| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| ... | ... | ... | ... |

## Proactive Suggestions
### Cost Optimization
- Subscription alerts
- Unused service detection

### Upcoming Deadlines
- Project deadlines
- Payment due dates
```

## Commands

### List Scheduled Tasks

```bash
python -c "from skills_silver import SchedulingSkill; s = SchedulingSkill(); [print(t['name'], t['schedule']) for t in s.list_scheduled_tasks()]"
```

### Get Setup Instructions

```bash
python -c "
from skills_silver import SchedulingSkill
s = SchedulingSkill()
task = s.create_scheduled_task('test', 'test.py', '0 * * * *')
print(task['setup_instructions']['windows'])
"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task not running | Check scheduler service is running |
| Python not found | Use full path to python executable |
| File not found | Ensure 'Start in' directory is set |
| No output in logs | Check file permissions |
| Cron not working | Verify crontab syntax with `crontab -l` |

## Best Practices

1. **Log everything** - Always redirect output to log files
2. **Set proper working directory** - Tasks may run from different locations
3. **Use absolute paths** - Avoid relative path issues
4. **Test before scheduling** - Run commands manually first
5. **Monitor regularly** - Check logs for errors
6. **Handle errors gracefully** - Scripts should not crash silently

## Related Skills

- `planning-skill` - For planning scheduled operations
- `approval-workflow` - For approving scheduled actions
