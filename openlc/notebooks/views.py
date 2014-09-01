from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django import forms
from models import UserProfile, User, Category, Notebook
from forms import NotebookForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from openlc.settings import BASE_DIR, MEDIA_URL
import subprocess
import os
from django.utils.text import slugify
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):

    new_notebooks = Notebook.objects.all().order_by('-pub_date')[:10]
    likes_notebooks = Notebook.objects.all().order_by('-likes')[:10]
    views_notebooks = Notebook.objects.all().order_by('-views')[:10]

    categories = Category.objects.all()

    context = {'new_notebooks' : new_notebooks, 'likes_notebooks' : likes_notebooks, 'views_notebooks' : views_notebooks, 'categories' : categories}
    return render(request, 'index.html', context)

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            return redirect('/notebooks')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}

    return render(request, 'register.html', context)

def user_login(request):


    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(username=username, password=password)


        if user:

            if user.is_active:

                login(request, user)
                return redirect('/notebooks')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        context = {}
        return render(request, 'login.html', context)


@login_required
def user_logout(request):

    logout(request)

    return redirect('/notebooks')

def profile_page(request, username):

    profile_user = User.objects.get(username=username)

    try:
        profile_user_profile = UserProfile.objects.get(user=profile_user)

    except:
        profile_user_profile = None

    notebooks = Notebook.objects.all()

    profile_user_notebooks = []
    for notebook in notebooks:
        if notebook.user == profile_user:
            profile_user_notebooks.append(notebook)

    context = {'profile_user_notebooks' : profile_user_notebooks, 'profile_user': profile_user, 'profile_user_profile' : profile_user_profile}


    return render(request, 'profile_page.html', context)

def category_page(request, category):

    category = Category.objects.filter(category=category)

    notebooks_list = Notebook.objects.filter(category=category).order_by('-pub_date')

    paginator = Paginator(notebooks_list, 15) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        notebooks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notebooks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notebooks = paginator.page(paginator.num_pages)

    context = {'notebooks' : notebooks, 'category' : category[0]}

    return render(request, 'category_page.html', context)


@login_required
def add_notebook(request):

    u = User.objects.get(username=request.user)
    file_error = None

    if request.method == "POST":
        form = NotebookForm(request.POST, request.FILES)
        if form.is_valid():

            model_instance = form.save(commit=False)
            file_extension = os.path.splitext(str(model_instance.file))[-1].lower()
            if file_extension == '.ipynb':

                model_instance.user = u
                model_instance.slug = slugify(model_instance.title)
                model_instance.save()

                subprocess.call(['ipython', 'nbconvert' , '--to', 'html', BASE_DIR + MEDIA_URL + 'content/' + u.username + '/' + os.path.basename(model_instance.file.name)])
                subprocess.call(['mv', BASE_DIR + '/' + os.path.basename(model_instance.file.name)[:-6] + '.html', BASE_DIR + MEDIA_URL + 'content/' + u.username + '/' + model_instance.slug + '.html'])
                subprocess.call(['mv', BASE_DIR + MEDIA_URL + 'content/' + u.username + '/' + os.path.basename(model_instance.file.name), BASE_DIR + MEDIA_URL + 'content/' + u.username + '/' + model_instance.slug + '.ipynb'])


                return render(request, "thanks.html")
            else:
                file_error = '<ul class="errorlist"><li>The file you selected is not an ipython notebook.</li></ul>'
    else:
        form = NotebookForm()

    return render(request, "add_notebook.html", {'form': form, 'file_error': file_error})

def notebook_viewer(request, id, user, slug):

    notebook = Notebook.objects.filter(pk=id).update(views=F('views') + 1)

    notebook = Notebook.objects.get(pk=id)
    notebook_html = 'content/' + user + '/' + slug + '.html'
    filename = 'content/' + user + '/' + slug + '.ipynb'

    return render(request, "base_notebook.html", {'notebook_html': notebook_html, 'filename' : filename, 'notebook' : notebook})


def like_notebook(request):

    if request.method == 'GET':
        notebook_id = request.GET['notebook_id']

    if notebook_id:
        Notebook.objects.filter(id=int(notebook_id)).update(likes=F('likes')+1)
    else:
        test='hej'

    notebook = Notebook.objects.filter(id=int(notebook_id))

    likes = 'Likes: ' + str(notebook[0].likes)

    return HttpResponse(likes)


def twitter_license(request):

    return render(request, "twitter_license.html")

def ipython_license(request):

    return render(request, "ipython_license.html")

def django_license(request):

    return render(request, "django_license.html")


