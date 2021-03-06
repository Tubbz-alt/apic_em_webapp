__author__ = 'brbuxton'

#! built with python3

"""A simple bot script based off https://github.com/CiscoDevNet/ciscosparkapi

This is a sample largely based off the work done by CiscoDevNet.
Many thanks to that team.  I have adapted their work for django.

You must create a Spark webhook that points to the URL where this script is
hosted.  You can do this via the CiscoSparkAPI.webhooks.create() method.

Additional Spark webhook details can be found here:
https://developer.ciscospark.com/webhooks-explained.html

A bot must be created and pointed to this server in the My Apps section of
https://developer.ciscospark.com.  The bot's Access Token should be added as a
'SPARK_ACCESS_TOKEN' environment variable on the web server hosting this
script.
"""

#from __future__ import print_function
from builtins import object

import json
import requests
import os

from django.http import HttpResponse, QueryDict, JsonResponse

from .get_stuff import return_dict_example

from ciscosparkapi import CiscoSparkAPI, Webhook

def webhook_init():
    #Webhook attributes
    webhookname="brbuxton_Get_Config"
    resource="messages"
    event="created"
    url_suffix="/apic/sparkwebhook/"
    web_server="http://apic-em-webapp.apps.imapex.io"

    #grab the at from a local at.txt file instead of global variable
    #fat=open ("apic_em/at.txt","r+")
    #at=fat.readline().rstrip()
    #fat.close
    at = os.environ['SPARK_AT']
    print (at)

    api = CiscoSparkAPI(at)
    whid=findwebhookidbyname(api, webhookname)
    print (whid)
    Url=web_server+url_suffix

    if "not found" in whid:
        #create
        print ("not found")
        dict=api.webhooks.create(webhookname, Url, resource, event)
        print (dict)
    else:
        #update
        print (whid)
        dict=api.webhooks.update(whid, name=webhookname, targetUrl=Url)
        print (dict)

    return dict

def get_config():
    """Get a config from apic_em and return it as a json.
    """
    apic_em_ip = "https://sandboxapic.cisco.com/api/v1"

    #response = return_dict_example(apic_em_ip)
    #return response['response']
    return apic_em_ip

def findwebhookidbyname(api, webhookname):
    webhooks = api.webhooks.list()
    for wh in webhooks:
        if wh.name == webhookname:
            return wh.id

    return "not found"

def webhook(request):
    #fat=open ("apic_em/at.txt","r+")
    #at=fat.readline().rstrip()
    #fat.close
    at = os.environ['SPARK_AT']
    print (at)

    api = CiscoSparkAPI(at)

    #print (json.loads(request.body.decode('utf-8')))
    """Respond to inbound webhook JSON HTTP POSTs from Cisco Spark."""
    json_data =  json.loads(request.body.decode('utf-8')) # Get the POST data sent from Spark
    print("\nWEBHOOK POST RECEIVED:")
    print(json_data, "\n")

    webhook_obj = Webhook(json_data)                        # Create a Webhook object from the JSON data
    room = api.rooms.get(webhook_obj.data.roomId)           # Get the room details
    message = api.messages.get(webhook_obj.data.id)         # Get the message details
    person = api.people.get(message.personId)               # Get the sender's details

    print("NEW MESSAGE IN ROOM '{}'".format(room.title))
    print("FROM '{}'".format(person.displayName))
    print("MESSAGE '{}'\n".format(message.text))

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    me = api.people.me()
    if message.personId == me.id:
        # Message was sent by me (bot); do not respond.
        return 'OK'
    else:
    # Message was sent by someone else; parse message and respond.
        if "get config" in message.text:
            print("FOUND 'config'")
            config = get_config()                                         # Get the config 
            print("SENDING config '{}'".format(config))
            response_message = api.messages.create(room.id, text=config)    # Post the fact to the room where the request was received
    return


if __name__ == '__main__':
    app.run()
