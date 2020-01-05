from django.shortcuts import render
from .models import Book, Users, Authors
from .forms import RegisterForm
from django.shortcuts import redirect


def index(request):
    context = {'posts': Book.objects.all()}
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
            post.save()
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'blog/registration.html', {'form': form})
