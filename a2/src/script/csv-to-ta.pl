#/usr/bin/perl
use strict;
use warnings;

# Convert CSV format to TA format
# Usage: perl transformUnderstand.pl <csv_dependency_file>

my ($header, $from, $to, $reference, $v1, $v2, $output_file);
my (%FILE_HASH, %CALL_HASH, $name, $value, $count, $hash, $line);

$header = 0;

open INPUT, "$ARGV[0]";

if ($ARGV[0] =~ /(.*)\.csv/) {
	$output_file = $1 . ".raw.ta";
}

open OUTPUT, ">$output_file";

print OUTPUT "FACT TUPLE :\n";


while (<INPUT>) {
	$line =$_;
	chomp $line;

	if ($header == 0) {
		$header++;
		next;
	}

	($from, $to, $reference, $v1, $v2) = split(/,/, $line);

	# comment out if we don't want to consider header files
	# note: should we consider header files or just c files?
#	if ($from =~ /\.h/ or $to =~ /\.h/) {
#		next;
#	}

    # comment this out if quotations are not generated in csv file
#    $from = substr $from, 1, -1;
#    $to = substr $to, 1, -1;

	$FILE_HASH{$from}++;
	$FILE_HASH{$to}++;
	$CALL_HASH{$from}{$to}++;
}

# output the list of files
while (($name, $value) = (each %FILE_HASH)) {
	# $INSTANCE codegen.o[.text+0x0] cFunction
	print OUTPUT "\$INSTANCE $name cFile\n";
}

# output the list of call relations
while (($name, $hash) = (each %CALL_HASH)) {
	while (($value, $count) = (each %$hash)) {
		# cLinks codegen.o[.text+0x3f3] semantics.o[.bss+0x0]
		# print OUTPUT "contain $name $value\n";
		print OUTPUT "cLinks $name $value\n";
	}
}

close INPUT;
close OUTPUT;
