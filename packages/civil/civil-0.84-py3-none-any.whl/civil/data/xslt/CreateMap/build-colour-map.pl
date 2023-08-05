print "  >>> Opening input:  map.txt";
open(IN, "map.txt") || die " unable to open input map data...";

print "\n  >>> Opening output: colour-map.xml";
open(OUT, ">>colour-map.xml") || die "unable to open output file...";

print "\n  >>> Trying to build...\n";

print OUT "<?xml version=\"1.0\"?>\n<colourmap>\n";

$n = 0;

while(<IN>)
{	 
	 $str = substr($_,0,16) = " ";
	 if($str =~ /(\d*),[\s]*(\d*),[\s]*(\d*)/)
	 {
		  if($1 != undefined)
		  {
				$n ++;
				print OUT "<icon number=\"$n\" r=\"$1\" g=\"$2\" b=\"$3\" />\n";
		 }
    }
}

print OUT "</colourmap>";

close IN;
close OUT;

print "  >>> Processing complete...\n\n";
print "Things appear to have worked, if colour-map.xml exists, copy it to ../scenario2html/\n\n";
	
