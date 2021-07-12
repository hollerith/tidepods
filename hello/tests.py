from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .views import index
from .specs import TrackingRequestXML

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

    def test_weather(self):
        """
        Check the weather 
        """
        import requests

        url="https://wsbeta.fedex.com:443/web-services"
        #headers = {'content-type': 'application/soap+xml'}
        headers = {'content-type': 'text/xml'}
        body = """<?xml version="1.0" encoding="UTF-8"?>
         <SOAP-ENV:Envelope xmlns:ns0="http://ws.cdyne.com/WeatherWS/" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" 
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
              <ns1:Body><ns0:GetWeatherInformation/></ns1:Body>
         </SOAP-ENV:Envelope>"""

        response = requests.post(url,data=body,headers=headers)
        print(response.content)

    def test_tracking(self):
        """
        Check the service 
        """
        import requests

        url="https://wsbeta.fedex.com:443/web-services"
        headers = {'content-type': 'application/soap+xml'}
        #headers = {'content-type': 'text/xml'}
        
        ParentCredentialKey = ""
        ParentCredentialPassword = ""
        UserCredentialKey = ""
        UserCredentialPassword = ""
        AccountNumber = ""
        MeterNumber = ""
        TrackingNumber = ""
        
        body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v14="http://fedex.com/ws/track/v14">
   <soapenv:Header/>
   <soapenv:Body>
      <v14:TrackRequest>
         <v14:WebAuthenticationDetail>
            <v14:ParentCredential>
               <v14:Key>{ ParentCredentialKey }</v14:Key>
               <v14:Password>{ ParentCredentialPassword }</v14:Password>
            </v14:ParentCredential>
            <v14:UserCredential>
               <v14:Key>{ UserCredentialKey }</v14:Key>
               <v14:Password>{ UserCredentialPassword }</v14:Password>
            </v14:UserCredential>
         </v14:WebAuthenticationDetail>
         <v14:ClientDetail>
            <v14:AccountNumber>{ AccountNumber }</v14:AccountNumber>
            <v14:MeterNumber>{ MeterNumber }</v14:MeterNumber>
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
               <v14:Value>{ TrackingNumber }</v14:Value>
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

        response = requests.post(url,data=body,headers=headers)
        print(response.content)
