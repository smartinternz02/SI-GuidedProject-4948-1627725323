import wiotp.sdk.device
import time
import random

from ibmcloudant.cloudant_v1 import CloudantV1
from ibmcloudant import CouchDbSessionAuthenticator
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

authenticator = BasicAuthenticator('apikey-v2-1nwejm8ytwf942jovbc22ypplmjcgqzxkmk9kzuqb5de', '3b70fd2e1a2e6331a9807bf4bbd9483f')

service = CloudantV1(authenticator=authenticator)

service.set_service_url('https://apikey-v2-1nwejm8ytwf942jovbc22ypplmjcgqzxkmk9kzuqb5de:3b70fd2e1a2e6331a9807bf4bbd9483f@d1cf88ff-d098-4502-8be4-2bc64779192b-bluemix.cloudantnosqldb.appdomain.cloud')

myConfig = { 
    "identity": {
        "orgId": "fhmboz",
        "typeId": "PragatiDevice",
        "deviceId":"12312"
    },
    "auth": {
        "token": "njwe9hfaidn1"
    }
}

def myCommandCallback(cmd):
    t = cmd.data['text']
    print("printing: - - - ", t)
    print()

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

while True:
    temp=random.randint(100,800)
    hum=random.randint(0,100)
    flame=0
    fire=0

    # Scenario when fire is present
    if(temp>400 or hum>80):
        temp=random.randint(400,800)
        hum=random.randint(80,100)
        flame=random.randint(0,1)
        # flame=1
        if(flame):
            fire=random.randint(1,3)
        
    myData={'temperature':temp, 'humidity':hum, 'flame': flame, 'fireHeight': fire}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: ", myData)

    response = service.post_document(db='sample', document=myData).get_result()
    print("Data stored in Cloudant ___________",response)

    client.commandCallback = myCommandCallback
    time.sleep(1)
client.disconnect()