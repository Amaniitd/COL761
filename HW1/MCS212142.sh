ifile=$2;
sup=$3;
ofile=$4

if [ "$1" = "-plot" ];
then
  python3 plot.py $ifile $sup
elif [ "$1" = "-apriori" ];
  then 
  ./apriori.o $ifile $sup $ofile 
elif [ "$1" = "-fptree" ];
  then 
  ./fptree.o $ifile $sup $ofile 
else
  echo "Incorrect arguments" 
fi
