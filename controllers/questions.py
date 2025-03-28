from models.questions import Question

from models import db
from schemas.questions import QuestionCreate, QuestionResponse


def get_all_questions() -> list[dict[str, int | str]]:
    questions = Question.query.all()

    questions_data = [
        QuestionResponse.model_validate(question).model_dump()
        for question in questions
    ]

    return questions_data


def get_question_by_id(id_: int) -> Question | None:
    question = Question.query.get(id_)

    return question


def create_new_question(raw_data: dict[str, str]) -> Question:
    validated_obj = QuestionCreate.model_validate(raw_data)

    new_obj = Question(text=validated_obj.text)

    db.session.add(new_obj)
    db.session.commit()

    return new_obj


def update_question(entity: Question, row_data: dict[str, str]) -> Question:
    entity.text = row_data["text"]
    db.session.commit()
    return entity
