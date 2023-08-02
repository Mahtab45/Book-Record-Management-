from django.shortcuts import render
from BRMapp.forms import NewBookForms, SearchForms
from BRMapp import models
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/BRMapp/login/')
def searchBook(request):
    form=SearchForms()
    res=render(request,'BRMapp/search_book.html',{'form':form})
    return res

@login_required(login_url='/BRMapp/login/')
def search(request):
    form=SearchForms(request.POST)
    book=models.Book.objects.filter(title=form.data['title'])
    res=render(request,'BRMapp/search_book.html',{'form':form,'book':book})
    return res

@login_required(login_url='/BRMapp/login/')
def deleteBook(request):
    bookid=request.GET['bookid']
    book=models.Book.objects.filter(id=bookid)
    book.delete()
    return HttpResponseRedirect('BRMapp/view-books')

@login_required(login_url='/BRMapp/login/')
def editBook(request):
    book=models.Book.objects.get(id=request.GET['bookid'])
    fields={'title':book.title,'price':book.price,'author':book.author,'publisher':book.publisher}
    form=NewBookForms(initial=fields)
    res=render(request,'BRMapp/edit_book.html',{'form':form,'book':book})
    return res

@login_required(login_url='/BRMapp/login/')
def edit(request):
    if request.method=='POST':
        form=NewBookForms(request.POST)
        book=models.Book()
        book.id=request.POST['bookid']
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()
    return HttpResponseRedirect('BRMapp/view-books')

@login_required(login_url='/BRMapp/login/')
def viewBooks(request):
    books=models.Book.objects.all()
    username=request.session['username']
    res=render(request,'BRMapp/view_book.html',{'books':books,'username':username})
    return res

@login_required(login_url='/BRMapp/login/')
def newBook(request):
    form=NewBookForms()
    res=render(request,'BRMapp/new_book.html',{'form':form})
    return res

@login_required(login_url='/BRMapp/login/')
def add(request):
    if request.method=='POST':
        form=NewBookForms(request.POST)
        book=models.Book()
        book.title=form.data['title']
        book.price=form.data['price']
        book.author=form.data['author']
        book.publisher=form.data['publisher']
        book.save()

    s="Record Stored<br><a href='/BRMapp/view-books'>View all Books</a>"
    return HttpResponse(s)

def userLogin(request):
    data={}
    if request.method=="POST":
        username=request.POST['username'];
        password=request.POST['password'];
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect('/BRMapp/view-books/')
        else:
            data['error']="User or Password is incorrect"
            res=render(request,'BRMapp/user_login.html',data)
            return res
    else:
        return render(request,'BRMapp/user_login.html',data)

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/BRMapp/login/')
