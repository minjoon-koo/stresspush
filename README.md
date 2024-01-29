# api-sec.soldout.co.kr 데이터독 log push API 사용법

datadog log 검색 필터: `host:.api.sec`  

## Log 수동 업로드
**경로**: `log/`

이미 생성된 로그 파일을 데이터독에 업로드하여 분석에 활용할 수 있습니다. 로그는 평문 텍스트 형태와 JSON 형태로 구분하여 업로드가 가능하며, 태그 설정을 통해 데이터독에서의 로그 검색에 활용할 수 있습니다.

- (text형식) `source:text_log_file`
- (json형식) `source:json_log_file`
- (tag 지정시) `tag:[본인지정태그]`  
  


## REST API - json 로그
**경로**: `log/json/`

토큰 획득 방식: `'/oAuth/'`에 접속 후 Google oAuth2로 로그인합니다. 로그인 후 해당 페이지를 다시 방문하여 API 인증 토큰을 획득하세요.

### Tag를 지정하여 검색필터를 사용하는 경우:
```http
POST /ddpush/log/json/ HTTP/1.1
Host: api-sec.soldout.co.kr
Authorization: Token 2ce562d720a0a85d6637936b5375ed3a70e91752
Content-Type: application/json

{
  "tag": "Your Tag Name",
  "log": {
    "Your Json Key": "Your Json Value"
  }
}
```
Search filter: `> service:ddpush/log/json/ , tag:'Your Tag Name'`

### [로그만 전송하는 경우(tag:"api.sec,ddpush/log/json/")]
```http
POST /ddpush/log/json/ HTTP/1.1
Host: api-sec.soldout.co.kr
Authorization: Token 2ce562d720a0a85d6637936b5375ed3a70e91752
Content-Type: application/json

{'Your Json Log'}
```

Search filter: `> service:ddpush/log/json/ , tag:api.sec, tag:ddpush/log/json/`  
  


### 코드 샘플(PHP)
```php
<?php

$json_log = '{"type":1234,"case":{"dict":"dict1234"}}';
$tagging_data = [
    "tag" => "my-tag, my-tag2",
    "log" => $json_log
];
$tagging_log = json_encode($tagging_data);

$token = ''; //구글 로그인 후 /oAuth/ 페이지 접속으로 토큰 획득

$headers = [
    "Authorization: Token $token",
    "Content-Type: application/json"
];

// 첫 번째 요청
$ch1 = curl_init('http://api-sec.soldout.co.kr/ddpush/log/json/');
curl_setopt($ch1, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch1, CURLOPT_POSTFIELDS, $json_log);
curl_setopt($ch1, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch1, CURLOPT_HTTPHEADER, $headers);
$result1 = curl_exec($ch1);
curl_close($ch1);

// 두 번째 요청
$ch2 = curl_init('http://api-sec.soldout.co.kr/ddpush/log/json/');
curl_setopt($ch2, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch2, CURLOPT_POSTFIELDS, $tagging_log);
curl_setopt($ch2, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch2, CURLOPT_HTTPHEADER, $headers);
$result2 = curl_exec($ch2);
curl_close($ch2);

?>
```  
  

### 코드 샘플(python)
```python
#해당 예시에서는 로그를 변수로 직접 지정하여 전송
#상황에 맞게 api 호출 
json_log ='''{"type":1234,"case":{"dict":"dict1234"}}''' 
tagging_log = {
    "tag" : "my-tag, my-tag2"
    "log" : json_log
}

#header 지정 => Token 지정 
token = '' #구글 로그인 후 /oAuth/ 페이지 접속으로 토큰 획득

headers = {
'Authorization': f'Token {token}',
'Content-Type': 'application/json', 
}

#api 호출
requests.post('http://api-sec.soldout.co.kr/ddpush/log/json/', headers=headers, data=json_log)
requests.post('http://api-sec.soldout.co.kr/ddpush/log/json/', headers=headers, data=json.dumps(tagging_log))
            
```  
  


