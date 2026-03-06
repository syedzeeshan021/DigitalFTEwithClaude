---
name: planning-skill
description: |
  Create and manage plans with Claude reasoning loop. Creates Plan.md files in the
  AI Employee vault with structured objectives, steps, and progress tracking. Use for
  breaking down complex tasks, project planning, and tracking multi-step workflows.
---

# Planning Skill - Claude Reasoning Loop

Create structured plans with Claude reasoning capabilities for the AI Employee.

## Quick Start

### Create a New Plan

```bash
python -c "from skills_silver import PlanningSkill; p = PlanningSkill(); print(p.create_plan('My Plan', 'Objective description', context='Background info', steps=['Step 1', 'Step 2'], priority='high'))"
```

### Plan File Location
Plans are created in: `AI_Employee_Vault/Plans/`

## Plan Structure

```markdown
---
title: Plan Title
objective: Main objective
priority: high
status: planning
created_at: 2026-03-03T00:00:00
updated_at: 2026-03-03T00:00:00
---

# Plan: Title

## Objective
Main objective description

## Context
Background and context

## Steps
- [ ] Step 1: Description
- [ ] Step 2: Description

## Claude Reasoning Notes

### Analysis
- What is the main goal?
- What are the constraints?
- What resources are needed?

### Strategy
- What approach will be taken?
- What are the potential obstacles?
- How will success be measured?

### Progress
- Steps completed: 0
- Steps remaining: TBD
- Blockers: None identified yet
```

## Usage Patterns

### Pattern 1: Simple Plan

```python
from skills_silver import PlanningSkill

planning = PlanningSkill()
plan_path = planning.create_plan(
    title="Weekly Content Calendar",
    objective="Create 5 LinkedIn posts for this week",
    priority="medium"
)
```

### Pattern 2: Detailed Plan with Steps

```python
from skills_silver import PlanningSkill

planning = PlanningSkill()
plan_path = planning.create_plan(
    title="Q1 Sales Campaign",
    objective="Increase Q1 sales by 25% through LinkedIn outreach",
    context="Current sales are at $100K/month, target is $125K/month",
    steps=[
        "Analyze current sales pipeline",
        "Create LinkedIn content calendar",
        "Set up automated posting schedule",
        "Track engagement metrics",
        "Adjust strategy based on results"
    ],
    priority="high"
)
```

### Pattern 3: Update Plan Progress

```python
from skills_silver import PlanningSkill

planning = PlanningSkill()
planning.update_plan("PLAN_20260303_Q1_Sales_Campaign.md", {
    "status": "active",
    "new_steps": ["Follow up with leads"]
})
```

### Pattern 4: Check Plan Status

```python
from skills_silver import PlanningSkill

planning = PlanningSkill()
status = planning.get_plan_status("PLAN_20260303_Q1_Sales_Campaign.md")
print(f"Progress: {status['steps_completed']}/{status['steps_total']}")
```

## Integration with AI Employee

### Workflow

1. **Trigger**: New item in Needs_Action requires planning
2. **Create Plan**: PlanningSkill creates Plan.md in Plans/
3. **Claude Processes**: AI analyzes and executes steps
4. **Update Progress**: Mark steps complete as work progresses
5. **Complete**: Move to Done when all steps finished

### Example Flow

```
Needs_Action/CLIENT_INQUIRY.md
       ↓
PlanningSkill.create_plan()
       ↓
Plans/PLAN_CLIENT_INQUIRY.md
       ↓
Claude executes steps
       ↓
Done/PLAN_CLIENT_INQUIRY.md
```

## Priority Levels

| Priority | Use Case | Response Time |
|----------|----------|---------------|
| critical | Urgent client issues, system outages | Immediate |
| high | Revenue-generating activities | Same day |
| medium | Regular business operations | Within 24 hours |
| low | Nice-to-have improvements | When time permits |

## Status Values

| Status | Description |
|--------|-------------|
| planning | Plan being created/refined |
| active | Plan in execution |
| blocked | Waiting on external factor |
| completed | All steps finished |
| cancelled | Plan no longer needed |

## Commands

### List All Plans
```bash
python -c "from skills_silver import PlanningSkill; p = PlanningSkill(); print('\n'.join(p.list_plans()))"
```

### List Plans by Status
```bash
python -c "from skills_silver import PlanningSkill; p = PlanningSkill(); print('\n'.join(p.list_plans('active')))"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plan not created | Check vault path is correct |
| Can't update plan | Verify plan filename exists in Plans/ |
| Status not updating | Ensure plan file is not open in another program |

## Related Skills

- `approval-workflow` - For plans requiring approval
- `linkedin-posting` - For LinkedIn-related plans
- `scheduling-skill` - For scheduling plan-related tasks
