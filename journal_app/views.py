from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.template import loader
from .models import Topic, Entry

from django.utils import timezone


from django.urls import reverse
# Create your views here.

def index(request):
    return render(request, 'journal_app/index.html')

def topic(request):
    latest_topics_list = Topic.objects.order_by('-date_added')[:5]
    #template = loader.get_template('journal_app/index.html')
    context = {'latest_topics_list' : latest_topics_list}

    
    
    return render(request, 'journal_app/topics.html', context)

# TO DO:
# Test the detail html file:
# Create new entries for the Topic, What is up
# Then loop to see all of the entries of that topic.

def detail(request, topic_id : int):
    
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        raise Http404('Page does not exists')
    return render(request, 'journal_app/detail.html', {'topic' : topic})

def entry(request):
    # Entries Variables:
    last_five_entries = Entry.objects.order_by('date_added')[0:5]
    last_25_entries = Entry.objects.order_by('date_added')[0:25]
    return render(request, 'journal_app/entries.html', 
                  {'last_five_entries' : last_five_entries,
                   'last_25_entries' : last_25_entries})

# Viewing the Entry provided, not a view.
def view(request, entry_id : int):
    """Where we will handle modify request for entries"""
    entry = get_object_or_404(Entry, pk= entry_id)
    return render(request, 'journal_app/entry_detail.html', {'entry' : entry})

def edit(request, entry_id : int):
    """The view for editing entries"""
    entry = get_object_or_404(Entry, pk=entry_id)
    list_topics = Topic.objects.all()

    return render(request, 'journal_app/edit_entry.html', {'entry' : entry,
                                                           'list_topics' : list_topics})

def modify(request, entry_id : int, form=0):
    """Doing something with the data from the edit entry view"""
    entry = get_object_or_404(Entry, pk=entry_id)

    # Getting the data provided by the form.
    # Or a 404 page
    try:
        text = request.POST['edit_entry_text']
        entry_title = request.POST['edit_entry_title']
        edit_topic = request.POST['edit_entry_topic']
    except KeyError:
        raise Http404('Could not access the data provided by the edit page.')

    # Checking if the topic exists
    # If it does, save it. But if not raise 404:
    try:
        edit_topic_object = Topic.objects.get(pk=edit_topic)
    except (ValueError, Topic.DoesNotExist):
        raise Http404(f'Could not find object with ID {edit_topic}')
    

    # Working with the Data provided

    entry.entry_title = f'{entry_title}'
    entry.entry_text = f'{text}'
    entry.topic = edit_topic_object
    entry.save()

    return HttpResponseRedirect(reverse("journal_app:view", args=(entry_id,)))

def createEntry(request):
    list_topics = Topic.objects.all()
    return render(request, "journal_app/create_entry.html", context={'list_topics' : list_topics})

def addEntry(request):
    """Adding a new Entry to the database"""
    # Getting the POST objects that were transfered

    try:
        new_entry_topic_id = request.POST['new_entry_topic']
        new_entry_title = request.POST['new_entry_title']
        new_entry_text = request.POST['new_entry_text']

    except ValueError:
        raise Http404("Please enter valid information")
    
    else:

        # Modifying the Database

        # Declaring the New Entry
        # It has a topic set to None, the program will change it
        # ...later on if it finds the correct ID, if it does not
        # ...it would be change as None:


        new_entry = Entry(topic=None,
                           entry_title=new_entry_title,
                           entry_text=new_entry_text) 

        # Checking if the new Topic is in the database
        # If so, we will let the User know they have entered a wrong Topic ID
        # ...and will be asked to input a correct topic.
        # Else I will render the previous view with an error.
        if new_entry_topic_id != 'None':

            # Trying to get the Topic with given ID
            try:
                new_entry_topic = Topic.objects.get(pk=new_entry_topic_id)
            except (ValueError, Topic.DoesNotExist):
                list_topics = Topic.objects.all()
                # Error page
                return render(request, 
                                'journal_app/create_entry.html', 
                                context={'error_message' : 
                                         "The Topic selected does not exists",
                                'list_topics' : list_topics})
            else:
            # Adding the new entry's arguments
                new_entry.topic = new_entry_topic
        
        # If the user did not gave a Topic:
        elif new_entry_topic_id == 'None':
            # Rendering the previous view, asking the user to select a Topic
            list_topics = Topic.objects.all()
            return render(request, 
                                'journal_app/create_entry.html', 
                                context={'error_message' : "Please select a Topic.",
                               'list_topics' : list_topics})
        
        # Saving the New Entry:
        new_entry.save()

        return HttpResponseRedirect(reverse('journal_app:view', 
                                            args=(new_entry.id,)))
        
            




def editTopic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, "journal_app/edit_topic.html", {"topic" : topic})

def modifyTopic(request, topic_id):

    topic = get_object_or_404(Topic, pk=topic_id)

    try:
        topic_title = request.POST['new_topic_title']

    except (ValueError, Topic.DoesNotExist):
        return render(request, 
                      "journal_app/edit_topic.html", 
                      {"topic": topic, 
                       "error_message" : "Please send valid data"})
    
    # Working with the given data
    # Changing the Topic's text
    topic.topic_text = topic_title
    topic.save()
    
    # Returning the corresponding request
    return HttpResponseRedirect(reverse("journal_app:detail", args=(topic_id,)))

def createTopic(request):
    """View for creating a new Topic"""
    time = timezone.now()
    return render(request, "journal_app/create_topic.html", context={"time" : time})

def addNewTopic(request):
    """Modifying the database to add a new Topic"""

    try:
        post_topic = request.POST['add_topic']
        #post_date_added = request.POST['add_topic_date']
    except ValueError:
        raise Http404('Could not find the POST information requiered')

# Crate a system that can find the latest topic id and append it to the database

    # Checking if the User has entered correct information:
    if type(post_topic) != str:
        raise Http404(f'Value post topic: {type(post_topic)}, and date_post: {type(post_date_added)}')
    
    new_topic = Topic(topic_text=f"{post_topic}")
    
    
    
    # Adding the new topic to the database:
    new_topic.save()


    return HttpResponseRedirect(reverse("journal_app:detail", 
                                        args=(new_topic.id,)))

def removeTopic(request, topic_id):

    # Making sure the User does not delete the No Topics Topic.
    if topic_id == 0:
        raise Http404('You cannot delete the No Topic Topic!')

    # Getting the Topic object.
    try:
        topic_object = Topic.objects.get(pk=str(topic_id))
    except Topic.DoesNotExist:
        raise Http404(f'The topic with ID {topic_id} does not exists.')
    
    

    #Deleting the Topic.
    topic_object.delete()
    print(f'Topic {topic_object} has been deleted!')

    return HttpResponseRedirect(reverse('journal_app:topic'))




# TASK: Create a page that can allow the user to create new Topics
# Simple Taks:
# 1.X Create the view and the URL for the page. X
# 2.X Make a HTML document with a form element.
# 2.X/ Make the esential tags.
# 2.X/ Create FOrm
# X Create spaces for the date added and topic.
# X Link it to the other view.
# 3. X Create a view and URL for the page that will process the information.
# 4. Create the system to add a new Topic to the list.


# Html document with form> that has the topic's title, and date added
# Idea :
# topic = Topic()
# topic.objects.create()