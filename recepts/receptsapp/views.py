from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import logging

from .forms import SignInForm, SignUpForm, RecepeForm
from .models import Recepe

logger = logging.getLogger(__name__)


def log_this(f):
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        logger.info(f'Func "{f.__name__}" was called')
        return res

    return wrapper


def get_random_recepe():
    count = Recepe.objects.filter(is_visible=True).count()
    random_index = randint(0, count - 1)
    random_recepe = Recepe.objects.all()[random_index]
    return random_recepe


@log_this
def index(request):
    number_of_cards = 5
    recepts = []
    count = Recepe.objects.filter(is_visible=True).count()
    if count == 0:
        return render(request, "receptsapp/index.html")
    if count == 1:
        recepts = [Recepe.objects.all()[0]]
        return render(request, "receptsapp/index.html", {'recepts': recepts})
    if 1 < count < number_of_cards:
        number_of_cards = count
    while len(recepts) < number_of_cards:
        recepe = get_random_recepe()
        if recepe not in recepts:
            recepts.append(recepe)
    return render(request, "receptsapp/index.html", {'recepts': recepts})


@log_this
def user(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            reg_form = SignUpForm(request.POST)
            if reg_form.is_valid():
                reg_form.save()
                email = reg_form.cleaned_data['email']
                password = reg_form.cleaned_data['password1']
                user = authenticate(request, email=email, password=password)
                login(request, user)
                return redirect('/cooker')
            else:
                messages.error(request, 'Форма регистрации заполнена неверно')
        elif 'login' in request.POST:
            login_form = SignInForm(request.POST)
            if login_form.is_valid():
                if user := authenticate(request, **login_form.cleaned_data):
                    login(request, user)
                    return redirect('/cooker')
                messages.error(request, 'Ошибка авторизации')
            else:
                messages.error(request, 'Форма авторизации заполнена неверно')

    reg_form = SignUpForm()
    login_form = SignInForm()

    context = {
        'reg_form': reg_form,
        'login_form': login_form
    }
    return render(request, 'receptsapp/user.html', context)


@log_this
@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


@log_this
@login_required
def cooker(request):
    recipes = Recepe.objects.filter(is_visible=True, author=request.user)
    return render(request, "receptsapp/cooker.html", {'recepts': recipes})


@log_this
@login_required
def recepe_add(request):
    is_completed = False
    if request.method == 'POST':
        form = RecepeForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            cooking_steps = form.cleaned_data['cooking_steps']
            cooking_time = form.cleaned_data['cooking_time']
            image = form.cleaned_data['image']
            author = request.user
            category = form.cleaned_data['category']
            recepe = Recepe(title=title,
                            description=description,
                            cooking_steps=cooking_steps,
                            cooking_time=cooking_time,
                            image=image,
                            author=author,
                            category=category)
            recepe.save()
            is_completed = True
    else:
        is_completed = False
        form = RecepeForm()
    return render(request, 'receptsapp/recepe_add.html',
                  {'form': form, 'is_completed': is_completed})


@log_this
@login_required
def recepe_edit(request, recepe_id):
    is_completed = False
    recepe = Recepe.objects.filter(pk=recepe_id).first()
    recepe_img = recepe.image
    if request.user != recepe.author:
        return redirect('/')
    if request.method == 'POST':
        form = RecepeForm(request.POST, request.FILES)
        if form.is_valid():
            recepe.title = form.cleaned_data['title']
            recepe.description = form.cleaned_data['description']
            recepe.cooking_steps = form.cleaned_data['cooking_steps']
            recepe.cooking_time = form.cleaned_data['cooking_time']
            recepe.category = form.cleaned_data['category']
            if form.cleaned_data['image'] is not None:
                recepe.image = form.cleaned_data['image']
            recepe.save()
            is_completed = True
    else:
        is_completed = False
        if recepe:
            data = {'title': recepe.title,
                    'description': recepe.description,
                    'cooking_steps': recepe.cooking_steps,
                    'cooking_time': recepe.cooking_time,
                    'category': recepe.category}
            if recepe.image is not None:
                recepe_img = recepe.image
            form = RecepeForm(data)
        else:
            form = RecepeForm()
    return render(request, 'receptsapp/recepe_edit.html',
                  {'form': form,
                   'is_completed': is_completed,
                   'recipe_img': recepe_img,
                   'recipe': recepe})


@log_this
@login_required
def recepe_delete(request, recepe_id):
    recepe = Recepe.objects.filter(pk=recepe_id).first()
    if request.user != recepe.author:
        return redirect('/')
    if recepe:
        recepe.is_visible = False
        recepe.save()
    return redirect('/cooker')


@log_this
def recepe_detail(request, recepe_id):
    recepe = Recepe.objects.get(id=recepe_id)
    context = {
        'recepe': recepe
    }
    return render(request, 'receptsapp/recepe_detail.html', context)


@log_this
def handler404(request, exception):
    return render(request, '404.html', status=404)


@log_this
def handler500(request):
    return render(request, '500.html', status=500)
