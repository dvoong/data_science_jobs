from django.shortcuts import render

def home_page(request):
    return render(request, 'data_science_jobs/home.html')
