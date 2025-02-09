select
    api_topic.name,
    api_person.last_name,
    auth_user.username
from
    api_topic,
    api_preferredmodality,
    api_person,
    auth_user
where
    api_preferredmodality.topic_id = api_topic.id
and api_person.id = api_preferredmodality.person_id
and api_person.user_id = auth_user.id