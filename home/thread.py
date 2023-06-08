import threading
from django.core.mail import get_connection

class sendMail(threading.Thread):

    def __init__(self, reciever1, reciever2) -> None:
        self.rc1 = reciever1
        self.rc2 = reciever2
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

            
        