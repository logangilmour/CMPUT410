Assignment 3 - CMPUT 410 Winter 2012
Logan Gilmour

My Application is running at http://ikno.ws

I modified my previous perl script for this assignment, and added php invoice page.

Since I built a key-value store from hidden-form inputs on the last assignment, I was able to simply change the implementation of key-value store to cookie-based storage to accomodate the cookies requirement.

I Added CGI validation for quantities, emails, and postal-codes as I missed them in the previous assignment. I also added a validation confirmation box that allows the user to cancel the actions they've taken on a product page.

So I wouldn't have to rewrite (in php) the code that stores arbitrary product quantities into the value store, I instead have the main index.cgi perl script submit to itself for the 'checkout' tab, then write a redirect header pointing at [base-url]/invoice.php. This allows my cookies storage logic to stay in the perl script.

Sales tax is just a php associative array mapping to the value of the 'province' field in the store.

The main issue I noted is that php and perl serialize cookie-names slightly differently, so care must be taken when storing from one of them and then reading from another.
