from django.shortcuts import render, redirect
from .forms import RegisterForm

# Views:
def register(request):
    # Check if the form has been submitted
    if request.method == 'POST':
        # Input submitted info into the form
        form = RegisterForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        # redirect to a clean registration page
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})
