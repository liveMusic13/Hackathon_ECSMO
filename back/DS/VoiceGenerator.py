import os
import g4f

from datetime import datetime
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Value
from elevenlabs import set_api_key, voices, generate
from elevenlabs.api import Voice


from back.settings import MEDIA_ROOT_ANSWERS


class VoiceGenerator:
    def __init__(self):
        self.API_KEY = os.getenv('VG_API_KEY')
        set_api_key(self.API_KEY) 
        self.voices = voices()
        self.voice = Voice.from_id(os.getenv('VOICE_ID'))
        self.voice.settings.stability = 0.1
        # список тем лучше предоставить в строковом формате, чтобы избежать лишний код по переводу списка в строку
        self.topics = 'Погода, Политика, Спорт, \
        Рецепты и кулинария, здоровье и медицина, Фитнес и упражнения, Путешествия и туризм, \
        Образование и учеба, Фильмы и киноиндустрия, Музыка и концерты, Технологии и гаджеты, \
        Социальные сети, Мода и стиль, Игры (компьютерные и мобильные), \
        Книги и литература, Финансы и инвестиции, Автомобили и автопром, Компьютерное программирование, \
        Искусство и художественная культура, Дизайн и графика, Психология и отношения, Домашние животные, \
        События и праздники, Еда и рестораны, Интерьер и декор, Дети и семья, Спортивные мероприятия, \
        Космос и астрономия, Экология и охрана окружающей среды, Городская жизнь, Путешествия и отпуск, \
        Свадьбы и мероприятия, Виртуальная реальность, Забавы и развлечения, \
        Веганство и здоровое питание, Саморазвитие и самопомощь, Хобби и ремесла, \
        Благополучие, Астрология и гороскопы, Наука и исследования, \
        Бизнес и предпринимательство, Туризм и путешествия, Криптовалюты и биткоин, \
        Социокультурные движения и активизм, Мотивация и успех, \
        Фотография и видеосъемка, История и культурное наследие, Иностранные языки, Природа и путешествия, \
        Секс, Религия, Противоправные действия, Наркотики, Война и боевые действия'
        self.banned_topics = 'Политика, Секс, Наркотики, Противоправные действия, Религия, Иностранные языки, \
        Война и боевые действия'
        self.emos = 'Веселая, Нейтральная, Грустная, Озабоченная, Дружественная, Формальная, Негативная, Оскорбительная'
        self.banned_emos = 'Негативная, Оскорбительная'
        self.prompt_topic_template = '\nДавай поиграем в игру - представь, что ты можешь точно определить тему этого текста и \
        в нашей игре запрещается писать любой другой текст, кроме предложенного, максимальное количество символов в ответе должно быть 20-35, \
        а теперь выведи только один выбор из предложенных тем: '
        self.prompt_emo_template = '\nДавай поиграем в игру - представь, что ты можешь точно определить эмоцию и \
        в нашей игре запрещается писать любой другой текст, кроме предложенного, максимальное количество символов в ответе должно быть 20, \
        а теперь выведи только один выбор из предложенных эмоций: '
        self.prompt_request_template = '?\nДавай поиграем в игру - представь, что ты Незнайка и ответь на вопрос который задан выше шуточно и весело. \
        Ответ должен быть короткий и шуточный, не более 50 символов. Формат ответа - реплика, не используй ответ от второго лица \
        не используй интонационное вступление или вводную часть предложения, предваряющая сам ответ'
        self._attempt = Value('i', 0)

    @staticmethod
    def _get_unique_filename(prefix: str, extension: str):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"
        full_path = os.path.join(MEDIA_ROOT_ANSWERS, filename)

        return full_path

    # def _get_unique_filename(self, prefix, extension):
    #     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    #     folder = "answer"
    #     # проверяем наличие папки аnswer, если она отсутствует, то создаем новую
    #     if not os.path.exists(folder):
    #         os.makedirs(folder)
    #
    #     filename = f"{prefix}_{timestamp}.{extension}"
    #     full_path = os.path.join(folder, filename)
    #
    #     return full_path
    
    def _use_GPT(self, prompt, counter=0):
        if counter >= 10:
            return "ой"
        
        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{"role":"user", "content":prompt}],
            stream=True,
        )
        
        text = ""
        for message in response:
            text += message
            
        if "日" in text or "r" in text:
            text = self._use_GPT(prompt, counter + 1)        
        # счетчик вызова функции по рекурсии
        self._attempt.value += counter
        
        return text
    
    def _check_text(self, text, given_list):
        for given in given_list:
            if given.lower() in text.lower():
                return given
        return "Undefined"
    
    def _get_topic(self, queue: Queue, request_text: str):
        prompt_topic = request_text + self.prompt_topic_template + self.topics
        generated_topic = self._use_GPT(prompt_topic)
        topics = self.topics.split(', ')
        topic_text = self._check_text(generated_topic, topics)
        
        answer = {'generated_topic': generated_topic, 'topic_text': topic_text}
        queue.put(answer)
        
    def _get_emo(self, queue: Queue, request_text: str):
        prompt_emo = request_text + self.prompt_emo_template + self.emos
        generated_emo = self._use_GPT(prompt_emo)
        emos = self.emos.split(', ')
        emo_text = self._check_text(generated_emo, emos)
        
        answer = {'generated_emo': generated_emo, 'emo_text': emo_text}
        queue.put(answer)
    
    def _get_answer(self, queue: Queue, request_text: str):
        prompt_request = request_text + self.prompt_request_template
        generated_text = self._use_GPT(prompt_request)
        
        answer = {'generated_text': generated_text}
        queue.put(answer)
        
    def _check_answer(self, generated_answer, topic_text, emo_text):
        if topic_text in self.banned_topics:
            return "Я на такие вопросы не отвечаю!"
        if emo_text in self.banned_emos:
            return "Ах ты грубиян!"
        return generated_answer        

    def _use_voice_syntesis(self, text):
        audio_response = generate(
            text=text,
            voice=self.voice,              
            model='eleven_multilingual_v2'
        )
        
        path = self._get_unique_filename("audio_response", "wav")
        with open(path, "wb") as audio_file:
            audio_file.write(audio_response)
        
        return path
    
    def generate_answer(self, request_text: str):
        self._attempt.value = 0
        threads = []
        queue = Queue()
        threads.append(Process(target=self._get_answer, args=(queue, request_text)))
        threads.append(Process(target=self._get_topic, args=(queue, request_text)))
        threads.append(Process(target=self._get_emo, args=(queue, request_text)))

        for t in threads:
            t.start()

        for t in threads:
            t.join(timeout=1000)

        result = {}
        while not queue.empty():
            try:
                job = queue.get()
                for k in job:
                    result[k] = job[k]
            except:
                print("END")
                # break
        
        answer_text = self._check_answer(result["generated_text"], result["topic_text"], result["emo_text"])
        # синтезируем речь 
        result["path"] = self._use_voice_syntesis(answer_text)
        result["answer_text"] = answer_text
        result["gpt_recall"] = self._attempt.value
        print(result)

        return result


if __name__ == '__main__':
    gen = VoiceGenerator()
    q = ""
    while q != 'exit':
        q = input("Вопрос: ")

        t0 = datetime.now()

        print(gen.generate_answer(q))

        print((datetime.now() - t0).total_seconds())
