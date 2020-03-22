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
  teacherDetails: TeacherDetails
  helpCount: number
}

TeacherDetails {
  name: string,
  profileImageUrl: string | base64,
  subjects: {
    [subject: string]: number[] // grades
  }
  communicationMethods: {[medium: string]: string} // {skype: asdf87,  phone: +4912534534, telegram: t.co/asdf87}
}

LearnRequest {
  learnRequestId: string,
  lastModificationDate: DateTime,
  studentUid: string,
  subject: string,
  topics: string[],
  image: Image?,
  question: string?,
  status: LearnRequestStatus = Open,
  messages: {}
}

LearnRequestStatus [Open, Offer sent, Offer accepted, Closed]

HelpOffer {
  helpOfferId: string,
  teacherUid: string,
  messages: string[]
}

HelpOfferStatus [Open, Contacted, Helped, Not helped]

```
## APIs:
```
### /
GET grades
Response: {grades: number[]}

GET subjects
Response: {subjects: string[]}

GET subject/topics
Request: {subject: string, grade: number}
Response: {topics: string[]}


### student/profile
POST
Request: {name: string, grade: number}
Response: {studentUid: string}


### /learnRequest/
POST
Request: {learnRequest: LearnRequest}
Response: {}

GET
Request: {studentUid: string, learnRequestId: string}
Response: {learnRequest: LearnRequest}

Request: {studentUid: string}
Response: {learnRequests: LearnRequest[]}

// FOR DEBUGGING | MAY BE DELETED IN FUTURE
Request: {teacherUid: string}
Reponse: {learnRequests: LearnRequest[]}


DELETE
Request: {studentUid: string, learnRequestId: string}

#### /learnRequest/{learnRequestId}/helpOffer
GET
Response {helpOffer: HelpOffer[], teacher: TeacherProfile}

POST
Request: {teacherUid: string}
Response: {helpOfferId: string} 

##### /learnRequest/{learnRequestId}/helpOffer/{status: HelpOfferStatus}
PUT


### teacher/profile
POST
Request: {teacherDetails: TeacherDetails}
Response: {teacherUid: number}

#### teacher/profile/{teacherId: string}
GET
Response: {teacherProfile: TeacherProfile}




