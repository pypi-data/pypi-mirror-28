from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^token$', views.get_csrf_token, name="token"),
    url(r'^events/firebase$', views.register_firebase_event, name="firebase_registration")
]
