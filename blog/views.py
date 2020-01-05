from django.shortcuts import render
from .models import Book, Users


def index(request):
    context = {'posts': Book.objects.all()}
    return render(request, 'blog/index.html', context)


def book(request, pk):
    post = Book.objects.filter(book_id=pk)
    context = {'posts': post}
    return render(request, 'blog/book.html', context)


def registration(request):
    Users.objects.create(
        login=request.POST['login'],
        email=request.POST['email'],
        password=request.POST['password']
    )
    return render(request, 'blog/registration.html')
