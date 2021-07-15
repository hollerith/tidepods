# tidepods 

```
#!/bin/bash

curl -X POST https://wsbeta.fedex.com:443/web-services -H "Content-Type: application/soap+xml" -H "Accept: application/soap+xml" --data-binary @- <<DATA
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v14="http://fedex.com/ws/track/v14">
   <soapenv:Header/>
   <soapenv:Body>
      <v14:TrackRequest>
         <v14:WebAuthenticationDetail>
            <v14:ParentCredential>
               <v14:Key>$KEY</v14:Key>
               <v14:Password>$PASS</v14:Password>
            </v14:ParentCredential>
            <v14:UserCredential>
               <v14:Key>$USER_KEY</v14:Key>
               <v14:Password>$USER_PASS</v14:Password>
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
               <v14:Value>122816215025810</v14:Value>
            </v14:PackageIdentifier>           
            <v14:ShipmentAccountNumber/>
            <v14:SecureSpodAccount/>
              <v14:Destination>
               <v14:GeographicCoordinates>rates evertitque aequora</v14:GeographicCoordinates>
            </v14:Destination>
         </v14:SelectionDetails>
      </v14:TrackRequest>
   </soapenv:Body>
</soapenv:Envelope>
DATA
```
