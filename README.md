# TCP Client

TCP 통신용 switch, sensor, binary_sensor, button을 생성하는 컴포넌트

---

## - 설치 방법
</br>

- 소스코드를 다운로드 받은 후 HA 내부의 custom_components 경로에 tcp_client 폴더를 넣어주고 재시작

또는

- HACS
HACS 의 custom repository에 https://github.com/oukene/tcp_client 주소를 integration 으로 추가 후 설치

- 설치 후 통합구성요소 추가하기에서 tcp client를 검색 하여 설치 한 후 구성을 진행합니다.
</br></br>


[설정 예제]


```
host: 192.168.11.120
port: 8888

sensor:
  - name: 테스트
    state:
      '0': ['00']
      '1': ['01']
      '2': ['02']
switch:
  - name: test
    state:
      'on': ['00']
      'off': ['01']
    command:
      'on': ['00 01']
      'off': ['01']
    off_timer: 5

binary_sensor:
  - name: test1
    state:
      'on': ['00', '01']
      'off': ['02']
    off_timer: 5
    device_class: sound

button:
  - name: test2
    command:
      'press': ["00"]

```


