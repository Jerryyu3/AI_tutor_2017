#!/bin/bash
	
	filename=$1 # Enter the full name (exclude .zip) of the zip file
	#filename="${filename%%.*}"
	filename2="${filename%_*}" # Eliminate the first string after "_"
	filename="${filename2%_*}".txt
	filename2="${filename2%_*}"
	filename2="${filename2#*_}" # Eliminate the first string before "_"
	echo $filename

		cd ./tracking_grade
		python autograder.py -t test_cases/q1/2-ExactObserve --no-graphics > ../result/$filename  # Tese case by case to reduce the effect of crash on some question
		#python autograder.py -q q1 --no-graphics > ../result/$filename
		python autograder.py -t test_cases/q1/4-ExactObserve --no-graphics >> ../result/$filename
		echo "*End Q1" >> ../result/$filename

		#python autograder.py -q q2 --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q2/2-ExactElapse --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q2/3-ExactElapse --no-graphics >> ../result/$filename
		
		echo "*End Q2" >> ../result/$filename

		python autograder.py -q q3 --no-graphics >> ../result/$filename
		echo "*End Q3" >> ../result/$filename

		#python autograder.py -q q4 --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q4/2-ParticleObserve --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q4/4-ParticleObserve --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q4/5-ParticleObserve --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q4/7-ParticleObserve --no-graphics >> ../result/$filename
	
		echo "*End Q4" >> ../result/$filename

		#python autograder.py -q q5 --no-graphics >> ../result/$filename	
		python autograder.py -t test_cases/q5/2-ParticleElapse --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q5/3-ParticleElapse --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q5/4-ParticleElapse --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q5/6-ParticleElapse --no-graphics >> ../result/$filename
	
		echo "*End Q5" >> ../result/$filename
		
		#python autograder.py -q q6 --no-graphics >> ../result/$filename	
		python autograder.py -t test_cases/q6/2-JointParticleObserve --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q6/3-JointParticleObserve --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q6/4-JointParticleObserve --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q6/5-JointParticleObserve --no-graphics >> ../result/$filename	
		echo "*End Q6" >> ../result/$filename

		#python autograder.py -q q7 --no-graphics >> ../result/$filename	
		python autograder.py -t test_cases/q7/1-JointParticleElapse --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q7/2-JointParticleElapse --no-graphics >> ../result/$filename
		python autograder.py -t test_cases/q7/3-JointParticleObserveElapse --no-graphics >> ../result/$filename
	
		echo "*End Q7" >> ../result/$filename

		mv bustersAgents.py ../Check_Honesty/$filename2-bustersAgents.py 
		mv inference.py ../Check_Honesty/$filename2-inference.py 

		cd ..
		python grading_hw3.py ./result/$filename 0
		
