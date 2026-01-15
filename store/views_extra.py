from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def feedback(request):
    if request.method == 'POST':
        message = 'Thanks for feedback!'
        return render(request, 'store/feedback.html', {'message': message})
    return render(request, 'store/feedback.html')
