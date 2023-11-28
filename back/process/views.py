from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import get_object_or_404
from django.http import (
    JsonResponse,
    FileResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseBase,
    HttpRequest,
)

from .models import Question, Answer
from DS.VoiceGenerator import VoiceGenerator


generator = VoiceGenerator()


def create_response(output_json: dict, pk: int) -> HttpResponseBase:
    try:
        topic = output_json['generated_topic']
        emotion = output_json['emo_text']
        full_path = output_json['path']
        filename = full_path.split(sep='/')[-1]
        ans_text = output_json['answer_text']
    except KeyError as e:
        return HttpResponseServerError('Invalid or missing JSON key: %s' % e)

    quest = get_object_or_404(
        klass=Question,
        id=pk,
    )
    Answer.objects.create(
        audio_full_path=full_path,
        topic=topic,
        emotion=emotion,
        text=ans_text,
        question=quest,
    )

    response = FileResponse(
        open(
            file=full_path,
            mode='rb',
        ),
        filename=filename,
    )
    response['Content-Disposition'] = 'attachment; filename=' + filename

    return response


@csrf_exempt
def question(request: HttpRequest) -> HttpResponseBase:
    if request.method == 'GET':
        return JsonResponse(
            status=200,
            data={
                'status': 200,
                'message': 'Hello!',
            },
        )
    if request.method == 'POST':
        try:
            text = request.POST['text']
            name_id = request.POST['name']
        except KeyError as e:
            return HttpResponseServerError('Invalid or missing field: %s' % e)

        new_question = Question.objects.create(
            audio_name_id=name_id,
            text=text,
        )
        new_question_id = new_question.pk

        result = generator.generate_answer(request_text=text)

        response = create_response(
            output_json=result,
            pk=new_question_id,
        )
        return response

    return HttpResponseBadRequest()


def answer_text(request: HttpRequest, answer_id: str) -> HttpResponseBase:
    if request.method == 'GET':
        try:
            quest = get_object_or_404(
                klass=Question,
                audio_name_id=answer_id,
            )
            ans = get_object_or_404(
                klass=Answer,
                question=quest,
            )
        except MultipleObjectsReturned as e:
            return HttpResponseServerError(e)

        if ans:
            data = {
                'filename': answer_id + '.wav',
                'text': ans.text,
            }
            return JsonResponse(
                status=200,
                data=data,
                safe=False,
            )

    return HttpResponseBadRequest()
