from django.http import HttpResponseRedirect
from django.shortcuts import render
from .business_logic import *
from .models import Book, Users, Authors, Session, Comment, BookAndAuthors
from .forms import RegisterForm
from django.shortcuts import redirect
from datetime import datetime, timedelta


def index(request):
    context = {'posts': Book.objects.all(),
               'user': get_user_session(request)
               }

    return render(request, 'blog/index.html', context)


def book(request, pk):
    post = Book.objects.get(book_id=pk)
    comments = Comment.objects.filter(book_id=pk)
    # author = comments.objects.filter(user_id__password='06102017')
    context = {'posts': post,
               'user': get_user_session(request),
               'comments': comments,
               # 'author': author
               }
    if request.method == 'POST':
        Comment.objects.create(
            user=get_user_session(request),
            publish_date=datetime.now(),
            text=request.POST['text'],
            book=Book.objects.get(book_id=pk)
        )
    return render(request, 'blog/book.html', context)


def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.login = request.POST['login']
            post.email = request.POST['email']
            post.password = request.POST['password']
            post.user_category_id = 1
            post.save()
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'blog/registration.html', {'form': form})


def login(request):
    error = ''
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        sessid = do_login(login, password)
        url = request.POST.get('continue', '/')
        if sessid:
            responce = HttpResponseRedirect(url)
            responce.set_cookie('sessid', sessid,
                                domain='127.0.0.1',
                                httponly=True,
                                expires=datetime.now() + timedelta(days=5)
                                )
            return responce
        else:
            error = 'Неверный логин / пароль'
    return render(request, 'blog/login.html', {'error': error})


def cabinet(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
        'user': get_user_session(request)
    }
    return render(request, 'blog/cabinet.html', context)


def logout(request):
    sessid = request.COOKIES['sessid']
    if sessid is not None:
        session = Session.objects.get(key=sessid)
        session.delete()
    return redirect('index')
