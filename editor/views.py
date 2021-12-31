from django.shortcuts import render
from helpers import get_code_result
import json
from django.http import JsonResponse
import os
import time
import json
from pusher import Pusher

from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee

from dotenv import load_dotenv
from os.path import join, dirname

from django.contrib.auth import get_user_model

dotenv_path = '.env'
load_dotenv(dotenv_path)


pusher_client = Pusher(app_id=os.environ.get('PUSHER_APP_ID'),
                       key=os.environ.get('PUSHER_KEY'),
                       secret=os.environ.get('PUSHER_SECRET'),
                       ssl=True,
                       cluster=os.environ.get('PUSHER_CLUSTER')
                       )

# Create your views here.
def editor_view(request):
    return render(request, 'editor/editor.html')

def run_code(request):
    post_data = json.loads(request.body.decode("utf-8"))
    res = get_code_result(post_data['code'], post_data['lang'], post_data['input'])
    print(res)
    return JsonResponse({"output": res["output"]})

def pusher_auth(request):
    print("This user has trying to connect to pusher: " + request.user.username)
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'id': request.user.id,
                'name': request.user.username
            }
        })
    return JsonResponse(payload)


def generate_agora_token(request):
    appID = os.environ.get('AGORA_APP_ID')
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
    channelName = json.loads(request.body.decode(
        'utf-8'))['channelName']
    userAccount = request.user.username
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithAccount(
        appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)

    return JsonResponse({'token': token, 'appID': appID})


def call_user(request):
    body = json.loads(request.body.decode('utf-8'))

    user_to_call = body['user_to_call']
    channel_name = body['channel_name']
    caller = request.user.id

    pusher_client.trigger(
        'presence-online-channel',
        'make-agora-call',
        {
            'userToCall': user_to_call,
            'channelName': channel_name,
            'from': caller
        }
    )
    return JsonResponse({'message': 'call has been placed'})

def index(request):
    User = get_user_model()
    all_users = User.objects.exclude(id=request.user.id).only('id', 'username')
    return render(request, 'editor/index.html', {'allUsers': all_users})
