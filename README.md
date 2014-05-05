DRA-fabric-tornado-couchdb-redis
===========

This is a **DRA** project using python fabric, tornado, couchdb and redis.

**DRA** implements the backend end side to **Swipe CMS**.

**Swipe CMS** is a convention for implementing 
content management systems for single page apps.

This convention is backend agnostic and front end agnostic.
What that means is that it doesn't matter what technologies
you use to implement them as long as they follow a certain convention
for allowing the different pieces of the project to communicate with each other.

This convention has two parts.
a **DRA** and **RPM** s.

a **DRA** stands for **Data**, **Routes**, and **Apps**.
This is the backend piece to **Swipe CMS**.

Data:
-----
Before you get started on creating any web application you need to decide on what
your data is going to be, how your data will be organized and what schema should it follow.


Routes:
-------
Once you decide on what your data is going to look like, you need to define 
the REST API endpoints in order to share or add to that data.
You will need to implement at least 2 endpoints,  */pages* and */data*.
the */pages* endpoint returns a data structure that represents the
pages hierarchy to your site.
the data endpoint returns a data structure which represents the data that those pages
use. 


Apps:
-----
once you have your data and routes figures out you then decide on what apps
you want in your project in order to manage that data or share it to the world.

you should have a minimum of two apps, an *admin* app and a *client* app.
the *admin* app serves as the administrator page to your site.
The *client* is the client part of your site which shares that data to rest of the world and can allow users to interact with it.

Each one of these apps follow a convention call **RPM**.

**RPM** stands for **Routes**, **Pages**, **Models**.

a **RPM** app is in charge of communicating with a **DRA** project getting the data structures from the */pages*
and */data* endpoint, in order to generate a web site.


Routes:
-------
here you define the routes to your app.  
each route is linked to a page item in the */pages* data structure.
when a route is triggered it will read that page item and generate the appropriate
page base on that data.



Pages:
------
here you define the templates to your pages. when a route is trigger it will read
it's associated page item from the */pages* data structure.  base on that information
it will tell our app which template we should use to generate the page and 
what data should we link it to, if any.

Models:
-------
this represents the data that your pages use, like blog posts or shopping items.
depending on the page it may not have a data item associated with it

- - -

a **DRA** project is technology agnostic.
Meaning that it doesn't matter what technology stack you use to implement this.
You can use python, ruby, node.js, or clojure.  it doesnt matter. As long as your 
project knows to create the */pages* and */data* data structures,  
the **RPM** apps has everything it needs to create a website.

- - -

this project has two branches.

*master*, and *admin*.

*admin*: is a rpm app that implements the admin piece to your site

*master*: is a rpm project that implements the client piece to your site


to get started

1. install node.js and npm
2. gem install compass
3. clone this project 
4. cd to your project and checkout the appropriate branch
3. npm install
4. bower install
5. grunt build

then Happy Hacking :)

