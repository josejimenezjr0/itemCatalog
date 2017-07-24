# Udacity Project Item Catalog

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Setup

- Make sure you have the following installed:
    - python
    - git
    - Vagrant
    - VirtualBox

- Clone the master fork from https://github.com/josejimenezjr0/itemCatalog.git
- Clone the Vagrant machine from Udacity from https://github.com/udacity/fullstack-nanodegree-vm
- Move the contents of the cloned fork to the Vagrant shared directory
- Inside the vagrant subdirectory run the command `vagrant up` then `vagrant ssh`
- cd into /vagrant/catalog and run `createdb itemcatalog.db`
- then run the following three lines:
    - `python databasesetup.py`
    - `python populate_db.py`
    - `python project.py`

## How to Run

The site should now be accessible from your localhost at port 5000: `localhost:5000`. You can login and begin making changes or browsing the items. If you want different items populated initially you can modify the contents of the `populate.db` file.

#### Access JSON

The JSON API endpoint is accessible at `localhost:5000/JSON`