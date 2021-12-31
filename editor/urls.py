from django.urls import path
from . import views

urlpatterns = [
    path('editor/', views.editor_view, name='index'),
    path("run/", views.run_code, name="run_code"),
    path('', views.index, name='agora-index'),
    path('pusher/auth/', views.pusher_auth, name='agora-pusher-auth'),
    path('token/', views.generate_agora_token, name='agora-token'),
    path('call-user/', views.call_user, name='agora-call-user'),
]