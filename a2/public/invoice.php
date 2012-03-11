<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>Assignment 1 - Checkout</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <LINK REL=StyleSheet HREF="style.css" TYPE="text/css" MEDIA=screen>
    <script type="text/javascript">
       function submitPage(num){
            document.getElementById('pageField').value=num;
            document.store.submit();
        }
  </script>
</head>
<?php
    
function safe($str){
    $str= strtolower($str);
    $str = str_replace(" ","-",$str);
    return $str;
}
function unsafe($str){
    $str = str_replace("-"," ",$str);
    $str = ucwords($str);
    return $str;
}
    $nameF="Name";
    $streetF="Street Address";
    $cityF="City";
    $provinceF="Province";
    $postF="Postal Code";
    $emailF="Email Address";
    $birthF="Birth Date"; 
    $provinces = array("alberta"=>0.05,"british-columbia"=>0.07,"manitoba"=>0.12,"new-brunswick"=>0.13,"newfoundland-and-labrador"=>0.13,"nova-scotia"=>0.13,"ontario"=>0.08,"prince-edward-island"=>0.105,"quebec"=>0.07875,"saskatchewan"=>0.1,"northwest-territories"=>0.05,"nunavut"=>0.05,"yukon-territories"=>0.05);
    $products = array(array("name"=>"Extreme Iron","cost"=>100),array("name"=>"Kevlar Ironing-Board","cost"=>140),array("name"=>"Space-Time Iron","cost"=>88),array("name"=>"Light Vacuum","cost"=>1000),array("name"=>"Extraction Nozzle","cost"=>25),array("name"=>"Nuclear Vacuum-bag","cost"=>45),array("name"=>"Laser Pot","cost"=>180),array("name"=>"Spatula of The Abyss","cost"=>42),array("name"=>"Fork","cost"=>10000),array("name"=>"Spoon","cost"=>10000));

    function retrieve($name){
        return $_COOKIE[safe($name)];
    }
    
?>
<body id="tab4">
<ul id="tabnav">
<li class="tab1"><a href="#" onclick="submitPage(1)">Ironing</a></li>
<li class="tab2"><a href="#" onclick="submitPage(2)">Vacuuming</a></li>
<li class="tab3"><a href="#" onclick="submitPage(3)">Cooking</a></li>
<li class="tab4"><a href="#" onclick="submitPage(4)">Checkout</a></li>
</ul>

<div id="pane">
<div id="content">
<h1>Checkout</h1>
<div id="error-message"></div>
<form method='POST' action='/' name='store'><input id='pageField' type='hidden' name='page' value='1'><input id='validField' type='hidden' name='valid' value='1'>
<table>
<tr><th align='left'>Invoice To:</th></tr>
<tr><td><?echo retrieve($nameF)?></td></tr>
<tr><td><?echo retrieve($streetF)?></td></tr>
<tr><td><?echo retrieve($cityF)?>, <?echo unsafe(retrieve($provinceF))?>&nbsp;&nbsp;<?echo retrieve($postF)?></td></tr>
<?
   $ci=""; 
    $email = retrieve($emailF);
    $birth = retrieve($birthF);
    if(!(preg_match("/^\s*$/",$email))){
        $ci.="<tr><td>$email</td></tr>";
    }
    if(!(preg_match("/^\s*$/",$birth))){
        $ci.="<tr><td>Birthdate: $birth</td></tr>";
    }
    echo $ci;?>
    </table><table id='invoice'>
    <tr><th>Item</th><th>Cost</th><th>Qty</th><th>Line Cost</th></tr>

    <?
    $total=0;
    
    foreach($products as $_){
        $name = $_['name'];
        $cost = $_['cost'];
        $qty = retrieve($name);
        if($qty>0){ 
            $lcost=$qty*$cost;
            if(preg_match("/^\s*$/",$qty)){$qty=0;}
            echo "<tr><td>$name</td><td>\$$cost</td><td>$qty</td><td>\$$lcost</td></tr>\n";
            $total+=$lcost;
        }
    }
    $tax = $total*$provinces[safe(retrieve($provinceF))];
    $gtotal = $total+$tax;
    ?>
    <tr><td colspan='3'><b>Total</b></td><td>$<? echo number_format($total, 2, '.', '');?></td></tr>
    <tr><td colspan='3'><b>Sales Tax</b></td><td>$<? echo number_format($tax, 2, '.', ''); ?></td></tr>
    <tr><td colspan='3'><b>Grand Total</b></td><td>$<? echo number_format($gtotal, 2, '.', '');?></td></tr>
    </table>
    </form>
</div>
</div>
</body>
</html>
