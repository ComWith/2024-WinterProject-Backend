### [ComWith] 2024-WinterProject-Backend
> **인천대학교 정보통신공학과 프로그래밍 소모임 ComWith**

<br/>

<div align="center">
  <h1>🎼 NotaNova 🎼</h1>
  <p> 원하는 음악을 악보로 변환하는 맞춤형 악보 제작 웹 서비스 </p>
</div>

<br/>

<div align="center">
  <img src="https://github.com/user-attachments/assets/07d90b7a-72ae-42d1-8fc6-37ae5b2ee92f" alt="Main" width="60%"/>
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

## Tech Stacks

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

## ⚙️ 주요 기능

### 1) 🔑 로그인 · 회원가입
- 이메일/소셜 로그인 지원 (예정 범위 포함)
- 첫 로그인 이후 개인화된 프로젝트/악보 관리

<div align="center">
  <img src="https://github.com/user-attachments/assets/fd17c101-055b-4f2c-847d-5ae423f2b91d" alt="로그인/회원가입 시연" width="80%"/>
</div>

&nbsp;

### 2) 📤 동영상 업로드
- 사용자가 보유한 음악/연주 영상(mp3/wav/mp4 등) 업로드
- 업로드 완료 후 자동 전처리 및 분석 대기

<div align="center">
  <img src="https://github.com/user-attachments/assets/fe8ecedc-0cdd-4d08-9e21-5a0fd8c0d7fd" alt="동영상 업로드 시연" width="80%"/>
</div>

&nbsp;

### 3) 🧾 악보 추출 및 다운로드
- **AI Music Analysis API** (Klangio)로 음악 분석 → 악보 자동 생성
- PDF 미리보기/다운로드 제공, 제목·작곡가 등 메타데이터 편집

<div align="center">
  <img src="https://github.com/user-attachments/assets/6da64889-8940-4015-956b-7cf2fd06cf21" alt="악보 추출 및 다운로드 시연" width="80%"/>
</div>

<details>
  <summary>세부 옵션 (난이도 · 악기) 펼치기</summary>

  #### 🎚 난이도 단계별 악보
  - **초급**: 주멜로디 중심, 간단한 코드 표기  
  - **중급**: 코드 진행/리듬/장식음 추가  
  - **고급**: 세부 화음/복잡 리듬/연주기법(트릴·글리산도 등) 포함

  #### 🎻 악기 선택
  - 변환 시 원하는 **악기 파트**(예: 피아노, 기타 등) 지정 가능
</details>

&nbsp;

### 4) 🎬 연주 영상 업로드
- 생성된 악보 기반의 **연주 영상 업로드** 및 웹 재생 지원
- 악보/영상 연동으로 학습·공유에 용이

<div align="center">
  <img src="https://github.com/user-attachments/assets/ea195e97-b6b6-474b-ad37-4da645c6adcb" alt="연주 영상 업로드 시연" width="80%"/>
</div>
<br/>

## 아키텍쳐
<div align="center">
  <img src="https://github.com/user-attachments/assets/41b8c17f-134c-455e-a738-5a38f438db99" 
       alt="Main" 
       width="70%"
       style="border-radius: 20px;"/>
</div>

<br/>

## ERD
<div align="center">
  <img src="https://github.com/user-attachments/assets/3e9c4f45-8d97-4a58-9882-7d2acfd0173c" 
       alt="Main" 
       width="70%"
       style="border-radius: 20px;"/>
</div>

## 프로젝트 팀원

🎯 **Team Leader** : 박병욱  

🎨 **Frontend** : 김경재 · 박병욱 · 전민경  

⚙️ **Backend** : 이성민 · 임재영 · 이채원  
