arg1=$1
arg2=$2
arg3=$3
arg4=$4

if [ "$1" = "train" ];
then
  python3 1.py $2 $3 $4
else
  python3 1test.py $2 $3 $4 
fi
