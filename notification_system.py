from abc import ABC,abstractmethod
import uuid
from queue import Queue
from datetime import datetime
import time
import threading
deliveryLogs=[]
class NotificationSender(ABC):
    @abstractmethod
    def send(self,recipient,message):
        pass
class EmailSender(NotificationSender):
    def send(self,recipient,message):
        print(f"Sending message to {recipient} to {message}")
        return True
class SMSSender(NotificationSender):
    def send(self,recipient,message):
        print(f"Sending message to {recipient} to {message}")
        return True
class PushSender(NotificationSender):
    def send(self,recipient,message):
        print(f"Sending message to {recipient} to {message}")
        return True
class Notification:
    def __init__(self,message,recipient,sender,channel,retryCount=0):
        self.id = str(uuid.uuid4())
        self.message = message
        self.recipient = recipient
        self.sender = sender
        self.channel = channel
        self.retryCount=retryCount
class NotificationService:
    def __init__(self):
        self.queues = {
            "SMS":Queue(),
            "Push":Queue(),
            "Email":Queue()
        }
        self.sender = {
            "SMS":SMSSender(),
            "Push":PushSender(),
            "Email":EmailSender()
        }
    def start(self):
        for channel in self.queues:
            t=threading.Thread(target=self.worker,args=(channel,),daemon=True)
            t.start()
    def send_notification(self,recipient,message,channel):
        sender = self.sender.get(channel)
        if(sender):
            notif = Notification(message,recipient,sender,channel)
            self.queues[channel].put(notif)
    def worker(self,channel):
        queue = self.queues[channel]
        while True:
            notif = queue.get()
            try:
                success = notif.sender.send(notif.recipient,notif.message)
                deliveryLogs.append((notif.recipient,notif.sender.__class__.__name__,notif.message,notif.channel,'SUCCESS' if success else 'FAILURE',notif.retryCount,datetime.now()))
                if(not success and notif.retryCount<3):
                    notif.retryCount+=1
                    time.sleep(2**notif.retryCount)
                    queue.put(notif)
            except Exception as e:
                deliveryLogs.append((notif.recipient,notif.sender.__class__.__name__,notif.message,notif.channel,'ERROR',notif.retryCount,datetime.now()))
            finally:
                queue.task_done()
service = NotificationService()
service.start()
service.send_notification('aishu@example.com', 'Hi Loosu', 'Email')
service.send_notification('aishu', 'Hi Loosu', 'SMS')
service.send_notification('aishu', 'Hi Loosu', 'Push')
time.sleep(5)
for log in deliveryLogs:
    print(log)
                
