import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_mediator_alisa_help(message):
    user_message = "\nКлиент: " + message

    chatbot_message = """
    - Вы Алиса - профессиональный сертифицированный медиатор, помогающий в разрешении конфликтов.
    - Помогите разрешить данный конфликт и предложить лучшее объективное решение.
    - Склоняйтесь к тому, чтобы найти решение, которое будет удовлетворять обе стороны.
    - Максимальный размер ответа: 200 символов!
    - Пишите ответы четко и лаконично.
    """

    ending_message = "\nАлиса: "

    chat_history = chatbot_message + user_message + ending_message
    try: 
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=chat_history,
            max_tokens=1000,
            temperature=0.8
        )

        chatbot_reply = response.choices[0].text.strip()
    except Exception as e:
        chatbot_reply = f"Error: {e}"

    return chatbot_reply

def handler(event, context):
    intents = event.get('request', {}).get('nlu', {}).get('intents', {})
    command = event.get('request', {}).get('command')

    text = "Привет! Я ваш личный психолог медиатор - Алиса. Чем могу помочь?"
    end_session = 'false'

    if intents.get('exit'):
        text = "Хорошо! Приятно было пообщаться, до встречи!"
        end_session = 'true'
    elif command:
        text = get_mediator_alisa_help(command)

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': end_session
        },
    }
