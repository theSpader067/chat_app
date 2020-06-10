from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
import json
from .forms import personal_profileForm,social_links_profileForm,about_profileForm,contactLookupForm,testForm
from django.utils.safestring import mark_safe
from django.views import View
from .models import profile,friendRequest,message,groups
from django.utils.decorators import method_decorator


def index(request):
    return redirect('/accounts/signup')

@login_required
def room(request, room_name,friend):
    time_series = {"username": request.user.username}
    json_string = json.dumps(time_series)
    pro = profile.objects.filter(profile_name=request.user)[0]
    twitter = pro.twitter_handle
    instagram = pro.instagram_handle
    facebook = pro.facebook_handle
    phone = pro.phone
    friends = [friend_names.profile_name.username for friend_names in pro.friends.all()]
    is_group = True
    is_friend = len(profile.objects.filter(profile_id=friend))>0
    if len(profile.objects.filter(profile_id=friend))>0:
        friend_profile = profile.objects.filter(profile_id=friend)[0]
    else :
        friend_profile = pro
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',testForm().create(friends))
    my_groups = list(groups.objects.filter(group_member=pro.profile_name))
    context={'room_name': room_name,
    'usern':request.user.username,
    'username':mark_safe(json.dumps(request.user.username)),
    'json_string': json_string,
    'friend':friend,
    'receiver':mark_safe(json.dumps(friend)),
    'contact':contactLookupForm(),
    'twitter':twitter,
    'instagram':instagram,
    'facebook':facebook,
    'phone':phone,
    'friends':friends,
    'defaultimage':'images/anon.png',
    'social_link_profile':social_links_profileForm(),
    'personal_profile':personal_profileForm(),
    'about_profile':about_profileForm(),
    'pro':pro,
    'friend_profile':friend_profile,
    #'group_form':t_form
    'my_groups':my_groups,
    'is_friend':mark_safe(json.dumps(is_friend)),
    }
    friend_requests=list()
    if len(friendRequest.objects.filter(to_user=request.user,status='P'))>0:

            friend_requests = [profile.objects.filter(profile_name = fr.from_user)[0] for fr in friendRequest.objects.filter(to_user=request.user,status='P')]
            context['friend_requests'] = friend_requests
            context['friend_requests_length']=len(friend_requests)
    else:
        print('didnt find any friend requests')
        context['friend_requests_length']=len(friend_requests)
    friends_objects=list()
    if pro.friends.all().count() >0:
        for f in pro.friends.all():
            if len(message.get_last_10_messages(f.profile_name,request.user))>0:
                #friends_objects[f] = friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom
                if len(friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name]))>0:
                    friends_objects.append((f,friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom,
                    message.get_last_10_messages(f.profile_name,request.user)[0].content))
            else:
                if len(friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name]))>0:
                    print('wubalabadubdub',friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom)
                    friends_objects.append((f,friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom,'say hi to your friend'))
        context['friends_objects'] = friends_objects
    return render(request, 'styx.html', context)


class register_profile(View):
    @method_decorator(login_required)
    def post(self,*args,**kwargs):
        print('::::::::::::::::::::::::::::::',kwargs)
        social_link_form = social_links_profileForm(data=self.request.POST)
        if social_link_form.is_valid():
            twitter = social_link_form.cleaned_data.get('twitter_handle')
            instagram = social_link_form.cleaned_data.get('instagram_handle')
            facebook = social_link_form.cleaned_data.get('facebook_handle')
            linkedin = social_link_form.cleaned_data.get('linkedin_handle')
            youtube = social_link_form.cleaned_data.get('youtube_handle')
            pro = profile.objects.filter(profile_name=self.request.user)[0]
            pro.twitter_handle = twitter
            pro.instagram_handle = instagram
            pro.facebook_handle = facebook
            pro.linkedin_handle = linkedin
            pro.youtube_handle = youtube
            pro.save()
            return redirect('social_app:room',room_name=kwargs['room_name'],friend=kwargs['friend'])
        personal_form = personal_profileForm(data=self.request.POST)
        if personal_form.is_valid():
            full_name = personal_form.cleaned_data.get('full_name')
            email = personal_form.cleaned_data.get('email')
            phone = personal_form.cleaned_data.get('phone')
            pro = profile.objects.filter(profile_name=self.request.user)[0]
            pro.phone = phone
            pro.email = email
            pro.profile_id = full_name
            pro.save()
            return redirect('social_app:room',room_name=kwargs['room_name'],friend=kwargs['friend'])
        about_form = about_profileForm(data=self.request.POST)
        if about_form.is_valid():
            motto = about_form.cleaned_data.get('personal_motto')
            pro = profile.objects.filter(profile_name=self.request.user)[0]
            pro.personal_motto = motto
            pro.save()
            return redirect('social_app:room',room_name=kwargs['room_name'],friend=kwargs['friend'])

