Assignment 4 - CMPUT 410 Winter 2012
Logan Gilmour

My application is running at http://ikno.ws

I implemented this assignment in php. I did the actual parsing and rendering
using expat, then realized that it didn't support validation (which I wanted
to use to make sure the given xml is good). To validate againts the DTD
contained here, I loaded the xml with DOMDocument and then injected the DTD
before validating (as we assume the DTD won't be specified with the given
XML.)

