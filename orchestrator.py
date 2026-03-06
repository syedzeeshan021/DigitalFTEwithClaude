"""
AI Employee Orchestrator

This script manages the overall AI Employee system, coordinating between
watchers, Claude Code processing, and the Obsidian vault.
"""

import time
import logging
from pathlib import Path
from datetime import datetime
import subprocess
import os
import json


class AI_Employee_Orchestrator:
    """Main orchestrator for the AI Employee system."""

    def __init__(self, vault_path="AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.setup_logging()
        self.setup_directories()

    def setup_logging(self):
        """Setup logging configuration."""
        log_dir = self.vault_path / 'Logs'
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f'orchestrator_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def setup_directories(self):
        """Ensure all required directories exist."""
        directories = [
            'Inbox',
            'Needs_Action',
            'Done',
            'Plans',
            'Logs',
            'Pending_Approval',
            'Approved',
            'Rejected'
        ]

        for directory in directories:
            (self.vault_path / directory).mkdir(exist_ok=True)

        self.logger.info("All required directories verified/created")

    def update_dashboard(self, status_update=None):
        """Update the Dashboard.md file with current status."""
        dashboard_path = self.vault_path / "Dashboard.md"

        if dashboard_path.exists():
            content = dashboard_path.read_text()
        else:
            content = "# AI Employee Dashboard\n\nDefault dashboard content."

        # Count items in various folders
        needs_action_count = len(list((self.vault_path / "Needs_Action").glob("*.md")))
        inbox_count = len(list((self.vault_path / "Inbox").glob("*")))
        pending_approval_count = len(list((self.vault_path / "Pending_Approval").glob("*.md")))
        done_today = len(list((self.vault_path / "Done").glob(f"*_{datetime.now().strftime('%Y%m%d')}*.md")))

        # Update the status sections
        updated_content = content.replace(
            "## System Status\n- **AI Employee:** Idle",
            f"## System Status\n- **AI Employee:** Active\n- **Last Update:** {datetime.now().isoformat()}"
        )

        # Update stats
        stats_start = content.find("## Quick Stats")
        if stats_start != -1:
            stats_end = content.find("\n\n", stats_start)
            old_stats = content[stats_start:stats_end]

            new_stats = f"""## Quick Stats
- **Inbox:** {inbox_count} items
- **Needs Action:** {needs_action_count} items
- **Pending Approval:** {pending_approval_count} items
- **Completed Today:** {done_today} items"""

            content = content.replace(old_stats, new_stats)

        # Add recent activity if provided
        if status_update:
            activity_start = content.find("## Recent Activity")
            if activity_start != -1:
                # Find the end of the recent activity section
                next_header = content.find("\n## ", activity_start + 1)
                if next_header == -1:
                    next_header = len(content)

                old_activity = content[activity_start:next_header]
                new_activity = f"## Recent Activity\n- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {status_update}"

                content = content.replace(old_activity, new_activity)

        # Write updated dashboard
        dashboard_path.write_text(content)
        self.logger.info("Dashboard updated")

    def process_needs_action(self):
        """Process files in the Needs_Action folder."""
        needs_action_dir = self.vault_path / "Needs_Action"
        files = list(needs_action_dir.glob("*.md"))

        if not files:
            self.logger.info("No files in Needs_Action folder")
            return

        self.logger.info(f"Processing {len(files)} files in Needs_Action folder")

        for file_path in files:
            self.logger.info(f"Processing file: {file_path.name}")

            # Log the activity
            self.update_dashboard(f"Processing {file_path.name}")

            # For Bronze tier, we'll just move the file to Done
            # In a more advanced implementation, this would trigger Claude Code
            done_path = self.vault_path / "Done" / file_path.name
            file_path.rename(done_path)

            self.logger.info(f"Moved {file_path.name} to Done folder")

    def process_pending_approval(self):
        """Process files in the Pending_Approval folder."""
        pending_dir = self.vault_path / "Pending_Approval"
        files = list(pending_dir.glob("*.md"))

        if not files:
            self.logger.info("No files in Pending_Approval folder")
            return

        self.logger.info(f"Checking {len(files)} approval requests")

        # For Bronze tier, we'll just log that there are pending approvals
        # In Silver/Gold tier, this would have logic to handle approvals
        for file_path in files:
            self.logger.info(f"Approval required for: {file_path.name}")

    def run_claude_processing(self):
        """Placeholder for Claude Code integration."""
        # This would be where we'd integrate with Claude Code
        # For Bronze tier, we'll just log the attempt
        self.logger.info("Claude Code integration would process Needs_Action files here")

    def run_cycle(self):
        """Run one complete cycle of the orchestrator."""
        self.logger.info("Starting orchestrator cycle")

        # Update dashboard with current status
        self.update_dashboard("Starting new cycle")

        # Process any pending items
        self.process_needs_action()
        self.process_pending_approval()

        # Update dashboard again
        self.update_dashboard("Cycle completed")

        self.logger.info("Orchestrator cycle completed")

    def run_continuous(self, interval=60):
        """Run the orchestrator continuously."""
        self.logger.info(f"Starting continuous orchestrator (interval: {interval}s)")
        self.update_dashboard("System started - Orchestrator active")

        try:
            while True:
                self.run_cycle()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info("Orchestrator stopped by user")
            self.update_dashboard("System stopped by user")


def main():
    """Main function to run the orchestrator."""
    print("AI Employee Orchestrator")
    print("=" * 30)

    # Create orchestrator instance
    orchestrator = AI_Employee_Orchestrator()

    # Run in continuous mode (this would typically be run as a service)
    print("Starting orchestrator... (Press Ctrl+C to stop)")
    orchestrator.run_continuous(interval=30)  # Check every 30 seconds


if __name__ == "__main__":
    main()