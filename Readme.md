# **Students Portal**

![image](https://scontent-waw1-1.xx.fbcdn.net/v/t35.0-12/21764131_1539065169469950_807266089_o.png?oh=7b7d17b9338aabf0c43fd7308cb315c2&oe=59C30B08)

# Introduction

*We wanted to create a page where **students** will be able to **share** their own **recipes**. Our **aim** was to make
that page look **clear** and **readable**.*

*So, we made a page where all **variables** included in recipe are **divided**. There are **separated** fields for: ingredients,
instructions, title, photo and author. Thanks to it recipes on our page are **easier to read**.*

![image](https://user-images.githubusercontent.com/26097838/30609314-647db020-9d7b-11e7-8b9c-06135f82a121.png)

# Installation

* First you need to install Python 3.6.2
* Next install **Django** by writing in your terminal: *$ pip install Django==1.11.4*
* Install **django-extensions** by writing: *$ pip install django-extensions*

# Usage

* *$ python manage.py runserver*
* enter ip address and port number in your browser

# Detailed description

Our project is based on **Django** - the Web framework.

For every part of **recipe** we have different class model. Every model is somehow **related** to another.
Most of relations are ManyToMany relations.

![image](https://user-images.githubusercontent.com/26097838/30642207-3652fe82-9e0a-11e7-8ada-15e23e36d9a2.jpg)

As you can see on first image in Readme, we have got **recipe-matcher** which finds recipes with chosen ingredients.
It returns a list of recipes sorted by the amount of matching ingredients.

**Search-field** and **ingredient-field**(in add-recipe form) are using jQuery autocomplete to suggest to user
already existing recipes/ingredients.

We have prepared **likes** functionality, to create **ranking** of active users.
