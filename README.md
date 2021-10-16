# **⚫️ DotFriends**

[![시연동영상](https://images.velog.io/images/sdk1926/post/ed163123-f7c1-4f44-91ef-76fe807dbb82/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-09-11%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2010.41.19.png)](https://youtu.be/T5bOgE7dzwk)

**🌄 이미지를 클릭하면 시연 영상을 시청하실 수 있습니다.**

---

## ⭐️ **프로젝트 소개**

- 라인프렌즈 커머스 사이트 라인프렌즈샵 클론 프로젝트

- 기획, 디자인 시간 단축을 위해 사이트의 디자인과 레이아웃만 참고해서 만들었습니다.

###  **🤔 기획 의도**

- 라인프렌즈 사이트 자체를 따라하기 보다는 재치있는 아이디어를 통해, Line 이 아니라 Dot Friends 로 이름을 정했습니다.

- 코로나시대에 맞게 사람과 사람을 연결하는 Line이 아니라 개인 혼자 (Dot) 집에서 지낼 때 활용할 수 있는 상품을 판매하는 컨셉을 잡았습니다

### **📆 개발 기간**

- 2021.08.30 - 2021.09.09
- 리팩토링은 계속 진행 중입니다. 

### **👨‍👩‍👦 개발 인원**

- **FrontEnd**
  - 금보배, 박은정, 주철진
- **BackEnd**
  - 신우주, 김동준, 서동규

## **🎬 시연 영상**
* [시연 영상 보러 가기](https://youtu.be/T5bOgE7dzwk)

## **📝 프로젝트 후기**
* 예정 
---
## 🛠 **테크 스택**

### **Backend**
* Python ```3.7```
* Django ```3.2```
* MYSQL ```5.7```

### **DevOps**
* AWS EC2
* AWS RDS

## **👩‍👩‍👧‍👦 협업 도구**

* Slack
* Github
* Trello

---
# **🚀 구현 기능**
## **상품 리스트 조회 API**
---
### 상품 리스트 조회 API

- 쿼리 파라미터값에 어떤 값을 넣어 주어도 500에러가 나지 않게 했습니다.

과정 기록 블로그 링크:[https://kingofsiliconvalley.tistory.com/26](https://kingofsiliconvalley.tistory.com/26)

- 기존에 4개의 분기가 있던 코드에서 테스트 코드를 짜기 쉽고 디버깅에 용이하기 위해서 분기를 1개로 줄였습니다.

과정 기록 블로그 링크: [https://kingofsiliconvalley.tistory.com/27](https://kingofsiliconvalley.tistory.com/27)

- 데이터가 100만개가 넘어가면 정렬 기능과 페이징 기능의 쿼리 호출시간이 4초이상 걸렸던 쿼리문을 0.1초로 줄였습니다.

과정 기록 블로그 링크: [https://kingofsiliconvalley.tistory.com/47](https://kingofsiliconvalley.tistory.com/47)

---

### 상품 상세 페이지 조회 API

- 장고 ORM selected_related와 prefetch_related를 사용해서 N+1문제를 해결했습니다.

- 로그인한 유저와 하지 않은 유저에 대한 조회API 엔드포인트를 나누었습니다.

## Reference

- 이 프로젝트는 [라인프렌즈샵](https://brand.naver.com/linefriends/?nt_source=emnet_google_sa&nt_medium=search&nt_detail=store&nt_keyword=%EB%9D%BC%EC%9D%B8%EC%8A%A4%ED%86%A0%EC%96%B4&gclid=CjwKCAjw4KyJBhAbEiwAaAQbE93SzYQM2APropv_Ed2sO5bOHfEYnNEbiFW2_WzL52GNw2gXiBwVtBoCZIQQAvD_BwE) 사이트를 참조하여 학습목적으로 만들었습니다
- 학습수준의 프로젝트로 만들었기 때문에 이 코드 및 데모영상을 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.