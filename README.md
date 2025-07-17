# Car Rental System

- A project that manages rentals, users and payments for a car rental company.
- The implementation is elaborated upon below, in step-by-step format.
- Currently still in progress (latest progress: Custom users (for registration & login), templates and models set up.)

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
    # config/settings.py
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

        (The urls.py files for the other apps will be handled later.)
        ```python
        # users/urls.py
        from django.urls import path, include
        from . import views

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

4. Create the template files:
    - templates/base.html
        ```html
        {% load static %}
        <!DOCTYPE html>
        <html>
        <head>
        <title>{% block title %}Car Rental{% endblock %}</title>
        <link rel="stylesheet" type="text/css" href="{% static 'css/main.css' %}" />
        </head>
        <body>
        <header>
            <h1>🚗 Car Rental Booking System</h1>
            <nav>
            <a href="/">Home</a>
            <a href="/cars/">Cars</a>
            <a href="/bookings/">Bookings</a>
            </nav>
        </header>
        <div class="container">
            {% block content %}{% endblock %}
        </div>
        </body>
        </html>
        ```
    - templates/registration/login.html
    - templates/users/register.html

### Static Files
- Static files are used to store CSS, JS, images etc.
- They can be accessed using the `{% static %}` tag.

1. Create the "static" folder in the root directory
    ```shell
    mkdir static
    ```
2. Create seperate folders for each type of the static files:
    ```shell
    mkdir static/css
    mkdir static/js
    mkdir static/img
    ... etc.
    ```
3. Update the project's settings.py:
    ```python
    STATICFILES_DIRS = [BASE_DIR / "static"]
4. Update the html files to load the static files:

    - Django Template Language provides a special template tag that allows to load static files into your template
    - The `{% load static %}` tag is supposed to be at the top of the HTML document
    - It allows you to enter a path to your desired static file. (NB to alternate between single and double quotes.)
        ```html
        <link rel="stylesheet" type="text/css" href="{% static 'css/main.css' %}" />
        <img src="{% static 'images/hello.png' %}" />
        <script src="{% static 'js/script.js' %}"></script>
        ```

### URL's

- In order to avoid path collision you should create a seperate "urls.py" file in each app
- Ensure to use URL namespacing to create an extra level of specificity
- This will allow you to call URL's via the format `<namespace>:<url-name>`. E.g: `redirect("core:home")`

1. Create urls.py files in each app and give each a unique `app_name` variable
    ```python
    from django.urls import path
    from . import views

    app_name = "<app_name>"
    urlpatterns = [

    ]
    ```

2. Include the files in the project's main `urls.py` file with appropriate namespaces.

    ```python
    # config/urls.py
    # ...
    from django.urls import path, include

    urlpatterns = [
        # ...
        path('bookings/', include("bookings.urls", namespace="bookings")),
        path('cars/', include("cars.urls", namespace="cars")),
        path('payments/', include("payments.urls", namespace="payments")),
        path('users/', include("users.urls", namespace="users")),
        path('', include("core.urls", namespace="core")),
    ]
    ```

## Step 5: Models and Database setup

### PostgreSQL DB Setup

1. Create database in PostgreSQL
    ```shell
    # Login to psql
    sudo -u postgres psql
    ```
    ```sql
    # Create a new database
    CREATE DATABASE car_rental;
    ```
2. Create a user with the appropriate permissions
    (First connect to the car_rental db first)
    ```sql
    -- Create a new user with CREATEDB permission
    CREATE USER rental_admin CREATEDB WITH PASSWORD 'rental_admin123';

    -- Grant all privileges on the database to the user
    GRANT ALL PRIVILEGES ON DATABASE car_rental TO rental_admin;
    GRANT ALL PRIVILEGES ON SCHEMA public TO rental_admin;
    ```
3. Change settings.py to reflect the changes made above
    1. Install `python-dotenv` and `psycopg2-binary`:
        ```shell
        uv add python-dotenv
        uv add psycopg2-binary
        ```
    2. Add `.env` file to the root directory and fill it with the following information:
        ```dotenv
        DATABASE_NAME=car_rental
        DATABASE_USER=rental_admin
        DATABASE_PASSWORD=rental_admin123
        DATABASE_HOST=<your-database-host>
        DATABASE_PORT=<your-db-port>
        ```
    3. Add the `.env` to `.gitignore`
    4. Update the db settings in `settings.py`
        ```python
        # config/settings.py
        import os
        from dotenv import load_dotenv
        load_dotenv()
        # ...
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.getenv('DB_NAME'),
                'USER': os.getenv('DB_USER'),
                'PASSWORD': os.getenv('DB_PASSWORD'),
                'HOST': os.getenv('DB_HOST'),
                'PORT': os.getenv('DB_PORT')
            }
        }
        # ...
        ```

### Models setup and migrations

1. Cars model:

    ```python
    # cars/models.py
    from django.db import models

    class Car(models.Model):

        class Type(models.TextChoices):
            SUV = ('SUV', 'Sport Utility Vehicle')
            SEDAN = ('SEDAN', 'Standard Sedan')
            HATCHBACK = ('HATCHBACK', 'Compact Hatchback')
            COUPE = ('COUPE', 'Two-door Coupe')
            CONVERTIBLE = ('CONVERTIBLE', 'Convertible')
            VAN = ('VAN', 'Van')
            MINIVAN = ('MINIVAN', 'Minivan')
            PICKUP_TRUCK = ('PICKUP_TRUCK', 'Pickup Truck')
            MOTORCYCLE = ('MOTORCYCLE', 'Motorcycle')

        name = models.CharField(max_length=100)
        brand = models.CharField(max_length=100)
        reg_number = models.CharField(max_length=20)
        vehicle_type = models.CharField(choices=Type.choices)
        year = models.IntegerField()
        vin_number = models.CharField(max_length=25)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        availability = models.BooleanField(default=True)

        def __str__(self):
            return f"{self.year} - {self.brand} {self.name} - {self.reg_number}"
    ```

2. Bookings model:

    ```python
    # bookings/models.py
    from users.models import CustomUser
    from cars.models import Car

    class Booking(models.Model):
        customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        car = models.ForeignKey(Car, on_delete=models.CASCADE)
        start_date = models.DateField()
        end_date = models.DateField()
        confirmed = models.BooleanField(default=False)

        def total_days(self):
            return (self.end_date - self.start_date).days + 1

        def total_price(self):
            return self.car.price * self.total_days()

        def __str__(self):
            return f"{self.customer.username} - {self.car.name} ({self.start_date})"
    ```

3. Payments model:

    ```python
    # payments/models.py
    from bookings.models import Booking

    class Payment(models.Model):
        class Status(models.TextChoices):
            SUCCESS = ("success", "Success")
            PENDING = ("pending", "Pending")
            FAILED = ("failed", "Failed")

        booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
        amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
        payment_date = models.DateTimeField(auto_now_add=True)
        status = models.CharField(choices=Status.choices, default=Status.PENDING)

        def __str__(self):
            return f"Payment #{self.booking} - ${self.amount_paid}"
    ```

4. Create migration file and apply migrations
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```