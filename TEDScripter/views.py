# -*- coding: utf-8 -*-

from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from TEDScripter.ted import get_talk

@login_required
def index(request):
    return TemplateResponse(request, 'index.html', {})

@login_required
def talk(request, talk_id):
    talk = get_talk(talk_id)
    return JsonResponse(talk)
