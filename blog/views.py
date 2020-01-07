from django.http import HttpResponseRedirect
from django.shortcuts import render
from .business_logic import do_login
from .models import Book, Users, Authors
from .forms import RegisterForm
from django.shortcuts import redirect
from datetime import datetime, timedelta


def index(request):
    context = {'posts': Book.objects.all(),
               'user': request.user
               }

    return render(request, 'blog/index.html', context)


def book(request, pk):
    post = Book.objects.filter(book_id=pk)
    context = {'posts': post}
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


def check(request):
    if Users.objects.filter(login=request.GET['login'], password=request.GET['password']):
        return redirect('index')
    else:
        return redirect('login')


def cabinet(request):
    request.session['sessionid'] = 'mart'
    first_session = request.session['sessionid']
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'first_session': first_session,
        'num_visits': num_visits
    }
    return render(request, 'blog/cabinet.html', context)
