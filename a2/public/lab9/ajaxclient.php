<?php



require_once('lib/nusoap.php');

$client = new nusoap_client('http://ikno.ws/lab9/webservice.php?wsdl', true);

$value = $_GET['q'];
$ret = $client->call('convert', array('value' => $value));
echo $ret;
?>
