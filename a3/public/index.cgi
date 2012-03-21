#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use HTML::Entities;
use strict;
use warnings;
my $q = CGI->new;
my $params = $q->Vars;

#Figure out which page we're on
my $pg = $params->{'page'};
my $validT = $params->{'valid'};
#Persisted values
my %store = ();
my @newCookies = ();

my ($nameF,$streetF,$cityF,$provinceF,$postF,$emailF,$birthF) = 
    ("Name","Street Address","City","Province","Postal Code","Email Address","Birth Date");
my @allFields = ($nameF,$streetF,$cityF,$provinceF,$postF,$emailF,$birthF);
my @mandatory = ($nameF,$streetF,$cityF,$provinceF,$postF);
my @p1_prods = ({"name"=>"Extreme Iron","cost"=>100},{"name"=>"Kevlar Ironing-Board","cost"=>140},{"name"=>"Space-Time Iron","cost"=>88});
my @p2_prods = ({"name"=>"Light Vacuum","cost"=>1000},{"name"=>"Extraction Nozzle","cost"=>25},{"name"=>"Nuclear Vacuum-bag","cost"=>45});
my @p3_prods = ({"name"=>"Laser Pot","cost"=>180},{"name"=>"Spatula of The Abyss","cost"=>42},{"name"=>"Fork","cost"=>10000},{"name"=>"Spoon","cost"=>10000});
products(@p1_prods,@p2_prods,@p3_prods);
userInfo(@allFields);
my $redirect = undef;
my $validations;
my $content;
my $title;
my $tabs = <<TABS; 
<ul id="tabnav">
<li class="tab1"><a href="#" onclick="submitPage(1)">Ironing</a></li>
<li class="tab2"><a href="#" onclick="submitPage(2)">Vacuuming</a></li>
<li class="tab3"><a href="#" onclick="submitPage(3)">Cooking</a></li>
<li class="tab4"><a href="#" onclick="submitPage(4)">Checkout</a></li>
</ul>
TABS

