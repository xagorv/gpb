#!/usr/bin/perl
use strict;
use warnings;

print "Content-type: text/html\n\n";
my $params = $ENV{'QUERY_STRING'};
$params =~ s/%40/@/;
my ($email) = ($params =~ /.*=(.*)/);



1;

