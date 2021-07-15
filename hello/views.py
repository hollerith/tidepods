from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
from .models import Greeting
from .constants import TrackingStatus, TrackRequest

import os
import json
import xmltodict
from types import SimpleNamespace

import requests

def index(request):
    response = requests.get('http://httpbin.org/status/418')
    print(response.text)
    return render(request, "results.html", {"results": response.text})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def search(request):

    if request.POST:
        tracking_number = request.POST["tracking_number"]

        # If the tracking number is cached 
        cached_file = os.path.join(settings.MEDIA_ROOT, f"{tracking_number}.xml")
        if os.path.isfile(cached_file):
            with open(cached_file) as fi: data = fi.read()
            response = MockResponse(data, 200)
        else:
            parent_key = settings.PARENT_KEY
            parent_pass = settings.PARENT_PASS
            user_key = settings.USER_KEY
            user_pass = settings.USER_PASS
            
            url = "https://wsbeta.fedex.com:443/web-services"
            headers = {'content-type': 'application/soap+xml'}
            body = TrackRequest % (parent_key, parent_pass, user_key, user_pass , tracking_number)
            response = requests.post(url, data=body, headers=headers)

        if response.status_code == 200:

            data = xmltodict.parse(response.content)
            data = json.loads(json.dumps(data))

            trackreply = TrackReply(data)
            if trackreply.TrackReply.HighestSeverity == "SUCCESS":
                if trackreply.severity in ('ERROR', 'FAILURE'):
                    context = {
                        "results": response.content,
                        "json_data": [],
                        "error_message" : trackreply.message
                    }
                    return render(request, "results.html", context)
                else:
                    context = {
                        "results": response.content,
                        "json_data": trackreply.api_track,
                    }
                    return render(request, "results.html", context)
            else:
                context = {
                    "results": response.text,
                    "json_data": [],
                    "error_message": trackreply.message
                }
                return render(request, "results.html", context)

        context = {
            "results": response.text,
            "error_message" : response.reason
        }
        return render(request, "results.html", context)

# have to mock responses here because the service
# is not responding at all at the moment to valid requests
class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.text = content
        self.status_code = status_code

    def content(self):
        return self.content

    def json(self):
        return self.content

class TrackReply:
    def __init__(self, data):

        self.TrackReply = SimpleNamespace(**data["SOAP-ENV:Envelope"]['SOAP-ENV:Body']['TrackReply'])
    
        if self.TrackReply.HighestSeverity == "SUCCESS":

            self.TrackDetails = SimpleNamespace(**data["SOAP-ENV:Envelope"]['SOAP-ENV:Body']['TrackReply']['CompletedTrackDetails']['TrackDetails']) 

            self.severity = self.TrackDetails.Notification['Severity']
            self.message = self.TrackDetails.Notification['Message'] 
            if self.severity == "SUCCESS":
                self.code = self.TrackDetails.StatusDetail['Code'] 

                self.carrier = "fedex" # Multiple codes... FXDE so?
                self.delivered, self.delivery_date = self.getDelivered()
                self.estimated_delivery = self.getEstimatedDelivery()
                self.tracking_number = self.TrackDetails.TrackingNumber 
                self.status = self.TrackDetails.StatusDetail['Description'] 
                self.tracking_stage = TrackingStatus[self.code]
                self.checkpoints = self.getCheckpoints()

                self.api_track = self.getTrack()
        else:
            self.message = TrackReply.Notifications['Message']
        
    def getDelivered(self):
        if self.TrackDetails.StatusDetail['Code'] == 'DL':
            return (True, self.TrackDetails.StatusDetail['CreationTime'])
        else:
            return (False, "")

    def getEstimatedDelivery(self):
        try:
            if self.TrackDetails.DatesOrTimes["Type"] == "ESTIMATED_DELIVERY":
                return self.TrackDetails.DatesOrTimes['DateOrTimeStamp']
        except:
            pass # old schema

    def getCheckpoints(self):
        checkpoints = []
        events = self.TrackDetails.Events
        if type(events) != list: events = [events]

        # format_dates()
        # 2021-06-07T10:46:07+06:00 --> "2021-06-07T10:46:07.000+1000"
        events.reverse()
        for event in events:
            event_type = event['EventType']

            if event_type == 'DL':
                self.delivered = True
                self.delivery_date = event['Timestamp']

            checkpoints.append({
                "description": event['EventDescription'],
                "status": event['EventDescription'],
                "tracking_stage": TrackingStatus[event_type],
                "time": event['Timestamp'] 
            })
        return checkpoints
    
    def getTrack(self):

        ugly = {
            "carrier": self.carrier,
            "delivered": self.delivered,
            "estimated_delivery": self.estimated_delivery,
            "delivery_date": self.delivery_date,
            "tracking_number": self.tracking_number,
            "status": self.status,
            "tracking_stage": self.tracking_stage,
            "checkpoints": self.checkpoints
        } 
        return json.dumps(ugly, indent=4)
    