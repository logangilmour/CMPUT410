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

persist();
my $storeString = makeStore();


my $page = <<HTML;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>Assignment 1</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
    <LINK REL=StyleSheet HREF="style.css" TYPE="text/css" MEDIA=screen>
    <script type="text/javascript">
        function submitPage(num){
            document.getElementById('pageField').value=num;
            document.store.submit();
        }
    </script>
</head>

<body id="tab$pg">
$storeString

<ul id="tabnav">
    <li class="tab1"><a href="#" onclick="submitPage(1)">Ironing</a></li>
    <li class="tab2"><a href="#" onclick="submitPage(2)">Vacuuming</a></li>
<li class="tab3"><a href="#" onclick="submitPage(3)">Cooking</a></li>
<li class="tab4"><a href="#" onclick="submitPage(4)">Checkout</a></li>
</ul>

<div id="pane">
<div id="content">
<h1>Vintage Stove</h1>

<p>Our new Big Chill stove combines the iconic look of a 50's style retro range with all the modern amenities of a modern unit. Purchase through authorized dealers around the country or order directly through Big Chill.</p>
<table>
<tr>
<td class="highlight">Vintage Stove</td>
<td>MSRP \$4295</td>
</tr>
<tr>
<td class="highlight">Matching Hood</td>
<td>MSRP \$1395</td>
</tr>
</table>
</div>
</div>
</body>
</html>
HTML
#Print header and page
print $q->header();
print $page;
sub persist {
	foreach (@_){
		$store{$_}=$params->{$_};
	}	
}
sub makeStore {
	my $ret = "<form method='POST' name='store'><input id='pageField' type='hidden' name='page' value='1'>";
	foreach(keys %store){
		$ret.= "<input type='hidden' name='$_' value='$store{$_}'>";
	}
	return "$ret </form>";
}
sub product{
	$name=$_[0];
	return "<input type='text' name='pName'>$store{$name+'_qty'}</input>"
1;
