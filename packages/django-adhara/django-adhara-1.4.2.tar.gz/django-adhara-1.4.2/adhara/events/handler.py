from ..models.event_models import FirebaseEvents
from ..utilities import get_config


def emit(user_id, title, content, notification_params, data):
    events = get_config("EVENTS")
    for event_type, config in events.items():
        if event_type == "FIREBASE":
            from .firebase import FirebaseEventHandler
            firebase = FirebaseEventHandler(config["SERVER_KEY"])
            user_firebase_config = FirebaseEvents.objects.values("registration_token").get(user_id=user_id)
            firebase.notify(user_firebase_config["registration_token"], title, content, notification_params, data)
        else:
            pass
