# AI Employee - Personal Digital FTE (Full-Time Equivalent)

This project implements a complete "Digital FTE" (Full-Time Equivalent) AI employee system that autonomously manages personal and business affairs 24/7 using Claude Code as the reasoning engine and Obsidian as the management dashboard.

## 🚀 Project Overview

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

This implementation follows the "Personal AI Employee Hackathon 0: Building Autonomous FTEs in 2026" architectural blueprint and achieves **Silver Tier** requirements with advanced automation capabilities.

## ✨ Key Features

### 🧠 The Brain
- **Claude Code** acts as the reasoning engine with continuous iteration capabilities
- **Ralph Wiggum Stop hook pattern** keeps the agent working until tasks are complete

### 💾 The Memory/GUI
- **Obsidian vault** (local Markdown) as the dashboard and knowledge base
- Keeps all data local and accessible with full privacy control

### 👁️ The Senses (Watchers)
- **Gmail Watcher** - Monitors Gmail with OAuth2 authentication
- **WhatsApp Watcher** - Monitors WhatsApp Web with Playwright automation
- **Filesystem Watcher** - Monitors file system for new items
- **LinkedIn Watcher** - Monitors and posts to LinkedIn with Playwright automation

### 🤖 The Hands (MCP)
- **Model Context Protocol (MCP) servers** handle external actions
- **Email MCP** for sending emails with approval workflow
- **Browser automation** for various web interactions

## 🏆 Achievement Levels

### ✅ Bronze Tier: Foundation
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (File System Monitoring)
- ✅ Claude Code successfully reading from and writing to the vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ All AI functionality implemented as Agent Skills

### ✅ Silver Tier: Functional Assistant
- ✅ All Bronze requirements
- ✅ **Four** Watcher scripts (Gmail, WhatsApp, LinkedIn, Filesystem)
- ✅ Automatically Post on LinkedIn about business to generate sales
- ✅ Claude reasoning loop that creates Plan.md files
- ✅ One working MCP server for external action (Email MCP)
- ✅ Human-in-the-loop approval workflow for sensitive actions
- ✅ Basic scheduling via cron/Task Scheduler/PM2
- ✅ All AI functionality as Agent Skills

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI EMPLOYEE ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EXTERNAL SOURCES                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐ │
│  │    Gmail    │ │  WhatsApp   │ │   Files     │ │ LinkedIn │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘ │
│           │              │               │              │       │
│           ▼              ▼               ▼              ▼       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                   PERCEPTION LAYER                        │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐   │ │
│  │  │ Gmail        │ │ WhatsApp     │ │ Filesystem       │   │ │
│  │  │ Watcher      │ │ Watcher      │ │ Watcher          │   │ │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘   │ │
│  └───────────────────────────────────────────────────────────┘ │
│                        │                                         │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                   OBSIDIAN VAULT (Local)                    │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │ /Needs_Action/  │ /Plans/  │ /Done/  │ /Logs/        │ │ │
│  │  ├────────────────────────────────────────────────────────┤ │ │
│  │  │ Dashboard.md    │ Company_Handbook.md │ Business_Goals│ │ │
│  │  ├────────────────────────────────────────────────────────┤ │ │
│  │  │ /Pending_Approval/  │  /Approved/  │  /Rejected/     │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                        │                                         │
│                        ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    REASONING LAYER                          │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │                    CLAUDE CODE                          │ │ │
│  │  │   Read → Think → Plan → Write → Request Approval       │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                        │                                         │
│              ┌─────────┴──────────┐                              │
│              ▼                    ▼                              │
│  ┌─────────────────────────┐ ┌─────────────────────────────────┐ │
│  │   HUMAN-IN-THE-LOOP     │ │         ACTION LAYER            │ │
│  │  ┌──────────────────┐   │ │  ┌─────────────────────────┐    │ │
│  │  │ Review Approval  │───┼───▶│    MCP SERVERS          │    │ │
│  │  │ Files            │   │ │  │  ┌────────┐ ┌──────────┐ │    │ │
│  │  │ Move to /Approved│   │ │  │  │Email   │ │ Browser  │ │    │ │
│  │  └──────────────────┘   │ │  │  │ MCP    │ │ MCP      │ │    │ │
│  └─────────────────────────┘ │ │  │  └────────┘ └──────────┘ │    │ │
│                              │ │  └─────────────────────────┘    │ │
│                              │ └─────────────────────────────────┘ │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                 ORCHESTRATION LAYER                         │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │              Orchestrator.py (Master Process)           │ │ │
│  │  │   Scheduling │ Folder Watching │ Process Management    │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  │  ┌─────────────────────────────────────────────────────────┐ │ │
│  │  │              Watchdog.py (Health Monitor)               │ │ │
│  │  │   Restart Failed Processes │ Alert on Errors            │ │ │
│  │  └─────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technical Stack

