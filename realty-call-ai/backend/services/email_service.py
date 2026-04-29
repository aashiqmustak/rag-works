"""
Email service for sending follow-ups
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models.config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class EmailService:
    """Email service for sending follow-ups"""
    
    def __init__(self):
        """Initialize email service"""
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
    
    async def send_email(self, 
                        to_email: str,
                        subject: str,
                        body: str,
                        html_body: str = None) -> bool:
        """Send email"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.smtp_user
            message["To"] = to_email
            
            # Attach text and HTML
            message.attach(MIMEText(body, "plain"))
            if html_body:
                message.attach(MIMEText(html_body, "html"))
            
            # Send email
            async with aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port) as smtp:
                await smtp.starttls()
                await smtp.login(self.smtp_user, self.smtp_password)
                await smtp.sendmail(self.smtp_user, to_email, message.as_string())
            
            logger.info(f"Email sent to {to_email}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    async def send_bulk_email(self, 
                             recipients: list,
                             subject: str,
                             body: str) -> int:
        """Send bulk emails"""
        sent_count = 0
        for email in recipients:
            if await self.send_email(email, subject, body):
                sent_count += 1
        
        return sent_count


# Global email service instance
_email_service = None


def get_email_service() -> EmailService:
    """Get or create email service"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
