from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone

class StudentGroup(models.Model):
    number = models.CharField(max_length=20, unique=True, help_text="Номер групи, напр. 'CS-101'")
    motto = models.CharField(max_length=200, blank=True, help_text="Гасло групи")
    meeting_room = models.CharField(max_length=50, blank=True, help_text="Кабінет зборів")

    def __str__(self):
        return f"{self.number}"


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    student_card_number = models.CharField(
        max_length=30,
        unique=True,
        validators=[MinLengthValidator(4)],
        help_text="Номер студентської карти, унікальний"
    )
    group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\+?[0-9\- ]+$', "Введіть коректний номер телефону")]
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.student_card_number})"


class LibraryCard(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='library_card')
    issued_at = models.DateField(default=timezone.now)
    expires_at = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Card {self.id} for {self.student}"


class Literature(models.Model):
    GENRE_CHOICES = [
        ('FI', 'Fiction'),
        ('NF', 'Non-fiction'),
        ('SF', 'Sci-Fi'),
        ('FA', 'Fantasy'),
        ('BI', 'Biography'),
        ('HI', 'History'),
        ('OT', 'Other'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=200, blank=True)
    genre = models.CharField(max_length=2, choices=GENRE_CHOICES, default='OT')
    published_date = models.DateField(null=True, blank=True)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True, help_text="ISBN або внутрішній ідентифікатор")
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"{self.title} — {self.author or 'Unknown'}"


class BorrowProcess(models.Model):
    library_card = models.ForeignKey(LibraryCard, on_delete=models.PROTECT, related_name='borrow_records')
    literature = models.ForeignKey(Literature, on_delete=models.PROTECT, related_name='borrow_records')
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    issued_by = models.CharField(max_length=200, blank=True, help_text="ПІБ бібліотекаря, котрий видав книгу")
    borrower_full_name = models.CharField(max_length=200, blank=True, help_text="ПІБ людини, яка взяла книгу")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-borrowed_at']

    def __str__(self):
        return f"Borrow {self.literature.title} by card {self.library_card.id} at {self.borrowed_at.strftime('%Y-%m-%d %H:%M')}"
    

class ReaderProfile(models.Model):
    library_card = models.OneToOneField(LibraryCard, on_delete=models.CASCADE, related_name='reader_profile')
    favorite_genre = models.CharField(max_length=50, blank=True)
    reading_level = models.CharField(
        max_length=20,
        choices=[('BASIC', 'Базовий'), ('INTERMEDIATE', 'Середній'), ('ADVANCED', 'Просунутий')],
        default='BASIC'
    )
    total_read = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reader Profile for {self.library_card.student}"


class Author(models.Model):
    full_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)
    books = models.ForeignKey(Literature, on_delete=models.SET_NULL, null=True, blank=True, related_name='authors')

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class RecommendedList(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='recommended_lists')
    books = models.ManyToManyField(Literature, related_name='recommended_in_groups')
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Recommended List for {self.group.number}"