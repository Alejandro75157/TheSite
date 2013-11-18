from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from app.forms import MessageForm
from app.models import Message, Person, Relationship
import datetime


def home(request):
    if ('member_id' in request.session):
       cur_user_id = request.session['member_id']
       cur_user_id = int(cur_user_id)
       return render(request, 'base.html', {'cur_user_id': cur_user_id})
    else:
       return render(request, 'base.html')



@login_required(redirect_field_name='/accounts/login')
def userpage(request, user_id):
    if request.method == "POST":
        income_title = request.POST['title']
        income_text = request.POST['text']
        if income_title and income_text:
            message = Message()
            message.author = request.user
            message.date = datetime.datetime.now()
            message.title = income_title
            message.text = income_text
            message.save()

    user_id = int(user_id)
    current_user_id = request.session['member_id']
    current_user = User.objects.get(id=current_user_id)
    page_owner = User.objects.get(id=user_id)
    message = Message.objects.filter(author=page_owner).order_by('-id')

    owner_person = Person.objects.get(user=page_owner)
    current_person = Person.objects.get(user=current_user)

    subscribings_user = Person.get_following(current_person)
    subscribers_user = Person.get_followers(current_person)
    subscribings_owner = Person.get_following(owner_person)
    subscribers_owner = Person.get_followers(owner_person)

    condition=False
    i=0
    for subscribings in subscribings_user:
        if page_owner.id != subscribings.user.id:
            i += 1

    if i == len(subscribings_user):
        condition=True

    last_message=datetime.datetime.now()
    for one in message:
        last_message=one.date

    if current_user_id == user_id:
        message = Message.objects.filter(author=current_user).order_by('-id')
        mesform = MessageForm()
        last_message=datetime.datetime.now()
        for one in message:
            last_message=one.date
        return render(request, 'userpage.html', {'mesform': mesform,
                                                 'message': message,
                                                 'page_owner': page_owner,
                                                 'cur_user_id': current_user_id,
                                                 'subscribings_user': subscribings_user,
                                                 'subscribers_user': subscribers_user,
                                                 'last_message': last_message}, )
    else:
        return render(request, 'user.html', {'message': message,
                                             'page_owner': page_owner,
                                             'cur_user_id': current_user_id,
                                             'subscribings_owner': subscribings_owner,
                                             'subscribers_owner': subscribers_owner,
                                             'subscribings_user': subscribings_user,
                                             'condition': condition,
                                             'last_message': last_message}, )


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    #u = User.objects.get(username=request.POST['username'])
    if user is not None and user.is_active:
        auth.login(request, user)
        request.session['member_id'] = user.id
        return HttpResponseRedirect("/")
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_person = Person(user=new_user, name=new_user.username)
            new_person.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    auth.logout(request)
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect("/")

def search(request):
    cur_user_id = request.session['member_id']
    cur_user_id = int(cur_user_id)
    if 'q' in request.GET:
        q = request.GET['q']
        srch_user = User.objects.filter(username__icontains=q)
        return render(request, 'search.html', {'srch_user': srch_user, 'query': q, 'cur_user_id': cur_user_id})
    return render(request, 'search.html', {'cur_user_id': cur_user_id})

def add_relationships(request, user_id):
    current_user_id = request.session['member_id']
    current_user = User.objects.get(id=current_user_id)
    page_owner = User.objects.get(id=user_id)

    owner_person = Person.objects.get(user=page_owner)
    current_person = Person.objects.get(user=current_user)

    Person.add_relationship(current_person, owner_person, 1)

    return HttpResponseRedirect ("/accounts/profile/"+user_id)

def remove_relationships(request, user_id):
    current_user_id = request.session['member_id']
    current_user = User.objects.get(id=current_user_id)
    page_owner = User.objects.get(id=user_id)

    owner_person = Person.objects.get(user=page_owner)
    current_person = Person.objects.get(user=current_user)

    Person.remowe_relationship(current_person, owner_person, 1)

    return HttpResponseRedirect ("/accounts/profile/"+user_id)

def delete_message(request, user_id, message_id):
    current_user_id = request.session['member_id']
    current_user = User.objects.get(id=current_user_id)
    Message.objects.filter(author=current_user).get(id=message_id).delete()
    return HttpResponseRedirect ("/accounts/profile/"+user_id)