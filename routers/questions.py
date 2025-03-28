from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError

from controllers.questions import (
    get_all_questions,
    create_new_question, get_question_by_id, update_question
)
from schemas.questions import QuestionResponse

questions_bp = Blueprint(name="questions", import_name=__name__)


# @questions_bp.route('', methods=["GET"])
# def get_all_questions():
#     return "ALL QUESTIONS"
#
# @questions_bp.route('', methods=["POST"])
# def create_question():
#     return "CREATE QUESTION"
#
#
# @questions_bp.route('/<int:id>', methods=["GET"])
# def get_question_by_id(id: int):
#     return f"QUESTION - {id}"
#
#
# @questions_bp.route('/<int:id>', methods=["PUT"])
# def update_question(id: int):
#     return f"QUESTION UPDATE BY ID - {id}"
#
#
# @questions_bp.route('/<int:id>', methods=["DELETE"])
# def delete_question(id: int):
#     return f"QUESTION DELETE BY ID - {id}"


@questions_bp.route('', methods=["GET", "POST"])
def questions_list() -> Response | tuple[Response, int]:
    if request.method == "GET":
        questions = get_all_questions()

        return jsonify(questions)

    else:
        data = request.json

        try:
            new_question = create_new_question(raw_data=data)
        except ValidationError as err:
            return jsonify(err.errors()), 400
        return jsonify(
            QuestionResponse(
                id=new_question.id,
                text=new_question.text
            ).model_dump()
        ), 201  # CREATED


# request.args => { "agree_count": True }
# http://127.0.0.1:5000/questions/?agree_count=ture
# Questions.query.order_by(desc(agree_count)).all()

@questions_bp.route('/<int:id>', methods=["GET", "PUT", "DELETE"])
def retrieve_question(id: int):
    if request.method == "GET":
        question = get_question_by_id(id_=id)

        if question:
            return jsonify(
                {
                    "id": question.id,
                    "text": question.text
                }
            ), 200
        else:
            return jsonify(
                {}
            ), 204

    if request.method == "PUT":
        question = get_question_by_id(id_=id)

        if not question:
            return jsonify(
                {}
            ), 204

        data = request.get_json()

        if "text" not in data:
            return jsonify(
                {
                    "error": "Question was not provided."
                }
            ), 400

        updated_obj = update_question(entity=question, row_data=data)

        return jsonify(
            {
                "id": updated_obj.id,
                "text": updated_obj.text
            }
        ), 200

    if request.method == "DELETE":
        return f"QUESTION DELETE BY ID - {id}"
