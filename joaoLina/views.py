from django.shortcuts import render

def handle_404_view(request, exception):
  return render(request, '404.html')

def handle_500_view(request):
  return render(request, '500.html')