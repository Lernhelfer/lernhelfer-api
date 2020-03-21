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
                if not results:
                    abort(404, message="Parameter student_uid does not exist.")
                return results
            except Exception as e:
                abort(500, message=e)

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
            if not results:
                abort(404, message="No student exists.")
            return results
        except Exception as e:
            abort(500, message=e)

    def post(self):
        new_user = request.get_json()
        if not new_user:
            abort(400, message="Student is not valid.")
        try:
            student_uid = service.post_students(new_user['name'], new_user['class'])
            return {"student_uid": str(student_uid)}
        except Exception as e:
            abort(500, message=e)


# add URLs
version = "v1"
api.add_resource(Student, f'/{version}/student/<student_uid>')
api.add_resource(Students, f'/{version}/student')


@app.route('/')
def get_version():
    return f"LernserviceSupport: {version}"


if __name__ == '__main__':
    service = LearnSupportService()
    app.run(debug=True, host='0.0.0.0')
