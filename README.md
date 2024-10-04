# Lea Cottage Django Project

## Overview

`lea_cottage` is a Django-based web application designed for managing a home bakery business. It provides a system for managing products, including ingredients and stock items, and allows users to reserve items for collection. The project includes two primary apps:

1. **Product**: Manages ingredients, stock items, and other product-related details.
2. **Reservation**: Handles the reservation process for users, including adding items to reservations and managing reservation statuses.

## UI/UX Design
### Overall Design Approach

The design of the site embraces the Swedish principle of **"less is more"** to deliver a clean, simple, and functional interface. The focus is on clarity and ease of use, avoiding unnecessary visual distractions or clutter. The result is a minimalistic layout that supports the primary goals of the home bakery business: providing a streamlined experience for users to browse products and make reservations without being overwhelmed by excessive features or complex navigation.

The design ensures that every element on the site serves a clear purpose, reflecting a calm and intentional user experience. The emphasis on simplicity allows users to focus on key tasks—browsing, selecting, and reserving items—without being distracted by unnecessary visual or interactive components.

### Agile Development

This project was developed using the **agile methodology**, from initial planning to final development. The process was visualized using GitHub Projects, where tasks were broken down into user stories and manageable chunks. A **Kanban board** was used to track the progress of each user story, ensuring the project stayed on track.

Each user story was tagged with labels to indicate its priority and significance within the overall scope of the project. The goal was to maintain a high level of focus on the most important features while remaining flexible enough to adapt to changes or improvements along the way.

### Wireframes

The initial wireframes were created in Figma to outline the basic structure of the site. These wireframes were kept intentionally simple, reflecting the minimalist design approach. While not all features were covered in the early drafts, they served as a foundation for developing the essential components of the site.

**Wireframe Images**  


### Site Goals

The main objective of this site is to offer a straightforward platform where users can browse and reserve bakery items with ease. The site intentionally limits user actions to maintain simplicity and avoid overwhelming the user with too many choices. The absence of social media links or unnecessary commercial elements is deliberate, in line with the site's goal of reducing distractions and sensory overload.

Rather than attempting to cater to multiple functions, the site focuses solely on product display and reservations. This minimal approach fosters a calm, focused environment for users, with potential for future expansions if they align with the site's simple and functional design ethos.

### Strategy

The primary objective of the `lea_cottage` project is to create a simple, intuitive interface for a home bakery business. Unlike many modern web applications focused on complex commerce or social interactions, this site is designed to serve both the bakery owners and customers by allowing product browsing and reservations with minimal distraction. The user’s needs focus on reserving items, while the business objective centers on tracking inventory and fulfilling customer orders efficiently.

### Scope

The core functions of the project are deliberately kept minimal to streamline both the user and administrative experience. This includes essential features such as product display, ingredient listing, and the ability to reserve items. User authentication is required for reservations, which ensures that the process is secure and user-specific. Basic CRUD functionality is included for managing products and reservations, and only the necessary features were implemented to maintain the project’s simplicity. Future features will be considered based on user feedback but were deemed outside the current scope.

### Structure

The site’s structure follows a straightforward approach, ensuring easy navigation for both customers and bakery staff. Users can browse products (items) and view detailed ingredient information. The structure is designed to allow authenticated users to reserve stock items and manage their reservations. The layout is inspired by typical e-commerce systems but simplified to reduce clutter. For instance, while customers can explore products without an account, an account is required to reserve items, maintaining a clean distinction between browsing and ordering.

### Skeleton

The website’s skeleton translates the defined structure into practical, navigable elements. A clear navbar is present on all pages, allowing users to easily access product lists, view reservations, and manage their account. For smaller screen sizes, a responsive hamburger menu ensures the site remains accessible on mobile devices. On the product pages, items are displayed in a list view, with details easily accessible through links or buttons. Clear call-to-action buttons guide users through the reservation process, and the layout adheres to familiar design patterns that are intuitive for users across all devices.

### Surface

