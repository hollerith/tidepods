from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import json
import xmltodict
from types import SimpleNamespace

# Create your views here.
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

        url = "https://wsbeta.fedex.com:443/web-services"
        headers = {'content-type': 'application/soap+xml'}
        tracking_number = "122816215025810"

        body = \
f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v14="http://fedex.com/ws/track/v14">
    <soapenv:Header/>
    <soapenv:Body>
        <v14:TrackRequest>
            <v14:WebAuthenticationDetail>
                <v14:ParentCredential>
                    <v14:Key>HicUfijJZSUAtqAG</v14:Key>
                    <v14:Password>2IX4AJyvWW9WltylOvw3RokcN</v14:Password>
                </v14:ParentCredential>
                <v14:UserCredential>
                    <v14:Key>mIAfOSJ0e32Zc4oV</v14:Key>
                    <v14:Password>gvTG2nBBVKwZq9dWJnBnJ7rVH</v14:Password>
                </v14:UserCredential>
            </v14:WebAuthenticationDetail>
            <v14:ClientDetail>
                <v14:AccountNumber>602091147</v14:AccountNumber>
                <v14:MeterNumber>118785166</v14:MeterNumber>
            </v14:ClientDetail>
            <v14:TransactionDetail>
                <v14:CustomerTransactionId>Track By Number_v14</v14:CustomerTransactionId>
                <v14:Localization>
                    <v14:LanguageCode>EN</v14:LanguageCode>
                    <v14:LocaleCode>US</v14:LocaleCode>
                </v14:Localization>
            </v14:TransactionDetail>
            <v14:Version>
                <v14:ServiceId>trck</v14:ServiceId>
                <v14:Major>14</v14:Major>
                <v14:Intermediate>0</v14:Intermediate>
                <v14:Minor>0</v14:Minor>
            </v14:Version>
            <v14:SelectionDetails>
                <v14:CarrierCode>FDXE</v14:CarrierCode>
                <v14:PackageIdentifier>
                   <v14:Type>TRACKING_NUMBER_OR_DOORTAG</v14:Type>
                   <v14:Value>{ tracking_number }</v14:Value>
                </v14:PackageIdentifier>           
                <v14:ShipmentAccountNumber/>
                <v14:SecureSpodAccount/>
                  <v14:Destination>
                   <v14:GeographicCoordinates>rates evertitque aequora</v14:GeographicCoordinates>
                </v14:Destination>
            </v14:SelectionDetails>
        </v14:TrackRequest>
    </soapenv:Body>
</soapenv:Envelope>"""

        response = requests.post(url, data=body, headers=headers)

        if response.status_code == 200:
                       
            data = xmltodict.parse(response.content)
            data = json.loads(json.dumps(data))

            TrackDetails = SimpleNamespace(**data["SOAP-ENV:Envelope"]['SOAP-ENV:Body']['TrackReply']['CompletedTrackDetails']['TrackDetails'])

            if TrackDetails.Notification['Severity'] == 'ERROR':
                context = {
                    "results": response.text,
                    "json_data": data,
                    "error_message" : TrackDetails.Notification['Message']
                }
                return render(request, "results.html", context)

            if TrackDetails.DatesOrTimes["Type"] == "ANTICIPATED_TENDER":
                estimated_delivery = TrackDetails.DatesOrTimes['DateOrTimeStamp']

            delivered = True
            delivery_date = "2021-06-07T00:00:00.000Z"
            status = "Delivered to a mailbox"
            tracking_stage = "DELIVERED"

            apijson = {
                "carrier": "fedex",
                "delivered": delivered,
                "estimated_delivery": estimated_delivery,
                "delivery_date": delivery_date,
                "tracking_number": tracking_number,
                "status": status,
                "tracking_stage": tracking_stage,
                "checkpoints": [
                    {
                    "description": "Delivered to a mailbox",
                    "status": "Delivered to a mailbox",
                    "tracking_stage": "DELIVERED",
                    "time": "2021-06-07T10:46:07.000+1000"
                    }
                ]
            }
            
        return render(request, "results.html", {"results": response.text, "json": json})
