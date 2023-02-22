#!/bin/bash
################################################################################
# Create the final containment files: note to make sure you have JAVA_HOME on path
################################################################################

command="final-containment.sh"

function outputUsage() {
    usage="Create the final ta file to display. Run before ls-edit.sh.\n\n
    Usage:\n
        $command -j <ql-jar-file> -n <output-file-name> -t <ta-dependency-file> -c <containment-file>\n
        $command -h | --help\n
    Options:\n
        -h --help Show usage.\n
        -c --contain=<containment-file> Dependency containment file.\n
        -t --tafile=<ta-dependency-file> TA containment dependency file.\n
        -n --name=<output-file-name> TA file name to output (no extension).\n
        -j --jar=<ql-jar-file> The ql jar file location.\n
    "
    echo -e "$usage"

    # if errorCode
    if [[ -n "$1" ]]; then
        exit $1
    else
        exit 0
    fi
}

# $1=message, $2=errorCode, $3=outputUsage(0,1)
function errorMessage() {
    echo -e "Error: $1\n"
    # if outputUsage
    if [[ -n "$3" ]]; then
        outputUsage $2
    fi
    exit $2
}

# options
SHORT=h,c:,t:,n:,j:
LONG=help,contain:,tafile:,name:,jar:

# parse options and arguments
PARSED=$(getopt --options=$SHORT --longoptions=$LONG --name "$0" -- "$@")

# check for parsing error
if [[ $? -ne 0 ]]; then
    exit 2
fi

eval set -- "$PARSED"

# initialize
contain=""
ta=""
name=""
jar=""

# iterate over the options
while true; do
    case "$1" in
        -h|--help)
            outputUsage
            shift
            ;;
        -c|--contain)
            contain="$2"
            shift 2
            ;;
        -t|--tafile)
            ta="$2"
            shift 2
            ;;
        -n|--name)
            name="$2"
            shift 2
            ;;
        -j|--jar)
            jar="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            errorMessage "Unknown option '$1'" 3 1
            exit 3
            ;;
    esac
done

# check required args

if [[ -z "$contain" ]]; then
    errorMessage "Missing option 'contain'" 2 1
fi

if [[ -z "$ta" ]]; then
    errorMessage "Missing option 'ta'" 2 1
fi

if [[ -z "$name" ]]; then
    errorMessage "Missing option 'name'" 2 1
fi

if [[ -z "$jar" ]]; then
    errorMessage "Missing option 'jar'" 2 1
fi

java -Xms1g -Xmx3g -classpath $jar ca.uwaterloo.cs.ql.Main addcontain.ql $contain $ta $name.con.ta && cat schema.asv.ta $name.con.ta > $name.ls.ta
