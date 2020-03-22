import os
from flask import Flask, request
from flask_restful import Resource, Api, abort
from learnsupport_service import LearnSupportService

app = Flask(__name__)
api = Api(app)


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
    # TODO: leere DB gibt 500
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

class Teacher_Profiles(Resource):
    def get(self, teacher_uid):
        if not teacher_uid:
            abort(400, message="Parameter teacher_uid is empty.")
        else:
            try:
                results = service.get_teacher_profile(teacher_uid)
                if results:
                    return results
            except Exception as e:
                abort(500, message=e)
            abort(404, message="Parameter teacher_uid does not exist.")

    def post(self, teacher_uid):
        new_details = request.get_json()
        if not new_details:
            abort(400, message="Teacher is not valid.")
        try:
            service.post_teacher_details(teacher_uid, new_details['order_number'], new_details['contact_type'], new_details['contact_reach'])
            return True
        except Exception as e:
            abort(500, message=e)
# add URLs
version = "v1"

# students
api.add_resource(Student, f'/{version}/student/<student_uid>')
api.add_resource(Students, f'/{version}/student')

# teachers
api.add_resource(Teacher, f'/{version}/teacher/<teacher_uid>')
api.add_resource(Teachers, f'/{version}/teacher')

# details #TODO: passt das so mit der URL?
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
