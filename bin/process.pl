#!/usr/bin/env perl

use strict;
use warnings;
use Cwd 'abs_path';
use YAML::Tiny;
use DBI;
use Data::Dumper;

sub get_email{
    my $str = $_[0];
    my ($email) = ($str =~ /([A-Za-z1-9_]+@[A-Za-z1-9_]+\.[A-Za-z]+)/);
    if (!$email) {
        $email = ''
    }
    return $email
}

my $script_location = abs_path($0);
my ($repo_root) = ($script_location =~ /^(.*\/gpb\/)/);
my $files = $repo_root.'src/*';
my $cfg_file = $repo_root.'httpd/config.yml';
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
        my ($date, $timestamp, $int_id, $rest) = ($line =~ /(\S+)\s+(\S+)\s+(\S+)\s+(.*)/);
        my ($operation, $text) = ($rest =~ /(\S+)\s+(.*)/);
        if ($operation and $operation eq '<=') {
            my ($id) = ($text =~ /id=(\S+)/);
            if ($id) {
                my $sth = $dbh->prepare(
                    'INSERT INTO message (created, id, int_id, str) VALUES (?, ?, ?, ?)'
                ) or die 'prepare statement failed: ' . $dbh->errstr();
                $sth->execute("$date $timestamp", $id, $int_id, "$int_id $rest");
            }
            else {
                print("FATAL: Cannot put message '$line' to table because cannot determine id.\n")
            }
        }
        else {
            my $email = get_email($rest);
            my $sth = $dbh->prepare(
                'INSERT INTO log (created, int_id, str, address) VALUES (?, ?, ?, ?)'
            ) or die 'prepare statement failed: ' . $dbh->errstr();
            $sth->execute("$date $timestamp", $int_id, $rest, $email);
        }
    }
    close(S);
}
$dbh->disconnect();

1;