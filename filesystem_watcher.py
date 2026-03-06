"""
File System Watcher for AI Employee

This script monitors a designated 'drop folder' for new files and moves them
to the AI Employee's Needs_Action folder for processing.
"""

import time
import logging
from pathlib import Path
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime


class DropFolderHandler(FileSystemEventHandler):
    """Handles file system events in the drop folder."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.vault_path / 'Logs' / f'watcher_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        # Get the source file
        source = Path(event.src_path)
        self.logger.info(f"New file detected: {source.name}")

        # Create a markdown file with metadata about the dropped file
        self.create_action_file(source)

    def on_moved(self, event):
        """Handle file move events."""
        if event.is_directory:
            return

        source = Path(event.src_path)
        self.logger.info(f"File moved: {source.name}")
        self.create_action_file(source)

    def create_action_file(self, source: Path):
        """Create an action file in Needs_Action folder."""
        # Create metadata file with .md extension
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_name = f"FILE_DROP_{timestamp}_{source.name}.md"
        dest_path = self.needs_action / dest_name

        # Create the content for the action file
        content = f"""---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size if source.exists() else 0}
timestamp: {datetime.now().isoformat()}
status: pending
priority: medium
---

# File Drop Notification

A new file has been placed in the monitored folder and requires attention.

## File Details
- **Original Name:** {source.name}
- **Size:** {source.stat().st_size if source.exists() else 0} bytes
- **Location:** {source.parent}
- **Dropped at:** {datetime.now().isoformat()}

## Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process file as needed
- [ ] Update status when complete

## File Path
```
{source}
```

## Next Steps
Please review this file and take appropriate action based on its contents and importance.
"""

        # Write the action file
        dest_path.write_text(content)
        self.logger.info(f"Action file created: {dest_path.name}")

        # Also log the event
        action_log = self.vault_path / 'Logs' / f'actions_{datetime.now().strftime("%Y%m%d")}.log'
        with action_log.open('a') as log_file:
            log_file.write(f"{datetime.now().isoformat()} - File drop detected: {source.name}\n")


def main():
    """Main function to run the file system watcher."""
    # Set up vault path (default to current directory)
    vault_path = Path("AI_Employee_Vault")

    # Ensure the vault and required directories exist
    needs_action_dir = vault_path / "Needs_Action"
    logs_dir = vault_path / "Logs"

    needs_action_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Create the event handler
    event_handler = DropFolderHandler(str(vault_path))

    # Monitor the Inbox folder for new files
    watch_path = vault_path / "Inbox"
    watch_path.mkdir(exist_ok=True)  # Create if it doesn't exist

    # Create observer
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)

    print(f"Starting file system watcher for: {watch_path}")
    print(f"Vault location: {vault_path}")
    print("Press Ctrl+C to stop...")

    # Start the observer
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping file system watcher...")

    observer.join()
    print("File system watcher stopped.")


if __name__ == "__main__":
    main()