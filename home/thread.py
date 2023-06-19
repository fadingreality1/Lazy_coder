import threading
from django.core.mail import get_connection, EmailMultiAlternatives
from Lazy_coder import settings


class sendMail(threading.Thread):

    def __init__(self,form) -> None:
        mail_to_user = EmailMultiAlternatives(
                "Thank You for Contacting Lazy Coder!",
                f"""
                Dear {form.cleaned_data.get('name')},<br/>
                <p>
                Thank you for reaching out to Lazy Coder! We appreciate your interest and the time you took to contact us. Your message has been received, and we will get back to you as soon as possible.
                </p>
                <p>
                At Lazy Coder, we strive to provide prompt and personalized assistance to our readers. Our team is reviewing your inquiry, and we will address your questions, feedback, or any other matter you raised in your message. We aim to deliver a comprehensive response that meets your expectations and assists you in the best possible way.
                </p>
                <p>
                While we work on crafting a thoughtful reply, we kindly ask for your patience. Depending on the volume of inquiries we receive, it may take us a couple of business days to respond. However, please rest assured that we value your contact and will do our utmost to provide you with the information or assistance you seek.</p><p>
                Best regards,<br/>
                </p>
                <p>
                Kunal verma<br/>
                Lazy Coder Team<br/>
                </p>
                """,
                f"{settings.EMAIL_HOST_USER}",
                [f"{form.cleaned_data.get('email')}"],
            )
        
        mail_to_lazycoder = EmailMultiAlternatives(
                f"{form.cleaned_data.get('name')} has Contacted us.",
                f"Some one wants to contact us.<br>Responses are:-<br>Name: {form.cleaned_data.get('name')}<br>Email: {form.cleaned_data.get('email')}<br>Phone: {form.cleaned_data.get('phone')}<br>Website: {form.cleaned_data.get('website')}<br>Message: {form.cleaned_data.get('message')}",
                f"{settings.EMAIL_HOST_USER}",
                ["kunalverma.learn@gmail.com"],
            )
        
        mail_to_user.content_subtype = 'html'
        mail_to_lazycoder.content_subtype = 'html'
        
        self.rc1 = mail_to_user
        self.rc2 = mail_to_lazycoder
        threading.Thread.__init__(self)

    def run(self):
        try:
            connection = get_connection()
            connection.open()
            self.rc1.send()
            self.rc2.send()
            connection.close()
        except Exception as e:
            print(e)

            
        