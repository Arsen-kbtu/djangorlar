from django.shortcuts import render

def welcome(request):
    return render(request, 'index.html')

def users(request):
    return render(request, 'users.html')

def world_time(request):
    return render(request, 'world_time.html')

def counter(request):
    text = request.GET.get('text', '')
    word_count = len(text.split())
    return render(request, 'count.html', {'word_count': word_count})
