import threading
from django.core.mail import get_connection, EmailMultiAlternatives

class sendMail(threading.Thread):

    def __init__(self,form) -> None:
        mail_to_user = EmailMultiAlternatives(
                "Mail From Lazy coder",
                f"Thanks for Visiting our Blog and contacting us, Our team will approach you soon on your given email address or phone number.<br>Your responses are :-{form}",
                "bablu123890kumar@gmail.com",
                [f"{form.cleaned_data.get('email')}"],
            )
        
        mail_to_lazycoder = EmailMultiAlternatives(
                f"{form.cleaned_data.get('name')} has Contacted us.",
                f"Some one wants to contact us<br>responses are<br>{form}",
                "bablu123890kumar@gmail.com",
                ["kunalverma.learn@gmail.com"],
            )
        
        mail_to_user.content_subtype = 'html'
        mail_to_lazycoder.content_subtype = 'html'
        
        self.rc1 = mail_to_user
        self.rc2 = mail_to_lazycoder
        threading.Thread.__init__(self)

    def run(self):
        try:
            print("____________________thread execution has started____________________")
            connection = get_connection()
            connection.open()
            self.rc1.send()
            self.rc2.send()
            connection.close()
            print("_______________________thread execution has Ended______________________")
        except Exception as e:
            print(e)

            
        