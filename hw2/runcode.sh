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
		unrar $file 
		mv multiAgents.py -t submissions/checkfile
	elif [ "$exten" == "7z" ]; then
		7z x $file
		mv multiAgents.py -t submissions/checkfile	
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
	
	if [ -f checkfile/multiAgents.py ] ; then
		mv -t ../multiagents_grade checkfile/multiAgents.py

		cd ../multiagents_grade
		python pacman.py -p ReflexAgent -l openClassic -n 10 -q > ../result/$filename
		echo "*End Q1" >> ../result/$filename

		python autograder.py -t test_cases/q2/8-pacman-game >> ../result/$filename
		echo "*End Q2" >> ../result/$filename

		python autograder.py -t test_cases/q3/8-pacman-game  >> ../result/$filename
		echo "*End Q3" >> ../result/$filename

		python autograder.py -t test_cases/q4/7-pacman-game >> ../result/$filename
		echo "*End Q4" >> ../result/$filename

		python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 30 >> ../result/$filename
		echo "*End Q5" >> ../result/$filename

		mv multiAgents.py ../Check_Honesty/$filename2-multiAgents.py 

		cd ..
		#python grading_hw2.py ./result/$filename $k

		cd submissions
	fi
	
	rm -r checkfile
	cd ../
		
done
