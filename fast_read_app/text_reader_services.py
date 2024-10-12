from .models import Text, Block, Quetions, Answer

def get_text_words_count(text: Text) -> int:
    blocks = get_text_blocks(text)
    text : str = ""
    for block in blocks:
        text += block.text
    return len(text.split())

def get_random_text() -> Text:
    return Text.objects.order_by('?').first()

def get_text_blocks(text: Text) -> list[Block]:
    return text.blocks.all()

def get_block_questions(block: Block) -> list[Quetions]:
    return block.tests.all()

def get_text_read_speed(text: str, time: float) -> float:
    text = text.split(' ')
    words = len(text)
    speed = words / time
    return speed


def get_correct_answers_count(text_id, answers: dict[str, list[int]]):
    print(answers)
    correct_answers = 0
    text = Text.objects.get(id=text_id)
    blocks = get_text_blocks(text)
    count = 0
    
    for block in blocks:
        questions = get_block_questions(block)
        count += len(questions)
        for question in questions:
            question_id = str(question.id)
            question_answers = answers[question_id]
            correct_answers += 1
            for answer in question_answers:
                if not Answer.objects.get(id=answer).is_valid:
                    correct_answers -= 1
                    break
              
    return correct_answers, count, 100 / count * correct_answers