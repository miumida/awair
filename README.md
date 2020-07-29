# AWAIR Local Sensor

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.4][version-shield]

AWAIR Local Sensor for Home Assistant 입니다.<br>

![screenshot_2](https://github.com/miumida/awair2mqtt/blob/master/image/awair2mqtt_sensor.png?raw=true)<br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2020.06.30  | First version  |
| v1.0.1  | 2020.07.02  | unit_of_measurement 추가 |
| v1.0.2  | 2020.07.29  | air-data 속성 추가 &  |

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/awair/__init__.py`<br>
  `<config directory>/custom_components/awair/manifest.json`<br>
  `<config directory>/custom_components/awair/sensor.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>

<br>

## Usage
### configuration
- HA 설정에 awair sensor를 추가합니다.<br>
```yaml
sensor:
  - platform: awair
    scan_interval: 60
    devices:
      - id: '[Your AWAIR Device ID]'
        name: '[Your AWAIR Device Name]'
        ip: '[Your AWAIR Device IP]'
```
<br><br>
### 기본 설정값

|옵션|내용|
|--|--|
|name| (옵션) Name / default(awair)|
|devices| (필수) AWAIR Devices |
|scan_interval| (옵션) Sensor Update Term / default(10s) |

<br>

### devices 설정값

|옵션|값|
|--|--|
|id| (필수) AWAIR ID, 띄워쓰기(X), 한글(X) |
|name| (필수) AWAIR Nickname |
|ip| (필수) AWAIR Local IP |

<br>

### awair_type 설정값

|코드|값|Score|Temperature|Humidity|VOC|CO2|PM2.5|Light|Noise|
|--|--|--|--|--|--|--|--|--|--|
|S| 2nd Edition |O|O|O|O|O|O|X|X|
|M| Mint |O|O|O|O|X|O|O|O|
|O| Omni |O|O|O|O|O|O|O|O|
|E| Element |O|O|O|O|O|O|X|X|

<br>

## 참고사이트
[1] 네이버 HomeAssistant 카페 | 랜이님의 어웨어 로컬센서 설정기 (<https://cafe.naver.com/koreassistant/703>)<br>
[2] 네이버 HomeAssistant 카페 | 크리틱님의 Awair를 Local로 사용하기 + α (<https://cafe.naver.com/koreassistant/729>)<br>

[version-shield]: https://img.shields.io/badge/version-1.0.1-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
