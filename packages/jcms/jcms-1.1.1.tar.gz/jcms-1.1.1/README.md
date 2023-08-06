# Jcms

Jcms is an easy to use cms for Django(python)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The only thing that you need to have installed is pip. But if you haven't this means you are also not using django which you should.

### Installing

Jcms is easy to install. First you install it via pip

```
pip install jcms
```

<br/>
Now you can add Jcms to INSTALLED_APPS in your settings file.

```python
INSTALLED_APPS = [
    'jcms'
]
```

<br/>
After this you need to add the urls to your urls.py. You can replace admin with everything you want.

```python
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', include('jcms.urls')),
]
```

Now to add a user you can do this via the commandline. Find more on this in the [documentation of Django](https://docs.djangoproject.com/en/1.11/topics/auth/default/)

<br/>
Now go to your site's url and do the /admin/ (or if you have chosen another path type that). You can now log in with the credentials you just created.


## Adding menu items

You can add menu items and urls to jcms. This means that the urls you add are connected to the Jcms app.

What you first have to do is add the jcms folder to the app. The file structure of the app is underneath

```
practice-app
    jcms
    migrations
    static
    templates
    other-folders
```

Everything for jcms can be done in the jcms folder. I opt to make the views in a views folder.

### Basic crud view

This is a basic example of a crud view for jcms.

```python
from dishes.models import Dish
from jcms.mixins.jcms_crud import JcmsCrud


class DishesView(JcmsCrud):
    model = Dish
    create_edit_list = ['number', 'name', 'price', 'menu_of_the_month', 'subtitle', 'category', 'image']
    list_fields = ['number', 'name', 'category']

```

The following options can be given:
* model = The model this crud is for
* create_edit_list = This is an array of items which you can create and edit in these views
* list_fields = This is a list of fields of the model which are shown in the list view

This makes the following views:
* Create. Viewname is ${model_name_lower}Create
* Edit. Viewname is ${model_name_lower}Edit
* List. Viewname is ${model_name_lower}List
* Delete. Viewname is ${model_name_lower}Delete

### Adding Jcms urls

First you need to create a urls.py in the jcms folder. WARNING: This has to be done in the jcms folder. Make sure you copy the example and replace the variables with yours.

```python
from dishes.views import dishesViews, categoryViews, sauceViews
from jcms.helpers import functions

cruds = [
    dishesViews.DishesView,
    categoryViews.CategoriesView,
    sauceViews.SaucesView,
]

urlpatterns = functions.add_crud(cruds)
```

The only thing you need to edit for this is the first line where the views are imported and the content of the crud array.


### Making the menu items

First you need to create a menu_item.py in the jcms folder. WARNING: This has to be done in the jcms folder. Make sure you copy the example and replace the variables with yours.

```python
from jcms.mixins.menu_item import MenuItem as GenericMenuItem
from jcms.helpers.menu_item import MenuItem as SingleMenuItem


class MenuItem(GenericMenuItem, object):
    slug = 'dishes'
    name = 'Dishes'
    icon = 'dish'

    items = [
        SingleMenuItem('Dishes', 'dishList'),
        SingleMenuItem('Categories', 'categoryList'),
        SingleMenuItem('Sauces', 'sauceList'),
    ]
```

You can give the following options:
* slug = The slug used in the url
* name = The name seen on the menu item
* icon = The svg used for the menu item. If there is no icon given it uses the fallback svg
* items = All the options in the menu item. This HAS to be a SingleMenuItem Object.

### Adding your menu item to jcms

The last step is to add the menu item to jcms. You can do this by going to your django settings and adding this line.

```python
JCMS_APPS = ['practice-app']
```

This are only the apps that should be in Jcms.

## Icons
You can use these icons like this:
```
{% include "icons/[icon-name].svg" %}
```

The icons you can use are =:
- add
- delete
- dropdown-caret
- edit
- groups
- hamburger
- home
- logout
- options
- standard-menu-item
- users
- cancel

## Templatetags

These are the template tags that you can use that are in Jcms

### add_item

Add a item to an array

```
{% load add_item %}
{% add_item array new_item as array %}
```

### crud_url

Load a crud url based upon the model

```
{% load crud_url %}
{% url "Create"|crud_url:model %}
```

### get_model_items

Get menu items for the cms

```
{% load get_menu_items %}
{% get_menu_items as menu_items %}
```

### get_model_name

Gets the name of a model

```
{% load get_model_name %}
{{ view.model|get_model_name }}
```

### get_object_attr

Gets the attribute of a object dynamically

```
{% load get_object_attr %}
{{ object|get_object_attr:field }}
```

## Deployment

Ask **[Jessie Liauw A Fong](https://github.com/jessielaf)** to for deployment

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Pip](https://pypi.python.org/pypi/pip) - Dependency Management
* [Yarn](https://yarnpkg.com/) - Npm package manager

## Authors

* **[Jessie Liauw A Fong](https://github.com/jessielaf)**
