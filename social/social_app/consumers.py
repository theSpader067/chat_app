import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import message,profile,groups,groupProfile

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def messages_to_json(self,messages):
        results = list()
        for msg in messages:
            if msg.author!=None:
                print('msgmsgmsgmsgmsgmsgmsgmsg',msg.author)
                json_msg = {
                'author': msg.author.username,
                'content':msg.content,
                'time_stamp':str(msg.time_stamp)
                }
                results.append(json_msg)
        return results

    def fetch_messages(self,data):
        print('fetch called')
        author = data['from']
        receiver = data['to']
        receiver_user = profile.objects.filter(profile_id=author)[0].profile_name
        if len(profile.objects.filter(profile_id=receiver))>0:
            author_user = profile.objects.filter(profile_id=receiver)[0].profile_name
            print(author_user,'::::',receiver_user)
            messages = message.get_last_10_messages(author_user,receiver_user)
        else :
            author_user = groupProfile.objects.filter(group_room=receiver)[0]
            print(author_user,'::::',receiver_user)
            messages = groupProfile.get_last_messages(receiver)

        content = {
        'command':'messages',
        'messages':self.messages_to_json(messages)
        }
        print(content)
        #message = data['message']
        #self.send_chat_messages(message)

        self.send_message(content)

    def new_messages(self,data):
        print('new_messages called')
        author = data['from']
        receiver = data['to']
        author_user = User.objects.filter(username=author)[0]
        if len(User.objects.filter(username=receiver)):
            receiver_user = User.objects.filter(username=receiver)[0]
            msg = message.objects.create(author=author_user,content=data['message'],receiver=receiver_user)
            msg = [msg]
        else:
            msg = groupProfile.objects.create(author=author_user,group_room=receiver,content=data['message'])
            msg = [msg]
        content={
        'command':'new_messages',
        'message':self.messages_to_json(msg)
        }
        return self.send_chat_messages(content)

    def create_group(self,data,data_group):
        print('gggggggggggggggggggggggggggggggggggg',data_group)
        for member in data_group['group_members']:
            member_profile = profile.objects.filter(profile_id=member)[0]
            g=groups(group_member = member_profile.profile_name,group_room=data_group['group_name'],group_description=data_group['description'])
            g.save()
            gp = groupProfile(group_room=data_group['group_name'])
            gp.save()
            print('group object created !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    commands={
    'fetch_messages':fetch_messages,
    'new_messages':new_messages,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print('-------------------------',data,'-----------------------------------------------')
        if data['command']=='create_group':
            self.create_group(self,data['group_members'])
        elif data['command']=='writing-status':
            writingSt='writing...'
            self.send(text_data=json.dumps(
                writingSt
            ))
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_status',
                    'status': writingSt,
                    'source':data['source']
                }
            )
        elif data['command']=='seen-signal':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_seen_signal',
                    'status': data['status'],
                    'source':data['source']
                }
            )
        elif data['command']=='video-control':
            video = data['video'].split('-')[0]
            print(video,data['status'],'tttttttttttttttttttttttttttttttttttttttttttttttt')
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'video_control',
                    'status': data['status'],
                    'source':data['source'],
                    'video':video
                }
            )

        elif data['command']=='offline_switch':
            print('closeeeeeeeeeeeeeeeeeeeeeeeeeeed')
            if len(profile.objects.filter(profile_id=data['source']))>0:
                pro = profile.objects.filter(profile_id=data['source'])[0]
                pro.profile_status =data['status']
                pro.save()
                print('saved status:' , pro.profile_status)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'offline_switch',
                        'status': pro.profile_status,
                        'source':data['source']
                    }
                )



        else:
            self.commands[data['command']](self,data)

        #message = data['message']
    def video_control(self,event):
        self.send(text_data=json.dumps(
            [event["status"],event["source"],event["video"]]
        ))

    def offline_switch(self,event):
        self.send(text_data=json.dumps(
            [event["status"],event["source"]]
        ))

    def send_status(self,event):
        self.send(text_data=json.dumps(
            [event["status"],event["source"]]
        ))

    def send_seen_signal(self,event):
        self.send(text_data=json.dumps(
            [event["status"],event["source"]]
        ))

    def send_chat_messages(self,message):

        # Send message to room group
        print(message['message'][0]['content'],'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def send_message(self,message):
        self.send(text_data=json.dumps(
            message
        ))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print(message,'------------------------------------------------------------------------------------------------------------------')
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            message,
        ))