| Component | Requirement | Purpose |
|:----------|:------------|:--------|
| [Claude Code](https://claude.com/product/claude-code) | Active subscription | Primary reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ (free) | Knowledge base & dashboard |
| [Python](https://www.python.org/downloads/) | 3.13 or higher | Sentinel scripts & orchestration |
| [Node.js](http://Node.js) | v24+ LTS | MCP servers & automation |
| [Github Desktop](https://desktop.github.com/download/) | Latest stable | Version control for your vault |

## 📦 Project Structure

```
F:\DigitalFTEwithClaude\
├── .claude/                    # Claude Code configuration
│   ├── skills/                 # Agent Skills as .md files
│   │   ├── approval-workflow/
│   │   ├── email-mcp/
│   │   ├── gmail-watcher/
│   │   ├── linkedin-posting/
│   │   ├── linkedin-watcher/
│   │   ├── planning-skill/
│   │   ├── scheduling-skill/
│   │   └── whatsapp-watcher/
│   └── settings.local.json
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Needs_Action/           # Items requiring processing
│   ├── Approved/               # Approved items
│   ├── Done/                   # Completed items
│   ├── Logs/                   # System logs
│   ├── .whatsapp_session/      # WhatsApp Web session
│   ├── .linkedin_session/      # LinkedIn session
│   ├── token.pickle            # Gmail OAuth2 token
│   ├── Dashboard.md
│   └── Company_Handbook.md
├── ecosystem.config.js         # PM2 process configuration
├── requirements.txt            # Python dependencies
├── orchestrator.py             # Main orchestrator
├── filesystem_watcher.py       # File system monitoring
├── gmail_watcher.py            # Gmail monitoring
├── whatsapp_watcher.py         # WhatsApp monitoring
├── linkedin_watcher.py         # LinkedIn automation
├── linkedin_posting.py         # LinkedIn post creation
├── demonstration.py            # System demo
├── vault_test.py               # Verification script
├── credentials.json            # Gmail API credentials
├── README.md                   # Bronze Tier documentation
├── SILVER_TIER_README.md       # Silver Tier documentation
└── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md
```

## 🚀 Getting Started

### Prerequisites
1. Install all required software listed above
2. Create a new Obsidian vault named "AI_Employee_Vault"
3. Verify Claude Code works by running: `claude --version`
4. Set up a UV Python project

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/syedzeeshan021/DigitalFTEwithClaude.git
   cd DigitalFTEwithClaude
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install PM2 for process management:**
   ```bash
   npm install -g pm2
   ```

4. **Setup Gmail API (optional but recommended):**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Gmail API
   - Create OAuth2 credentials
   - Download credentials.json to project root
   - Run the authentication flow

5. **Start all services:**
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   ```

6. **Setup authentication for services:**
   - **WhatsApp:** Run `python whatsapp_watcher.py` and scan QR code with phone
   - **LinkedIn:** Run `python linkedin_watcher.py` and log in to LinkedIn

### Running the System

The system runs as 5 PM2 processes:

| Process Name | Purpose |
|--------------|---------|
| ai-employee-orchestrator | Main orchestration and management |
| ai-employee-filesystem-watcher | Monitors file system |
| ai-employee-gmail-watcher | Monitors Gmail (if authenticated) |
| ai-employee-whatsapp-watcher | Monitors WhatsApp (if authenticated) |
| ai-employee-linkedin-watcher | Monitors/posts to LinkedIn (if authenticated) |

### Verification

Run the verification script to confirm all components are working:
```bash
python vault_test.py
```

## 🔐 Security & Privacy

### Credential Management
- Never store credentials in plain text or in your Obsidian vault
- Use environment variables for API keys
- Store credentials.json separately and add to .gitignore
- Rotate credentials monthly and after any suspected breach

### Human-in-the-Loop Safeguards
| Action Category | Auto-Approve Threshold | Always Require Approval |
|:----------------|:----------------------:|:------------------------|
| Email replies | To known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

### Audit Logging
Every action the AI takes is logged for review in the `/Logs/` folder with timestamp, action type, parameters, and approval status.

## 🎯 Use Cases

### Business Automation
- **Email triage** - Monitor and categorize incoming emails
- **Lead capture** - Identify potential customers from WhatsApp/LinkedIn
- **Social media** - Auto-post business updates and thought leadership
- **Task management** - Create and track business projects

### Personal Assistance
- **Calendar management** - Schedule meetings based on availability
- **Financial tracking** - Monitor bank transactions and flag anomalies
- **Communication** - Handle routine messages and inquiries
- **Scheduling** - Coordinate appointments and reminders

## 📊 Performance Benefits

| Feature | Human FTE | Digital FTE (Custom Agent) |
|:--------|:---------:|:--------------------------:|
| Availability | 40 hours / week | 168 hours / week (24/7) |
| Monthly Cost | $4,000 – $8,000+ | $500 – $2,000 |
| Ramp-up Time | 3 – 6 Months | Instant (via SKILL.md) |
| Consistency | Variable (85–95% accuracy) | Predictable (99%+ consistency) |
| Scaling | Linear (Hire 10 for 10x work) | Exponential (Instant duplication) |
| Cost per Task | ~$3.00 – $6.00 | ~$0.25 – $0.50 |

## 🔄 Workflow Example

### Complete Business Process
1. **Trigger:** Client sends inquiry via WhatsApp mentioning "pricing"
2. **Detection:** WhatsApp Watcher identifies keyword and creates action file
3. **Reasoning:** Claude creates a Plan.md with steps to respond
4. **Approval:** Payment/email over threshold requires human approval
5. **Action:** Email MCP sends customized response after approval
6. **Tracking:** Dashboard.md updates with new lead status
7. **Follow-up:** LinkedIn Watcher posts related business update

## 🤝 Contributing

This project is designed to be extensible. To add new capabilities:

1. **Create a new Agent Skill** in `.claude/skills/`
2. **Implement the functionality** in a Python file
3. **Update the orchestrator** to call the new skill
4. **Test thoroughly** before deployment

## 📚 Additional Resources

- **Claude Code Chapter:** [AI Tool Landscape](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- **Obsidian Integration:** [Claude Code and Obsidian for Personal Automation](https://www.youtube.com/watch?v=sCIS05Qt79Y)
- **Agent Skills:** [Claude Agent Skills - Automate Your Workflow Fast](https://www.youtube.com/watch?v=nbqqnl3JdR0)

## 📄 License

This project follows the architecture and guidelines from the "Personal AI Employee Hackathon 0: Building Autonomous FTEs in 2026" document.

## 🎯 Roadmap: Gold Tier

Future enhancements include:
- Facebook/Instagram integration
- Twitter (X) integration
- Odoo accounting system integration
- Multi-cloud deployment (Local + Cloud agents)
- Advanced audit logging
- Error recovery systems
- Ralph Wiggum persistence loops

---

**Note:** This system is designed for local-first operation with full privacy control. All sensitive data remains on your local machine.