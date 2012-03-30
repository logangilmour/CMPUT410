#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use HTML::Entities;
use strict;
use warnings;
my $q = CGI->new;
print $q->header();
print <<HTML;
<html>
<head>
</head>
<body>
<p>woo</p>
<div style='width:300;height=50; border:1px #000 solid;'>
<div style='background:#f00;position:relative;top:0;left:0;margin:1px;width:50%;'>
Stuff</div>
</div>
</body>
</html>
HTML
