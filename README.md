# Python3 Project_3
## Laser Displacement Measurement

### 사용 언어
**Python 3.7.6**  
**Arduino 1.8.13**  

### 사용 환경
**Ubuntu 18.04 LTS**  

### 라이브러리
 - Python  
   - __future__  
   - csv  
   - RPI.GPIO
   - pyserial  
   - time  
   - matplotlib
   - tkinter  
 
 - Arduino  
   - 기본 라이브러리 사용

### 라이브러리 설치
**Python**  

```python

python -m pip install 라이브러리명

```

**Arduino**  

필요한 라이브러리 인터넷 검색 후 zip 파일 다운로드  

C:\Users\사용자명\Documents\Arduino\libraries 에 zip 파일 저장  

zip 파일 불러오기  
![image](https://user-images.githubusercontent.com/96412126/159386813-feac94ca-6859-458a-b36c-97582c2fd0cd.png)

C:\Users\사용자명\Documents\Arduino\libraries 에서 다운로드한 zip 파일 선택  

### 동작 개요

arduino : Realtime으로 레일 위를 지나가며 측정, 레이저 변위 센서에서 출력하는 전압값 받고 필터링 후 변위로 치환하여 Raspberry pi 에 전송  
Raspberry pi : arduino에서 받은 변위 값 기록, 필터링 후 데이터 가공하여 레일의 개수, 레일 표면의 요철 측정, 그래프와 csv 파일 출력  
               Flag 입력 시 측정 종료

![image](https://user-images.githubusercontent.com/96412126/160346173-bccc9b76-8442-456a-9e52-b118411cae3f.png)

![image](https://user-images.githubusercontent.com/96412126/160356004-1d2bcd42-7a1a-436d-9cd6-c2070ef9d129.png)

### 코드 설명  

**LaserSensor.ino**  

Photo Sensor에 Flag 입력이 있는지 실시간으로 확인, 현재 레일의 바닥면까지의 거리 전압값 변위로 변환 후 현재 Flag 값과 변위 값 Raspberry pi에 전송  

**Rail_Measure.py**  

Photo Sensor에서 Flag 입력이 있을 때 까지 측정 시작  
레일 표면 측정하면서 레일과 레일 사이의 빈 간격도 측정  
빈 간격 측정 시 센서 측정 범위 초과하여 다음 레일로 건너간 것으로 인식  
레일의 끝까지 측정 후 Photo Sensor에 Flag 입력, 측정 종료  
종료 후 측정한 데이터 각 레일의 요철값으로 가공하여 csv 파일, 그래프로 저장  
각 레일 별 최대/최소 거리 txt파일에 기록
