# [Item Catalog]http://leilanixann.pythonanywhere.com/
version deployed does not require user login

This is a project for Udacity's Full Stack Nanodegree: Item Catalog Project 

## Features
<ol>
  <li>Facebook Login</li>
  <li>CRUD Item/Catalog operations</li>
  <li>Only users may edit/delete/add new items</li>
  <li>JSON Endpoints</li>
</ol>
| Request | What you get | 
| ------------- |:-------------:|
| /catalog/JSON | Get all Categories |
| /catalog/*category ID*/items/*item ID*/JSON | Get a single item |
| /catalog/*category ID*/items/JSON | Get all items that belongs to the given catgeory



## Quick start

To run this file, you'll need Vagrant and VirtualBox installed.

VirtualBox can be downloaded here: https://www.virtualbox.org/wiki/Downloads Vagrant can be found here: https://www.vagrantup.com/downloads.html

Once you have Vagrant and VirtualBox up and running, open a command prompt and navigate to vagrant/ inside this directory, and run the following commands:
```
vagrant up
```
```
vagrant ssh
```
```
cd /vagrant/catalog
```
```
python items.py (to populate database)
```
``` 
python project.py
```

Go to http://localhost:5000 to see app running


## Creator

**Leilani Raranga**

* <https://twitter.com/leilanirar>
* <https://github.com/leilaniann>


## Copyright and license

Copyright © 2016, [Leilani Raranga](http://github.com/leilaniann). 
Released under the [MIT license](https://github.com/helpers/helper-copyright/blob/master/LICENSE). 
Brand Icons: Font Awesome by Dave Gandy - http://fontawesome.io