class lookup_profile(View):
    def get(self,*args,**kwargs):
        form = contactLookupForm(data=self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('contact_name')
        try:
            user = profile.objects.filter(profile_id=name)[0]
            return redirect('social_app:foreign_profile',profile_id=name)
        except Exception as e:
            print (e)
            return render(self.request,'dead.html',{})

def foreign_profile(request,profile_id):
    pro = profile.objects.filter(profile_name=request.user)[0]
    foreign = profile.objects.filter(profile_id=profile_id)[0]
    twitter = pro.twitter_handle
    instagram = pro.instagram_handle
    facebook = pro.facebook_handle
    phone = pro.phone
    friends = [friend_names.profile_name.username for friend_names in pro.friends.all()]
    friends_objects=list()


    is_friend = profile_id in friends
    request_sent= False

    print(pro.profile_name)
    print(profile.objects.filter(profile_id=profile_id)[0].profile_name)
    print(friendRequest.objects.filter(to_user=profile.objects.filter(profile_id=profile_id)[0].profile_name,from_user=pro.profile_name))
    if len(list(friendRequest.objects.filter(to_user__in=[profile.objects.filter(profile_id=profile_id)[0].profile_name,pro.profile_name],from_user__in=[pro.profile_name,profile.objects.filter(profile_id=profile_id)[0].profile_name]))) > 0:
        request_sent = friendRequest.objects.filter(to_user__in=[profile.objects.filter(profile_id=profile_id)[0].profile_name,pro.profile_name],from_user__in=[pro.profile_name,profile.objects.filter(profile_id=profile_id)[0].profile_name])[0].status=='P'

    else:
        request_sent = False

    my_groups = list(groups.objects.filter(group_member=pro.profile_name))
    context={
    'usern':request.user.username,
    'username':mark_safe(json.dumps(request.user.username)),
    'foreign':foreign,
    'contact':contactLookupForm(),
    'twitter':twitter,
    'instagram':instagram,
    'facebook':facebook,
    'phone':phone,
    'friends':friends,
    'defaultimage':'images/anon.png',
    'friends_objects':friends_objects,
    'social_link_profile':social_links_profileForm(),
    'personal_profile':personal_profileForm(),
    'about_profile':about_profileForm(),
    'pro':pro,
    'is_friend':is_friend,
    'request_sent':request_sent,
    'my_groups':my_groups
    }

    if pro.friends.all().count() >0:
        for f in pro.friends.all():
            if len(message.get_last_10_messages(f.profile_name,request.user))>0:
                #friends_objects[f] = friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom
                if len(friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name]))>0:
                    friends_objects.append((f,friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom,
                    message.get_last_10_messages(f.profile_name,request.user)[0].content))
            else:
                if len(friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name]))>0:
                    print('wubalabadubdub',friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom)
                    friends_objects.append((f,friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom,'say hi to your friend'))
        context['friends_objects'] = friends_objects

    return render(request,'foreign_profile.html',context)

def post_signup(request):
    if len(profile.objects.filter(profile_name=request.user,profile_id=request.user.username))==0:
        pro = profile(profile_name=request.user,profile_id=request.user.username)
        pro.save()
    return redirect('social_app:profile')

