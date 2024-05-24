from django.shortcuts import render, redirect

from .models import Inbox, Message,Contact, MessageNotification


def my_inbox(request, type):
    if type == 0:
        my_inbox = request.user.meccanicoadmin.inbox
    if type == 1:
        my_inbox = Inbox.objects.get(owner=request.user.username)
    elif type == 2:
        my_inbox = Inbox.objects.get(owner=request.user.storeprofile.name +' Store')
    elif type == 3:
        my_inbox = Inbox.objects.get(owner=request.user.workshopprofile.name +' Workshop')
    contacts = my_inbox.mainInbx.all()
    context={
        'contacts': contacts,
        'my_inbox': my_inbox,
        }
    return render(request, 'inboxes/inbox.html', context)

def chat(request, type, id):
    contact = Inbox.objects.get(id=id)
    if type == 0:
        my_inbox = request.user.meccanicoadmin.inbox
    if type == 1:
        my_inbox = Inbox.objects.get(owner=request.user.username)
    elif type == 2:
        my_inbox = Inbox.objects.get(owner=request.user.storeprofile.name +' Store')
    elif type == 3:
        my_inbox = Inbox.objects.get(owner=request.user.workshopprofile.name +' Workshop')
        
    if(contact == my_inbox):
        return redirect('/')
    messages = my_inbox.sender.filter(receiver=contact) \
            | my_inbox.receiver.filter(sender=contact)
    messages = messages.order_by('timestamp') 
    MessageNotification.objects.filter(
            receiver_inbx=my_inbox,
            is_seen=False
        ).update(is_seen=True)
    Message.objects.filter(
            sender=contact,
            receiver=my_inbox,
            is_seen=False
        ).update(is_seen=True)
    contacts = my_inbox.mainInbx.all()
    context={
        'contact': contact,
        'contacts': contacts,
        'messages': messages,
        'my_inbox': my_inbox,
        }
    # users = User.objects.exclude(username=request.user.username)
    # chat = Chat.objects.get(thread_1name=thread_name)
    # message_objs =  chat.message_set.all()
    return render(request, 'inboxes/chat.html', context)