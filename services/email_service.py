import smtplib
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from config.settings import (
    EMAIL_SENDER_USER, 
    EMAIL_SENDER_PASSWORD, 
    EMAIL_SMTP_SERVER, 
    EMAIL_SMTP_PORT,
    DATA_DIR,
    BLOG_NAME
)

class EmailService:
    def __init__(self):
        self.logger = logging.getLogger("EmailService")
        self.subscribers_file = DATA_DIR / "subscribers.json"

    def get_subscribers(self):
        """Read subscribers from JSON file"""
        if not self.subscribers_file.exists():
            return []
        
        try:
            with open(self.subscribers_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error reading subscribers: {e}")
            return []

    def send_new_post_notification(self, post_title: str, post_excerpt: str, post_url: str):
        """Send email notification to all subscribers"""
        if not EMAIL_SENDER_USER or not EMAIL_SENDER_PASSWORD:
            self.logger.warning("Email credentials not set. Skipping notification.")
            return False

        subscribers = self.get_subscribers()
        if not subscribers:
            self.logger.info("No subscribers found. Skipping notification.")
            return False

        recipients = [sub['email'] for sub in subscribers if sub.get('email')]
        if not recipients:
            return False

        subject = f"New Article on {BLOG_NAME}: {post_title}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4f46e5;">New Post from {BLOG_NAME}</h2>
                    <h1 style="font-size: 24px; margin-bottom: 20px;">{post_title}</h1>
                    <p style="font-size: 16px; color: #555;">{post_excerpt}</p>
                    <div style="margin: 30px 0;">
                        <a href="{post_url}" style="background-color: #4f46e5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">Read Full Article</a>
                    </div>
                    <p style="font-size: 12px; color: #888; margin-top: 40px;">
                        You are receiving this email because you subscribed to {BLOG_NAME}.
                    </p>
                </div>
            </body>
        </html>
        """

        try:
            # Set up server
            server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
            server.starttls()
            server.login(EMAIL_SENDER_USER, EMAIL_SENDER_PASSWORD)

            # Send emails (using BCC to protect privacy)
            # For a large list, we should send individually or in batches, 
            # but for this MVP, one BCC loop is fine.
            
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{BLOG_NAME} <{EMAIL_SENDER_USER}>"
            msg["To"] = EMAIL_SENDER_USER # Send to self, everyone else BCC
            
            part1 = MIMEText(html_content, "html")
            msg.attach(part1)

            # Add BCC
            # Note: SMTP sendmail takes a list of strings for recipients
            all_recipients = [EMAIL_SENDER_USER] + recipients
            
            server.sendmail(EMAIL_SENDER_USER, all_recipients, msg.as_string())
            server.quit()

            self.logger.info(f"Notification sent to {len(recipients)} subscribers.")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
