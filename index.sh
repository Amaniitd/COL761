g++ ./modified_dataset.cpp
./a.out $1
./gSpan6/gSpan -f ./modified_dataset -s 0.6 -o -i
g++ generate_index.cpp
./a.out