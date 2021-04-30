from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from user.models import Closet
from user.forms import ClosetForm
import os

#################### index#######################################
def index(request):
    return render(request, 'user/index.html', {'title': 'index'})

########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            htmly = get_template('user/Email.html')
            d = {'username': username}
            subject, from_email, to = 'Thank You for Registering', 'khushbuoswal97@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title': 'reqister here'})


################ login forms###################################################
def Login(request):
    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' Welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form, 'title': 'log in'})


############################### UPLOAD Clothes####################################
def home(request):  # for homepage we will use index
    store = Closet.objects.all()
    return render(request, 'home.html', {'fashion_store': store})

# to create a new book
def upload_clothes(request):
    # Using ModelForm to specify the view or to update views
    obj = ClosetForm()  # initially its empty

    if request.method == "POST":
        # Once the form fields are submitted
        obj = ClosetForm(request.POST, request.FILES)  # it fetch the data and save it to obj

        # Once we get form fields(data entered by the user)
        # we will validate it
        if obj.is_valid():

            obj.save()  # commit is bydefault is true

            return redirect('home')

        else:
            return HttpResponse("<H1>Something is wrong</H1>,reload <a href='{{url:'home'}}'>reload</a>")


    else:

        # To initially display Blank form to user so that user can fill the details

        return render(request, "upload.html", {'upload_form': obj})


# Update


def update(request, clothes_id):
    clothes_id = int(clothes_id)  # to convert in integer(because python and sql datatype is different)

    try:

        clothes_selected = Closet.objects.get(id=clothes_id)



    except Closet.DoesNotExist:

        return redirect('home')




    else:

        # to display the form fields

        cl_form = ClosetForm(request.POST or None, instance=clothes_selected)

        # after getting form view with all fields

        # update required fields

        if cl_form.is_valid():
            old_image = ""
            if clothes_selected.cover:

                old_image = clothes_selected.cover.path

                form = ClosetForm(request.POST, request.FILES, instance=clothes_selected)

                if form.is_valid():

                    if os.path.exists(old_image):
                        os.remove(old_image)

                        form.save()

            return redirect('home')


        else:

            return render(request, 'upload.html', {'upload_form': cl_form})


# Delete

def delete(request, clothes_id):
    clothes_id = int(clothes_id)  # to convert in integer(because python and sql datatype is different)

    try:
        clothes_selected = Closet.objects.get(id=clothes_id)

    except Closet.DoesNotExist:
        return redirect('home')

    clothes_selected.delete()
    return redirect('home')

def about(request):
    return render(request,'about.html')