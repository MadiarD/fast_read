from django.http import HttpRequest, JsonResponse

from .models import ClientResult, Text, WhatsappMessage
from .whatsapp_services import send_whatsapp_message
from .text_reader_services import (get_block_questions,
                                   get_correct_answers_count, get_random_text,
                                   get_text_blocks, get_text_read_speed)




def read_request_handler(
    id : int, 
    text: str, 
    tel_number: str,
    time: float, 
    answers: dict[str, list[int]]
    ) -> JsonResponse:
    try: 
        speed = get_text_read_speed(text, time)
        correct_answers, count, percent = get_correct_answers_count(id, answers)
        text = Text.objects.get(id=id) 
    
        ClientResult.objects.create(
            text=text,
            speed=speed,
            correct_answers=correct_answers,
            count=count,
            percent=percent,
            tel_number=tel_number,
            send_message=False,
        )

        wh = WhatsappMessage.objects.filter().first()
        if(wh.is_default):
            message = f"""
            Скорость чтения: {speed}
            Количество правильных ответов: {correct_answers}
            Процент правильных ответов: {percent}

            """
            print(message)
        else:
            message = wh.text

        send_whatsapp_message(tel_number, message)

        return JsonResponse({'success': True})
    except Exception as e:
        print("error"+ str(e))
        return JsonResponse({'error': str(e)})


def get_text_and_quetions(request) -> JsonResponse:
    text = get_random_text()
    blocks = get_text_blocks(text)
    id = text.id
    texts:str = ""
    questions = []
    for block in blocks:
        texts += block.text
        block_questions = get_block_questions(block)
        for question in block_questions:
            questions.append({
                'id': question.id,
                'question': question.quetion,
                'answers': [{'id': answer.id, 'answer': answer.answer_text} for answer in question.answers.all()]
            })

    return JsonResponse({'id': id,'text': texts , 'questions': questions})