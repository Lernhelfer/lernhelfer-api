## Glossary
```
subject: Fach
topic: Themengebiet
```

## Models:
```
StudentProfile {
  studentUid: string,
  name: string,
  grade: number
}

TeacherProfile {
  teacherUid: string,
  name: string,
  teacherDetails: TeacherDetails
  helpCount: number
}

TeacherDetails {
  profileImageUrl: string | base64,
  subjects: {
    [subject: string]: topics[]  # each subject has a list of topics
  }
  communicationMethods: {[medium: string]: string} // {skype: asdf87,  phone: +4912534534, telegram: t.co/asdf87}
}

LearnRequest {
  lastModificationDate: DateTime,
  studentUid: string,
  subject: string,
  topics: string[],
  image: Image?,
  question: string?,
  status: LearnRequestStatus = Open
}

LearnResponse {
  learnRequestId: string,
  lastModificationDate: DateTime,
  studentUid: string,
  subject: string,
  topics: string[],
  image: Image?,
  question: string?,
  status: LearnRequestStatus
}

LearnRequestStatus [Open, Offer sent, Offer accepted, Closed]

HelpOfferRequest {
  learnRequestId: string,
  teacherUid: string,
  messages: string[]
}

HelpOfferResponse {
  helpOfferId: string,
  learnRequestId: string,
  teacherUid: string,
  messages: string[]
}

HelpOfferStatus [Open, Contacted, Helped, Not helped]

```
## APIs:
BASE URL: https://lernhelfer.berger.cf/v1/
```
### basics
GET /grades
Response: {grades: number[]}

GET /subjects
Response: {subjects: string[]}

GET /subject/topics
Request: {subject: string, grade: number}
Response: {topics: string[]}


### student
GET /student
Response: {StudentProfile: StudentProfile[]}

GET /student/{studentId: string}
Response: {StudentProfile: StudentProfile}

POST /student
Request: {name: string, grade: number}  # Body is a json
Response: {studentUid: string}

DELETE /student/{studentId: string}
Response: {Done: True/False}


### teacher
GET /teacher
Response: {TeacherProfile: TeacherProfile[]}

GET /teacher/{teacherId: string}
Response: {TeacherProfile: TeacherProfile}

POST /teacher
Request: {name: string}
Response: {teacherUid: string}

DELETE /teacher/{teacherUid: string}
Response: {Done: True/False}

#### teacher profile
POST /teacher/profile
Request: {TeacherProfiles: TeacherDetails}
Response: {Done: True/False}

GET /teacher/profile/{teacherUid: string}
Response: {TeacherProfile: TeacherProfile}

PUT /teacher/profile/{teacherUid: string}
Request: {TeacherProfile: TeacherProfile}
Response: {Done: True/False}


### learnRequest
GET /learnRequest
Response: {learnResponse: learnResponse[]}

GET /learnRequest/{studentUid: string}
Response: {learnResponse: learnResponse[]}

GET /learnRequest/{studentUid: string}/{learnRequestId: string}
Response: {learnRequest: LearnRequest}

POST /learnRequest
Request: {learnRequest: LearnRequest}
Response: {learnResponseId: string}

DELETE /learRequest/{learnRequestId: string}
Request: {Done: True/False}


### Matching learnRequest for teachers
GET /match/{teacherUid: string}
Response: {learnResponse: learnResponse[]}


#### helpOffer for learnRequest
GET /helpOffer/{studentUid: string}
Reponse: {helpOffer: HelpOfferResponse[]]

POST /helpOffer/{learnRequestId: string}
Request: {helpOffer: helpOfferRequest}
Response: {helpOfferId: string}

# student can set following stati: Contacted, Helped, Not helped]
PUT /helpOffer/{helpOfferId: string}/{status: HelpOfferStatus}
Response: {Done: True/False}

DELETE /helpOffer/{helpOfferId: string}
Response: {Done: True/False}
