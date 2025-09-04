### [ComWith] 2024-WinterProject-Backend
> **인천대학교 정보통신공학과 프로그래밍 소모임 ComWith**

<br/>

<div align="center">
  <h1>🎼 NotaNova 🎼</h1>
  <p> 원하는 음악을 악보로 변환하는 맞춤형 악보 제작 웹 서비스 </p>
</div>

<br/>

<div align="center">
  <h3>📍서비스 소개</h3>
  <p>
  연주하고 싶은 음악의 악보가 없어서 아쉬웠던 적이 있지 않으신가요? 
  
  NotaNova 서비스는 연주하고 싶은 곡의 악보가 없을 때, 누구나 쉽게 해당 음악의 악보를 얻을 수 있습니다. 

  사용자가 직접 업로드한 음악 파일을 기반으로 원하는 난이도와 악기 종류에 맞는 악보를 자동으로 생성하고, 
  
  작곡가와 악보 제목을 포함하여 개인화된 악보를 제작할 수 있습니다.

  <br/>

  또한, 제작된 악보는 PDF 파일로 미리 보기 및 다운로드가 가능하며,
  
  악기 연주 동영상 업로드 기능을 통해 연주를 웹 상에서 바로 재생할 수 있는 기능을 제공합니다.
  </p>
</div>

<br/>

## 프로젝트 정보
**진행 기간  :**  2024-12-28 ~ 2025-02-07

**프로젝트 형태  :**  WEB

**서비스 상태  :**  운영 중단

<br/>

## 배포 주소
<div align="center">
<table>
  <tr>
    <th>Site URL</th>
    <td><a href="https://smini.site/">NotaNova</a></td>
    <th>Frontend</th>
    <td><a href="https://github.com/ComWith/2024-WinterProject-Frontend">FE_Github</a></td>
    <th>Backend</th>
    <td><a href="https://github.com/ComWith/2024-WinterProject-Backend">BE_Github</a></td>
  </tr>
</table>
</div>

<br/>

## 개발자 소개
<div align="center">
<table>
  <tr>
    <td align="center"><b>이성민</b></td>
    <td align="center"><b>임재영</b></td>
    <td align="center"><b>이채원</b></td>
  </tr>
  <tr>
    <td align="center"><img width="160px" src="https://avatars.githubusercontent.com/smiinii" /></td>
    <td align="center"><img width="160px" src="https://avatars.githubusercontent.com/yim0327" /></td>
    <td align="center"><img width="160px" src="https://avatars.githubusercontent.com/C-ongshim" /></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/smiinii">@smiinii</a></td>
    <td align="center"><a href="https://github.com/yim0327">@yim0327</a></td>
    <td align="center"><a href="https://github.com/C-ongshim">@C-ongshim</a></td>
  </tr>
  <tr>
    <td align="center">인천대학교 정보통신공학과</td>
    <td align="center">인천대학교 정보통신공학과</td>
    <td align="center">인천대학교 정보통신공학과</td>
  </tr>
</table>
</div>

<br/>

## Stacks 🪄

### Framework
![Flask](https://img.shields.io/badge/flask-%23000000.svg?style=for-the-badge&logo=flask&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)

### DB & Storage
![MySQL](https://img.shields.io/badge/mysql-%234479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-%23569931.svg?style=for-the-badge&logo=amazons3&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DC382D.svg?style=for-the-badge&logo=redis&logoColor=white)

### Infra
![Docker](https://img.shields.io/badge/docker-%232496ED.svg?style=for-the-badge&logo=docker&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%2337814A.svg?style=for-the-badge&logo=celery&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS%20EC2-%23FF9900.svg?style=for-the-badge&logo=amazonec2&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

<br/>

## 주요 기능 🔥
### ⭐️ 업로드한 음악 파일을 자동으로 악보로 변환
- AI Music Analysis API | Klangio를 이용하여 음악 파일을 원하는 악보 형식으로 변경한다.

&nbsp;

### ⭐️ 무슨 악기의 악보를 원하는지 선택
- AI Music Analysis API | Klangio를 이용하여 악보로 변환할 때 사용자가 원하는 악기 선택 가능

&nbsp;

### ⭐️ 난이도 단계별 악보 표출
**a. 초급**
- 목표: 초보자도 쉽게 따라 할 수 있는 간단한 멜로디 제공
- 기준:
    1. 단순 멜로디: 곡의 주 멜로디만 추출. 화음(코드)나 복잡한 리듬은 생략
    2. 기본 코드: 멜로디와 함께 간단한 코드명 표시
    - 이유: 초급자는 화음 연주 대신 멜로디를 치는 데 집중하거나, 코드만 알아도 반주 가능
 
**b. 중급**

- 목표: 연주자의 표현력을 높이고, 음악적 이해를 확장.
- 기준:
    1. 코드 추가: 멜로디와 함께 코드 진행을 악보에 포함
    2. 리듬 추가: 원곡의 리듬감을 표현할 수 있도록 리듬 표기 추가
    3. 장식음: 꾸밈음, 이음줄 등을 추가해 악보를 풍부하게 구성
    - 이유: 중급자는 단순한 멜로디만 연주하기엔 지루할 수 있고, 리듬과 장식음은 더 자연스러운 연주로 이어짐
 
**c. 고급**

- 목표: 원곡에 최대한 가까운 연주를 위한 상세 정보 제공.
- 기준:
    1. 세부 화음: 코드뿐 아니라 화음의 세부 구성음까지 악보에 표시
    2. 복잡한 리듬: 빠른 음표, 복합 박자, 다이내믹 마크 등을 포함
    3. 연주 기법: 트릴, 글리산도, 스트로크, 핑거링 등 연주 기법 추가
    - 이유: 숙련자는 곡의 원곡 느낌을 살리는 디테일한 표현에 관심이 많음

<br/>

## 아키텍쳐
<div align="center">
  <img src="https://github.com/user-attachments/assets/41b8c17f-134c-455e-a738-5a38f438db99" 
       alt="Main" 
       width="700px"
       style="border-radius: 20px;"/>
</div>

<br/>

## ERD
<div align="center">
  <img src="https://github.com/user-attachments/assets/3e9c4f45-8d97-4a58-9882-7d2acfd0173c" 
       alt="Main" 
       width="700px"
       style="border-radius: 20px;"/>
</div>

