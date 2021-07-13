from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .views import index

from types import SimpleNamespace

import requests
import xmltodict
import json

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get("/")
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_tracking(self):
        """
        Check the service 
        """

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
        self.assertEqual(response.status_code, 200)
        print(response.content)

    def test_canned(self):
        """
        Check the canned response  
        """
        
        with open('./hello/static/response.xml', 'r') as fi: 
            data = fi.read()

        data = xmltodict.parse(data)
        dota = json.loads(json.dumps(data))

        TrackDetails = SimpleNamespace(**dota["SOAP-ENV:Envelope"]['SOAP-ENV:Body']['TrackReply']['CompletedTrackDetails']['TrackDetails'])

