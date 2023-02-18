import logging
import azure.functions as func

import datetime as dt
import sys
import requests
import pandas as pd
import uuid
from random import randrange
import json
from azure.iot.device import IoTHubDeviceClient, Message
from azure.iot.device import ProvisioningDeviceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Sending data to IOT central device.')

    request_data = req.get_json()
    origin = None
    destination = None
    key = None
    if request_data:
        origin = request_data['origin']
        destination = request_data['destination']
        key = request_data['key']

        print(origin)
        print(destination)
    
    query1 = {'wp.0': origin, 'wp.1': destination, 'optmz': 'distance', 'routeAttributes': 'routePath', 'key': key}

    response1 = requests.get('https://dev.virtualearth.net/REST/V1/Routes/Driving', params=query1)
    queryres=response1.json()

    dfnornamized=pd.json_normalize(queryres,['resourceSets','resources','routeLegs',['itineraryItems']])
    dffiltered=dfnornamized[['maneuverPoint.coordinates','travelDistance','travelDuration','instruction.text']]

    dltimestamp = []
    datenow = dt.datetime.now()
    value1=0
    for value in dffiltered['travelDuration']:
            value1= value+value1
            dat =  datenow + dt.timedelta(0,value1)
            dltimestamp.append(str(dat))

    dffiltered['datetime']=dltimestamp
    #dffiltered['tripId']=str(uuid.uuid4())
    print(dffiltered.rename(columns={"maneuverPoint.coordinates": "coordinates", "instruction.text": "directions"}))
    dffiltered = dffiltered.rename(columns={"maneuverPoint.coordinates": "coordinates", "instruction.text": "directions"})
    mydict = dffiltered.to_dict('records')

    # Azure IoT hub connection.
    # The client object is used to interact with your Azure IoT hub.
    provisioning_host = "global.azure-devices-provisioning.net"
    id_scope ="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    registration_id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    symmetric_key = "XXXXXXXXXXXXXXXXXXXXXXXXXX"

    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )

    # The result can be directly printed to view the important details.
    registration_result = provisioning_device_client.register()
    print(registration_result)

    # Connect the client.
    #device_client.connect()
    device_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=symmetric_key,
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id,
    )

    print(datenow.isoformat())

    device_client.connect()

    for dic in mydict:
        for k,v in dic.items():
            if str({k}) == "{'coordinates'}":
                coordinates = ["lat", "lon"]
                coordinates_dictionary = dict(zip(coordinates, v))
                coordinates_dictionary.update({'alt': randrange(100, 400, 2)})
                GeopointTelemetrydict=({'geolocation': coordinates_dictionary})
                GeopointTelemetrydict.update({'battery': randrange(30, 80, 2)})
                GeopointTelemetrydict.update({'accelerometer': {'x': randrange(15, 65, 2),'y': randrange(15, 65, 2),'z': randrange(15, 65, 2)}})
                GeopointTelemetrydict.update({'magnetometer': {'x': randrange(15, 65, 2),'y': randrange(15, 65, 2),'z': randrange(15, 65, 2)}})
                GeopointTelemetrydict.update({'gyroscope': {'x': randrange(15, 65, 2),'y': randrange(15, 65, 2),'z': randrange(15, 65, 2)}})
                GeopointTelemetrydict.update({'barometer': randrange(15, 65, 2)})  
                #GeopointTelemetrydict.update({'__t': 'c'})
                #Sensordict={'sensors': GeopointTelemetrydict}
                #msg = Message(str(Sensordict))   
                msg=(str(GeopointTelemetrydict))
                #print(msg) 
                msg = Message(str(GeopointTelemetrydict))             
                #payload = json.dumps(Sensordict) 
                payload = json.dumps(GeopointTelemetrydict)
                print(str(payload))
                msg = Message(payload)
                #msg = pnp_helper.create_telemetry(GeopointTelemetrydict, None)
                msg.content_encoding = "utf-8"
                msg.content_type = "application/json"
                msg.message_id = uuid.uuid4()
                device_client.send_message(msg)
    device_client.disconnect()
        
    return func.HttpResponse(f"Message Sent to IoT Central successfully.")

    #name = req.params.get('name')
    #if not name:
    #    try:
    #        req_body = req.get_json()
    #    except ValueError:
    #        pass
    #    else:
    #        name = req_body.get('name')

    #if name:
    #    return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    #else:
    #    return func.HttpResponse(
    #         "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #         status_code=200
    #    )
