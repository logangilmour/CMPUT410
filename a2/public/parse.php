<HTML>
<HEAD>
<TITLE>
Assignment 4
</TITLE>
</HEAD>
<BODY>

<?php


$root = 'catalog';

$old = new DOMDocument;
$old->load($_GET["url"]);

$creator = new DOMImplementation;
$doctype = $creator->createDocumentType($root, null, './catalog.dtd');
$new = $creator->createDocument(null, null, $doctype);
$new->encoding = "utf-8";

$oldNode = $old->getElementsByTagName($root)->item(0);
$newNode = $new->importNode($oldNode, true);
$new->appendChild($newNode);

$new->validate();


//Initialize the XML parser
 
$parser=xml_parser_create();
 
/*Function to use at the start of an element*/

$products = array();

$product=NULL;
$current=NULL;
$title="";

function start($parser,$element_name,$element_attrs)
 
 {
	$current = $element_name;
	if($current=="PRODUCT"){
		$product=array();
	} 
 }
 
//Function to use at the end of an element
 
function stop($parser,$element_name)
 
  {
	if($current=="PRODUCT"){
		$products[]=$product;
	}
  }
 
//Function to use when finding character data
 
function char($parser,$data)
 
  {
	if($current=="title"){
		$title.=$data;
		return;
	}
	$product[$current].=$data;
  }
 
//Specify element handler
 
xml_set_element_handler($parser,"start","stop");
 
//Specify data handler
 
xml_set_character_data_handler($parser,"char");
 
//Open XML file
 
$fp=fopen($_GET["url"],"r");
 
//Read data
 
while ($data=fread($fp,4096))
 
  {
 
    xml_parse($parser,$data,feof($fp)) or
 
    die (sprintf("XML Error: %s at line %d",
 
    xml_error_string(xml_get_error_code($parser)),
 
    xml_get_current_line_number($parser)));
 
  }
 
//Free the XML parser
 
xml_parser_free($parser);

function comp($a,$b){
	if($a['NAME']==$b['NAME']){
		$av = $a['QUANTITY']*$a['VALUE'];
		$bv = $b['QUANTITY']*$b['VALUE'];
		if($ab==$bv){
			return 0;
		}
		return $ab>bv?1:-1;
	}
	return $a['NAME']>$b['NAME']?1:-1;
}
usort($products,'comp');
$s = "</TD><TD>";
echo "<TR><TH>Product$h Name$h Description$h Price$h Quantity$h Image</TH></TR>
foreach ($products as $p){
	echo "<TR><TD>".$p['PRODUCT'].$s.$p['NAME'].$s.$p['SPECS'].$s.
	$p['PRICE'].$s.$p['QUANTITY'].$s.
	"<IMG SRC='".$p['IMAGE']."'></TD></TR>";
}
?>
</BODY>
</HTML>
