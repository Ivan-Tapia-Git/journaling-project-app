from django.urls import path

from . import views


app_name = 'journal_app'

#entries/URL
urlpatterns = [
    path("", views.index, name='index'),

    # Topics URLs:
    path("topics/", views.topic, name='topic'),
    # (Detail Pattern with topics/ as prefix)
    path("topics/<int:topic_id>/", views.detail, name='detail'),
    path("topics/edit/<int:topic_id>/", views.editTopic, name='edit_topic'),
    path("topics/edit/modify/<int:topic_id>/", views.modifyTopic, 
         name='modify_topic'),
    path("topics/edit/delete/<int:topic_id>/", views.removeTopic, name='remove_topic'),
    path("topics/create/", views.createTopic, name='create_topic'),
    path("topics/create/add", views.addNewTopic, name='add_topic'),

    # Entry URLs:
    path("entry/", views.entry, name='entry'),
    path("entry/<int:entry_id>/", views.view, name='view'),
    path("entry/edit/<int:entry_id>/", views.edit, name='edit'),
    path("entry/edit/modify/<int:entry_id>/", views.modify, name='modify'),
    path("entry/create/", views.createEntry, name="create_entry"),
    path("entry/create/add", views.addEntry, name="add_entry"),

    #path("")
]