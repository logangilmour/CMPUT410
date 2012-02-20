#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);
use CGI;
use strict;
use warnings;

my $q = CGI->new;

print $q->header();

print "Hello";
1;
