#!/usr/bin/perl
use strict;
use warnings;
use YAML::Tiny;
use DBI;
use Data::Dumper;
use Date::Parse;

sub right_order {
    my $mp1 = shift;
    my $mp2 = shift;
    # Check int ids
    if ($mp1->[1] le $mp2->[1]) {
        return 1;
    }
    elsif(str2time($mp1->[0]) <= str2time($mp1->[1])) {
        return 1;
    }
    return 0;
}

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

my $dsn = "DBI:mysql:database=$config->{database};host=$config->{host};port=$config->{port} + 1";
my $dbh = DBI->connect($dsn, $config->{db_user}, $config->{password});
my $sth = $dbh->prepare(
    'SELECT created, int_id, str FROM log WHERE address LIKE ? ORDER BY int_id, created ASC LIMIT 101'
) or die 'prepare statement failed: ' . $dbh->errstr();
$sth->execute($email) or die 'execute statement failed: ' . $dbh->errstr();
my ($ts, $int_id, $text);
my @lrecords = ();
while(($ts, $int_id, $text) = $sth->fetchrow()) {
    my @set = ($ts, $int_id, $text);
    push(@lrecords, \@set);
}
my $sth1 = $dbh->prepare(
    'SELECT created, int_id, str FROM message WHERE str LIKE ? ORDER BY int_id, created ASC LIMIT 101'
) or die 'prepare statement failed: ' . $dbh->errstr();
my($mts, $mint_id, $mtext);
$sth1->execute("\%$email\%");
my @mrecords = ();
while(($mts, $mint_id, $mtext) = $sth1->fetchrow()) {
    my @mset = ($mts, $mint_id, $mtext);
    push(@mrecords, \@mset);
}

my $l = 0;
my $m = 0;
my @records = ();
my $go = 1;
while ($go) {
    if ($m >= scalar(@mrecords) or right_order($lrecords[$l], $mrecords[$m])) {
        push(@records, $lrecords[$l++]);
    }
    if ($l >= scalar(@lrecords) or right_order($mrecords[$m], $lrecords[$l])){
        push(@records, $mrecords[$m++]);
    }
    if ($m >= scalar(@mrecords) and $l >= scalar(@lrecords)) {
        $go = 0;
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
                <th>Created</th><th>int id</th><th>text</th>
            </tr>
';
print "\n";

for my $p (@records) {
    my $rts = $p->[0];
    my $rint_id = $p->[1];
    my $rtext = $p->[2];
    print("<tr><td>$rts</td><td>$rint_id</td><td>$rtext</td></tr>");
}

print '     </table>
    </body>
</html>';

1;

