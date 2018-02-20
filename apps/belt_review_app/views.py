from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'belt_review_app/index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else: 
        User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password= bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()))
        id = User.objects.get(email=request.POST['email']).id
        request.session['id'] = id
        request.session['alias'] = User.objects.get(id=id).alias 
        return redirect('/books')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else: 
        id = User.objects.get(email=request.POST['logemail']).id
        request.session['id'] = id
        request.session['alias'] = User.objects.get(id=id).alias
        return redirect('/books')

def books(request):
    threereviews = []
    count = 3
    if Review.objects.all().count() <  3:
        # Review.objects.all()[:3]
        count = Review.objects.count()
    for num in range(0, count):
        threereviews.append(Review.objects.order_by("-created_at")[num])
    all_books = {'books' : Book.objects.all(),
    'recent' : threereviews,
    'users' : User.objects.all(),
    }
    return render(request, 'belt_review_app/books.html', all_books)

def book_id(request, book_id):
    book = {'specbook' : Book.objects.filter(id=book_id),
    'reviews' : Review.objects.filter(books_id=book_id),
    'users' : User.objects.all()
    }
    return render(request, 'belt_review_app/book_id.html', book)

def user(request, user_id):
    reviewedbooks = {}
    specreviews = Review.objects.filter(users_id = user_id)
    for review in specreviews:
        if Book.objects.get(id= review.books_id):
            reviewedbooks[review.books_id] = Book.objects.get(id= review.books_id)
            # print Book.objects.get(id= review.books_id)

    # u = User.objects.filter(id=user_id)[0]
    # r = u.user_reviews.all()
    # for rev in r:
    #     print rev.books.title

    user = { 'specuser' : User.objects.filter(id=user_id),
    'count' : Review.objects.filter(users_id=user_id).count(),
    'books' : Book.objects.filter(users_id=user_id),
    'reviewed' : reviewedbooks
    }
    return render(request, 'belt_review_app/user.html', user)

def add(request):
    print request.session['id']
    return render(request, 'belt_review_app/add.html')

def addreview(request):
    if not len(Book.objects.filter(title=request.POST['title'])) > 0:
        if len(request.POST['newauthor']) > 0: 
            Book.objects.create(title=request.POST['title'], author=request.POST['newauthor'], users=User.objects.get(id=request.session['id']))
        else:
            Book.objects.create(title=request.POST['title'], author=request.POST['author'], users=User.objects.get(id=request.session['id']))
    Review.objects.create(descr=request.POST['review'], rating= request.POST['rating'], books=Book.objects.filter(title=request.POST['title'])[0], users=User.objects.get(id=request.session['id']))
    return redirect('/books/' + str(Book.objects.filter(title=request.POST['title'])[0].id))

def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, review_id):
    Review.objects.get(id=review_id).delete()
    return redirect('/books/'+ review_id)
