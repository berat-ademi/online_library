from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Count
from datetime import datetime, timedelta
from django.core.paginator import Paginator


# Create your views here.
def books(request):
    books = Books.objects.order_by('author_id__author_name')
    paginator = Paginator(books, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': books,
        'page_obj': page_obj,
    }
    return render(request, 'books.html', context)



def author(request, id):
    author = Authors.objects.filter(id=id).first()
    books = Books.objects.filter(author_id=id)
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'author.html', context=context)
    




class LoginView(View):
    def get(self, request):
        if request.session.get('is_logged_in'):
            return redirect('dashboard')
        form = LoginForm()  #we import forms that we created in forms.py and use here.
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST) #we send the input using request.POST and then we see if they are valid.
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            customer = Customer.objects.filter(email=email, password=password)
            if customer:
                request.session['is_logged_in'] = True
                request.session['email'] = email
                
                #set cookies
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials!")
        context = {
            'form': form
        }      
        return render(request, 'login.html', context)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()            
        context = {
            'form': form
        }
        return render(request, 'register.html', context)
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, "User Exists!!")

        context = {
            'form' : form
        }

        return render (request, 'register.html', context)



def borrow(request, id):
    if not request.session.get('is_logged_in'):
        return redirect('login')
    email = Customer.objects.filter(email=request.session.get('email')).first()
    book = Books.objects.filter(id=id).first()
    borrows = Loans.objects.create(loan_date=datetime.now(), customer_id=email, book_id=book, loan_is_active=True)
    
    return redirect('dashboard')

def my_books(request, id):
    user = Customer.objects.filter(id=id).first()
    result = Loans.objects.filter(customer_id=user)
    books = []
    for r in result:
        book = Books.objects.filter(id=r.book_id_id).first()   # 'r' contains whole row of Loans table/// book_id_id is our book id numeber// if we do only book_id we get the name of the book// 
        author = Authors.objects.filter(id=r.book_id.author_id_id).first()  # here we need to get id based on the relation of  books and authors
        borrowed_date = r.loan_date
        return_date = r.loan_date
        data = {
            'book': book,
            'author': author,
            'borrow_date': borrowed_date,
            'return_date': return_date + timedelta(days=20)
        }
        books.append(data)
    context = {
        'books': books,
        'user': user,
        'result': result
    }
    return render(request, 'my_books.html', context=context)

def logout(request):
    del(request.session['email'])
    del(request.session['is_logged_in'])
    return redirect('login')



def dashboard(request):
    if not request.session.get('is_logged_in'):
         return redirect('login')
    user = Customer.objects.filter(email=request.session.get('email')).first()
    result = Loans.objects.filter(customer_id=user)
    messages = []
    for r in result:
        book = Books.objects.filter(id=r.book_id_id).first()
        return_date = r.loan_date + timedelta(days=20)
        diff = return_date - datetime.now().date()
        if diff.days >= 0:
            message = {
                'message': "You have " + str(diff.days) + " days to return the book " + book.book_name,
                'type': 1
            }
            messages.append(message)
        else:
            message = {
                'message': "You have succesfully read the book " + book.book_name,
                'type': 2
            }
            messages.append(message)


    context = {
        'messages': messages,
        'user': user,

    }
    return render(request, 'dashboard.html', context=context)


def return_book(request, id):
    book = Books.objects.filter(id=id).first()
    b = Loans.objects.filter(book_id=book.id).delete()
    return redirect('dashboard')


def profile(request):
    user = Customer.objects.filter(email=request.session.get('email')).first()
    context = {
        'user': user
    }
    return render(request, 'profile.html', context=context)