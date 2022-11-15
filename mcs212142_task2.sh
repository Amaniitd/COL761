arg1=$1 #train or test?
arg2=$2 #p
arg3=$3 #f
arg4=$4 #train/test data
arg5=$5 #adj/output
arg6=$6 #splits/model

if [ "$1" = "train" ];
then
  python3 2.py $arg4 $arg5 $arg6 $arg2 $arg3
else
  python3 2test.py $arg4 $arg5 $arg6 $arg2 $arg3 
fi
