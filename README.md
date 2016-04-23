# Pick-backend
Pick Backend Code

Well these are the project specifications. Our Service is called Pick.
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
2- Sender submits a new order (with the specified information bellow).
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

How to register with social app

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

