#!/bin/bash

	filename=$1 # Enter the full name (exclude .zip) of the zip file 
	#filename="${filename%%.*}"
	filename2="${filename%_*}" # Eliminate the first string after "_"
	filename="${filename2%_*}".txt
	filename2="${filename2%_*}"
	filename2="${filename2#*_}" # Eliminate the first string before "_"
	echo $filename

		cd multiagents_grade # Change to the working directory
		python pacman.py -p ReflexAgent -l openClassic -n 10 -q > ../result/$filename
		echo "*End Q1" >> ../result/$filename

		python autograder.py -q q2 --no-graphics >> ../result/$filename
		echo "*End Q2" >> ../result/$filename

		python autograder.py -q q3 --no-graphics  >> ../result/$filename
		echo "*End Q3" >> ../result/$filename

		python autograder.py -q q4 --no-graphics >> ../result/$filename
		echo "*End Q4" >> ../result/$filename

		python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 30 >> ../result/$filename
		echo "*End Q5" >> ../result/$filename

		mv multiAgents.py ../Check_Honesty/$filename2-multiAgents.py # Move the codes for honesty check

		if [ -f search.py ] ; then
			rm search.py
		fi
		if [ -f searchAgents.py ] ; then
			rm searchAgents.py
		fi

		cd ..
		python grading_hw2.py ./result/$filename 0 # Use the log file to output the result
	
		
