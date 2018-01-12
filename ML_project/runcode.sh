#!/bin/bash

for file in ./code/*
do

	k=0
	exten="${file##*.}"
	if [ "$exten" == "zip" ] ; then
		unzip $file -d ./Test_dir
		k=1
	elif [ "$exten" == "gz" ] || [ "$exten" == "tgz" ] || [ "$exten" == "tar" ]; then
		tar -zxvf $file -C ./Test_dir
		k=1
	elif [ "$exten" == "rar" ]; then
		unrar e $file ./Test_dir

	elif [ "$exten" == "7z" ]; then
		7z x $file -o ./Test_dir
	else
		continue
	fi

	filename="${file##*/}" # Eliminate all strings before "/"
	#filename="${filename%%.*}"
	filename2="${filename%_*}" # Eliminate the first string after "_"
	filename="${filename2%_*}".txt
	filename2="${filename2%_*}"
	filename2="${filename2#*_}" # Eliminate the first string before "_"
	echo $filename

	cp Train.csv ./Test_dir/Train.csv
	cp Test_Public.csv ./Test_dir/Test_Public.csv
	cp Test_Private.csv ./Test_dir/Test_Private.csv

	cd ./Test_dir
	chmod +x ./Default_train.sh 
	chmod +x ./Default_predict.sh

	./Default_train.sh Train.csv > ../log_file/$filename
	./Default_predict.sh Test_Public.csv Test_Private.csv >> ../log_file/$filename
	#python grading_ML.py 

	mv public.csv ../Temp_Save/$filename2-public.csv
	mv private.csv ../Temp_Save/$filename2-private.csv
	mv Documentation.pdf ../Documentation_dir/$filename2-Documentation.pdf

	cd ..

	rm -r ./Test_dir/*
	
done
