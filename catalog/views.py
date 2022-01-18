from django.db import models
from django.db.models.fields import mixins
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')