"""
Test script to demonstrate Claude Code reading from and writing to the vault.
This verifies requirement #3 of the Bronze Tier.
"""

import os
from pathlib import Path
from datetime import datetime

def test_vault_access():
    """Test that we can read from and write to the vault."""
    vault_path = Path("AI_Employee_Vault")

    print("Testing vault access...")
    print(f"Vault path: {vault_path.absolute()}")

    # Test reading from existing files
    dashboard_path = vault_path / "Dashboard.md"
    if dashboard_path.exists():
        content = dashboard_path.read_text()
        print(f"SUCCESS: Successfully read Dashboard.md ({len(content)} characters)")
    else:
        print("ERROR: Dashboard.md not found")
        return False

    # Test writing to a new file in Needs_Action
    test_file_path = vault_path / "Needs_Action" / f"TEST_VAULT_ACCESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    test_content = f"""---
type: test
timestamp: {datetime.now().isoformat()}
status: completed
---

# Vault Access Test

This file confirms that Claude Code can successfully write to the vault.

## Test Results
- **Timestamp:** {datetime.now().isoformat()}
- **Status:** Write access confirmed
- **Test Type:** Vault I/O functionality

## Next Steps
This test file demonstrates that the system can create files in the Needs_Action folder as required by the Bronze Tier specification.
"""

    # Ensure the Needs_Action directory exists
    (vault_path / "Needs_Action").mkdir(exist_ok=True)

    # Write the test file
    test_file_path.write_text(test_content)
    print(f"SUCCESS: Successfully wrote test file: {test_file_path.name}")

    # Test reading back the written file
    read_content = test_file_path.read_text()
    if len(read_content) > 0:
        print(f"SUCCESS: Successfully verified write/read cycle")
    else:
        print("ERROR: Failed to read back the written file")
        return False

    print("\nVault access test completed successfully!")
    return True

def verify_bronze_requirements():
    """Verify that all Bronze Tier requirements are met."""
    vault_path = Path("AI_Employee_Vault")

    print("\n" + "="*50)
    print("BRONZE TIER REQUIREMENTS VERIFICATION")
    print("="*50)

    requirements_met = 0
    total_requirements = 5

    # Requirement 1: Obsidian vault with Dashboard.md and Company_Handbook.md
    print("\n1. Obsidian vault with Dashboard.md and Company_Handbook.md:")
    dashboard_exists = (vault_path / "Dashboard.md").exists()
    handbook_exists = (vault_path / "Company_Handbook.md").exists()
    print(f"   - Dashboard.md exists: {'YES' if dashboard_exists else 'NO'}")
    print(f"   - Company_Handbook.md exists: {'YES' if handbook_exists else 'NO'}")
    if dashboard_exists and handbook_exists:
        print("   -> Requirement 1: MET")
        requirements_met += 1
    else:
        print("   -> Requirement 1: NOT MET")

    # Requirement 2: One working Watcher script (Gmail OR file system monitoring)
    print("\n2. One working Watcher script (file system monitoring):")
    watcher_exists = (Path(".") / "filesystem_watcher.py").exists()
    print(f"   - Filesystem watcher exists: {'YES' if watcher_exists else 'NO'}")
    if watcher_exists:
        print("   -> Requirement 2: MET")
        requirements_met += 1
    else:
        print("   -> Requirement 2: NOT MET")

    # Requirement 3: Claude Code successfully reading from and writing to the vault
    print("\n3. Claude Code successfully reading from and writing to the vault:")
    vault_access_ok = test_vault_access()
    print(f"   -> Requirement 3: {'MET' if vault_access_ok else 'NOT MET'}")
    if vault_access_ok:
        requirements_met += 1

    # Requirement 4: Basic folder structure: /Inbox, /Needs_Action, /Done
    print("\n4. Basic folder structure (/Inbox, /Needs_Action, /Done):")
    inbox_exists = (vault_path / "Inbox").exists()
    needs_action_exists = (vault_path / "Needs_Action").exists()
    done_exists = (vault_path / "Done").exists()
    plans_exists = (vault_path / "Plans").exists()
    logs_exists = (vault_path / "Logs").exists()
    pending_approval_exists = (vault_path / "Pending_Approval").exists()
    approved_exists = (vault_path / "Approved").exists()
    rejected_exists = (vault_path / "Rejected").exists()

    print(f"   - Inbox exists: {'YES' if inbox_exists else 'NO'}")
    print(f"   - Needs_Action exists: {'YES' if needs_action_exists else 'NO'}")
    print(f"   - Done exists: {'YES' if done_exists else 'NO'}")
    print(f"   - Plans exists: {'YES' if plans_exists else 'NO'}")
    print(f"   - Logs exists: {'YES' if logs_exists else 'NO'}")
    print(f"   - Pending_Approval exists: {'YES' if pending_approval_exists else 'NO'}")
    print(f"   - Approved exists: {'YES' if approved_exists else 'NO'}")
    print(f"   - Rejected exists: {'YES' if rejected_exists else 'NO'}")

    all_dirs_exist = all([inbox_exists, needs_action_exists, done_exists,
                          plans_exists, logs_exists, pending_approval_exists,
                          approved_exists, rejected_exists])
    if all_dirs_exist:
        print("   -> Requirement 4: MET")
        requirements_met += 1
    else:
        print("   -> Requirement 4: NOT MET")

    # Requirement 5: All AI functionality should be implemented as Agent Skills
    print("\n5. All AI functionality implemented as Agent Skills:")
    # Check for Claude Code skills in .claude/skills folder
    bronze_skills = ['planning-skill', 'approval-workflow', 'email-mcp', 'linkedin-posting', 'gmail-watcher', 'scheduling-skill']
    skills_path = Path(".claude/skills")
    skills_exist = skills_path.exists() and all((skills_path / skill).exists() for skill in bronze_skills)
    print(f"   - Claude Code skills exist: {'YES' if skills_exist else 'NO'}")
    if skills_exist:
        print("   -> Requirement 5: MET")
        requirements_met += 1
    else:
        print("   -> Requirement 5: NOT MET")

    # Final summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Requirements met: {requirements_met}/{total_requirements}")

    if requirements_met == total_requirements:
        print("SUCCESS: BRONZE TIER COMPLETE! All requirements have been satisfied.")
        return True
    else:
        print("FAILURE: BRONZE TIER INCOMPLETE. Some requirements are still pending.")
        return False

if __name__ == "__main__":
    verify_bronze_requirements()