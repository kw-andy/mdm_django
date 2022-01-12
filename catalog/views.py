from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views import generic

# Create your views here.

from .models import Book, Author, BookInstance, Genre


def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.all().count()

    num_books_that_contains_vent = Book.objects.filter(title__icontains='vent').count()

    num_genres_with_fantasy_in_genre = Genre.objects.filter(name__icontains='fantasy').count()

    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_authors': num_authors,
        'num_instances_available': num_instances_available,
        'num_books_that_contains_vent': num_books_that_contains_vent,
        'num_genres_with_fantasy_in_genre': num_genres_with_fantasy_in_genre,
        'num_visits': num_visits,
    }

    return render(request,'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    #queryset = Book.objects.filter(title__icontains='vent')[:5]
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book    
    paginate_by = 5

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author        
