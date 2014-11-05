#!/usr/bin/perl
use warnings;
use strict;

use Net::Subnet;
use Getopt::Long;
use Pod::Usage;

my $ranges = '';
my $listIPs = '';
my $list_in_range = 0;
my $list_out_range = 0;

GetOptions("range=s" => \$ranges,
	   "file=s" => \$listIPs,
   	   "in-range" => \$list_in_range,
   	   "out-range" => \$list_out_range) or die "Error in command line arguments\n";

unless ($ranges and $listIPs and ($list_in_range xor $list_out_range)) {
	pod2usage(1);
	exit;
}

open(RANGES, $ranges) or die "Cannot open file: $!";

my @unsafe_ranges = <RANGES>;
chomp foreach (@unsafe_ranges);
my @ranges = grep(/^\d+\.\d+\.\d+\.\d+/,@unsafe_ranges);
if (scalar(@ranges) != scalar(@unsafe_ranges)) {
	print STDERR "Warning: Some IPs in the range are fubar.  Original list had ".scalar(@unsafe_ranges).", now I'm using ".scalar(@ranges)."\n";
}
foreach my $r (@ranges) {
	unless ($r =~ /\//) {
		$r .= '/32';
	}
}
my $matcher = subnet_matcher @ranges;

close(RANGES);
open(IPS, $listIPs) or die "Cannot open file: $!";

while (<IPS>) {
	chomp;
	if ($list_in_range) {
		if ($matcher->($_)) {
			print "$_\n";
		}
	}
	elsif ($list_out_range) {
		unless ($matcher->($_)) {
			print "$_\n";
		}
	}
}

close(IPS);

__END__
=head1 IPCheckRange.pl

Simple script to check if a list of IPs is within the specified range

=head1 SYNOPSIS

./IPCheckRange.pl [options]

  Options:
    --range, -r			File of IP ranges, either in CIDR or in range format
    				Ex: 127.0.0.1/24  or  127.0.0.1-50

    --file, -f			File of IP addresses to test

    --in-range			Display IPs that are within specified ranges
				(Cannot be used with --out-range

    --out-range			Display IPs that are not within specified ranges
				(Cannot be used with --in-range)


Requires:
	Net::Subnet


