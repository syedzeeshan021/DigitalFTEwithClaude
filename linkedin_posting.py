"""
LinkedIn Posting for AI Employee - Silver Tier

This script creates LinkedIn post drafts and saves them to the AI Employee's
Needs_Action folder for approval before publishing.

Silver Tier Requirement: Automatically Post on LinkedIn about business to generate sales
"""

import logging
from pathlib import Path
from datetime import datetime


class LinkedInPostingSkill:
    """
    Skill for creating and managing LinkedIn posts for business growth.
    Creates draft posts that require human approval before publishing.
    """

    def __init__(self, vault_path="AI_Employee_Vault"):
        self.vault_path = Path(vault_path).resolve()
        self.hashtag_groups = {
            'business_growth': ['#BusinessGrowth', '#Entrepreneurship', '#Startup', '#SmallBusiness', '#GrowthMindset'],
            'technology': ['#AI', '#Automation', '#Technology', '#Innovation', '#DigitalTransformation'],
            'productivity': ['#Productivity', '#TimeManagement', '#Efficiency', '#WorkLifeBalance', '#Success'],
            'thought_leadership': ['#ThoughtLeadership', '#Leadership', '#BusinessStrategy', '#Innovation', '#Expertise'],
            'client_success': ['#ClientSuccess', '#Testimonial', '#CustomerExperience', '#BusinessGrowth', '#Results'],
        }

    def create_linkedin_post(
        self,
        content: str,
        post_type: str = "business_update",
        hashtags: list = None,
        schedule_time: str = None,
        call_to_action: str = None
    ) -> str:
        """
        Create a LinkedIn post draft file.

        Args:
            content: The main post content
            post_type: Type of post (business_update, announcement, tip, article, celebration, question)
            hashtags: List of hashtags (optional, will use defaults based on post_type)
            schedule_time: ISO format datetime for scheduled posting
            call_to_action: CTA text to append

        Returns:
            Path to created post file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"LINKEDIN_POST_{timestamp}_{post_type}.md"
        file_path = self.vault_path / "Needs_Action" / filename

        # Select default hashtags based on post type if not provided
        if hashtags is None:
            hashtags = self._get_default_hashtags(post_type)

        # Format hashtags
        hashtag_str = " ".join(hashtags)

        # Add CTA if provided
        if call_to_action:
            content = f"{content}\n\n{call_to_action}"

        post_content = self._format_post_content(content, post_type, hashtag_str)

        post_markdown = f"""---
type: linkedin_post
post_type: {post_type}
created: {datetime.now().isoformat()}
status: draft
scheduled_time: {schedule_time if schedule_time else 'Not scheduled'}
---

# LinkedIn Post Draft

## Content

{post_content}

## Post Type
{post_type}

## Created
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Hashtags
{hashtag_str}

## Suggested Actions
- [ ] Review content for accuracy
- [ ] Check for typos and formatting
- [ ] Add relevant images or media (optional)
- [ ] Move to Approved to publish
- [ ] Move to Rejected to discard

## Engagement Goals
- Target impressions: 1000+
- Target engagements: 50+
- Target leads: 5+

## Notes
Add any additional context or follow-up actions here.
"""

        file_path.write_text(post_markdown, encoding='utf-8')
        return str(file_path)

    def _get_default_hashtags(self, post_type: str) -> list:
        """Get default hashtags based on post type."""
        hashtag_mapping = {
            'business_update': self.hashtag_groups['business_growth'],
            'announcement': self.hashtag_groups['technology'],
            'tip': self.hashtag_groups['productivity'],
            'article': self.hashtag_groups['thought_leadership'],
            'celebration': self.hashtag_groups['client_success'],
            'question': self.hashtag_groups['thought_leadership'],
        }
        return hashtag_mapping.get(post_type, self.hashtag_groups['business_growth'])

    def _format_post_content(self, content: str, post_type: str, hashtags: str) -> str:
        """Format post content based on type."""
        if post_type == 'tip':
            return f"""{content}

{hashtags}"""
        elif post_type == 'question':
            return f"""{content}

Drop your thoughts in the comments!

{hashtags}"""
        else:
            return f"""{content}

{hashtags}"""

    def create_business_update_post(
        self,
        achievement: str,
        call_to_action: str = "Contact us today to learn how we can help your business grow."
    ) -> str:
        """
        Create a business update/milestone post.

        Args:
            achievement: The business achievement to announce
            call_to_action: CTA text

        Returns:
            Path to created post file
        """
        content = f"""Excited to share some great news!

{achievement}

