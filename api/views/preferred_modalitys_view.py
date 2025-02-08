from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from api.models.learning_modality import LearningModality
from api.models.person import Person
from api.models.preferred_modality import PreferredModality
from api.models.subject import Subject
from api.models.topic import Topic
from api.models.user_person import UserPerson


@api_view(["POST", "GET", "PUT", "DELETE"])
def preferred_modalitys(request: HttpRequest):
    if request.method == 'POST':
        learning_modality = None
        person_id = request.data.get('person_id')
        if not person_id:
            user_id = request.data.get('user_id')
            if user_id:
                user = User.objects.get(pk=user_id)
                user_person = UserPerson.objects.get(user_id=user.id)
                if user_person:
                    person_id = user_person.person_id
        if person_id:
            person = Person.objects.get(pk=person_id)
            topic_id = request.data.get('topic_id')
            if topic_id:
                topic = Topic.objects.get(pk=topic_id)
                learning_modailty_id = request.data.get('learning_modality_id')
                if learning_modailty_id:
                    learning_modality = LearningModality.objects.get(pk=learning_modailty_id)
                if person and topic:
                    # check for dupes
                    alreadys = PreferredModality.objects.filter(person=person, topic=topic)
                    created = None
                    if len(alreadys) == 0:
                        created = PreferredModality.objects.create(person=person, topic=topic)
                    else:
                        created = alreadys.first()
                    if learning_modality:
                        created.learning_modality = learning_modality
                        created.save()
                    created_dict = model_to_dict(created)
                    created_dict['person_id'] = created_dict['person']
                    if learning_modality:
                        created_dict['learning_modality_id'] = created_dict['learning_modality']
                    created_dict['topic_id'] = created_dict['topic']
                    created_dict['person'] = model_to_dict(person)
                    if learning_modality:
                        created_dict['learning_modality'] = model_to_dict(learning_modality)

                    topic_dict = model_to_dict(topic)
                    topic_dict['subject_id'] = topic_dict['subject']
                    topic_dict['subject'] = model_to_dict(topic.subject)
                    created_dict['topic'] = topic_dict
                    return JsonResponse(created_dict, status=201, safe=False)
                else:
                    return JsonResponse(
                        {"message": f"require person, topic for preferred_modality. found {person_id=}, {topic_id=}"},
                        status=400,
                        safe=False
                    )
            else:
                return JsonResponse({"message": f"require topic for preferred_modality. found {topic_id=}"}, status=400, safe=False)
        else:
            return JsonResponse({"message": f"require person for preferred_modality. found {person_id=}"}, status=400, safe=False)

    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            try:
                found = PreferredModality.objects.get(pk=id)
            except:
                return JsonResponse({
                    'error': f"no preferred_modality found for {id=}"
                }, status=404, safe=False)
            return JsonResponse([model_to_dict(found)], status=200, safe=False)

        topic_id = request.GET.get('topic_id')
        user_id = request.GET.get('user_id')
        person_id = request.GET.get('person_id')
        if not person_id:
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    if user:
                        user_person = UserPerson.objects.get(user_id=user_id)
                        if user_person:
                            person_id = user_person.person.id
                except Exception as person_e:
                    return JsonResponse({"message": f"require person_id or user_id for retrieve preferred_modality, found {user_id=}, {person_id=}"})

        filtered = False
        founds = PreferredModality.objects.all()
        if topic_id:
            filtered = True
            founds = founds.filter(topic_id=topic_id)
        if person_id:
            filtered = True
            founds = founds.filter(person_id=person_id)
        if filtered:
            dicts = [model_to_dict(found) for found in founds]
            for dict in dicts:
                dict['topic'] = model_to_dict(Topic.objects.get(pk=dict['topic']))
                dict['topic']['subject_id'] = dict['topic']['subject']
                dict['topic']['subject'] = model_to_dict(Subject.objects.get(id=dict['topic']['subject']))
            return JsonResponse(dicts, status=200, safe=False)
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