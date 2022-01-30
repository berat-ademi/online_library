from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('', views.books, name="books"),
    path('login', views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('logout', views.logout, name="logout"),
    path('author/<int:id>', views.author, name="author"),
    path('borrow/<int:id>', views.borrow, name="borrow"),
    path('books/<int:id>', views.my_books, name="my_books"),
    path('return_book/<int:id>', views.return_book, name="return_book"),
    path('profile', views.profile, name="profile"),
    
]