This milestone represents our commitment to delivering exceptional value to our clients. We're grateful for the trust you've placed in us."""

        return self.create_linkedin_post(
            content=content,
            post_type="business_update",
            hashtags=self.hashtag_groups['business_growth'],
            call_to_action=call_to_action
        )

    def create_tip_post(
        self,
        topic: str,
        tips: list,
        call_to_action: str = "Which tip resonates most with you? Share your thoughts in the comments!"
    ) -> str:
        """
        Create a thought leadership tip post.

        Args:
            topic: The topic of the tips
            tips: List of tips (3-5 recommended)
            call_to_action: CTA text

        Returns:
            Path to created post file
        """
        tips_formatted = "\n".join([f"{i+1}. {tip}" for i, tip in enumerate(tips)])
        content = f"""Here are {len(tips)} quick tips for {topic}:

{tips_formatted}"""

        return self.create_linkedin_post(
            content=content,
            post_type="tip",
            hashtags=self.hashtag_groups['productivity'],
            call_to_action=call_to_action
        )

    def create_question_post(
        self,
        question: str,
        context: str = ""
    ) -> str:
        """
        Create an engagement-focused question post.

        Args:
            question: The question to ask
            context: Optional context for the question

        Returns:
            Path to created post file
        """
        content = f"""Quick question for my network:

{question}"""

        if context:
            content += f"\n\n{context}"

        return self.create_linkedin_post(
            content=content,
            post_type="question",
            hashtags=self.hashtag_groups['thought_leadership']
        )

    def create_announcement_post(
        self,
        product_name: str,
        description: str,
        features: list = None,
        link: str = None
    ) -> str:
        """
        Create a product/service launch announcement.

        Args:
            product_name: Name of the product/service
            description: Description of what it does
            features: List of key features
            link: Link to learn more

        Returns:
            Path to created post file
        """
        content = f"""Big news! We're thrilled to announce {product_name}!

{description}"""

        if features:
            content += "\n\nKey features:\n"
            for feature in features:
                content += f"  {feature}\n"

        if link:
            content += f"\nReady to get started? {link}"

        return self.create_linkedin_post(
            content=content,
            post_type="announcement",
            hashtags=self.hashtag_groups['technology']
        )

    def list_drafts(self) -> list:
        """List all LinkedIn post drafts in Needs_Action folder."""
        needs_action = self.vault_path / "Needs_Action"
        if not needs_action.exists():
            return []

        drafts = []
        for f in needs_action.glob("LINKEDIN_POST_*.md"):
            drafts.append(str(f))
        return drafts

    def get_post_stats(self, post_path: str) -> dict:
        """Get statistics about a post draft."""
        path = Path(post_path)
        if not path.exists():
            return None

        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Count content lines (excluding frontmatter)
        in_content = False
        content_length = 0
        hashtag_count = 0

        for line in lines:
            if line.startswith('## Content'):
                in_content = True
                continue
            if in_content and line.startswith('##'):
                break
            if in_content:
                content_length += len(line)
                if line.startswith('#'):
                    hashtag_count += 1

        return {
            'character_count': content_length,
            'hashtag_count': hashtag_count,
            'is_valid': 50 <= content_length <= 3000  # LinkedIn limits
        }


def main():
    """Main function to demonstrate LinkedIn posting skill."""
    print("=" * 60)
    print("AI Employee - LinkedIn Posting Skill")
    print("=" * 60)

    vault_path = Path("AI_Employee_Vault")
    vault_path.mkdir(exist_ok=True)
    (vault_path / "Needs_Action").mkdir(exist_ok=True)

    linkedin = LinkedInPostingSkill(str(vault_path))

    print("\nLinkedIn Posting Skill - Demo Mode")
    print("-" * 40)
    print("This skill creates LinkedIn post drafts for approval.")
    print("Posts are saved to Needs_Action/ folder.")
    print("\nTo publish: Move post from Needs_Action/ to Approved/")
    print("\nAvailable post types:")
    print("  1. Business Update (milestone announcements)")
    print("  2. Tip Post (thought leadership)")
    print("  3. Question Post (engagement)")
    print("  4. Announcement (product launches)")
    print("\nExample usage:")
    print('  python -c "from linkedin_posting import LinkedInPostingSkill;')
    print('  l = LinkedInPostingSkill();')
    print('  print(l.create_business_update_post(\'We reached 1000+ clients!\'))"')

    # Create a demo post
    print("\nCreating demo business update post...")
    demo_post = linkedin.create_business_update_post(
        achievement="We're excited to announce the launch of our AI Employee system! This autonomous digital assistant helps businesses automate their daily operations and increase productivity.",
        call_to_action="Contact us today to learn how AI automation can transform your business."
    )
    print(f"Created: {demo_post}")

    # Show post stats
    stats = linkedin.get_post_stats(demo_post)
    if stats:
        print(f"\nPost Statistics:")
        print(f"  Character count: {stats['character_count']}")
        print(f"  Hashtag count: {stats['hashtag_count']}")
        print(f"  Valid length: {'YES' if stats['is_valid'] else 'NO'}")

    print("\nLinkedIn Posting Skill ready!")


if __name__ == "__main__":
    main()
