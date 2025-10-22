from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from main.models import Event, EventType 
from main.forms import EventForm

# Create your views here.
