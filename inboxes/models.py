from django.db import models


class Inbox(models.Model):
    owner = models.CharField(default='Owner',max_length=100)
    PROFILE_TYPE = (
        (0, 'Admin'),
        (1, 'Personal'),
        (2, 'Store'), 
        (3, 'Workshop')
    )
    type = models.IntegerField(choices=PROFILE_TYPE, default=1)
    
    def __str__(self):
        return f'{self.owner}'
    
    def count_unseen_notifications(self):
        return self.message_notification.filter(is_seen=False).count()
    

class Message(models.Model):
    sender = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.message
    

class Contact(models.Model):
    name = models.CharField(max_length=100, default="contact")
    contactInbx = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='contactInbx')
    mainInbx = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='mainInbx')

    def unread_messages(self):
        return Message.objects.filter(sender=self.contactInbx, receiver=self.mainInbx, is_seen=False).count()

    def __str__(self) -> str:
        return f'\'{self.mainInbx.owner}\'  with  \'{self.name}\''
    
    def save(self, *args, **kwargs):
        self.name = self.contactInbx.owner
        super(Contact, self).save(*args, **kwargs)

class MessageNotification(models.Model):
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    receiver_inbx = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='message_notification')
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.receiver_inbx.id)

    @classmethod
    def count_unseen_notifications(cls):
        count = cls.objects.filter(is_seen=False).count()
        print("count", count)
        return count