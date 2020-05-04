from ..services.QuestionService import QuestionService


def test_get_questions():
    question_service = QuestionService()
    questions = question_service.get_questions()
    assert len(questions) > 0
    assert questions[0]['product_id'] is not None


def test_answer_question():
    question_service = QuestionService()
    did_it_work = question_service.answer_question(product_id="MLB1353146627", question="Qual a cor?",
                                                   answer="Olá, A cafeteira é cinza")
    assert did_it_work
