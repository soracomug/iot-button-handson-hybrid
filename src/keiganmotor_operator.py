## Python 3.9
"""
Copyright (c) 2022 Kohei "Max" MATSUSHITA (ma2shita+git@ma2shita.jp)
Released under the MIT license
https://opensource.org/licenses/mit-license.php
"""

"""Requires Envrionments
- DEST_AWS_ACCESS_KEY_ID (from IAM User)
- DEST_AWS_SECRET_ACCESS_KEY (from IAM User)
- DEST_ENDPOINT_URL (from IoT Core.)
- DEST_REGION_NAME (DEST_ENDPOINT_URL's region name.)
"""

"""Test: soracomfunk
{
    "clickType": 2,
    "clickTypeName": "DOUBLE",
    "batteryLevel": 1,
    "binaryParserEnabled": true
}
"""

WHAT_YOUR_NAME = "" # 画面に表示する文字列(半角17文字以内)
# 同じ角度(ex.SINGLE2度押し)だと、動かない
DEGREE_MAP = { # ボタンの押し方と、向かせたい角度をマッピングしている
    "SINGLE":   0,
    "DOUBLE": 120,
    "LONG":   240
}
# 上級編 対応する角度はカスタマイズ可能

import json
import os

def lambda_handler(event, context):
    print(json.dumps(event))

    degree = DEGREE_MAP[event['clickTypeName']]
    message17b = WHAT_YOUR_NAME

    # Build payload for IoT Core's device shadow doc.
    payload = { "state": { "desired": {
        "degree": degree,
        "message": message17b
    }}}
    # fire !!
    import boto3
    iot = boto3.client('iot-data',
        region_name=os.getenv('DEST_REGION_NAME'),   # us-west-2
        endpoint_url=os.getenv('DEST_ENDPOINT_URL'), # https://****-ats.iot.us-west-2.amazonaws.com
        aws_access_key_id=os.getenv('DEST_AWS_ACCESS_KEY_ID'),        # AKI.. (Required `Allow iot:UpdateThingShadow`)
        aws_secret_access_key=os.getenv('DEST_AWS_SECRET_ACCESS_KEY') # *****
    )
    iot.update_thing_shadow(thingName="mcu1", shadowName="keiganmotor", payload=json.dumps(payload, ensure_ascii=False))
    return {'statusCode': 200, 'body': 'Completed.'}

if __name__ == '__main__': # ローカル開発用
    event = {
        "clickType": 2,
        "clickTypeName": "SINGLE",
        "batteryLevel": 1,
        "binaryParserEnabled": True
    }
    context = {}
    lambda_handler(event, context)


"""refs:
- [Publish to IoT Endpoint of other Account - IoTData SDK NodeJS Lambda](https://repost.aws/questions/QUyQP-7Ki6T2202ZHCZ-qkig/publish-to-io-t-endpoint-of-other-account-io-t-data-sdk-node-js-lambda)
- [Boto3の設定あれこれ（profile名、アクセスキー、Config、DEBUGログの設定とか）](https://zenn.dev/sugikeitter/articles/how-to-use-boto3-various-settings)
- [Boto3 / Session reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html)
- [Boto3 / IoTDataPlane](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html)
"""
