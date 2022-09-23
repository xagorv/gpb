#!/usr/bin/env perl

use strict;
use warnings;
use Cwd 'abs_path';
use YAML::Tiny;
use DBI;
use Data::Dumper;

my $script_location = abs_path($0);
my ($repo_root) = ($script_location =~ /^(.*\/gpb\/)/);
my $files = $repo_root.'src/*';
my $cfg_file = $repo_root.'conf/config.yml';
my $config = YAML::Tiny->read($cfg_file)->[0];
my $dsn = "DBI:mysql:database=$config->{database};host=$config->{host};port=$config->{port}";
my $dbh = DBI->connect($dsn, $config->{db_user}, $config->{password});

my @sources = glob($files);
for my $source (@sources) {
    open(S, '<', $source) or die $!;
    while(<S>) {
        my $line = $_;
        my ($date, $timestamp, $int_id, $operation, $text) = ($line =~ /(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s(.*)/);
        
    }
}


