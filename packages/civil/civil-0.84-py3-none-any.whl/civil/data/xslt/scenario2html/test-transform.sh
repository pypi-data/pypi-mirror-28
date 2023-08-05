#! /bin/sh
# TODO:
#  - Rename this to xslt_driver or something! ;-)
#  - Add timing...
#  - Buy chakie a beer for jumping in here and writing *real* bloody shell code... ;-P


##############################################################################
# store app name, needed for error messages
SCRIPT=$0

##############################################################################
# set default values for all parameters
IN="../../scenarios/clash_in_the_pass.xml"
OUT="test.html"
XSL="civil-scenario2html.xsl"
JAR=""

##############################################################################
# Prints usage information and exits
function usage () {
    cat <<EOF
Usage: $SCRIPT [options]
Creates a HTML proview from a Civil scenario.
where options are:

    -IN file   use 'file' as the input scenario file
    -OUT file  use 'file' as the output file for the result HTML
    -XSL file  specify a custom XSLT stylesheet

EOF

    # get out of here
    exit 1
}


# loop over all commandline parameters and do some fancy parsing
while true ; do
    case "$1" in 
        -IN)
            shift
            IN=$1
            shift
            
            # validate the IN parameter
            if [ x$IN = "x" ]; then
                echo "Missing parameter to -IN"
                usage
            fi

            # add the "file:" that Xalan may need
            $IN="file:$IN"
            ;;

        -OUT)
            shift
            OUT=$1
            shift
            
            # validate the OUT parameter
            if [ x$OUT = "x" ]; then
                echo "Missing parameter to -OUT"
                usage
            fi
            ;;

        -XSL)
            shift
            XSL=$1
            shift
            
            # validate the XSL parameter
            if [ x$XSL = "x" ]; then
                echo "Missing parameter to -XSL"
                usage
            fi
            ;;

        -JAR)
            shift
            JAR=$1
            shift
            
            # validate the JAR parameter
            if [ x$JAR = "x" ]; then
                echo "Missing parameter to -JAR"
                usage
            fi

            # add the needed "-cp " to the jar path
            JAR="-cp $JAR"
            ;;

        -h|--help|-help|-HELP|--HELP)
            usage
            ;;
        "")
            break
            ;;

        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
done

echo
echo
echo "Decompressing Scenario:"
echo "  >>> $IN"
echo
echo "Please note, if you terminate this process before it completes"
echo "you will have to recompress the scenario file you choose..."
echo
gunzip $IN

echo 
echo Starting Java Xalan Transformation process...
echo "  >>> input file:  $IN"
echo "  >>> output file: $OUT"
echo "  >>> xsl file:    $XSL"

# do the grunt work
java $JAR org.apache.xalan.xslt.Process -IN $IN -XSL $XSL -OUT $OUT

echo
echo "Compressing..."

# figure out the file we should compress. we have to remove the .gz extension
IN=`echo $IN | sed -e 's/\.gz//'`

gzip $IN
# rm $IN

echo
echo If there where no errors above, ./test.html should contain the transformed example file.
echo Please check the README for more details...



