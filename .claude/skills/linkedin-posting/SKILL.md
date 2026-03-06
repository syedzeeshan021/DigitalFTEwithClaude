---
name: linkedin-posting
description: |
  Create and manage LinkedIn posts for business growth and lead generation. Supports
  business updates, thought leadership tips, and automated posting with approval
  workflow. Use for social media marketing and brand building.
---

# LinkedIn Posting Skill

Create and manage LinkedIn posts for the AI Employee.

## Quick Start

### Create Business Update Post

```bash
python -c "from linkedin_posting import LinkedInPostingSkill; l = LinkedInPostingSkill(); print(l.create_business_update_post('We reached 1000+ satisfied clients!', 'Contact us to learn more.'))"
```

### Create Tip Post

```bash
python -c "from linkedin_posting import LinkedInPostingSkill; l = LinkedInPostingSkill(); print(l.create_tip_post('Productivity', ['Start with a plan', 'Focus on one task', 'Take regular breaks']))"
```

### Create Custom Post

```bash
python -c "from linkedin_posting import LinkedInPostingSkill; l = LinkedInPostingSkill(); print(l.create_linkedin_post('Exciting news about our new product launch!', 'announcement', ['#NewProduct', '#Innovation']))"
```

### Test the Skill

```bash
python linkedin_posting.py
```

## Post File Structure

```markdown
---
type: linkedin_post
post_type: business_update
created: 2026-03-03T00:00:00
status: draft
scheduled_time: Not scheduled
---

# LinkedIn Post Draft

## Content
Exciting business update content here!

## Post Type
business_update

## Created
2026-03-03T00:00:00

## Suggested Actions
- [ ] Review content for accuracy
- [ ] Check for typos and formatting
- [ ] Add relevant images or media (optional)
- [ ] Move to /Approved to publish
- [ ] Move to /Rejected to discard

## Engagement Goals
- Target impressions: 1000+
- Target engagements: 50+
- Target leads: 5+

## Notes
Add any additional context or follow-up actions here.
```

## Usage Patterns

### Pattern 1: Business Update Post (Sales Focus)

```python
from linkedin_posting import LinkedInPostingSkill

linkedin = LinkedInPostingSkill()

post_path = linkedin.create_business_update_post(
    achievement="We're excited to announce that we've reached 1000+ satisfied clients!",
    call_to_action="Contact us today to learn how we can help your business grow."
)
```

### Pattern 2: Thought Leadership Tip Post

```python
from linkedin_posting import LinkedInPostingSkill

linkedin = LinkedInPostingSkill()

post_path = linkedin.create_tip_post(
    topic="Productivity",
    tips=[
        "Start your day with a clear plan",
        "Use time-blocking for deep work",
        "Take regular breaks to stay fresh",
        "Review and adjust at end of day"
    ]
)
```

### Pattern 3: Custom Post with Hashtags

```python
from linkedin_posting import LinkedInPostingSkill

linkedin = LinkedInPostingSkill()

post_path = linkedin.create_linkedin_post(
    content="Just finished an amazing workshop on AI automation. The future is here!",
    post_type="event",
    hashtags=["AI", "Automation", "Workshop", "Learning"]
)
```

### Pattern 4: Question Post for Engagement

```python
from linkedin_posting import LinkedInPostingSkill

linkedin = LinkedInPostingSkill()

post_path = linkedin.create_question_post(
    question="What's the biggest challenge you face with AI adoption in your organization?",
    context="I'm curious to hear different perspectives from folks in various industries."
)
```

### Pattern 5: Product Announcement

```python
from linkedin_posting import LinkedInPostingSkill

linkedin = LinkedInPostingSkill()

post_path = linkedin.create_announcement_post(
    product_name="AI Employee v1.0",
    description="An autonomous digital assistant that automates your daily business operations.",
    features=[
        "24/7 email monitoring",
        "Automated task management",
        "WhatsApp integration",
        "Human-in-the-loop approvals"
    ],
    link="https://yourcompany.com/ai-employee"
)
```

## Post Types

| Type | Purpose | Example |
|------|---------|---------|
| business_update | Company news, milestones | "We reached 1000+ clients!" |
| announcement | Product launches, events | "New product launching today!" |
| tip | Thought leadership | "5 tips for better productivity" |
| article | Share blog posts | "Just published: AI in 2026" |
| celebration | Team achievements | "Welcome our new team member!" |
| question | Engagement focused | "What's your biggest challenge?" |

## Hashtag Strategy

### Recommended Hashtag Groups

**Business Growth:**
```
#BusinessGrowth #Entrepreneurship #Startup #SmallBusiness #GrowthMindset
```

**Technology:**
```
#AI #Automation #Technology #Innovation #DigitalTransformation
```

**Productivity:**
```
#Productivity #TimeManagement #Efficiency #WorkLifeBalance #Success
```

**Thought Leadership:**
```
#ThoughtLeadership #Leadership #BusinessStrategy #Innovation #Expertise
```

**Client Success:**
```
#ClientSuccess #Testimonial #CustomerExperience #BusinessGrowth #Results
```

## Content Templates

### Milestone Announcement

```
Excited to share some great news!

{ACHIEVEMENT}

This milestone represents our commitment to delivering exceptional value to our clients. We're grateful for the trust you've placed in us.

{CALL_TO_ACTION}

#Milestone #BusinessGrowth #ClientSuccess #Grateful
```

### Tip Post

