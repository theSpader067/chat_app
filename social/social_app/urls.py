
from django.contrib import admin
from django.urls import path,include
from . import views

app_name='social_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<str:room_name>/<str:friend>/', views.room, name='room'),
    path('profile',views.profileView,name='profile'),
    path('PS',views.post_signup,name='post_signup'),
    path('profile_register/<str:room_name>/<str:friend>/',views.register_profile.as_view(),name='profile_register'),
    path('lookup_profile',views.lookup_profile.as_view(),name='lookup_profile'),
    path('foreign_profile/<str:profile_id>',views.foreign_profile,name='foreign_profile'),
    path('add_friend/<str:profile_id>',views.addFriend,name='add_friend'),
    path('accept_friend/<str:friend_id>',views.accept_friend,name='accept_friend'),
    path('decline_friend/<str:friend_id>',views.decline_friend,name='decline_friend'),
    path('get_room/<str:friend_id>',views.get_room,name='get_room'),
]