### 코드 샘플(curl)
```bash
#log only
curl -X POST \
-H "Authorization: Token YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"type":1234,"case":{"dict":"dict1234"}}' \
http://api-sec.soldout.co.kr/ddpush/log/json/ 

#tagging
curl -X POST \
-H "Authorization: Token YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"tag": "my-tag, my-tag2", "log": "{\"type\":1234,\"case\":{\"dict\":\"dict1234\"}}"}' \
http://api-sec.soldout.co.kr/ddpush/log/json/
```  
  




## REST API - Text 로그
**경로**: `/log/text/`

### 토큰 획득 방식
'/oAuth/'에 접속 후 Google oAuth2로 로그인합니다. 로그인 후 해당 페이지를 다시 방문하여 API 인증 토큰을 획득하세요.  
  


### Tag를 지정하여 검색필터를 사용하는 경우:
```http
POST /ddpush/log/text/ HTTP/1.1
Host: api-sec.soldout.co.kr
Authorization: Token 2ce562d720a0a85d6637936b5375ed3a70e91752
Content-Type: application/json

{
  "tag": "Your Tag Name",
  "log": "Your Plain Text Log"
}
```
Search filter: `> service:ddpush/log/text/ , tag:'Your Tag Name'`  
  


### 로그만 전송하는 경우:
```http
POST /ddpush/log/text/ HTTP/1.1
Host: api-sec.soldout.co.kr
Authorization: Token 2ce562d720a0a85d6637936b5375ed3a70e91752
Content-Type: application/json

'Your Plain Text Log'
```
Search filter: `> service:ddpush/log/text/ , tag:api.sec, tag:ddpush/log/text/`  
  



### 코드 샘플(PHP)
```php
<?php

$text_log = 'plain text log - test api push "hello"';
$tagging_data = [
    "tag" => "my-tag, my-tag2",
    "log" => $text_log
];
$tagging_log = json_encode($tagging_data);

$token = ''; // 구글 로그인 후 /oAuth/ 페이지 접속으로 토큰 획득

$headers = [
    "Authorization: Token $token",
    "Content-Type: application/json"
];

// 첫 번째 요청
$ch1 = curl_init('http://api-sec.soldout.co.kr/ddpush/log/text/');
curl_setopt($ch1, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch1, CURLOPT_POSTFIELDS, $text_log);
curl_setopt($ch1, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch1, CURLOPT_HTTPHEADER, $headers);
$result1 = curl_exec($ch1);
curl_close($ch1);

// 두 번째 요청
$ch2 = curl_init('http://api-sec.soldout.co.kr/ddpush/log/text/');
curl_setopt($ch2, CURLOPT_CUSTOMREQUEST, "POST");
curl_setopt($ch2, CURLOPT_POSTFIELDS, $tagging_log);
curl_setopt($ch2, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch2, CURLOPT_HTTPHEADER, $headers);
$result2 = curl_exec($ch2);
curl_close($ch2);

?>
```  
  


### 코드샘플(python)
```python
# 해당 예시에서는 로그를 변수로 직접 지정하여 전송
# 상황에 맞게 api 호출 
text_log = 'plain text log - test api push "hello"'
tagging_log = {
    "tag" : "my-tag, my-tag2",
    "log" : text_log
}

# header 지정 => Token 지정 
token = '' # 구글 로그인 후 /oAuth/ 페이지 접속으로 토큰 획득

headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json', 
}

# api 호출
import requests
requests.post('http://api-sec.soldout.co.kr/ddpush/log/text/', headers=headers, data=text_log)
requests.post('http://api-sec.soldout.co.kr/ddpush/log/text/', headers=headers, data=json.dumps(tagging_log))
```  
  

### 코드 샘플(curl)
```bash
# log only
curl -X POST \
-H "Authorization: Token YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d 'plain text log - test api push "hello"' \
http://api-sec.soldout.co.kr/ddpush/log/text/

# tagging
curl -X POST \
-H "Authorization: Token YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"tag": "my-tag, my-tag2", "log": "plain text log - test api push \"hello\""}' \
http://api-sec.soldout.co.kr/ddpush/log/text/
```