@login_required
def profileView(request):
    pro = profile.objects.filter(profile_name=request.user)[0]
    twitter = pro.twitter_handle
    instagram = pro.instagram_handle
    facebook = pro.facebook_handle
    phone = pro.phone
    friends = [friend_names.profile_name.username for friend_names in pro.friends.all()]
    friends_objects = list()
    my_groups = list(groups.objects.filter(group_member=pro.profile_name))

    context={
    'usern':request.user.username,
    'username':mark_safe(json.dumps(request.user.username)),
    'contact':contactLookupForm(),
    'twitter':twitter,
    'instagram':instagram,
    'facebook':facebook,
    'phone':phone,
    'friends':friends,
    'defaultimage':'images/anon.png',
    'social_link_profile':social_links_profileForm(),
    'personal_profile':personal_profileForm(),
    'about_profile':about_profileForm(),
    'pro':pro,
    'my_groups':my_groups
    }
    if pro.friends.all().count() >0:
        for f in pro.friends.all():
            if len(message.get_last_10_messages(f.profile_name,request.user))>0:
                #friends_objects[f] = friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom
                if len(friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name]))>0:
                    friends_objects.append((f,friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom,
                    message.get_last_10_messages(f.profile_name,request.user)[0].content))
            else:
                if len(friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name]))>0:
                    print('wubalabadubdub',friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom)
                    friends_objects.append((f,friendRequest.objects.filter(to_user__in=[request.user,f.profile_name],from_user__in=[request.user,f.profile_name])[0].friendshipRoom,'say hi to your friend'))
        context['friends_objects'] = friends_objects

    friend_requests=list()
    if len(list(friendRequest.objects.filter(to_user=request.user,status='P')))>0:

            friend_requests = [profile.objects.filter(profile_name = fr.from_user)[0] for fr in friendRequest.objects.filter(to_user=request.user,status='P')]
            context['friend_requests'] = friend_requests
            context['friend_requests_length']=len(friend_requests)
    else:
        print('didnt find any friend requests')
        context['friend_requests_length']=len(friend_requests)

    return render(request,'profile.html',context)

def addFriend(request,profile_id):
    sender = profile.objects.filter(profile_id=request.user.username)[0].profile_name
    receiever = profile.objects.filter(profile_id=profile_id)[0].profile_name
    friendship = friendRequest(to_user=receiever , from_user=sender)
    friendship.save()
    print('--------------------------------------------------------added---------------------------------------------------')
    return redirect('social_app:foreign_profile',profile_id=profile_id)

def accept_friend(request,friend_id):
    friend = profile.objects.filter(profile_id=friend_id)[0]
    user = profile.objects.filter(profile_name=request.user)[0]
    user.friends.add(friend)
    friend.friends.add(user)
    fr = friendRequest.objects.filter(to_user=user.profile_name , from_user=friend.profile_name)[0]
    fr.status='A'
    fr.save()
    print(fr.status,'++++++++++++++++++++++++++++++++++++++++++++')
    return redirect('social_app:profile')

def decline_friend(request,friend_id):
    friend = profile.objects.filter(profile_id=friend_id)[0]
    user = profile.objects.filter(profile_name=request.user)[0]
    fr = friendRequest.objects.filter(to_user=user.profile_name , from_user=friend.profile_name)[0]
    fr.status='D'
    fr.save()
    return redirect('social_app:profile')

def get_room(request,friend_id):
    friend = profile.objects.filter(profile_id=friend_id)[0]
    user = profile.objects.filter(profile_name=request.user)[0]
    fr = friendRequest.objects.filter(to_user__in=[user.profile_name,friend.profile_name] , from_user__in=[friend.profile_name,user.profile_name])[0]

    roomName = fr.friendshipRoom
    context={
    'friend':friend
    }
    response = '/chat/'+roomName+'/'+friend_id+'/'
    return redirect(response)
