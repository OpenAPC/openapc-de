#!/usr/bin/env perl

=head1 SYNOPSIS

    perl fetch.pl [--refresh] --input {input_file.csv} --output {output_file.csv}

=head1 DESCRIPTION

This script fetches the unique identifier ("UT") from Web of Science.
You have to register your IP for the Article Match Retrieval Service:
http://wokinfo.com/products_tools/products/related/amr/

=head1 AUTHOR

Vitali Peil, vitali.peil at uni-bielefeld.de

=head1 LICENSE

This software is copyright (c) 2020 by Vitali Peil.

This is free software; you can redistribute it and/or modify it
under the same terms as the Perl 5 programming language system itself.

=cut

use Catmandu::Sane;
use Catmandu;
use Catmandu::Importer::CSV;
use Catmandu::Exporter::CSV;
use Getopt::Long;
use LWP::UserAgent;
use Try::Tiny;
use XML::Writer;
use XML::Simple;

local $SIG{__WARN__} = sub {

    # silent warnings
};

my ($in_file, $out_file, $refresh);
GetOptions(
    "input=s"  => \$in_file,
    "output=s" => \$out_file,
    "refresh"  => \$refresh,
) or die("Error in command line arguments\n");

die "Parameters '--input' and '--output' are required."
    unless $in_file and $out_file;

sub generate_xml {
    my (@data) = @_;

    my $xml = XML::Writer->new(OUTPUT => 'self', ENCODING => 'UTF-8');
    $xml->xmlDecl;
    $xml->startTag('request', 'xmlns' => 'http://www.isinet.com/xrpc41');

    $xml->startTag('fn', 'name' => 'LinksAMR.retrieve');
    $xml->startTag('list');
    $xml->emptyTag('map');

    $xml->startTag('map');
    $xml->startTag('list', 'name' => 'WOS');
    $xml->dataElement('val', 'ut');
    $xml->dataElement('val', 'doi');
    $xml->dataElement('val', 'pmid');
    $xml->endTag('list');
    $xml->endTag('map');

    $xml->startTag('map');

    foreach my $d (@data) {
        next if $d->{doi} eq "NA";

        $xml->startTag('map', 'name' => $d->{doi});
        foreach my $f (qw(ut doi pmid)) {
            if ($d->{$f} && $d->{$f} ne "NA") {
                $xml->dataElement('val', $d->{$f}, 'name' => $f);
                last;
            }
        }
        $xml->endTag('map');
    }

    $xml->endTag('map');

    $xml->endTag('list');
    $xml->endTag('fn');
    $xml->endTag('request');

    return $xml->to_string();
}

sub do_request {
    my $content = shift;

    my $ua       = LWP::UserAgent->new;
    my $response = $ua->post('http://ws.isiknowledge.com/cps/xrpc',
        Content => $content,);

    $response->is_success ? return $response->{_content} : return 0;
}

sub parse_xml {
    my $xml = shift;

    return unless $xml;

    try {
        my $xml_data = XMLin($xml);

        return if exists $xml_data->{error};
        my $items = $xml_data->{fn}->{map}->{map};

        my $result;
        foreach my $id (keys %$items) {
            next if ref $items ne 'HASH';

            my $tmp  = $items->{$id}->{map}->{val};
            my $data = {
                ut   => $tmp->{ut}->{content}      || '',
                doi  => lc($tmp->{doi}->{content}) || '',
                pmid => $tmp->{pmid}->{content}    || '',
            };
            push @$result, $data unless $data->{ut} eq '';
        }

        return $result;

    }
    catch {
        print STDERR "Error: $_";
    }
}

# main
my $csv = Catmandu::Importer::CSV->new(file => $in_file);

my $exporter = Catmandu::Exporter::CSV->new(
    file         => $out_file,
    sep_char     => ',',
    quote_char   => '"',
    always_quote => 1,
    fields       => ["doi", "ut", "pmid"],
);

my @data;
$csv->each(
    sub {
        my $rec = $_[0];
        next if $rec->{doi} eq "NA";
        if ($refresh) {
            delete $rec->{ut};
            push @data, $rec;
        }
        else {
            push @data, $rec if $rec->{ut} eq "NA";
        }
    }
);

my $counter;
while (my @chunks = splice(@data, 0, 50)) {
    my $request_body = generate_xml(@chunks);

    try {
        my $response    = do_request($request_body);
        my $parsed_data = parse_xml($response);
        $exporter->add_many($parsed_data) if $parsed_data;
        $counter++;
        print "Processed " . 50 * $counter . " records...\n"
            if $counter % 10 == 0;
    }
    catch {
        print STDERR "Error: $_";
    }
}

$exporter->commit;
