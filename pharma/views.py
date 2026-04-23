from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse

def pharmagen(request):
    return render(request, 'pharma/pages/pharmagen.html')

def test_view(request):
    return render(request, 'pharma/pages/test.html')


