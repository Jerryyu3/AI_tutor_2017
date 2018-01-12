#!/bin/bash

for file in ./submissions/*
do
	cd ./submissions
	mkdir checkfile
	cd ../

	k=0
	exten="${file##*.}"
	if [ "$exten" == "zip" ] ; then
		unzip $file -d submissions/checkfile
		k=1
	elif [ "$exten" == "gz" ] || [ "$exten" == "tgz" ] || [ "$exten" == "tar" ]; then
		tar -zxvf $file -C submissions/checkfile
		k=1
	elif [ "$exten" == "rar" ]; then
		unrar e $file submissions/checkfile
		#mv multiAgents.py -t submissions/checkfile

	elif [ "$exten" == "7z" ]; then
		7z x $file -o submissions/checkfile
		#mv multiAgents.py -t submissions/checkfile	
	else
		continue
	fi
	
	cd ./submissions/checkfile
	#count=$(ls | wc -l)
	#if [ $count != 2 ] ; then
	#	echo $count
	#	k=0
	#fi

	cd ../

	filename="${file##*/}" # Eliminate all strings before "/"
	#filename="${filename%%.*}"
	filename2="${filename%_*}" # Eliminate the first string after "_"
	filename="${filename2%_*}".txt
	filename2="${filename2%_*}"
	filename2="${filename2#*_}" # Eliminate the first string before "_"
	echo $filename
	
	#if [ -f checkfile/search.py ] ; then
	#	mv -t ../tracking_grade checkfile/search.py
	#fi

	#if [ -f checkfile/searchAgents.py ] ; then
	#	mv -t ../tracking_grade checkfile/searchAgents.py
	#fi

	if [ -f checkfile/inference.py ] && [ -f checkfile/bustersAgents.py ]; then
		mv -t ../tracking_grade checkfile/inference.py checkfile/bustersAgents.py

		cd ../tracking_grade
		python autograder.py -q q1 --no-graphics > ../result/$filename
		echo "*End Q1" >> ../result/$filename

		python autograder.py -q q2 --no-graphics >> ../result/$filename
		echo "*End Q2" >> ../result/$filename

		python autograder.py -q q3 --no-graphics >> ../result/$filename
		echo "*End Q3" >> ../result/$filename

		python autograder.py -q q4 --no-graphics >> ../result/$filename
		echo "*End Q4" >> ../result/$filename

		python autograder.py -q q5 --no-graphics >> ../result/$filename	
		echo "*End Q5" >> ../result/$filename
		
		python autograder.py -q q6 --no-graphics >> ../result/$filename	
		echo "*End Q6" >> ../result/$filename

		python autograder.py -q q7 --no-graphics >> ../result/$filename	
		echo "*End Q7" >> ../result/$filename

		mv bustersAgents.py ../Check_Honesty/$filename2-bustersAgents.py 
		mv inference.py ../Check_Honesty/$filename2-inference.py 

		#if [ -f search.py ] ; then
		#	rm search.py
		#fi
		#if [ -f searchAgents.py ] ; then
		#	rm searchAgents.py
		#fi

		cd ..
		python grading_hw3.py ./result/$filename $k

		cd submissions
	fi
	
	rm -r checkfile
	cd ../
		
done
