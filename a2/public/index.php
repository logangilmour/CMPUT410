<html>
<head>
<title>Assignment 5</title>
</head>
<body>

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
        return array('id'=>$id,'pname'=>$pname,'price'=>$price);
    }

    public static function fromArr($arr){
        return new self($arr['id'],$arr['pname'],$arr['price']);
    }

    public function render(){
        return '<tr><td>'.$this->id.'</td><td>'.$this->pname.
        '</td><td>'.$this->price.
        '</td><td><form method="GET"><input type="text" name="qty">'.
        '<input type="hidden" name="id" value="'.$this->id.'">'.
        '<input type="hidden" name="name" value="'.$this->pname.'">'.
        '<input type="submit" value="calculate price"></form>';
    }
}

$client = new nusoap_client('http://ikno.ws/lserve.php?wsdl', true);

$id = $_GET['id'];
$qty = $_GET['qty'];
$name = $_GET['name'];
if($id==NULL){
?>
<table border=1>
<tr><th>Id</th><th>Name</th><th>Price</th><th>Bulk Price Calculator</th></tr>
<?

$result2 = $client->call('Catalog',array());
foreach($result2 as $prod){
    $product = Product::fromArr($prod);
    echo $product->render();
}
?>
</table>
</html>
<?
}else{
if(!is_numeric($qty)){
    echo "'$qty' is not a valid quantity.";
}else{
$total = $client->call('Price', array('id' => $id,'qty'=>$qty));
echo "Price of $qty ".$name."s is \$".$total;
}
?><br><a href='/index.php'>Back</a></html><?}?>
