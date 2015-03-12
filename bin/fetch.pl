#!/usr/bin/env perl

=head1 SYNOPSIS

	perl fetch_ut.pl {input_file.csv}

=head1 DESCRIPTION

This script fetches the unique identifier ("UT") from Web of Science.
You have to register your IP for the Article Match Retrieval Service:
http://wokinfo.com/products_tools/products/related/amr/

=head1 AUTHOR

Vitali Peil, vitali.peil at uni-bielefeld.de

=head1 LICENSE

This software is copyright (c) 2014 by Vitali Peil.

This is free software; you can redistribute it and/or modify it
under the same terms as the Perl 5 programming language system itself.

=cut

use Catmandu::Sane;
use Catmandu;
use Catmandu::Importer::CSV;
use Catmandu::Exporter::CSV;
use LWP::UserAgent;
use XML::Simple;
use Try::Tiny;
use FindBin qw/$Bin/;

my $file   = $ARGV[0];
my $wosURL = 'http://apps.webofknowledge.com/';

sub _do_request {
    my $body = shift;

    sleep 2;
    my $ua       = LWP::UserAgent->new;
    my $response = $ua->post( 'https://ws.isiknowledge.com/cps/xrpc',
        Content => $body, );
    ( $response->is_success )
        ? ( return $response->{_content} )
        : ( return 0 );
}

sub _filter_xml {
    my $text = shift;

    for ($text) {
        s/&/&amp;/go;
        s/</&lt;/go;
        s/>/&gt;/go;
        s/"/&quot;/go;
        s/'/&apos;/go;

        # remove control characters
        s/[^\x09\x0A\x0D\x20-\x{D7FF}\x{E000}-\x{FFFD}\x{10000}-\x{10FFFF}]//go;
    }
    $text;
}

sub _generate_xml {
    my $data = shift;

    my $body = <<XML;
<?xml version="1.0" encoding="UTF-8" ?>
<request xmlns="http://www.isinet.com/xrpc41">
<fn name="LinksAMR.retrieve">
<list>
<map>
</map>
<map>
  <list name="WOS">
    <val>ut</val>
    <val>doi</val>
    <val>pmid</val>
  </list>
</map>
<map>
XML

    if ( $data->{doi} && $data->{doi} ne 'NA' ) {
        my $s = _filter_xml( $data->{doi} );
        $body .= <<XML3;
<map name="$data->{repo_id}">
	<val name="doi">$s</val>
</map>
XML3
    }
    elsif ( $data->{pmid} && $data->{pmid} ne 'NA' ) {
        my $s = _filter_xml( $data->{pmid} );
        $body .= <<XML4;
<map name="$data->{repo_id}">
	<val name="pmid">$s</val>
</map>
XML4
    }
    else {
        return 0;
    }

    $body .= '</map></list></fn></request>';

    return $body;
}

sub _parse {
    my $f = shift;
    return if !$f;
    my $xml;
    try {
        $xml = XMLin($f);
        return if exists $xml->{error};
        my $node = $xml->{fn}->{map}->{map}->{map}->{val};

        my $ut = $node->{ut}->{content} ||= '';
        return $ut;
    }
    catch {
        print STDERR "ERROR: $_";
    }
}

# main
my $csv      = Catmandu::Importer::CSV->new( file => $file );
my $exporter = Catmandu::Exporter::CSV->new(
  file => "$Bin/../data/doi_ut.csv",
  sep_char => ',',
  quote_char => '"',
  always_quote => 1,
  );

$csv->each(
    sub {
        my $data = $_[0];
        my $body = _generate_xml($data);
        if ($body && $data->{ut} eq 'NA') {
            my $ut = _parse( _do_request($body) );
            $exporter->add({doi => $data->{doi}, ut => $ut ? "ut:$ut" : 'NA'});
        } else {
            $exporter->add({doi => $data->{doi}, ut => $data->{ut}});
        }
    }
);
