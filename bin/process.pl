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
        # Remove leading and trailing spaces
        $line=~ s/^\s+|\s+$//g;
        my ($date, $timestamp, $int_id, $operation, $text) = ($line =~ /(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s(.*)/);
        if ($operation and $operation eq '<=') {
            my ($id) = ($text =~ /id=(\S+)/);
            if ($id) {
                my $lenid = length($id);
                my $sth = $dbh->prepare(
                    'INSERT INTO message (created, id, int_id, str) VALUES (?, ?, ?, ?)'
                ) or die 'prepare statement failed: ' . $dbh->errstr();
                $sth->execute("$date $timestamp", $id, $int_id, "$id $operation $text");
            }
            else {
                print("FATAL: Cannot put message '$line' to table because cannot determine id.\n")
            }
        }
        else {
            
        }
    }
    close(S);
}

