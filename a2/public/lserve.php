<?php
require_once('lib/nusoap.php');

class Product{
    public $id;
    public $pname;
    public $price;

    public function __construct($id,$pname,$price){
        $this->id=$id;
        $this->pname=$pname;
        $this->price=$price;
    }

    public function toArr(){
        return array('id'=>$this->id,'pname'=>$this->pname,'price'=>$this->price);
    }
}



// Create the server instance
$server = new soap_server();
// Initialize WSDL support
$namespace="http://ikno.ws/wsdl";

$server->configureWSDL('mywsdl',$namespace);
$server->wsdl->schemaTargetNamespace = $namespace;


$server->wsdl->addComplexType(
    'Product',
    'complexType',
    'struct',
    'all',
    '',
    array(
        'id'=>array(
            'name'=>'id',
            'type'=>'xsd:integer'),
        'pname'=>array(
            'name'=>'pname',
            'type'=>'xsd:string'),
        'price'=>array(
            'name'=>'price',
            'type'=>'xsd:double')

        )
    );
$server->wsdl->addComplexType(
    'Products',
    'complexType',
    'array',
    '',
    'SOAP-ENC:Array',
    array(),
    array(
        array('ref'=>'SOAP-ENC:arrayType',
            'wsdl:arrayType' => 'tns:Products[]')
        ),
        'tns:Product'
    );
$server->register('Catalog',
    array(),
    array('return'=>'tns:Products'),
    $namespace,
    $namespace.'#Catalog',
    'rpc','encoded','Gets the catalog of products'
);

// Register the method to expose
$server->register('Price',                // method name
    array('id'=>'xsd:integer','qty'=>'xsd:integer'),        // input parameters
    array('return' => 'xsd:double'),      // output parameters
    $namespace,                      // namespace
    $namespace.'#Price',                // soapaction
    'rpc',                                // style
    'encoded',                            // use
    'Gets the price of a specific product'            // documentation
);
$prods = array(1=>new Product(1,'ham',12.99),2=>new Product(2,'cheese',6.99),3=>new Product(3,'pickles',5.99),4=>new Product(4,'chicken soup',2.99),5=>new Product(5,'missile',567349.90));
// Define the method as a PHP function
function Catalog(){
    global $prods;
    foreach ($prods as $prod){
        $arr[] = $prod->toArr();
    }
    return $arr;
}
function Price($id,$qty) {
   global $prods; 
    return $prods[$id]->price*$qty;
}
// Use the request to (try to) invoke the service
$HTTP_RAW_POST_DATA = isset($HTTP_RAW_POST_DATA) ? $HTTP_RAW_POST_DATA : '';
$server->service($HTTP_RAW_POST_DATA);
?>