```
Here are {NUMBER} quick tips for {TOPIC}:

{TIP_1}
{TIP_2}
{TIP_3}

Which tip resonates most with you? Share your thoughts in the comments!

#Tips #{TOPIC} #BestPractices #Learning
```

### Question Post

```
Quick question for my network:

{QUESTION}

I'm curious to hear different perspectives from folks in various industries.

Drop your thoughts in the comments!

#Discussion #Networking #Business #Community
```

### Product/Service Launch

```
Big news! We're thrilled to announce {PRODUCT_NAME}!

After {TIME_PERIOD} of development, we're ready to help you {BENEFIT}.

Key features:
  {FEATURE_1}
  {FEATURE_2}
  {FEATURE_3}

Ready to get started? {LINK}

#NewProduct #Launch #Innovation #{INDUSTRY}
```

## Integration with AI Employee

### Automated Posting Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              LINKEDIN POSTING WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. AI Employee identifies posting opportunity              │
│     - Business milestone achieved                            │
│     - Time for scheduled tip                                 │
│     - Client success story                                   │
│                                                              │
│  2. LinkedInPostingSkill creates post draft                 │
│     - Generates content                                      │
│     - Adds relevant hashtags                                 │
│     - Saves to Needs_Action/                                 │
│                                                              │
│  3. Human reviews content                                   │
│     - Checks accuracy                                        │
│     - Edits if needed                                        │
│                                                              │
│  4. Approval decision                                       │
│     - Move to Approved/ → Publish                            │
│     - Move to Rejected/ → Discard                            │
│                                                              │
│  5. Post published (via LinkedIn API or manually)           │
│                                                              │
│  6. Logged and tracked in Done/                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Content Calendar Integration

```python
from linkedin_posting import LinkedInPostingSkill

linkedin = LinkedInPostingSkill()

# Create weekly tip posts
tips = [
    ["Tip 1 for Monday", "Tip 2 for Monday"],
    ["Tip 1 for Wednesday", "Tip 2 for Wednesday"],
    ["Tip 1 for Friday", "Tip 2 for Friday"]
]

for i, tip_group in enumerate(tips):
    post_path = linkedin.create_tip_post(
        topic="Weekly Topic",
        tips=tip_group
    )
    print(f"Created post {i+1}: {post_path}")
```

## Commands

### List All LinkedIn Drafts

```bash
python -c "from linkedin_posting import LinkedInPostingSkill; l = LinkedInPostingSkill(); print('\n'.join(l.list_drafts()))"
```

### Publish a Post (Manual)

```bash
# Move from Needs_Action to Approved for publishing
mv AI_Employee_Vault/Needs_Action/LINKEDIN_POST_*.md AI_Employee_Vault/Approved/
```

### Check Post Statistics

```bash
python -c "
from linkedin_posting import LinkedInPostingSkill
l = LinkedInPostingSkill()
stats = l.get_post_stats('AI_Employee_Vault/Needs_Action/LINKEDIN_POST_*.md')
print(f'Characters: {stats[\"character_count\"]}')
print(f'Hashtags: {stats[\"hashtag_count\"]}')
print(f'Valid: {stats[\"is_valid\"]}')
"
```

## Best Practices

### Content Quality
1. **Keep it professional** - LinkedIn is a business platform
2. **Add value** - Share insights, not just promotions
3. **Use whitespace** - Make posts easy to read
4. **Include CTA** - Tell readers what to do next
5. **Limit hashtags** - 3-5 relevant hashtags max

### Posting Frequency
- **Minimum**: 2-3 times per week
- **Optimal**: Daily (weekdays)
- **Maximum**: 2-3 times per day

### Best Times to Post
- Tuesday-Thursday: 9-11 AM
- Wednesday: Highest engagement
- Avoid: Weekends (lower engagement)

### Engagement Tips
1. Respond to comments within 24 hours
2. Comment on others' posts in your industry
3. Share and celebrate others' success
4. Use @mentions when relevant
5. Add images when possible (higher engagement)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Post not created | Check vault path is correct |
| Hashtags not showing | Ensure hashtags are in content, not just metadata |
| Can't publish | LinkedIn API setup required for auto-publishing |

## Related Skills

- `approval-workflow` - For post approval before publishing
- `scheduling-skill` - For scheduling posts
- `email-mcp` - For cross-channel promotion
- `planning-skill` - For creating posting plans
- `linkedin-watcher` - For automated posting via Playwright

## Automated Posting with LinkedIn Watcher

The `linkedin_watcher.py` script uses Playwright to automatically publish approved posts:

```bash
# Run the LinkedIn Watcher (auto-publishes from Approved/ folder)
python linkedin_watcher.py

# Post directly via command line
python -c "from linkedin_watcher import LinkedInWatcherSkill; l = LinkedInWatcherSkill(); l.post_to_linkedin('Your post content here')"
```

### How LinkedIn Watcher Works with Your Profile

1. **Session Management**: The watcher stores your LinkedIn login session in `AI_Employee_Vault/.linkedin_session/`
2. **First Run**: Opens browser for you to log in manually (session saved for future runs)
3. **Auto-Posting**: Reads approved posts from `Approved/` folder and publishes them
4. **Profile Monitoring**: Can check notifications and engagement metrics

### Workflow

```
1. Create post draft → Needs_Action/LINKEDIN_POST_*.md
2. Review and approve → Move to Approved/
3. Run watcher → Auto-publishes to your LinkedIn profile
4. Post published → Moved to Done/ folder
```
