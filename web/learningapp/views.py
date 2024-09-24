from django.shortcuts import render
from django.http import HttpResponseNotFound

# Home page view
def home(request):
    return render(request, 'home.html')  # Render your home template

# About page view
def about(request):
    return render(request, 'about.html')  # Render your about template

# Custom 404 page view
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)  # Render your custom 404 page

