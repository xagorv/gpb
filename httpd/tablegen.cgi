#!/usr/bin/perl
use strict;
use warnings;
use YAML::Tiny;
use DBI;
use Data::Dumper;

print "Content-type: text/html\n\n";
my $params = $ENV{'QUERY_STRING'};
my $email;
if (! $params) {
    $email = '%tpxmuwr@somehost.ru%';
}
else {
    $params =~ s/%40/@/;
    ($email) = ($params =~ /.*=(.*)/);
}
my $cfg_file = 'config.yml';
my $config = YAML::Tiny->read($cfg_file)->[0];
my @records = ();

my $dsn = "DBI:mysql:database=$config->{database};host=$config->{host};port=$config->{port} + 1";
my $dbh = DBI->connect($dsn, $config->{db_user}, $config->{password});
my $sth = $dbh->prepare(
    'SELECT created, int_id, str FROM log WHERE address LIKE ? LIMIT 101'
) or die 'prepare statement failed: ' . $dbh->errstr();
$sth->execute($email) or die 'execute statement failed: ' . $dbh->errstr();
my ($ts, $int_id, $text);
while(($ts, $int_id, $text) = $sth->fetchrow()) {
    my @set = ($ts, $int_id, $text);
    push(@records, \@set);
}
my $sth = $dbh->prepare(
    'SELECT created, int_id, str FROM message WHERE str LIKE ? LIMIT 101'
) or die 'prepare statement failed: ' . $dbh->errstr();
my($mts, $mint_id, $mtext);
$sth->execute("\%$email\%");
while(($mts, $mint_id, $mtext) = $sth->fetchrow()) {
    my @mset = ($mts, $mint_id, $mtext);
    push(@records, \@mset);
}

print '<html>
    <head>
        <style>
            body        {background-color: powderblue;}
            label       {color: red; font-family: helvetica,arial;}
            table, th, td {
                  border: 1px solid;
                  border-collapse: collapse;
                  font-family: helvetica,arial;
            }
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Created</th><th>int_id</th><th>text</th>
            </tr>
';
print "\n";

for my $p (@records) {
    print("<tr><td>$p->[0]</td><td>$p->[1]</td><td>$p->[2]</td></tr>");
}

print '     </table>
    </body>
</html>';

1;

