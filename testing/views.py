from django.shortcuts import render, render_to_response, redirect
from wmposts.models import BasePost
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import request
from wmuser.forms import ProfileForm, SignupForm
from django.template import RequestContext
# Create your views here.

def signuptest(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        formtwo =ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            usertwo = formtwo.save(commit=False)
            usertwo.user = user
            usertwo.save()
            return HttpResponseRedirect('../') # Working and Sensible Redirects
        else:
             return HttpResponse("Invalid shit ") ## jos esim 
    return render_to_response("signup.html", 
        {},#{'form': form, 'formtwo': formtwo},
        context_instance=RequestContext(request)
        )
