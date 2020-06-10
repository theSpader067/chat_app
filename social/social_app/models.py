import Crypto.Cipher.ARC4
from django.db import models
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
from django.conf import settings
# Create your models here.

User = get_user_model()

FRIENDSHIP_REQUEST_STATUS = (
('A','accepted'),
('D','declined'),
('C','cancelled'),
('P','pending')
)

PROFILE_STATUS = (
('ONN','online'),
('OFF','offline'),
('BUS','busy'),
)

class message(models.Model):
    author = models.ForeignKey(User,related_name='author_messages',on_delete= models.CASCADE)
    content = models.TextField()
    receiver = models.ForeignKey(User,related_name='receiver_messages',on_delete= models.CASCADE,null=True,blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author.username) +' to '+str(self.receiver.username)+':'+ str(self.content)[:10]

    def get_last_10_messages(author,receiver):
        print('fetching last 10 message')
        results = list()
        results.extend(message.objects.filter(author__in=[receiver,author],receiver__in=[author,receiver]).order_by('-time_stamp').all()[:10])
        return results[:10]

class groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_member = models.ForeignKey(User, related_name="group_members",on_delete=models.CASCADE)
    group_room = models.CharField(max_length=200,blank=True,null=True)
    group_description = models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return self.group_room+':'+self.group_member.username

class groupProfile(models.Model):
    group_profile_id = models.AutoField(primary_key=True)
    group_room = models.CharField(max_length=200,blank=True,null=True)
    content = models.CharField(max_length=200,blank=True,null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,related_name='group_profile_author',null=True,on_delete= models.CASCADE)

    def get_last_messages(group):
        print('fetching last 10 message')
        results = list()
        results.extend(groupProfile.objects.filter(group_room=group).order_by('-time_stamp').all()[:10])
        return results[:10]

class profile(models.Model):
    profile_name = models.OneToOneField(User,on_delete= models.CASCADE)
    twitter_handle = models.CharField(max_length=200,default='Empty')
    facebook_handle = models.CharField(max_length=200,default='Empty')
    instagram_handle = models.CharField(max_length=200,default='Empty')
    linkedin_handle = models.CharField(max_length=200,default='Empty')
    youtube_handle = models.CharField(max_length=200,default='Empty')
    phone = models.IntegerField(default=0,)
    email = models.CharField(max_length=200,default='Empty')
    friends = models.ManyToManyField("profile",blank=True)
    profile_id = models.CharField(max_length=200,default='anonym')
    profile_status = models.CharField(choices=PROFILE_STATUS, max_length=3, blank=True, default='OFF')
    personal_motto = models.CharField(max_length=200, blank=True, default='i am at work')
    avatar = models.CharField(max_length=200,default='images/anon.png')

    def __str__(self):
        return self.profile_name.username

    def save(self,*args,**kwargs):
        if str(self.profile_id[0]).lower()=='a':
            self.avatar = 'images/a.png'
        if str(self.profile_id[0]).lower()=='b':
            self.avatar = 'images/b.png'
        if str(self.profile_id[0]).lower()=='c':
            self.avatar = 'images/c.png'
        if str(self.profile_id[0]).lower()=='d':
            self.avatar = 'images/d.png'
        if str(self.profile_id[0]).lower()=='e':
            self.avatar = 'images/e.png'
        if str(self.profile_id[0]).lower()=='f':
            self.avatar = 'images/f.png'
        if str(self.profile_id[0]).lower()=='g':
            self.avatar = 'images/g.png'
        if str(self.profile_id[0]).lower()=='h':
            self.avatar = 'images/h.png'
        if str(self.profile_id[0]).lower()=='i':
            self.avatar = 'images/i.png'
        if str(self.profile_id[0]).lower()=='j':
            self.avatar = 'images/j.png'
        if str(self.profile_id[0]).lower()=='k':
            self.avatar = 'images/k.png'
        if str(self.profile_id[0]).lower()=='l':
            self.avatar = 'images/l.png'
        if str(self.profile_id[0]).lower()=='m':
            self.avatar = 'images/m.png'
        if str(self.profile_id[0]).lower()=='n':
            self.avatar = 'images/n.png'
        if str(self.profile_id[0]).lower()=='o':
            self.avatar = 'images/o.png'
        if str(self.profile_id[0]).lower()=='p':
            self.avatar = 'images/p.png'
        if str(self.profile_id[0]).lower()=='q':
            self.avatar = 'images/q.png'
        if str(self.profile_id[0]).lower()=='r':
            self.avatar = 'images/r.png'
        if str(self.profile_id[0]).lower()=='s':
            self.avatar = 'images/s.png'
        if str(self.profile_id[0]).lower()=='t':
            self.avatar = 'images/t.png'
        if str(self.profile_id[0]).lower()=='u':
            self.avatar = 'images/u.png'
        if str(self.profile_id[0]).lower()=='v':
            self.avatar = 'images/v.png'
        if str(self.profile_id[0]).lower()=='w':
            self.avatar = 'images/w.png'
        if str(self.profile_id[0]).lower()=='x':
            self.avatar = 'images/x.png'
        if str(self.profile_id[0]).lower()=='y':
            self.avatar = 'images/y.png'
        if str(self.profile_id[0]).lower()=='z':
            self.avatar = 'images/z.png'

        super(profile, self).save(*args, **kwargs)


class friendRequest(models.Model):
    to_user = models.ForeignKey(User,related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User,related_name='from_user',on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=FRIENDSHIP_REQUEST_STATUS, max_length=2, blank=True, default='P')
    friendshipRoom = models.CharField(max_length=256,null=True,blank=True)
    def __str__(self):
        return 'from '+self.from_user.username+' to '+self.to_user.username

    def save(self,*args,**kwargs):
        string= self.to_user.username[0]+''+self.from_user.username[0]

        self.friendshipRoom = string

        super(friendRequest, self).save(*args, **kwargs)
