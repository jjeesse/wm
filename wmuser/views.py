from django.shortcuts import render
from wmuser.forms import ProfileForm, SignupForm, UploadProfilePicForm, ForgotPasswordForm
from wmuser.models import BaseUser
from wmposts.models import BasePost
from wmcomment.models import BaseComment
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
#from _winapi import NULL
import string, random
from openid.cryptutil import randomString
from wmbitcoin.models import Transaction

def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
       # formtwo =ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            user.set_password(user.password)
            print(user)
            user.save()
            print(user)
          #  usertwo = formtwo.save(commit=False)
          #  usertwo.user = user
          #  usertwo.save()
            return HttpResponseRedirect('../signin') # Working and Sensible Redirects
        else:
             return HttpResponse("Invalid shit ") # Jos jotkin arvot kusevat, pitaa tehdda kunnollinen response
    return render_to_response("signup.html", 
        {},#{'form': form, 'formtwo': formtwo},
        context_instance=RequestContext(request)
        )


def signin(request):
    if request.method == 'POST':
        # Password change form
        if request.POST.get("forgotPassword"):
            form = ForgotPasswordForm(request.POST)
            return render_to_response('forgot_pass.html', 
            {'form' :form},
            context_instance=RequestContext(request)
            )
            
            # Send Mail
        elif request.POST.get('sendpass'):
        
            uName = request.POST.get('usernameInput') 
            eMail = request.POST.get('emailInput') 
                        
            print('username:' + uName +": , email:"+eMail)
            
            #joku parempi joskus. vain kokeilu
            randomstring = ''.join(random.choice(string.ascii_uppercase) for i in range(20))
            r=str(randomstring)
                        
            if uName != "" and BaseUser.objects.filter(username = uName).exists():
                user = BaseUser.objects.get(username = uName)
                print("invalid username")
            elif eMail != "" and BaseUser.objects.filter(email = eMail).exists():
                user =  BaseUser.objects.get(email = eMail )
                print("invalid email")
            else:
                return HttpResponse("Invalid shit ")
            
            #   if uName != NULL:
            #      user = User.objects.get(username = uName)
            # else: 
            #ei tee mitaan mutta pakko olla
            from_email =""
            #Otsikko
            subject, to = 'Password change, WhizMill',  user.email
            #Ei myoskaan tee mitaan
            text_content = 'You requested a new password for user: '+ user.username +' \nClick the following link to change it.'
            #tassa voisi olla vain linkki mutta teksi ei toimi niin on koko paska
            html_content = ('<p>You requested a new password for user:' + user.username+ '<p>'
            '<p> Click the following link to change it.</p>'
            '<br>'
            '<p><a href="http://localhost:8000/changepass/onetimesecret/'+r+'">Password change link</a>'  
            '</p><br><br><br><br><br><br><br><p>WhizMill people</p>'
            )               
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("email succesfull")
                            
          #  send_mail('Password change WhizMill', teksti, 'kauppi.jesse@gmail.com',[request.POST.get('emailInput')], fail_silently=False)
            return HttpResponseRedirect('/signin')

        elif request.POST.get("login"):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username, password = password)
            
            if user is not None:
                if user.is_active: 
                    #Jos kayttajan on validi niin kirjaudutaan sisaan.
                    login(request,user)
                    return HttpResponseRedirect('../') # Working and Sensible Redirects
                else:
                    # if deleted or not yet activated, Tannekkin kunnon responset.
                    return HttpResponse("Account disabled")
            else:
                return HttpResponse("Invalid login details supplied.") #Tannekkin kunnon responset
            
        elif request.POST.get("register"):
            return HttpResponseRedirect('/signup')
    else:
        return render_to_response('signin.html', 
            {},
            context_instance=RequestContext(request)
            )
        

@login_required
def signout(request):
	logout(request)
	return HttpResponseRedirect('../')
    
           
def changePassword(request):
    return HttpResponse("Not working yet")
            
                        
def profile(request):

    img_source = request.user.profile_pic

    return render_to_response('profile.html', 
        {'source' : img_source},
        context_instance=RequestContext(request)
        )
    
def account_holdings(request):
    bitcoins = request.user.balance
    
    if(request.method == 'POST'):
        bu = request.user
        bu.balance += 100
        bu.save()
    
    return render_to_response('btctest.html',
        {'bitcoins': bitcoins},
        context_instance=RequestContext(request)
        )


def profileSettings(request):   
    # jos vaihtaa kuvaa
    if request.method == 'POST':

        form = UploadProfilePicForm(request.POST, request.FILES) 
        
        
        if form.is_valid():

            instance = request.user
            instance.profile_pic = request.FILES['profile_pic']
            instance.save()
            return HttpResponseRedirect('')
    else:

        form = UploadProfilePicForm       
    img_source = request.user.profile_pic
    return render_to_response('profile_settings.html',
        {'form': form,'img' : img_source},
        context_instance=RequestContext(request)
        )

    
def profileMyPosts(request):
    buser = request.user
    post_list = BasePost.objects.filter(uploader = buser).order_by('date_added').reverse()
    return render_to_response('profile_myposts.html',
        {'post_list': post_list},
        context_instance=RequestContext(request)
        )
    
def profileUpvotes(request):
    buser = request.user
    upvotes_list = Transaction.objects.filter(sender = buser).order_by('date_sent').reverse()
    return render_to_response('profile_upvotes.html',
        {'upvotes_list':upvotes_list},
        context_instance=RequestContext(request)
        )

def profileComments(request):
    buser = request.user
    comment_list = BaseComment.objects.filter(linked_user=buser).order_by('posted_on').reverse()
    return render_to_response('profile_comments.html',
        {'comment_list': comment_list},
        context_instance=RequestContext(request)
        )