# Pick-backend

These are the project specifications. Our Service is called Pick.
Pick is uber style parcel delivery. It allows users to send parcels from anywhere to anywhere.


Delivery management is going to be done using external service called getswift.co.

Actors:
Seller:
Who wants his order to be delivered to his customer (buyer).
Seller could be a physical store, or an e-commerce seller, in this doc usually called Sender.
Buyer:
Who is the customer of the seller, he is the receiver of the order that placed by the sender. Buyer could be anyone, one time user so the buyer is not a direct app user.And doesn't have to login.
In this document, buyer usually called Receiver.
Glossary:
Order: which is the shipment (parcel) that is going to be delivered from the sender to the receiver.


The process goes like this :
1- Sender logs in using one of our apps.
2- Sender submits a new order (with the specified information below).
3- When Order is submitted an sms is sent to the receiver with a link to specify his location.
4- When receiver submits his/her location delivery job gets submit to the delivery management api(specified above).
5- When driver completes the job the delivery management will notify our system using a web-hook.


Order information :
1- Pick-up address.
2- Destination (Drop off). 
3- Destination address: already known through the second screen. 
4- Contact name: name of the receiver who is will receive the order.
5- Phone: phone of the receiver who is will receive the order.
6- Scheduled pick-up time
7- Scheduled drop-off time
8- Items: predefined categories
9- Payment type: COD (Cash On Delivery) and pre-paid.


Sender information:
1- Full name.
2- Phone number.		*
3- email.
4- gender.				*
5- Store url.			*
6- default location.	*
7- Package type (Based on predefined packages)	*

How to register with social app (django-allauth documentation)

- Twitter

	You will need to create a Twitter app and configure the Twitter provider for your Django application via the admin interface.
	App registration

	To register an app on Twitter you will need a Twitter account after which you can create a new app via:

	https://apps.twitter.com/app/new

	In the app creation form fill in the development callback URL:

	http://127.0.0.1:8000

	Twitter won’t allow using http://localhost:8000.

	For production use a callback URL such as:

	http://{{yourdomain}}.com

	To allow user’s to login without authorizing each session select “Allow this application to be used to Sign in with Twitter” under the application’s “Settings” tab.
	App database configuration through admin

	The second part of setting up the Twitter provider requires you to configure your Django application. Configuration is done by creating a Socialapp object in the admin. Add a social app on the admin page:

	/admin/socialaccount/socialapp/

	Use the twitter keys tab of your application to fill in the form. It’s located:

	https://apps.twitter.com/app/{{yourappid}}/keys

	The configuration is as follows:

	    Provider, “Twitter”
	    Name, your pick, suggest “Twitter”
	    Client id, is called “Consumer Key (API Key)” on Twitter
	    Secret key, is called “Consumer Secret (API Secret)” on Twitter
	    Key, is not needed, leave blank


- Instagram

	App registration:
	    https://www.instagram.com/developer/clients/manage/
	Example valid redirect URI:
	    http://localhost:8000/accounts/instagram/login/callback/

- Email

	ACCOUNT_AUTHENTICATION_METHOD = 'email'
	ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
	ACCOUNT_SIGNUP_PASSWORD_VERIFICATION  = False
	ACCOUNT_UNIQUE_EMAIL = True
	ACCOUNT_USERNAME_REQUIRED = False
	EMAIL_CONFIRMATION_SIGNUP = True
	ACCOUNT_UNIQUE_USERNAME = False

	ACCOUNT_EMAIL_REQUIRED = True
	ACCOUNT_CONFIRM_EMAIL_ON_GET = True
	ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
	ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5


	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_HOST_USER = 'test@gmail.com'
	EMAIL_HOST_PASSWORD = 'password'
	EMAIL_PORT = 587
	EMAIL_USE_TLS = True
	DEFAULT_FROM_EMAIL = 'test@gmail.com'
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


How to send SMS using twilio (twilio documentation)

	Create twilio an account.
	Register AccountSID, AuthToken
	Send request to twilio to send SMS.
	*** Phone number should be began with '+' sign.
	
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	client.messages.create(
		to=post.phone, 
		from_="+12025688404", 
		body="Please provide your address and confirm your order. http://api.pick.sa/order_confirm/%d/%s" % (post.id, post.key),  
	)


GetSwift API for delivery (getswift api documentation)

