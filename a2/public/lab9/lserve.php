<?php
require_once('lib/nusoap.php');

// Create the server instance
$server = new soap_server();
// Initialize WSDL support
$namespace="http://ikno.ws/wsdl";

$server->configureWSDL('mywsdl',$namespace);
$server->wsdl->schemaTargetNamespace = $namespace;

// Register the method to expose
$server->register('convert',                // method name
    array('value'=>'xsd:double'),        // input parameters
    array('return' => 'xsd:double'),      // output parameters
    $namespace,                      // namespace
    $namespace.'#convert',                // soapaction
    'rpc',                                // style
    'encoded',                            // use
    'converts feet to meters'            // documentation
);

function convert($value) {
    return $value*0.3048;
}
// Use the request to (try to) invoke the service
$HTTP_RAW_POST_DATA = isset($HTTP_RAW_POST_DATA) ? $HTTP_RAW_POST_DATA : '';
$server->service($HTTP_RAW_POST_DATA);
?>
