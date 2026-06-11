from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    data = db.get_all_students()
    return jsonify(data),200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.json

    if student_data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", None)

    if name is None or course is None:
        return jsonify({"error": "Missing name or course"}), 400

    if mark is not None:
        try:
            mark = int(mark)
        except (ValueError, TypeError):
            return jsonify({"error": "Mark must be an integer"}), 400

    new_student = db.insert_student(name, course, mark)

    return jsonify(new_student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.get_json()

    if student_data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if name is not None and (not isinstance(name, str) or not name.strip()):
        return jsonify({"error": "Name must be a non-empty string"}), 400

    if course is not None and (not isinstance(course, str) or not course.strip()):
        return jsonify({"error": "Course must be a non-empty string"}), 400

    if mark is not None:
        if not isinstance(mark, int):
            return jsonify({"error": "Mark must be an integer"}), 400

        if mark < 0 or mark > 100:
            return jsonify({"error": "Mark must be between 0 and 100"}), 400

    updated_student = db.update_student(
        student_id,
        name=name.strip() if isinstance(name, str) else None,
        course=course.strip() if isinstance(course, str) else None,
        mark=mark
    )

    if updated_student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted_student = db.delete_student(student_id)

    if deleted_student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(deleted_student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()

    marks = [
        student["mark"]
        for student in students
        if isinstance(student.get("mark"), int)
    ]

    if not marks:
        return jsonify({
            "count": 0,
            "average": 0,
            "min": None,
            "max": None
        }), 200

    return jsonify({
        "count": len(marks),
        "average": round(sum(marks) / len(marks), 2),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
