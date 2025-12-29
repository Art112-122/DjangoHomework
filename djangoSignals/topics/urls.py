from django.urls import path
from . import views

urlpatterns = [
    path("", views.topics_view, name="topics"),
    path("subscribe/<int:id>/", views.subscribe_view, name="subscribe"),
    path("unsubscribe/<int:id>/", views.unsubscribe_view, name="unsubscribe"),
    path("create/", views.create_topic_view, name="create_topic"),
    path("delete/<int:id>/", views.delete_topic_view, name="delete_topic"),
]