The visual design focuses on a calm, welcoming atmosphere, reflecting the cottage-style bakery. Soft colors, clean typography, and minimalistic visuals aim to create a sense of warmth and trust. Visual hierarchy is maintained through simple layouts, with clear navigation and call-to-action elements. Icons and buttons are used sparingly but effectively, ensuring that users can navigate and interact with the site without confusion. The use of whitespace and large, readable fonts ensures that the content feels approachable and not overwhelming, whether viewed on a large desktop screen or a small mobile device.

## Database Design

### Database Model

The database for `Lea Cottage` is structured to be scalable and efficient, adhering to the DRY (Don't Repeat Yourself) principle. The **StockItem** table is central to this design, linking multiple models and efficiently storing item quantities, preservation methods, and reservations without duplication of data.

The initial design of the entity-relationship diagram (ERD) captures the core models of the system, including the relationships between bakery items, ingredients, stock, and reservations. Every part of the model is carefully constructed to ensure maximum reuse and minimal redundancy.

### ERD

Below is a visual representation of the database model for the `Lea Cottage` project:

![ERD](docs/erd-lea-cottage.png)

### Custom Models

The database includes several custom models tailored specifically to the needs of `Lea Cottage`:

- **StockItem**: At the heart of the system, the `StockItem` model tracks available inventory, linking each stock entry to the item it represents, along with its preservation method, quantity, and reservation status. By centralizing this information in one model, the application adheres to the DRY principle, avoiding unnecessary duplication across tables.

- **MyReservation**: This model is used to track the reservations made by users, including details such as reservation notes and the date of reservation. It is linked to the `User` model, which represents the customers of the bakery, and connects to `StockItem` to allow users to reserve items.

These models make use of foreign key relationships to keep the data model clean and flexible. For example, instead of duplicating ingredient data across multiple item entries, the `Item` and `Ingredient` models are connected via a many-to-many relationship. This approach reduces redundancy and keeps the database optimized.

### CRUD Functionality

The CRUD (Create, Read, Update, Delete) principle is foundational to the design of the database and the entire application:

- **Create**: Authenticated users can create reservations, adding specific `StockItem` entries to their reservations. Administrators can add new items and update inventory using the `StockItem` model.

- **Read**: Both users and admins can view products (items), their available stock, and details like ingredient lists and preservation methods.

- **Update**: Users can update their reservations, modifying reservation details such as date and notes before finalizing the reservation. Admins can update stock levels and item details.

- **Delete**: Users can delete their reservations before they are finalized, and admins can remove items or stock entries from the system if they are no longer available.





# Lea Cottage Home Bakery Project - Automated Testing

This project includes automated testing for the **Lea Cottage Home Bakery** web application. The tests cover models, forms, and views to ensure everything functions as expected.


## Requirements

Ensure you have the following installed to run the tests:

1. **Python python-3.9.20.x**
2. **Django 4.2** 
3. **sqlite3** 
4. **Virtual environment (optional)**

## Setup

### 1. Clone the Repository
If you haven't already cloned the project, use the following command:

```bash
git clone <rhttps://github.com/behemot-biz/lea-cottage.gitl>
cd <repository-folder>
```

### 2. Create a Virtual Environment (Optional)
If you wish to run the project in an isolated environment, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
Install the necessary packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Set Up Database
Ensure you have set up your database configurations. Make sure the test database configurations are correct in your `settings.py` or in your environment variables.

### 5. Migrate the Database
Apply migrations to set up your test database:

```bash
python manage.py migrate
```

## Running Tests

### Run All Tests

You can run all tests using Django's `test` command:

```bash
python manage.py test
```

This will automatically detect and run tests from `tests_models.py`, `tests_forms.py`, and `tests_views.py`.

### Run Specific Test Modules

You can also run specific test modules:

```bash
python manage.py test reservation.tests_models
python manage.py test reservation.tests_forms
python manage.py test reservation.tests_views
```

## Test Structure

### `tests_models.py`
This file contains tests related to the models in your project. These tests ensure that:
- Reservations are created correctly.
- The relationships between models, such as `StockItem` and `MyReservation`, work as expected.
- Status updates (like marking reservations as complete) function properly.

### `tests_forms.py`
This file contains tests for the forms in the project. It ensures that:
- Forms are validated correctly.
- Required fields are present.
- Validation rules (like valid dates) are enforced.

### `tests_views.py`
This file tests the views in your project to make sure they return the correct responses. It includes tests such as:
- Successful reservation submissions.
- Adding items to reservations.
- Handling invalid form submissions.
- Ensuring appropriate redirects.

## Notes

- **Database**: The tests will run using a test database, which Django creates and destroys automatically for each test run.
- **Messages**: Be sure to match any success or error messages in the views with the assertions in the tests.
- **Edge Cases**: It's a good idea to write additional tests for edge cases, such as invalid form submissions or unauthorized access.

For any issues or suggestions, feel free to open a discussion or submit a pull request.

## Technologies Used

### Work Environments and Hosting

- **Photoshop: Used for creating wireframes to visualize the design and layout of the application before and during development.
- **[DBDiagram](https://https://dbdiagram.io/)**: Used to design the Entity-Relationship Diagrams (ERDs) and to visualize the database structure of the project.
- **[GitHub](https://github.com/)**: Version control system used to manage the codebase, track changes, and collaborate on the project.
- **VSCode**: Used for writing and running the project’s code during development.
- **[Heroku](https://heroku.com/)**: Hosting platform used to deploy and manage the live version of the application.
- **[Cloudinary](https://cloudinary.com/)**: Used for serving static and media files, including images for the items in the bakery.

### Python Libraries

- **[Gunicorn](https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/gunicorn/)**: A Python WSGI HTTP server used to serve the application in a production environment on Heroku.
- **[psycopg2](https://pypi.org/project/psycopg2/)**: PostgreSQL adapter for Python, used to manage the connection between Django and the PostgreSQL database.

### Django Libraries

- **[django-allauth](https://django-allauth.readthedocs.io/en/latest/)**: Provides user authentication, including signup, login, and social authentication.
- **[django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)**: Controls the rendering of Django forms, allowing for cleaner and more customized form layouts.

### External Libraries and Applications

- **[Whitenoise](https://whitenoise.evans.io/en/latest/)**: A library used for serving static files in production, without requiring external file servers.
- **[Summernote](https://summernote.org/)**: A WYSIWYG editor that is currently installed for potential future use, allowing for rich text content management.

### Database

- **[PostgreSQL] **: PostgreSQL from Code Institute.

## Deployment

This project was deployed using [Heroku](https://heroku.com/), [Cloudinary](https://cloudinary.com/), and [Whitenoise](https://whitenoise.evans.io/en/latest/). The PostgreSQL database was provided by the Code Institute as part of the course infrastructure. For a full list of libraries and technologies used, refer to the [Technologies Used](#technologies-used) section.

### Installing Libraries

The following steps outline the necessary libraries for successful deployment on Heroku. All additional configuration updates, such as changes to `settings.py`, are assumed as logical follow-up steps once the libraries are installed. For full details on how to install these libraries, refer to the relevant links in the [Technologies Used](#technologies-used) section.

- Install **Django** and **Gunicorn** (server used to run Django on Heroku):  
  ```bash
  pip3 install django gunicorn
  ```
- Install **psycopg2** (to connect to PostgreSQL):  
  ```bash
  pip3 install dj_database_url psycopg2
  ```
- Install **Cloudinary** (to host static files and images):  
  ```bash
  pip3 install dj3-cloudinary-storage
  ```
- Install **Whitenoise** (to serve static files and prevent issues with custom stylesheets on Heroku):  
  ```bash
  pip3 install whitenoise
  ```

### Creating the Heroku App

1. Log in to Heroku and navigate to your dashboard.
2. Click **New** and select **Create new app**.
3. Enter an appropriate name for your app and choose the relevant region.
4. Click **Create App**.

### Setting up the PostgreSQL Database

Since the database is provided by the Code Institute, no additional setup is required through ElephantSQL. The PostgreSQL database is managed as part of the provided infrastructure. Ensure your Django settings point to the provided database URL, which will be made available in your environment settings.

### Hiding Sensitive Information

1. Create an `env.py` file in your project root and ensure it is included in your `.gitignore` file.
2. Add the following code to `env.py` to set up environment variables:
   ```python
   import os
   os.environ["DATABASE_URL"] = "<your_database_url>"
   os.environ["SECRET_KEY"] = "<your_secret_key>"
   os.environ["CLOUDINARY_URL"] = "<your_cloudinary_url>"
   ```
3. In your `settings.py` file, modify the top of the file to import the environment variables:
   ```python
   import os
   import dj_database_url
   if os.path.isfile('env.py'):
       import env
   ```
4. Replace the insecure Django-provided secret key with the environment variable:
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

### Update Settings for the Database

1. To connect to the database provided by the Code Institute, update the `DATABASES` setting in `settings.py`:
   ```python
   DATABASES = {
       'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
   }
   ```
2. Run migrations to apply the database changes:
   ```bash
   python3 manage.py migrate
   ```

### Configuring Heroku

1. In your Heroku dashboard, go to the **Settings** tab.
2. Add the following Config Vars:
   - **DATABASE_URL**: The URL of the provided database.
   - **SECRET_KEY**: Your secret key for Django.
   - **CLOUDINARY_URL**: Your Cloudinary API environment variable.
   - **PORT**: Set this to `8000`.

### Connecting to Cloudinary

1. In your Cloudinary dashboard, copy the **API Environment Variable**.
2. In `env.py`, add the following:
   ```python
   os.environ["CLOUDINARY_URL"] = "<your_cloudinary_url>"
   ```
3. In your Heroku Config Vars, add the same `CLOUDINARY_URL`.

4. In `settings.py`, modify the `INSTALLED_APPS` list:
   ```python
   INSTALLED_APPS = [
       'cloudinary_storage',
       'django.contrib.staticfiles',
       'cloudinary',
       # other installed apps
   ]
   ```
5. Configure static and media file storage in `settings.py`:
   ```python
   STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

#### Allow Heroku as host

- In ``settings.py`` add
    ````
    ALLOWED_HOSTS = ['app-name.herokuapp.com', 'localhost']
    ````

## Development

The following options are available for working with this codebase or running the project in a local environment.

### Fork

Forking the repository allows you to create your own copy of the project under your GitHub account. Any changes made to a forked repository do not affect the original repository.

- Log into GitHub and navigate to the main repository ([lea-cottage](https://github.com/behemot-biz/lea-cottage.git)).
- Click the **Fork** button in the top right-hand corner.
- Choose a different owner (if necessary) or leave it as your account.
- Click **Create Fork**.
- You now have your own forked version of the repository, which can be cloned or modified without impacting the original.

### Clone

Cloning the repository allows you to download the full project to your local machine and make changes that will affect the original repository if you push them back (unless it's a forked instance).

- Navigate to the main page of the repository ([lea-cottage](https://github.com/behemot-biz/lea-cottage.git)).
- Click on the **Code** dropdown above the list of files.
- Choose a method to copy the URL for the repository:
  - **HTTPS**
  - **SSH key**
  - **GitHub CLI**
- Open your terminal or Git Bash and navigate to the directory where you want to clone the repository.
- Run the following command, replacing `URL` with the copied URL:
  ```bash
  git clone URL
  ```
- Press **Enter** to start cloning the repository to your local machine.

### Download as ZIP

If you prefer not to use Git, you can download the repository as a ZIP file.

- Log into GitHub and navigate to the main repository ([lea-cottage](https://github.com/behemot-biz/lea-cottage.git)).
- Click on the **Code** dropdown and select **Download ZIP**.
- Once the download is complete, extract the ZIP file to your desired location.
- You can now open and work on the project in your local environment.
