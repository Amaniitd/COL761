ifile=$2;
sup=$3;
ofile=$4

secondarg=$2;
if [ "$1" = "-plot" ];
then
  python3 Plot.py $ifile
elif [ "$1" = "-apriori" ];
  then 
  ./apriori $ifile $sup $ofile 
elif [ "$1" = "-fptree" ];
  then 
  ./fptree $ifile $sup $ofile 
else
  echo "Incorrect arguments" 
fi
