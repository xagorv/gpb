#!/usr/bin/perl
use strict;1RwtJj-000ApM-CO
use warnings;
use YAML::Tiny;
use DBI;
use Data::Dumper;

print "Content-type: text/html\n\n";
my $params = $ENV{'QUERY_STRING'};
my $email;
if (! $params) {
    $email = 'udbbwscdnbegrmloghuf@london.com';
}
else {
    $params =~ s/%40/@/;
    ($email) = ($params =~ /.*=(.*)/);
}
my $cfg_file = 'config.yml';
my $config = YAML::Tiny->read($cfg_file)->[0];
my $dsn = "DBI:mysql:database=$config->{database};host=$config->{host};port=$config->{port} + 1";
my $dbh = DBI->connect($dsn, $config->{db_user}, $config->{password});
my $sth = $dbh->prepare(
    'SELECT created, int_id, str FROM log WHERE address LIKE ?'
) or die 'prepare statement failed: ' . $dbh->errstr();
$sth->execute($email) or die 'execute statement failed: ' . $dbh->errstr();
my ($ts, $int_id, $text);
my $sth1 = $dbh->prepare(
    'SELECT created, str FROM message WHERE int_id LIKE ?'
) or die 'prepare statement failed: ' . $dbh->errstr();
my($mts, $mtext);
while(($ts, $int_id, $text) = $sth->fetchrow()) {
    print "<tr><td>$ts</td><td>$int_id</td><td>$text</td></tr>\n";
    $sth1->execute($int_id);
    while(($mts, $mtext) = $sth1->fetchrow()) {
        print "<tr style=\"font-color: blue\"><td style=\"font-color: blue\">$mts</td><td>$int_id</td><td>$mtext</td></tr>";
    }
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


print '     </table>
    </body>
</html>';

1;

