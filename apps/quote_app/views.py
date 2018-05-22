from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import *
from django.contrib import messages, sessions
import bcrypt

def index(request):
    print "******"
    print "main route" #to display "main" in index url
    print "******"
    return render(request, 'quote_app/index.html')

def processReg(request):
    print "******"
    print "registration route"
    print "******"
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print errors
        return redirect('/')
    else:
        hashedPW = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(         #set variable to access user_id by "user.id" (store in session)
        name = request.POST['name'],
        alias = request.POST['alias'],
        email = request.POST['email'],
        password = hashedPW
            # dateOfBirth = postData['dateOfBirth']   don't worry about updating bday in database
        )
    # print user.id
    request.session.modified = True
    request.session['user_id'] = user.id                    #stores REGISTERED user in session
    request.session['email'] = request.POST['email']
    request.session['name'] = request.POST['name']
    current_user = request.session['name']                  #just quick access to session['name']
    return redirect('/quotes')

# def processLog(request):
#     #get user data from post request form
#     errors = User.objects.login_validator(request.POST)

#     #check for errors in login validation and create messages / redirect users if so
#     if len(errors) == list:
#         for err in result:
#             messages.error(request, err)
#         return redirect(index)

#     #if no errors in registration validation, redirect user to the welcome page & set post data
#     request.session['user_id'] = User.objects.get(email=me).id
#     messages.success(request, "Successfully logged in!")
#     return redirect('/quotes')


def processLog(request):
    print "******"
    print "login route"
    print "******"
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print errors
        return redirect('/')
    else:
        request.session.modified = True
        me = request.POST['me']                               #stores LOGGED IN user in session                                  #store "me" as 'email' in session
        request.session['user_id'] = User.objects.get(email=me).id    #gets user_id that matches form email, stores in session
        request.session['name'] = User.objects.get(email=me).name    #gets user_id that matches form email, stores in session
        return redirect('/quote')

def quotes(request):
    print "*************"
    print "made it to quotes route"
    print "*************"
    me = User.objects.get(id=request.session['user_id'])
    # current_user = request.session['user_id']
    context = {
            'quote_query': Quote.objects.all(),
            'my_faves': Quote.objects.filter(faved_by=me),
            'not_my_faves':Quote.objects.exclude(faved_by=me)
    }


    return render(request, 'quote_app/quotes.html', context)


def createQuote(request):
    author = request.POST['author']
    text = request.POST['text']
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.create(
        author=author,
        text=text,
        posted_by=user,
    )
    return redirect('/quotes')
def addQuote(request, quote_id):
    print "*************"
    print "made it!! route"
    print "*************"
    Quote.objects.addQuote(quote_id, request.session['user_id'])
    return redirect('/quotes')

def removeQuote(request, quote_id):
    # id = request.session['id']
    # user =
    Quote.objects.removeQuote(quote_id, request.session['user_id'])
    print "*************"
    print "made it XXX!! route"
    print "*************"
    return redirect('/quotes')

def users(request, user_id):
    Selected_user = User.objects.get(id=user_id)
    context = {
        'quote_query': Selected_user.posted_quote.all(),
        'count': Selected_user.posted_quote.all().count(),
        'user_name':Selected_user.name,

    }

    return render(request,'quote_app/users.html', context)
