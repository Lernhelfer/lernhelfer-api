import os
from flask import Flask, request
from flask_restful import Resource, Api, abort
from learnsupport_service import LearnSupportService

app = Flask(__name__)
api = Api(app)

# grades
class Grades(Resource):
    def get(self):
        try:
            results = service.get_grades()
            if results:
                return results
        except Exception as e:
            abort(500, message=e)
        abort(404, message="Database contains no grades.")

# subjects
class Subjects(Resource):
    def get(self):
        try:
            results = service.get_subjects()
            if results:
                return results
        except Exception as e:
            abort(500, message=e)
        abort(404, message="Database contains no subjects.")

# topics
class Topics(Resource):
    def get(self):
        body = request.get_json()
        if not body:
            abort(400, message="Subject or grade is not valid.")
        try:
            results = service.get_topics(body["subjectName"], body["grade"])
            if results:
                return results
        except Exception as e:
            abort(500, message=e)
        abort(404, message="Database contains no topics.")


# student
class Student(Resource):
    def get(self, student_uid):
        if not student_uid:
            abort(400, message="Parameter student_uid is empty.")
        else:
            try:
                results = service.get_student(student_uid)
                if results:
                    return results
            except Exception as e:
                abort(500, message=e)
            abort(404, message="Parameter student_uid does not exist.")

    def delete(self, student_uid):
        if not student_uid:
            abort(400, message="Parameter student_uid is empty.")
        else:
            try:
                service.delete_student(student_uid)
            except Exception as e:
                abort(500, message=e)

class Students(Resource):
    def get(self):
        try:
            results = service.get_students()
            if results:
                return results
        except Exception as e:
            abort(500, message=e)
        abort(404, message="No student exists.")

    def post(self):
        new_user = request.get_json()
        if not new_user:
            abort(400, message="Student is not valid.")
        try:
            student_uid = service.post_students(new_user['name'], new_user['class'])
            return {"student_uid": str(student_uid)}
        except Exception as e:
            abort(500, message=e)

# teachers
class Teacher(Resource):
    def get(self, teacher_uid):
        if not teacher_uid:
            abort(400, message="Parameter teacher_uid is empty.")
        else:
            try:
                results = service.get_teacher(teacher_uid)
                if results:
                    return results
            except Exception as e:
                abort(500, message=e)
            abort(404, message="Parameter teacher_uid does not exist.")

    def delete(self, teacher_uid):
        if not teacher_uid:
            abort(400, message="Parameter teacher_uid is empty.")
        else:
            try:
                service.delete_teacher(teacher_uid)
            except Exception as e:
                abort(500, message=e)

class Teachers(Resource):
    def get(self):
        try:
            results = service.get_teachers()
            if results:
                return results
        except Exception as e:
            abort(500, message=e)
        abort(404, message="No teacher exists.")

    def post(self):
        new_user = request.get_json()
        if not new_user:
            abort(400, message="Teacher is not valid.")
        try:
            teacher_uid = service.post_teachers(new_user['name'])
            return {"teacher_uid": str(teacher_uid)}
        except Exception as e:
            abort(500, message=e)


class Teacher_Profile(Resource):
    def post(self):
        teacher_profile = request.get_json()
        if not teacher_profile:
            abort(400, message="Teacher is not valid.")
        try:
            service.post_teacher_profile(teacher_profile)
            return True
        except Exception as e:
            abort(500, message=e)

class Teacher_Profiles(Resource):
    def get(self, teacher_uid):
        if not teacher_uid:
            abort(400, message="Parameter teacher_uid is empty.")
        else:
            try:
                result = service.get_teacher_profile(teacher_uid)
                if result:
                    return result
            except Exception as e:
                abort(500, message=e)
            abort(404, message="Parameter teacher_uid does not exist.")

    def put(self, teacher_uid):
        if not teacher_uid:  # TODO: ID not necessary?
            abort(400, message="Parameter teacher_uid is empty.")
        else:
            teacher_profile = request.get_json()
            if not teacher_profile:
                abort(400, message="Teacher is not valid.")
            if teacher_uid != teacher_profile['teacherUid']:
                abort(400, message="TeacherUid is not valid.")
            try:
                service.post_teacher_profile(teacher_profile)
                return True
            except Exception as e:
                abort(500, message=e)


# add URLs
version = "v1"

# basics
api.add_resource(Grades, f'/{version}/grades')
api.add_resource(Subjects, f'/{version}/subjects')
api.add_resource(Topics, f'/{version}/subject/topics')

# students
api.add_resource(Student, f'/{version}/student/<student_uid>')
api.add_resource(Students, f'/{version}/student')

# teachers
api.add_resource(Teacher, f'/{version}/teacher/<teacher_uid>')
api.add_resource(Teachers, f'/{version}/teacher')

# teacher details
api.add_resource(Teacher_Profile, f'/{version}//teacher/profile')
api.add_resource(Teacher_Profiles, f'/{version}/teacher/profile/<teacher_uid>')

@app.route('/')
def get_version():
    return f"LernserviceSupport: {version}"


if __name__ == '__main__':
    try:
        service = LearnSupportService()
    except Exception as e:
        print(e)
    debug = False
    if "DEBUG_LOCAL" in os.environ.keys():
        debug = True
    app.run(debug=debug, host='0.0.0.0')
