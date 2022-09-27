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
    $email = 'udbbwscdnbegrmloghuf@london.com';
}
else {
    $params =~ s/%40/@/;
    ($email) = ($params =~ /.*=(.*)/);
}
print "EMAIL: $email";
my $cfg_file = 'config.yml';
my $config = YAML::Tiny->read($cfg_file)->[0];
my $dsn = "DBI:mysql:database=$config->{database};host=$config->{host};port=$config->{port} + 1";
my $dbh = DBI->connect($dsn, $config->{db_user}, $config->{password});
my $sth = $dbh->prepare(
    'SELECT created, int_id, str FROM log WHERE address LIKE ?'
) or die 'prepare statement failed: ' . $dbh->errstr();
$sth->execute($email);
my ($ts, $int_id, $text);
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
                <th>Created</th><th>text</th>
            </tr>
';
print "\n";
while(($ts, $int_id, $text) = $sth->fetchrow()) {
print "<tr><td>$ts</td><td>$text</td></tr>\n";
}
print '     </table>
    </body>
</html>';

1;