my $error=checkMandatory(@mandatory);
if (!defined($error) && defined(retrieve($emailF)) && !(retrieve($emailF)=~/^\s*$/) && !(retrieve($emailF)=~/^[\w\.-]+@([\w\-]+\.)+[A-z]{2,4}$/)){
    $error = "Invalid email.";
}
if (!defined($error) && !(retrieve($postF)=~/^[A-z]\d[A-z]\s*-?\s*\d[A-z]\d$/)){
    $error = "Invalid postal code.";
}
if(!defined($pg) or defined($error)){
    if(!defined($pg)){
        $error="Fields marked with an asterisk are mandatory.";
        $pg=1;
    }
    $title="Customer Identification";
    $content=userPage();
    $validations="";
    $tabs="";
}elsif($pg==1){
    $error="";
    $title="Ironing";
    $content=productPage(@p1_prods);
    $validations=productValidations(@p1_prods);
}elsif($pg==2){
    $error="";
    $title="Vacuuming";
    $content=productPage(@p2_prods);
    $validations=productValidations(@p2_prods);
}elsif($pg==3){
    $error="";
    $title="Cooking";
    $content=productPage(@p3_prods);
    $validations=productValidations(@p3_prods);
}elsif($pg==4){
    $redirect="/invoice.php";
}
my $safeEmail=safe($emailF);
my $safePost = safe($postF);
my $page = <<HTML;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>Assignment 3 - $title</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <LINK REL=StyleSheet HREF="style.css" TYPE="text/css" MEDIA=screen>
    <script type="text/javascript">
        var changes = false;
        function checkEmail(){
            var text = document.getElementById('$safeEmail');
            if(!text.value.match(/^[\\w\\.-]+@([\\w\\-]+\\.)+[A-z]{2,4}\$/)){
                alert(text.value+" is not a valid email.");
                text.value="";
            }
        }
        function checkPost(){
            var text = document.getElementById('$safePost');
            if(!text.value.match(/^[A-z]\\d[A-z]\\s*-?\\s*\\d[A-z]\\d\$/)){
                alert(text.value+" is not a valid postal code.");
                text.value="";
            }
        }
        function submitPage(num){
            document.getElementById('pageField').value=num;
            if(changes){
                document.getElementById('validField').value=confirm("Are you sure you want to make these changes to your cart?")?1:0;
            }
            
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
        function allCheck(list){
            for(var i=0;i<list.length;i++){
                var box = getCheckBox(list[i]);
                var text = getTextBox(list[i]);
                if(text.value.match(/^\\s*\$/)){
                    text.value=1;
                    box.checked=true;
                    changes = true;
                }
            }
        }
        function validate(){
            $validations 
        }
        function checkProduct(name){
            changes=true;
            var text = getTextBox(name); 
            var check = getCheckBox(name); 
            if(!isNumber(text.value)){
                text.value="";
                alert("Quantities must be whole numbers.");
            }
            if(text.value=="" || text.value==0){
                check.checked=false;
                text.value="";
            }if(text.value!="" && isNumber(text.value)&& text.value>0){
                check.checked=true;
            }
        }
        function checkbox(name){
            changes=true;
            var text = document.getElementById('text-'+name);
            var check =  document.getElementById('check-'+name);
            if(check.checked==true && !isNumber(text.value) || text.value<1){
                text.value=1;
            }
            if(check.checked==false){
                text.value="";
            }
        }
            
    </script>
</head>

<body id="tab$pg">
$tabs
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
if(defined $redirect){
print $q->redirect('-uri'=>$q->url(-base=>1).$redirect,'-cookie'=> \@newCookies);
}else{
print $q->header('-cookie'=> \@newCookies);
print $page;
}

#Routines for hidden-variable keystore

sub persist {
    foreach (@_){
        $store{safe($_)}=$q->cookie(safe($_));
    }	
}
sub setStored{
    if($validT){
        push @newCookies, $q->cookie('-name'=>safe($_[0]),'-value'=>"$_[1]");
        $store{safe($_[0])}=$_[1];
    }
}

sub retrieve {
    return $store{safe($_[0])};
}

sub products{
    foreach (@_){
        my $name=$_->{'name'};
        persist($name);
        my $newQty=$params->{safe($name)};
        if(defined($newQty) && $newQty=~/^\s*\d*\s*$/){
            setStored($name,$newQty);
        }
    }
}
#Routines for rendering forms
sub userInfo{
    foreach(@_){
        persist($_);
        my $in = $params->{safe($_)};
        if(defined($in)){setStored($_,$in);}
    }
}

sub makeU{
    my $name = shift @_;
    my $val = retrieve($name);
    my $change = "";
    if(@_){$change=" onchange='".(shift @_)."'";}

    my $mand = "";
    foreach(@mandatory){
        if($name eq $_){
            $mand="<td><span style='color:red'>*</span></td>";
        }
    }
    return "<tr><td><label for='".safe($name)."'>$name</label></td><td><input type='text' name='".safe($name)."' id='".safe($name)."' value='".encode_entities($val)."'$change></td>$mand</tr>\n";
}
sub makeUserSelect{
    my $name = shift @_;
    my $opts = "<option value=''>Choose $name</option>\n";
    my $val = retrieve($name);
    foreach (@_){
        my $checked = ""; 
        if($val eq safe($_)){
            $checked=" selected='selected'";
        }
        $opts.="<option value='".safe($_)."'$checked>$_</option>\n";
    }

    return "<tr><td><label for='".safe($name)."'>$name</label></td><td><select name='".safe($name)."' id='".safe($name)."'>$opts</select></td><td><span style='color:red'>*</span></td></tr>\n";
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
    my $ret="<tr><th>Item</th><th>Price</th><th>Y/N</th><th>Quantity</th></tr>\n";
    foreach (@_){
        my $name=$_->{'name'};
        my $cost=$_->{'cost'};
        my $image=$_->{'image'};
        my $qty=retrieve($name);
        my $checked = "";
        if(!defined $qty){$qty=""}
        if ($qty ne "" && $qty>0){
            $checked=" checked='true'";
        }
        $ret.= "<tr><td>$name</td><td>\$$cost</td><td><input type='checkbox' onchange='checkbox(\"".safe($name)."\")' id='check-".safe($name)."'$checked></td><td><input type='text' name='".safe($name)."' value='".encode_entities($qty)."' onchange='validate()' id='text-".safe($name)."'></td></tr>\n";
    }
    return $ret;
}
sub productValidations{
    my $ret;
    foreach (@_){
        $ret.="checkProduct('".safe($_->{'name'})."');\n";
    }
    return $ret;
}
#Page builders
sub form{ 
    return "<form method='POST' action='/' name='store'><input id='pageField' type='hidden' name='page' value='1'><input id='validField' type='hidden' name='valid' value='1'>\n<table>\n".$_[0]."\n</table>\n</form>\n";
}
sub productPage{
    my $all = "[";
    for (@_){
        $all.=('"'.safe($_->{'name'}).'",');
    }
    chop($all);
    $all="allCheck($all])";

    return form(makeProducts(@_))."<img src='cart.jpg' alt = 'add all to cart' style='cursor: pointer' onclick='$all'>";
}
sub userPage{
    return form(makeU($nameF).makeU($streetF).makeU($cityF).makeUserSelect($provinceF,"Alberta","British Columbia","Manitoba","New Brunswick","Newfoundland and Labrador","Nova Scotia","Ontario","Prince Edward Island","Quebec","Saskatchewan","Northwest Territories","Nunavut","Yukon Territories").makeU($postF,"checkPost()").makeU($emailF,"checkEmail()").makeU($birthF)."<tr><td colspan='2'><input type='button' value='Submit' onclick='submitPage(1)'></td></tr>");
}
sub checkoutPage{
    my $ci = "<tr><th align=left>Invoice To:</th></tr>\n";
    $ci.="<tr><td>".retrieve($nameF)."</td></tr>";
    $ci.="<tr><td>".retrieve($streetF)."</td></tr>";
    $ci.="<tr><td>".retrieve($cityF).", ".retrieve($provinceF)."&nbsp;&nbsp;".retrieve($postF)."</td></tr>";
    my $email = retrieve($emailF);
    my $birth = retrieve($birthF);
    if(!($email=~/^\s*$/)){
        $ci.="<tr><td>$email</td></tr>";
    }
    if(!($birth=~/^\s*$/)){
        $ci.="<tr><td>Birthdate: $birth</td></tr>";
    }

    my $lines = "<tr><th>Item</th><th>Cost</th><th>Qty</th><th>Line Cost</th></tr>\n";
    my $total=0;
    
    foreach((@p1_prods,@p2_prods,@p3_prods)){
        my $name = $_->{'name'};
        my $cost = $_->{'cost'};
        my $qty = retrieve($name);
        if($qty>0){ 
            my $lcost=$qty*$cost;
            if($qty =~/^\s*$/){$qty=0}
            $lines.="<tr><td>$name</td><td>\$$cost</td><td>$qty</td><td>\$$lcost</td></tr>\n";
            $total+=$lcost;
        }
    }
    $lines.="<tr><td colspan='3'><b>Total</b></td><td>\$$total</td></tr>";
    return form("$ci</table><table id='invoice'>$lines");
}
sub safe{
    my $str = shift @_;
    $str= lc $str;
    $str =~ s/\s+/-/g;
    return $str;
}
1;