- Book a delivery

	POST api/v2/deliveries

	Booking a delivery is very similar to getting a quote. When booking, you will receive back details of the delivery as well as time estimates and price. You can open the examples by clicking on the link below, or see much more detailed information provided in the technical documentation.

	Request

	Below is a simple job booking example. As no pickup or finish time is specified, this delivery will be sent to our drivers immediately. Please note that only the pickup and drop-off addresses are mandatory. 

	{
	    "apiKey": "MERCHANT_KEY",
	    "booking":{
	        "pickupDetail": {
	            "name": "Rupert",
	            "phone": "1234567890",
	            "address": "57 luscombe st, brunswick, melbourne"
	        },
	        "dropoffDetail": {
	            "name": "Igor",
	            "phone": "0987654321",
	            "address": "105 collins st, 3000"
	        }
	    }
	}	

	Response

	The response contains pricing and time estimations (quote), a record of the delivery including the reference number and tracking links (request), as well as a copy of the data used to create the booking (delivery).

            

	{
	    "apiKey": "MERCHANT_KEY",
	    "booking":{
	        "pickupDetail": {
	            "name": "Rupert",
	            "phone": "1234567890",
	            "address": "57 luscombe st, brunswick, melbourne"
	        },
	        "dropoffDetail": {
	            "name": "Igor",
	            "phone": "0987654321",
	            "address": "105 collins st, 3000"
	        }
	    }
	}            

	Response

	The response contains pricing and time estimations (quote), a record of the delivery including the reference number and tracking links (request), as well as a copy of the data used to create the booking (delivery).
	            
	{
	    "quote": {
	        "created": "2015-03-17T00:44:29.4172047Z",
	        "start": "2015-03-17T00:44:00Z",
	        "distanceKm": 1.3,
	        "fee": {
	            "cost": 7.97,
	            "costCents": 797,
	        },
	        "pickup": {
	            "time": {
	                "average": "2015-03-17T00:59:00Z",
	                "earliest": "2015-03-17T00:44:00Z",
	                "latest": "2015-03-17T01:09:00Z"
	            },
	            "address": "67 Brunswick Street, Fitzroy VIC 3065, Australia"
	        },
	        "dropoff": {
	            "time": {
	                "average": "2015-03-17T01:21:00Z",
	                "earliest": "2015-03-17T00:59:00Z",
	                "latest": "2015-03-17T01:44:00Z"
	            },
	            "address": "105 Collins Street, Melbourne VIC 3000, Australia"
	        }
	    },
	    "delivery": {
	        "created": "2015-03-17T00:44:29.8390888Z",
	        "id": "4d9b9e22-1f0f-4b23-87bd-91b3938561ad",
	        "reference": "476",
	        "pickupLocation": {
	            "name": "Rupert",
	            "address": "67 Brunswick Street, Fitzroy VIC 3065, Australia",
	            "phone": "1234567890"
	        },
	        "dropoffLocation": {
	            "name": "Igor",
	            "address": "105 Collins Street, Melbourne VIC 3000, Australia",
	            "phone": "0987654321"
	        },
	        "lastUpdated": "2015-03-17T00:44:29.8390888Z",
	        "currentStatus": "Received",
	        "driver": null,
	        "items": [],
	        "pickupTime": null,
	        "dropoffTime": {
	            "earliestTime": "2015-03-17T00:59:00Z",
	            "latestTime": "2015-03-17T01:44:00Z"
	        },
	        "deliveryInstructions": "",
	        "trackingUrls": {
	            "www": "https://app.getswift.co/Tracking/TransportJob/5fe6b4a6-39ed-4f82-8e15-2296cfd5b567",
	            "api": "https://app.getswift.co/api/v2/deliveries/5fe6b4a6-39ed-4f82-8e15-2296cfd5b567"
	        }
	    },
	    "request": {
	        "reference": null,
	        "deliveryInstructions": null,
	        "itemsRequirePurchase": false,
	        "items": null,
	        "pickupTime": null,
	        "pickupDetail": {
	            "name": "Rupert",
	            "phone": "1234567890",
	            "email": null,
	            "description": null,
	            "addressComponents": null,
	            "address": "67 brunswick st, melbourne"
	        },
	        "dropoffWindow": null,
	        "dropoffDetail": {
	            "name": "Igor",
	            "phone": "0987654321",
	            "email": null,
	            "description": null,
	            "addressComponents": null,
	            "address": "105 collins st, 3000"
	        }
	    }
	}
	            
	