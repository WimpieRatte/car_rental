# Car Rental System

- A project that manages rentals, users and payments for a car rental company.
- The implementation is elaborated upon below, in step-by-step format.
- Currently still in progress (latest progress: Custom users (for registration & login) set up.)

# Step 1: Setup

1. Create the Project Folder
    ```shell
    mkdir car_rental
    cd car_rental
    ```
2. Create and activate the virtual environment
    ```shell
    # Using UV:
    uv init
    uv venv
    .venv\Scripts\activate
    ```
3. Install Django
    ```shell
    uv add django
    ```
4. Create requirements.txt file
    ```shell
    uv pip freeze > requirements.txt
    ```

# Step 2: Project Structure

1. Define the project and app folders

```shell
# Create project
django-admin startproject config .

# Create the apps
django-admin startapp core  # Manage common functionality and pages
django-admin startapp users  # Manages user accounts
django-admin startapp cars  # Manages car inventory
django-admin startapp bookings  # Manages rental bookings
django-admin startapp payments  # Manages payment confirmation and history
```

2. Register the new apps in config:
    ```python
    # config/settings.py
    INSTALLED_APPS = [
        # ...
        'core',
        'users',
        'cars',
        'bookings',
        'payments'
    ]
    ```

# Step 3: User Authentication

- Django uses a built-in authentication system, that is also customisable.
- In order to allow for easy customisation or future modification you must create a custom user model that inherits from the AbstractUser class.
- This will ensure that the built-in user managers and any other functionality tied to authentication is brought in to your custom model.

1. Create a custom user model.

    VERY important to do this BEFORE we run any migrations.
    ```python
    # users/models.py
    from django.contrib.auth.models import AbstractUser
    from django.db import models

    class CustomUser(AbstractUser):
        is_customer = models.BooleanField(default=False)
    ```

2. Update the "settings.py":

    - Indicate which model to use for the authentication system
    ```python
    AUTH_USER_MODEL = 'users.CustomUser'
    ```

3. Create the registration and login views:
    1. Registration:
        1. Create a user registration form:
            - Create a user registration form
            ```python
            # users/forms.py
            from django import forms
            from django.contrib.auth.forms import UserCreationForm
            from .models import CustomUser

            class RegisterForm(UserCreationForm):
                # Using the built-in form field to add validation
                email = forms.EmailField()

                class Meta:
                    model = CustomUser
                    fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
            ```

        2. Create the registration view in `users/views.py`:
            ```python
            from django.shortcuts import render, redirect
            from .forms import RegisterForm

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
            ```

    2. Login:
        - Django has built-in authentication urls. In order to utilize these you just need to include them in your `urls.py` file
        - These urls are tied to built-in authentication views that look for templates inside a folder called `registration`

        ```python
        # users/urls.py
        from django.urls import path, include

        app_name = "users"

        urlpatterns = [
            # ...
            path("register/", views.register, name="register"),
            path("", include("django.contrib.auth.urls")),
        ]
        ```

        ```python
        # config/urls.py
        from django.contrib import admin
        from django.urls import path, include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('users/', include("users.urls", namespace="users")),
        ]
        ```

        Run server
        ```shell
        python manage.py makemigrations
        python manage.py runserver
        ```

## Step 4: Templates and URLs configuration

1. Create the templates folder in the root directory
    ```shell
    mkdir templates
    ```
2. Set up folders for each app inside the templates folder and a folder for the registration template
    ```shell
    mkdir templates/core
    mkdir templates/users
    mkdir templates/cars
    mkdir templates/bookings
    mkdir templates/payments
    mkdir templates/registration  # for the built-in authentication urls
    ```
3. Change the `TEMPLATES` setting to point to the new `templates` folder:
    ```python
    # config/settings.py
    TEMPLATES = [
        {
            # ...
            "DIRS": [BASE_DIR/"templates"],
        },
    ]
    ```

4. Create the registration files:
    - templates/registration/login.html
    - templates/users/register.html