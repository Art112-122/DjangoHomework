
from django.contrib import admin
from .models import Author, Book


class BookInline(admin.TabularInline):
    model = Book
    extra = 1  
    max_num = 5  
    fields = ("title", "status", "published_year")
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "birth_year",
        "books_count",
    )

    

    fieldsets = (
        (
            "Основна інформація",
            {"fields": ("name", "birth_year")},
        ),
        (
            "Додатково",
            {
                "fields": ("country", "books_count"),
                "classes": ["collapse"],
            }
        )
    )

    search_fields = ("name", "country")
    list_filter = ("country",)
    inlines = [BookInline]

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = "Books"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def is_large(self, obj):
        return obj.pages > 300

    is_large.boolean = True
    is_large.short_description = "Large book"

    list_display = (
        "title",
        "author",
        "published_year",
        "status",
        "is_large",
    )

    fieldsets = (
        (
            "Основна інформація",
            {"fields": ("title", "author")},
        ),
        (
            "Додатково",
            {
                "fields": ("published_year", "status", "is_large"),
                "classes": ["collapse"],
            },
        ),
    )

    list_filter = (
        "status",
        "published_year",
        "author",
    )

    search_fields = (
        "title",
        "author__name",
    )

    list_select_related = ("author", "published_year")

    actions = ["mark_as_archived"]

    @admin.action(description="Archive selected books")
    def mark_as_archived(self, request, queryset):
        updated = queryset.update(status="archived")
        self.message_user(
            request,
            f"{updated} book(s) archived successfully."
        )

