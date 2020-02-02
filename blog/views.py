from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .business_logic import *
from .models import Book, BlogSession, Comment, Rate, BuyedBook
from .forms import RegisterForm
from django.shortcuts import redirect
from datetime import datetime, timedelta
import psycopg2
import json


def test_view(request, pk):
    i = 0
    conn = psycopg2.connect(dbname='manga_ranobe', user='ruslan', password='06102017', host='localhost')
    cursor = conn.cursor()
    cursor.execute("SELECT add_item(%s, %s, %s,%s)",
                   [i, pk, datetime.now(), get_user_session(request).user_id])
    data = request.POST['id']
    BuyedBook.objects.create(
        book=Book.objects.get(book_id=pk),
        date=datetime.now(),
        user=get_user_session(request)
    )
    return HttpResponse(
        json.dumps({
            "data": get_user_session(request).user_id,
        }),
        content_type="application/json"
    )


def index(request):
    context = {'posts': Book.objects.all(),
               'user': get_user_session(request)
               }

    return render(request, 'blog/index.html', context)


def editor(request):
    conn = psycopg2.connect(dbname='manga_ranobe', user='ruslan', password='06102017', host='localhost')
    cursor = conn.cursor()
    cursor.execute("""select book.title, count(*) , sum(book.price) 
                    from book
                    inner join buyed_book on book.book_id = buyed_book.book_id
                    where buyed_book."date" between '2019-12-19' and '2020-03-01'
                    group by book.title""")

    curs = conn.cursor()
    curs.execute("""
        select login, count(*)
        from users
        inner join buyed_book on users.user_id = buyed_book.user_id 
        group by users.login
        """)

    cur = conn.cursor()
    cur.execute("""
        select book.title,count(*)  ,book.publish_date,book.price  
    from book 
    inner join buyed_book on book.book_id = buyed_book.book_id 
    where buyed_book."date" between '2019-12-19' and '2020-03-01'
    group by book.description, book.title, book.publish_date,book.price 
        """)
    context = {'user': get_user_session(request),
               'datas': cursor.fetchall(),
               "metas": curs.fetchall(),
               "petas": cur.fetchall(),
               }

    cursor.close()
    conn.close()
    return render(request, 'blog/admin.html', context)


def editor_result(request):
    conn = psycopg2.connect(dbname='manga_ranobe', user='ruslan', password='06102017', host='localhost')
    cursor = conn.cursor()
    cursor.execute("""select book.title, count(*) , sum(book.price) 
                    from book
                    inner join buyed_book on book.book_id = buyed_book.book_id
                    where buyed_book."date" between '2019-12-19' and '2020-03-01'
                    group by book.title""")

    return HttpResponse(
        json.dumps({
            "result": "hello from server",
            "data": cursor.fetchall(),

        }),
        content_type="application/json"
    )


def book(request, pk):
    post = Book.objects.get(book_id=pk)
    comments = Comment.objects.filter(book_id=pk)
    rate = Rate.objects.filter(book_id=pk)
    # author = comments.objects.filter(user_id__password='06102017')
    context = {'posts': post,
               'user': get_user_session(request),
               'comments': comments,
               'rates': rate,
               # 'author': author
               }
    if request.method == 'POST':
        Comment.objects.create(
            user=get_user_session(request),
            publish_date=datetime.now(),
            text=request.POST['comment'],
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

            sessid = do_login(request.POST['login'], request.POST['password'])
            url = request.POST.get('continue', '/')
            if sessid:
                responce = HttpResponseRedirect(url)
                responce.set_cookie('sessid', sessid,
                                    domain='127.0.0.1',
                                    httponly=True,
                                    expires=datetime.now() + timedelta(days=1)
                                    )
                return responce
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
                                expires=datetime.now() + timedelta(days=1)
                                )
            return responce
        else:
            error = 'Неверный логин / пароль'
    return render(request, 'blog/login.html', {'error': error})


def cabinet(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    books = BuyedBook.objects.filter(user=get_user_session(request).user_id)
    context = {
        'num_visits': num_visits,
        'user': get_user_session(request),
        'books': books
    }
    return render(request, 'blog/cabinet.html', context)


def logout(request):
    sessid = request.COOKIES['sessid']
    if sessid is not None:
        session = BlogSession.objects.get(key=sessid)
        session.delete()
    return redirect('index')
