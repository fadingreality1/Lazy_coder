import threading
from django.core.mail import get_connection, EmailMultiAlternatives
from Lazy_coder import settings

# ? Email multi alternative is used to send html code to reciever
class sendMail(threading.Thread):
    def __init__(self,form) -> None:
        mail_to_user = EmailMultiAlternatives(
                "Welcome to Lazy Coder!",
                f"""
                Dear {form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')},<br/>
                <p>
                Welcome to Lazy Coder! We're thrilled to have you as a new member of our coding community. Thank you for signing up on our website.
                </p>
                <p>
                At Lazy Coder, we're passionate about coding and productivity, and we're here to support you on your coding journey. As a member, you'll have access to a wealth of resources, tutorials, and discussions that will help you enhance your coding skills and stay motivated.
                </p>
                <p>
                We encourage you to explore our blog, engage with fellow coders, and make the most of the knowledge shared within our community. Whether you're a beginner or an experienced developer, there's something for everyone at Lazy Coder.</p>
                <p>
                If you have any questions, need assistance, or simply want to share your coding achievements, don't hesitate to reach out to us. Our team is here to help and support you.
                </p>
                <p>
                Once again, welcome to Lazy Coder! We're excited to have you on board, and we can't wait to see how your coding journey unfolds.
                </p>
                <p>
                Happy coding!<br/>
                </p>
                <p>
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
                f"{form.cleaned_data.get('first_name')} has Registered with us.",
                f"Some one wants to contact us.<br>Responses are:-<br>Name: {form.cleaned_data.get('first_name')}<br>Email: {form.cleaned_data.get('email')}<br>",
                f"{settings.EMAIL_HOST_USER}",
                ["kunalverma.learn@gmail.com"],
            )
        
        mail_to_user.content_subtype = 'html'
        mail_to_lazycoder.content_subtype = 'html'
        
        
        # ? rc1, rc2, are recievers
        
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

            
        