from django.conf.urls import url
from.import views


urlpatterns = [
    url(r'^$', views.main, name='homepage'),
    url(r'^register$', views.register),
    # url(r'^display$', views.display),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]