#!/bin/bash
################################################################################
# Run LSEDIT: note to make sure you have JAVA_HOME on path
################################################################################

command="ls-edit.sh"

function outputUsage() {
    usage="Visualize TA file dependency using LSEDIT.\n\n
    Usage:\n
        $command -f <ta-dependency-file> -j <lsedit-jar-file>\n
        $command -h | --help\n
    Options:\n
        -h --help Show usage.\n
        -f --file=<ta-dependency-file> TA containment dependency file.\n
        -j --jar=<lsedit-jar-file> The LSEDIT jar file location.\n
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
SHORT=h,f:,j:
LONG=help,file:,jar:

# parse options and arguments
PARSED=$(getopt --options=$SHORT --longoptions=$LONG --name "$0" -- "$@")

# check for parsing error
if [[ $? -ne 0 ]]; then
    exit 2
fi

eval set -- "$PARSED"

# initialize
file=""
jar=""

# iterate over the options
while true; do
    case "$1" in
        -h|--help)
            outputUsage
            shift
            ;;
        -f|--file)
            file="$2"
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

if [[ -z "$file" ]]; then
    errorMessage "Missing option 'file'" 2 1
fi

if [[ -z "$jar" ]]; then
    errorMessage "Missing option 'jar'" 2 1
fi

java -Xms1g -Xmx3g -jar $jar -v -d $file
