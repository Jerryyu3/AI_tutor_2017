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

	elif [ "$exten" == "7z" ]; then
		7z x $file -o submissions/checkfile
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

	if [ -f checkfile/analysis.py ] && [ -f checkfile/qlearningAgents.py ] && [ -f checkfile/valueIterationAgents.py ] ; then
		mv -t ../reinforcement_grade checkfile/analysis.py checkfile/qlearningAgents.py checkfile/valueIterationAgents.py

		cd ../reinforcement_grade
		python autograder.py -t test_cases/q1/1-tinygrid --no-graphics > ../result/$filename
		python autograder.py -t test_cases/q1/2-tinygrid-noisy --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q1/3-bridge --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q1/4-discountgrid --no-graphics >> ../result/$filename
		
		echo "*End Q1" >> ../result/$filename

		python autograder.py -q q2 --no-graphics >> ../result/$filename
		echo "*End Q2" >> ../result/$filename

		python autograder.py -q q3 --no-graphics >> ../result/$filename
		echo "*End Q3" >> ../result/$filename

		python autograder.py -t test_cases/q4/1-tinygrid --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q4/2-tinygrid-noisy --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q4/3-bridge --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q4/4-discountgrid --no-graphics >> ../result/$filename
		echo "*End Q4" >> ../result/$filename

		python autograder.py -t test_cases/q5/1-tinygrid --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q5/2-tinygrid-noisy --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q5/3-bridge --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q5/4-discountgrid --no-graphics >> ../result/$filename	
		echo "*End Q5" >> ../result/$filename
		
		python autograder.py -q q6 --no-graphics >> ../result/$filename	
		echo "*End Q6" >> ../result/$filename

		#python autograder.py -q q7 --no-graphics >> ../result/$filename	
		python pacman.py -p PacmanQAgent -x 2000 -n 2020 -l smallGrid -q >> ../result/$filename
		echo "*End Q7" >> ../result/$filename

		python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 70 -l mediumClassic -q >> ../result/$filename
		echo "*End Q8" >> ../result/$filename

		mv qlearningAgents.py ../Check_Honesty/$filename2-qlearningAgents.py 
		mv analysis.py ../Check_Honesty/$filename2-analysis.py 
		mv valueIterationAgents.py ../Check_Honesty/$filename2-valueIterationAgents.py
		rm qlearningAgents.pyc
		rm analysis.pyc
		rm valueIterationAgents.pyc

		cd ..
		python grading_hw4.py ./result/$filename $k

		cd submissions
	fi
	
	rm -r checkfile
	cd ../
		
done
