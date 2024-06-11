from django.shortcuts import render,redirect
from django.http import HttpResponse,request,HttpRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User 
from user_agents import parse
from requests import request
import datetime
from django.core.mail import send_mail
from django.http.request import HttpRequest
from .models import *
from .forms import *