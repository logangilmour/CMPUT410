Assignment 2 - CMPUT 410 Winter 2012
Logan Gilmour

Given the technology constraints, I decided to implement this application as one big perl CGI. Since the user never gets a permanent username or other permanent identification token assigned to him/her, I elected to store all application state on the client in a custom-built key-value store. 

I built the key-value store on top of hidden form elements, as cookies were not allowed in this assignment.

Javascript is used for validation and submission of the form containing the key-value store when the user switches tabs. The requested tab is part of the POST request as another hidden element.

The CGI uses a small army of helper subroutines to customize the main chunk of HTML stored as a multi-line string within the CGI script (index.cgi). The server could easily store submitted information, email it, etcetera, but that was not part of the spec. Right now the server only renders HTML/Javascript and manages the datastore.

I'm used to much higher level tools than CGI with no cookies - as result, I found I wrote some pretty hairy spaggetti code to get things working.


