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
There are 2 types of users in the system. it create an admin or superuser the email should start with <admin> example ```admin@filler.io```, for a normal user any email we be ok eg. ```kofi@epals.com```. Also, when a user is created, the user as a wallet worth of 50.0 at the the time of this documentation whilst admins have 0.0 of wallet worth.

#### HOW TO USE THE RESOURCES 

##### NOTE THE FOLLOWING 

1. ALL APIs MUST START WITH THE BASE_URL = ```http://127.0.0.1:5001```
2. EXAMPLE SHOWN IN THE FIRST 2 RESOURCES, REGISTRATION AND LOGIN
3. ANY NAME IN ANGLE BRACKET IS A PATH VARIABLE EG. ```BASE_URS/api/<name>```
4. ALL APIs WITH OR CONTAIN ```admin``` ARE ADMIN RESOURCES OR APIs
5. ALL APIs REQUIRE AUTHENTICATION AND OR AUTHORIZATION EXCEPT GET ITEM(S) AND RESTAURANT(S) APIs

##### REGISTRATION =>  POST: ```{{BASE_URL}}/api/register```
 
{
    "email": "vida@turntabl.io",
    "firstName": "Angelina",
    "lastName": "Kyeah",
    "password": "thanks",
    "imageUrl": "image"
}

##### LOGIN => POST: ```{{BASE_URL}}/api/login```
NB: If admin you are provided with refresh token while a user is access token

   **sample request details**
   
{
    "email": "vida@turntabl.io",
    "password": "thanks"
}

##### ALL USERS GET: ```{{BASE_URL}}/api/users/admin```

##### GET USER BY EMAIL ADMIN RESOURCE  DELETE: ```/api/users/admin/<email>```
##### GET: api/items
##### POST: /api/admin/items

**Sample Requests Details **

NB: ImageUrl is Optional 

{
    "name": "leaf",
    "description": "organic",
    "price": 30.5,
    "imageUrl": "image",
    "qty": 10
}

##### POST: _api/admin/restaurants_

**Sample Request Details**
NB: itemId must exists before reference, worry not the response will guide you if you forget.

{
    "name": "Papaye",
    "city": "Accra",
    "itemId": 2
}

##### GET: _/api/restaurants_
##### GET: _/api/restaurants/<name>_
##### PUT: _api/admin/restaurants/<name>_

**Sample Request**
NB: itemId must exists before reference, worry not the response will guide you if you forget.

{
    "name": "bread",
    "city": "Accra",
    "itemId": 3
}

##### DELETE: _api/admin/restaurants/<name>_
##### POST: _api/orders/place/users_

**Sample Request**

{
 "qty": 1,
 "userId": 16,
 "itemId": 5
}

##### GET: ```api/orders/<email>/<orderId>```
##### PUT: ```api/orders/<email>/<orderId>```

**Sample Request**

```{
    "qty": 1
}```

##### DELETE: ```api/orders/<email>/<orderId>```
##### GET: ```api/orders/admin```
##### PUT: ```api/admin/orders/fulfilment```

**Sample Requests Details**

```{
    "email": "vida@turntabl.io",
    "orderId": 2
}```
