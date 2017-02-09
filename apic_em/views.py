from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from rest_framework.renderers import JSONRenderer
import requests
import json
from .get_stuff import get_token, get_config, get_device_id
from .bot import webhook_init, webhook


#Disable SSL warning
requests.packages.urllib3.disable_warnings()

# Create your views here.

apic_em_ip = "https://sandboxapic.cisco.com/api/v1"
catfacts_ip = 'http://catfacts-api.appspot.com/api'

def practice(request):

    requests.packages.urllib3.disable_warnings()
    api_call = "/facts"
    url = catfacts_ip + api_call
    header = '"text/html; charset=utf-8"'

    #get the cat fact - type will return as requests.models.Response
    my_response = requests.get(url, params='number=5', verify=False)

    #take the "utf-8" response value and convert it to a json disctionary
    data = json.loads(HttpResponse.getvalue(my_response).decode('utf-8'))

    #save one of the facts out to a variable
    response = data['facts'][0]

    return HttpResponse(response)

def index(request):

    template = loader.get_template('apic/index.html')
    auth_token = get_token(apic_em_ip)
    #print (type(auth_token))
    auth_token = json.loads(HttpResponse.getvalue(auth_token).decode('utf-8'))
    auth_token = auth_token['response']['serviceTicket']
    #print (auth_token)
    device_id = get_device_id(auth_token, apic_em_ip)
    #print (type(device_id))
    #device_id = json.loads(HttpResponse.getvalue(device_id).decode('utf-8'))
    #print (device_id)
    config = get_config(auth_token, apic_em_ip, device_id)
    output = config['response'].split('\n')
    context = {
        'output': output,
    }
    #print (type(config))
    print(config)
    #config = json.loads(HttpResponse.getvalue(config).decode('utf-8'))

    return HttpResponse(template.render(context, request))

def apic_api(request):

    #template = loader.get_template('apic/index.html')
    auth_token = get_token(apic_em_ip)
    #print (type(auth_token))
    auth_token = json.loads(HttpResponse.getvalue(auth_token).decode('utf-8'))
    auth_token = auth_token['response']['serviceTicket']
    #print (auth_token)
    device_id = get_device_id(auth_token, apic_em_ip)
    #print (type(device_id))
    #device_id = json.loads(HttpResponse.getvalue(device_id).decode('utf-8'))
    #print (device_id)
    config = get_config(auth_token, apic_em_ip, device_id)
    #output = config['response'].split('\n')
    #context = {
    #    'output': output,
    #}
    print (type(config))
    #print(config)
    #config = json.loads(HttpResponse.getvalue(config).decode('utf-8'))

    return JsonResponse(config)

def wh_init(request):
    response = webhook_init()
    return HttpResponse(response)

def sparkwebhook(request):
    wh_request = webhook(request)
    return