from django.conf.urls import url
from . import views #(imports views.py of the current folder)

urlpatterns = [
    url(r'^$', views.index), #name = 'index)
    url(r'^main$', views.index),                #show "main" in URL
    url(r'^processReg$', views.processReg),   #process registration
    url(r'^processLog$', views.processLog),   #process login
    url(r'^quotes$', views.quotes),
    url(r'^createQuote$', views.createQuote),
    url(r'^addQuote/(?P<quote_id>\d+)$', views.addQuote),
    url(r'^removeQuote/(?P<quote_id>\d+)$', views.removeQuote),
    url(r'^users/(?P<user_id>\d+)$', views.users),
    ]


