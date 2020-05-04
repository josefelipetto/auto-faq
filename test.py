from services.FAQService import FAQService

faq = FAQService("resources/models/faq-MLB1353146627.csv")

faq.get_questions_with_answers()