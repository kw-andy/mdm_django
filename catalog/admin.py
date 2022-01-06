from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookInline(admin.TabularInline):
    model = Book    

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")

    fields = ["last_name", "first_name", ("date_of_birth", "date_of_death")]

    inlines = [BookInline]

# why use decorators?

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")

    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "id", "due_back")

    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Avalaibility", {"fields": ("status", "due_back")}),
    )



admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book,BookAdmin)
# admin.site.register(BookInstance,BookInstanceAdmin)
