# The Flash
소프트웨어 마에스트로 6기 1단계 1차 프로젝트입니다.
마블 코믹스의 'The Flash'처럼, 실생활에 적용할 수 있는 '빠른' 서비스를 만들고자 시작되었습니다.

최종 결과물은 비콘 기반의 실내 위치 측위입니다. 'The Flash'가 블루투스가 켜진 스마트폰만 가지고 있다면, 언제든지 위치를 추적할 수 있습니다.(라고 의미를 부여해 봅니다)

# Requirements
- Python 2.7.10
- Flask 0.10.1
- Redis 3.0.3
- MariaDB 10.0.20

# Service Flow
1. 실내에 BLE 하드웨어 장착
1. BLE 하드웨어에서 Advertising Data(Broadcast) 송신
1. 스마트폰에서 데이터 수신 및 서버에 BLE 하드웨어 등록
1. 스마트폰에서 블루투스 신호의 세기를 기반으로 위치 계산
1. 서버로 위치 전송
1. 서버는 사용자들의 위치 공유

# Server Role
서버는 3가지 역할을 수행합니다.
1. 스마트폰과 통신하며 서비스 제공
1. 웹에서 서비스 사용자들의 위치 확인 기능
1. 생각중
