TrackRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v14="http://fedex.com/ws/track/v14">
    <soapenv:Header/>
    <soapenv:Body>
        <v14:TrackRequest>
            <v14:WebAuthenticationDetail>
                <v14:ParentCredential>
                    <v14:Key>%s</v14:Key>
                    <v14:Password>%s</v14:Password>
                </v14:ParentCredential>
                <v14:UserCredential>
                    <v14:Key>%s</v14:Key>
                    <v14:Password>%s</v14:Password>
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
                   <v14:Value>%s</v14:Value>
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

TrackingStatus = {
    'PF' : 'Plane in Flight',
    'AA' : 'At Airport',
    'PL' : 'Plane Landed',
    'AC' : 'At Canada Post facility',
    'PM' : 'In Progress',
    'AD' : 'At Delivery',
    'PU' : 'Picked Up',
    'AF' : 'At FedEx Facility',
    'PX' : 'Picked up (see Details)',
    'AP' : 'At Pickup',
    'RR' : 'CDO requested',
    'AR' : 'Arrived at',
    'RM' : 'CDO Modified',
    'AX' : 'At USPS facility',
    'RC' : 'CDO Cancelled',
    'CA' : 'Shipment Cancelled',
    'RS' : 'Return to Shipper',
    'CH' : 'Location Changed',
    'RP' : 'Return label link emailed to return sender',
    'DD' : 'Delivery Delay',
    'LP' : 'Return label link cancelled by shipment originator',
    'DE' : 'Delivery Exception',
    'RG' : 'Return label link expiring soon',
    'DL' : 'Delivered',
    'RD' : 'Return label link expired',
    'DP' : 'Departed',
    'SE' : 'Shipment Exception',
    'DR' : 'Vehicle furnished but not used',
    'SF' : 'At Sort Facility',
    'DS' : 'Vehicle Dispatched',
    'SP' : 'Split Status',
    'DY' : 'Delay',
    'TR' : 'Transfer',
    'EA' : 'Enroute to Airport',
    'ED' : 'Enroute to Delivery',
    'CC' : 'Cleared Customs',
    'EO' : 'Enroute to Origin Airport',
    'CD' : 'Clearance Delay',
    'EP' : 'Enroute to Pickup',
    'CP' : 'Clearance in Progress',
    'FD' : 'At FedEx Destination',
    'EA' : 'Export Approved',
    'HL' : 'Hold at Location',
    'SP' : 'Split Status',
    'IT' : 'In Transit',
    'IX' : 'In transit (see Details)',
    'CA' : 'Carrier',
    'LO' : 'Left Origin',
    'RC' : 'Recipient',
    'OC' : 'Order Created',
    'SH' : 'Shipper',
    'OD' : 'Out for Delivery',
    'CU' : 'Customs',
    'OF' : 'At FedEx origin facility',
    'BR' : 'Broker',
    'OX' : 'Shipment information sent to USPS',
    'PD' : 'Pickup Delay',
    'TP' : 'Transfer Partner',
    'SP' : 'Split status'
}