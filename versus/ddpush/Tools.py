from __future__ import absolute_import
from celery import shared_task
from django.utils import timezone
from django.core.cache import cache

import os, subprocess, sys  
import json,requests

def preprocess_and_load(json_str):
    # Replace escaped quotes with actual quotes
    preprocessed_str = json_str.replace("\\\"", "\"")

    # Check if the string is encapsulated with quotes and not a valid JSON structure
    if preprocessed_str[0] == '\"' and preprocessed_str[-1] == '\"' and not preprocessed_str[1] == '{':
        preprocessed_str = preprocessed_str[1:-1]

    # Load as JSON
    json_obj = json.loads(preprocessed_str)
    
    return json_obj


def convert_to_json(input_string):
    # Strip leading/trailing quotes
    input_string = input_string.strip('\'"')

    # First attempt to directly parse the string as JSON
    try:
        return json.loads(input_string)
    except json.JSONDecodeError:
        pass

    # Try again after accounting for escaped characters
    try:
        return json.loads(input_string.encode().decode('unicode_escape'))
    except json.JSONDecodeError:
        # This is not a valid JSON string, so return as plaintext wrapped in a dictionary
        return {"log": input_string}


def transform_format(data_str):
    data = json.loads(data_str)
    log_content = data["log"]
    formatted_str = f"'''{log_content}'''"
    return formatted_str

#파일업로드
def handle_uploaded_file(file,POST,url,headers):
    log_type=POST.get('logType', None)
    order = POST.get('order', None)
    tags = POST.get('tags', 'ddpuah_upload')
    current_time = timezone.now()
    file_path = os.path.join('logfile', file.name) + '-' +str(current_time)

    print(file_path)
    #파일 생성
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # line queue input
    with open(file_path, 'r', encoding='utf-8') as file_to_process:
        for line in file_to_process:
            if(log_type=='text'):
                data = {
                    "tag" : f"{tags}",
                    "log" : str(line.replace("\n","")),
                }
                row = json.dumps(data)
                handle_log_text.delay(row,'text_log_file',url,headers)
            if(log_type=='json'):
                row = line.replace("\n","")
                json.loads(row)
                data = {
                    "tag" : f"{tags}",
                    "log" : json.loads(row),
                }
                handle_log_json.delay(str(json.dumps(data)),'json_log_file',url,headers)
            pass
    
    os.remove(file_path)
    

    
    

    




# redis 비동기 작업
@shared_task
def handle_log_text(row, client_ip, url, headers):
    json_row = convert_to_json(row)
    tag = json_row.get('tag')
    logs = json_row.get('log')
    if tag is None : 
        tag = f"api.sec,ddpush/log/text/"
    if logs is None:
        logs = json_row
    data = {
        "message": f"[api.sec] : {str(logs)}",
        "ddsource": f"{client_ip}",
        "ddtags": f"{tag}",
        "service": "ddpush/log/text/",
        "hostname": "api.sec",
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))   
    return response


@shared_task
def handle_log_json(row, client_ip, url, headers):
    json_row = preprocess_and_load(row)
    print(row)
    tag = json_row.get('tag')
    logs = json_row.get('log')
    if tag is None: 
        tag = f"api.sec,ddpush/log/json/"
    if logs is None: 
        logs = json_row
    default = {
        "message": f"[api.sec] : {str(logs)}",
        "ddsource": f"{client_ip}",
        "ddtags": f"{tag}",
        "service": "ddpush/log/json/",
        "hostname": "api.sec",
    }
    data = {
        **default, 
        **logs
    }       
    print(data) 
    response = requests.post(url, headers=headers, data=json.dumps(data))   
    print(response)
    return response

@shared_task
def handle_push(row):
    url = 'https://test.soldout.co.kr/api/v3/point/promotion/participation'
    UUID = f"UUID-{row}"
    headers = {
    'soldapp': 'android|7.7.2|7.50|SM-N950N',
    'APPKEY': 'JAkSzosy4X7K2FvPBwut5GN0At8DFuIwdhfs1dvr',
    'Content-Type': 'application/json',
    'deviceid': UUID
    }
    data = {
    'point_promotion_id': 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response