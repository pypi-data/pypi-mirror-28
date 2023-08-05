from django.conf.urls import url
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^almacenamientoWeb/(?P<id_poll>[0-9]+)/(?P<id_user>[0-9]+)/(?P<id_questionOption>[0-9]*.*)/', views.insertVoteWeb),
    url(r'^almacenamientoSlack/(?P<id_poll>[0-9]+)/(?P<id_user>[0-9]+)/(?P<id_questionOption>[0-9]*.*)/', views.insertVoteSlack),
    url(r'^almacenamientoTelegram/(?P<id_poll>[0-9]+)/(?P<id_user>[0-9]+)/(?P<id_questionOption>[0-9]*.*)/', views.insertVoteTelegram)
]