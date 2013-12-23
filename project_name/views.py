#-*- coding: utf-8 -*-

# System Libs
import re
import json
import requests

# Django
from django.conf import settings
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Models
from django.contrib.auth.models import User
from models import Profile

# Yardımcı metodlar
def errors_to_json(errors):
    """
    Convert a Form error list to JSON::
    """
    return dict(
            (k, map(unicode, v))
            for (k,v) in errors.iteritems()
        )

def send_json_response(json_response, status=200):
    return HttpResponse(json.dumps(json_response), status=status, content_type='application/json')

def get_default_template_params(request):
    template_params = {
        'request': request,
        'user': request.user,
        'is_debug': settings.DEBUG,
        'is_template_debug': settings.TEMPLATE_DEBUG
    }
    template_params.update(csrf(request))
    return template_params

def not_found(request):
    return render(request, '404.html', get_default_template_params(request), status=404)

def internal_error(request):
    return render(request, '500.html', get_default_template_params(request), status=500)