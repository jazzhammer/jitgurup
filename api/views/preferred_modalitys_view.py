from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from api.models.learning_modality import LearningModality
from api.models.person import Person
from api.models.preferred_modality import PreferredModality
from api.models.topic import Topic


@api_view(["POST", "GET", "PUT", "DELETE"])
def preferred_modalitys(request: HttpRequest):
    if request.method == 'POST':
        person_id = request.data.get('person_id')
        if person_id:
            person = Person.objects.get(pk=person_id)
            topic_id = request.data.get('topic_id')
            if topic_id:
                topic = Topic.objects.get(pk=topic_id)
                learning_modailty_id = request.data.get('learning_modality_id')
                if learning_modailty_id:
                    learning_modality = LearningModality.objects.get(pk=learning_modailty_id)
                    if person and topic and learning_modality:
                        created = PreferredModality.objects.create(person=person, topic=topic, learning_modality=learning_modality)
                        created_dict = model_to_dict(created)
                        created_dict['person_id'] = created_dict['person']
                        created_dict['learning_modality_id'] = created_dict['learning_modality']
                        created_dict['topic_id'] = created_dict['topic']
                        created_dict['person'] = model_to_dict(person)
                        created_dict['learning_modality'] = model_to_dict(learning_modality)
                        topic_dict = model_to_dict(topic)
                        topic_dict['subject_id'] = topic_dict['subject']
                        topic_dict['subject'] = model_to_dict(topic.subject)
                        created_dict['topic'] = topic_dict
                        return JsonResponse(created_dict, status=201, safe=False)
                    else:
                        return JsonResponse(
                            {"message": f"require person, topic, learning_modality for preferred_modality. found {person_id=}, {topic_id=}, {learning_modailty_id=}"},
                            status=400,
                            safe=False
                        )
                else:
                    return JsonResponse({"message": f"require learning_modality for preferred_modality. found {learning_modailty_id=}"},status=400, safe=False)
            else:
                return JsonResponse({"message": f"require topic for preferred_modality. found {topic_id=}"}, status=400, safe=False)
        else:
            return JsonResponse({"message": f"require person for preferred_modality. found {person_id=}"}, status=400, safe=False)

    if request.method == 'GET':
        id = request.data.get('id')
        topic_id = request.data.get('topic_id')
        person_id = request.data.get('person_id')
        learning_modality_id = request.data.get('learning_modality_id')

        if id:
            try:
                found = PreferredModality.objects.get(pk=id)
            except:
                return JsonResponse({
                    'error': f"no preferred_modality found for {id=}"
                }, status=404, safe=False)
            return JsonResponse([model_to_dict(found)], status=200, safe=False)

        filtered = False
        founds = PreferredModality.objects.filter(deleted=False)
        if topic_id:
            filtered = True
            founds = founds.filter(topic_id=topic_id)
        if person_id:
            filtered = True
            founds = founds.filter(person_id=person_id)
        if filtered:
            return JsonResponse([model_to_dict(found) for found in founds], status=200, safe=False)
        else:
            return JsonResponse({"message": f"require topic | person to retrieve preferred_modality found: {person_id=}, {topic_id=}"}, status=400, safe=False)

    if request.method == 'PUT':
        id = request.data.get('id')
        person_id = request.data.get('person_id')
        topic_id = request.data.get('topic_id')
        learning_modality_id = request.data.get('learning_modality_id')

        found = None
        if id:
            try:
                found = PreferredModality.objects.get(pk=id)
            except:
                return JsonResponse({
                    'error': f"no preferred_modality found for {id=}"
                }, status=404, safe=False)
        if person_id:
            found.person = Person.objects.get(pk=person_id)
        if topic_id:
            found.topic = Topic.objects.get(pk=topic_id)
        if learning_modality_id:
            found.learning_modality = LearningModality.objects.get(pk=learning_modality_id)
        found.save()
        return JsonResponse(model_to_dict(found), status=200, safe=False)

    if request.method == 'DELETE':
        id: str = request.GET.get('id')
        if id and len(id.strip()) > 0:
            found = PreferredModality.objects.get(pk=id)
            found.delete()
            return JsonResponse({"message": f"success"}, status=200, safe=False)
        else:
            return JsonResponse({
                "error": f"unable to update preferred_modality for {id=}"
            }, status=400, safe=False)