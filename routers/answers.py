from flask import Blueprint


answers_bp = Blueprint('answers', __name__)


@answers_bp.route('', methods=["POST"])
def create_new_answer():
    return "CREATE NEW ANSWER"


@answers_bp.route('<int:id>', methods=['GET'])
def retrieve_answer(id):
    return f'Ответ на запрос по id {id}'
