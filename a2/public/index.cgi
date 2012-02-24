#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use strict;
use warnings;

my $q = CGI->new;
my $params = $q->Vars;

#Figure out which page we're on
my $pg = $params->{'page'};
if(!defined ($pg)){ $pg=1;}

#Persisted values
my %store = ();


my @mandatory = ("Name","Street Address","City","Province","Postal Code");
my @p1_prods = ({"name"=>"beer","cost"=>5},{"name"=>"Ham","cost"=>5},{"name"=>"third","cost"=>88});
my @p2_prods = ({"name"=>"Something","cost"=>5});
products(@p1_prods,@p2_prods);
userInfo(@mandatory);
my $validations;
my $content;
my $title;
my $error=checkMandatory(@mandatory);
if(defined($error)){
    $title="Customer Identification";
    $content=userPage(@mandatory);
    $validations="";
}elsif($pg==1){
    $title="Ironing";
    $content=productPage(@p1_prods);
    $validations=productValidations(@p1_prods);
}elsif($pg==2){
    $title="Vaccuuming";
    $content=productPage(@p2_prods);
    $validations=productValidations(@p2_prods);
}

my $page = <<HTML;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>Assignment 1 - $title</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <LINK REL=StyleSheet HREF="style.css" TYPE="text/css" MEDIA=screen>
    <script type="text/javascript">
        function submitPage(num){
            document.getElementById('pageField').value=num;
            document.store.submit();
        }
        function getCheckBox(name){
            return document.getElementById('check-'+name);
        }
        function getTextBox(name){
            return document.getElementById('text-'+name);
        }
        function isNumber(str){
            return str.match(/^\\d*\$/);
        }
        function all(list){
            for(var i=0;i<list.length;i++){
                var box = getCheckBox(list[i]);
                var text = getTextBox(list[i]);
                if(text.value.match(/^\\s*\$/)){
                    text.value=1;
                    box.checked=true;
                }
            }
        }
        function validate(){
            $validations 
        }
        function checkProduct(name){
            var text = getTextBox(name); 
            var check = getCheckBox(name); 
            if(!isNumber(text.value)){
                text.value="";
            }
            if(text.value==""){
                check.checked=false;
            }
        }
        function checkbox(name){
            var text = document.getElementById('text-'+name);
            var check =  document.getElementById('check-'+name);
            if(check.checked==true && !isNumber(text.value) || text.value<1){
                text.value=1;
            }
        }
    </script>
</head>

<body id="tab$pg">

<ul id="tabnav">
    <li class="tab1"><a href="#" onclick="submitPage(1)">Ironing</a></li>
    <li class="tab2"><a href="#" onclick="submitPage(2)">Vacuuming</a></li>
<li class="tab3"><a href="#" onclick="submitPage(3)">Cooking</a></li>
<li class="tab4"><a href="#" onclick="submitPage(4)">Checkout</a></li>
</ul>

<div id="pane">
<div id="content">
<h1>$title</h1>
<div id="error-message">$error</div>
$content
</div>
</div>
</body>
</html>
HTML
#Print header and page
print $q->header();
print $page;

#Routines for hidden-variable keystore
sub persist {
	foreach (@_){
		$store{$_."-store"}=$params->{$_."-store"};
	}	
}
sub setStored{
    $store{$_[0]."-store"}=$_[1];
}
sub retrieve {
	return $store{$_[0]."-store"};
}
#Should be called just before rendering page so that all saved entries are included
sub makeStore {
    my $ret;	
    foreach(keys %store){
		$ret.= "<input type='hidden' name='$_' value='$store{$_}'>";
	}
	return $ret;
}

sub products{
    foreach (@_){
        my $name=$_->{'name'};
        persist($name);
		my $newQty=$params->{$name};
        if(defined($newQty) && $newQty!=""){setStored($name,$newQty);}
    }
}
#Routines for rendering forms
sub userInfo{
    foreach(@_){
        persist($_);
    }
}

sub makeUserText{
    my $ret = "";
    foreach(@_){
        my $val = retrieve($_);
        $ret.="<tr><td><label for='$_'>$_</label></td><td><input type='text' name='$_' id='$_' value='$val'></td></tr>";
    }
    return $ret;
}

sub checkMandatory{
    foreach(@_){
	my $val = retrieve($_);
        if(not defined($val) or $val=~/^\s*$/){
            return "The $_ field must be filled.";
        }
    }
    return undef;
}

sub makeProducts{
    my $ret="<tr><th colspan='2'>Item</th><th>Price</th><th>Y/N</th><th>Quantity</th></tr>\n";
	foreach (@_){
		my $name=$_->{'name'};
		my $cost=$_->{'cost'};
        my $image=$_->{'image'};
		my $qty=retrieve($name);
        my $checked = "";
        if ($qty!="" && $qty>0){
            $checked=" checked='true'";
        }
	    $ret.= "<tr><td><img src='$image' alt='image of $name'></td><td>$name</td><td>$cost</td><td><input type='checkbox' onchange='checkbox(\"$name\")' id='check-$name'$checked></td><td><input type='text' name='$name' value='$qty' onchange='validate()' id='text-$name'></td></tr>\n";
	}
    return $ret;
}
sub productValidations{
    my $ret;
    foreach (@_){
        $ret.="checkProduct('$_->{'name'}');\n";
    }
    return $ret;
}
#Page builders
sub form{ 
    return "<form method='POST' name='store'><input id='pageField' type='hidden' name='page' value='1'>\n<table>\n".$_[0]."\n</table>\n</form>\n";
}
sub productPage{
    my $all = " new Array(";
    for (@_){
        $all.="\"$_->{'name'}\",";
    }
    chop($all);
    $all="all($all));";
        
    return form(makeProducts(@_).makeStore())."<img src='cart.jpg' alt = 'add all to cart' style='cursor: pointer' onclick='$all'>";
}
sub userPage{
    return form(makeUserText(@_).makeStore());
}
1;
