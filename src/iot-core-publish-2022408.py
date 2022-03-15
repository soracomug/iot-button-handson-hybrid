## Python 3.9
"""
Copyright (c) 2022 Kenichiro Wada(k0929wad@gmail.com)
based by Kohei "Max" MATSUSHITA (ma2shita+git@ma2shita.jp)
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""

"""Requires Envrionments
- DEST_AWS_ACCESS_KEY_ID (from IAM User)
- DEST_AWS_SECRET_ACCESS_KEY (from IAM User)
- DEST_ENDPOINT_URL (from IoT Core.)
- DEST_REGION_NAME (DEST_ENDPOINT_URL's region name.)
- MESSAGE (Message to be displayed on screen.)
- RPM (Sets the device's rotation speed. Range : 10-120)

"""

"""test:linebot-incoming
{
    "clickType": 1,
    "clickTypeName": "SINGLE",
    "batteryLevel": 0.75,
    "binaryParserEnabled": true
}
"""

import json
import os

def lambda_handler(event, context):
    ##print(json.dumps(event))


    # extract Click Type.
    try:
        click_type = event['clickType']
    except (IndexError, KeyError) as _:
        print('## Not exists `event.clickType`, done.')
        return {'statusCode': 200, 'body': 'event.clickType`, done.'}
    print(f'## click_type: {click_type}')

    # degree by Click Type.
    if click_type == 1:
        degree = 90
    elif click_type == 2:
        degree = 180
    else:
        degree = 360

    # rpm create randam
    rpm = os.getenv('RPM')
    # fire !!
    import boto3
    iot = boto3.client('iot-data',
        region_name=os.getenv('DEST_REGION_NAME'),   # us-west-2
        endpoint_url=os.getenv('DEST_ENDPOINT_URL'), # https://****-ats.iot.us-west-2.amazonaws.com
        aws_access_key_id=os.getenv('DEST_AWS_ACCESS_KEY_ID'),        # AKI.. (Required `Allow iot:Publish`)
        aws_secret_access_key=os.getenv('DEST_AWS_SECRET_ACCESS_KEY') # *****
    )
    topic = 'wiolte-797973/command'
    payload = {
        'method': 'moveByDistanceDegree', 'degree': degree, 'rpm': rpm, 'message': os.getenv('MESSAGE')
    }
    iot.publish(topic=topic, payload=json.dumps(payload, ensure_ascii=False))

    return {'statusCode': 200, 'body': 'Completed.'}

    """refs:
    - [Publish to IoT Endpoint of other Account - IoTData SDK NodeJS Lambda](https://repost.aws/questions/QUyQP-7Ki6T2202ZHCZ-qkig/publish-to-io-t-endpoint-of-other-account-io-t-data-sdk-node-js-lambda)
    - [Boto3の設定あれこれ（profile名、アクセスキー、Config、DEBUGログの設定とか）](https://zenn.dev/sugikeitter/articles/how-to-use-boto3-various-settings)
    - [Boto3 / Session reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html)
    - [Boto3 / IoTDataPlane](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html)
    """
