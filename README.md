## FOOD DELIVERY 

### DESCRIPTION 
It's a RESTful API for a food delivery service. Users can use the API to browse restaurants, see menus or items, place orders, and manage order fulfillment. It was created with Python, Flask and SQLite database.
#### CHALLENGES FACED 
* One of the major challenges I faced was when a user is updating a placed order. In this case the order has been placed, payment made and quantity of items reduced based on the order amount. I solved this problem by firstly returning the amount paid by the user likewise the quantity of items order. This was to ensure that there is no cheating on either side of the entities. After that, I then update the order taking into consideration the new ordering details.
* As am wrapping up this project based on deadline, some of the features I wish to add are system testing although unit and integration tests was written,  and update and delete of menu items.

### INSTALLATION GUIDE 
* Clone the project git clone _project url_
* cd into the project root directory
* create a virtual environment using ```pip install venv <virtual_name>``` where <virtual_name> is your env name eg. ```food-delivery-env``` as env name. If not clear copy, paste and run ```pip install venv food-delivery-env```
* Activate virtual environment ```source <virtual_name>/bin/activate```. But you used ```food-delivery-env``` as your env then use this ```source food-delivery-env/bin/activate``` in your terminal far left of the console will appear as ```(food-delivery-env)``` which means env is activated where the word in the parenthesis is your environment name
* Installing dependencies from the ```requirements.txt```. Copy, paste and run this ```pip install -r requirements.txt```
* Runnig the server ```python app.py``` you should see ``` Running on http://127.0.0.1:5001/ (Press CTRL+C to quit) ```
* Congratulations you have started server. If you have issues and need assistance contact me asap on Linkedin

### HOW TO USE THE PROJECT 
There are 2 types of users in the system. it create an admin or superuser the email should start with <admin> example ```admin@filler.io```, for a normal user any email we be ok eg. kofi@epals.com. Also, when a user is created, the user as a wallet balance worth of 50.0 at the the time of this documentation.
#### HOW TO USE THE RESOURCES 
```User Registration```

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |
