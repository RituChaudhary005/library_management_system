from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Book, Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Membership


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        membership_type = request.POST.get("membership_type", "6M")

        if form.is_valid():
            user = form.save()

            Membership.objects.create(
                user=user,
                membership_type=membership_type
            )

            login(request, user)
            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})
# Check Admin
def is_admin(user):
    return user.is_superuser


# Home (Role Based)
@login_required
def home(request):
    if request.user.is_superuser:
        return render(request, "admin_home.html")
    return render(request, "user_home.html")


# ADMIN ONLY - Add Book
@login_required
@user_passes_test(is_admin)
def add_book(request):
    if request.method == "POST":
        Book.objects.create(
            name=request.POST["name"],
            author=request.POST["author"],
            serial_no=request.POST["serial"],
            
           
        )
        return redirect("book_list")

    return render(request, "add_book.html")


# Book List + Search + Pagination
@login_required
def book_list(request):
    query = request.GET.get("q")
    books = Book.objects.all()

    if query:
        books = books.filter(name__icontains=query) | books.filter(author__icontains=query)

    paginator = Paginator(books, 5)  # 5 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "book_list.html", {"page_obj": page_obj})


# Issue Book
@login_required
def issue_book(request, id):
    book = get_object_or_404(Book, id=id)

    if book.available:
        Transaction.objects.create(user=request.user, book=book)
        book.available = False
        book.save()

    return redirect("book_list")


# Transactions
@login_required
def transactions(request):
    if request.user.is_superuser:
        data = Transaction.objects.all()
    else:
        data = Transaction.objects.filter(user=request.user)

    return render(request, "transactions.html", {"data": data})


# Return Book
@login_required
def return_book(request, id):
    trans = get_object_or_404(Transaction, id=id)
    trans.returned = True
    trans.book.available = True
    trans.book.save()
    trans.save()

    return redirect("transactions")