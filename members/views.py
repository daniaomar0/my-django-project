# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import Step1Form, Step2Form,SignUpForm,loginForm,UserUpdateForm,ProfileUpdateForm,BookingForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Course
from .forms import UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    pass_form = CustomPasswordChangeForm(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        pass_form = CustomPasswordChangeForm(request.user, request.POST)
        
        if u_form.is_valid() and p_form.is_valid() and pass_form.is_valid():
            u_form.save()
            p_form.save()
            user = pass_form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'pass_form': pass_form
    }
    return render(request, 'profile.html', context)



#remember to return to the managing users in django admin reading


def display_course(request, pk=None): 
    if pk: 
        courses = Course.objects.get(pk=pk) 
    else: 
        courses = "" 
    return render(request, 'course_display.html', {"course":courses}) 

def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {"courses": courses})


def search(request):
    query = request.GET.get('q')
    # Implement your search logic here
    # Example: search_results = MyModel.objects.filter(field__icontains=query)
    context = {
        'query': query,
        # 'search_results': search_results,  # Pass search results to the template
    }
    return render(request, 'search.html', context)

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def trainings(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)


def login_view(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            form.save()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

@login_required
def recommendations(request):
    if request.method == 'POST':
        if 'next' in request.POST:
            step1_form = Step1Form(request.POST)
            step2_form = Step2Form()
            if step1_form.is_valid():
                request.session['step1'] = step1_form.cleaned_data
        else:
            step1_form = Step1Form()
            step2_form = Step2Form(request.POST)
            if step2_form.is_valid():
                return redirect('home')
    else:
        step1_form = Step1Form()
        step2_form = Step2Form()

    username = request.user.username
    return render(request, 'recommendations.html', {
        'step1_form': step1_form,
        'step2_form': step2_form,
        'username':username
    })