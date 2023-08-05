import hashlib

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

from .models import Question, Choice, User
from .forms import UserForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                User.objects.create(username=username, password=password)
                return HttpResponse('sing up successfully.')
            else:
                error_message = "user name exists"
                context = {'form': form, 'error_message': error_message}
                return render(request, "polls/signup.html", context=context)
    else:
        form = UserForm()
    return render(request, "polls/signup.html", context={'form': form})


def gen_sid(text):
    return hashlib.sha1(text.encode()).hexdigest()


def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username, password=password):
                # 登录成功了
                delta = timedelta(days=1)
                expire_time = timezone.now() + delta
                session_data = expire_time.strftime('%s')
                session_id = gen_sid('%s:%s' % (username, session_data))
                request.session[session_id] = session_data
                url = reverse('polls:index')
                r = HttpResponseRedirect(url)
                r.set_cookie('sid', session_id, int(delta.total_seconds()))
                return r
            else:
                error_message = "login failed"
                context = {'form': form, 'error_message': error_message}
                return render(request, "polls/login.html", context=context)
    else:
        form = UserForm()
    return render(request, "polls/login.html", context={'form': form})


def logout(request):
    sid = request.COOKIES.get('sid', None)
    response = HttpResponseRedirect(reverse('polls:login'))
    if sid is not None:
        del request.session[sid]
        response.delete_cookie(sid)
    return response


def index(request):
    # 检验用户使用已经登录
    sid = request.COOKIES.get('sid', None)
    if sid is None:
        return HttpResponseRedirect(reverse('polls:login'))

    try:
        expire_second = int(request.session[sid])
    except KeyError:
        return HttpResponseRedirect(reverse('polls:login'))

    current_second = int(timezone.now().strftime('%s'))
    if expire_second < current_second:
        return HttpResponseRedirect(reverse('polls:login'))

    now = timezone.now()
    latest_questions = Question.objects.filter(pub_date__lt=now).order_by('-pub_date')[:3]
    context = {'latest_questions': latest_questions}
    r = render(request, "polls/index.html", context=context)
    return r


def detail(request, question_id):
    now = timezone.now()
    q = get_object_or_404(Question, pk=question_id, pub_date__lt=now)
    return render(request, "polls/detail.html", context={'q': q})


def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", context={'q': q})


def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    choice_id = request.POST.get('choice', None)
    if choice_id is None:
        error_message = "You have to make a choice"
        return render(request, "polls/detail.html",
                      context={'q': q, 'error_message': error_message})

    choice = get_object_or_404(Choice, question=q, pk=choice_id)
    choice.votes = F('votes') + 1
    choice.save()
    to = reverse('polls:results', args=(question_id,))
    return HttpResponseRedirect(to)
