#!/usr/bin/perl
use strict;
use warnings;
use Cwd 'abs_path';
use YAML::Tiny;
use DBI;

print "Content-type: text/html\n\n";
my $params = $ENV{'QUERY_STRING'};
$params =~ s/%40/@/;
my ($email) = ($params =~ /.*=(.*)/);

my $script_location = abs_path($0);
my ($repo_root) = ($script_location =~ /^(.*\/gpb\/)/);
my $files = $repo_root.'src/*';
my $cfg_file = $repo_root.'conf/config.yml';
my $config = YAML::Tiny->read($cfg_file)->[0];
print "Hey!"

1;

