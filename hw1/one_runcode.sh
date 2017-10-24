#!/bin/bash


	filename=$1
	#filename="${filename%%.*}"
	filename2="${filename%_*}"
	filename="${filename2%_*}".txt
	filename2="${filename2%_*}"
	filename2="${filename2#*_}"
	echo $filename
	

		cd search_grade
		python autograder.py -t test_cases/q1/graph_backtrack > ../result/$filename
		python autograder.py -t test_cases/q1/graph_bfs_vs_dfs >> ../result/$filename
		python autograder.py -t test_cases/q1/graph_infinite >> ../result/$filename
		python autograder.py -t test_cases/q1/graph_manypaths >> ../result/$filename
		python autograder.py -t test_cases/q1/pacman_1 >> ../result/$filename
		echo "*End Q1" >> ../result/$filename

		python autograder.py -t test_cases/q2/graph_backtrack >> ../result/$filename
		python autograder.py -t test_cases/q2/graph_bfs_vs_dfs >> ../result/$filename
		python autograder.py -t test_cases/q2/graph_infinite >> ../result/$filename
		python autograder.py -t test_cases/q2/graph_manypaths >> ../result/$filename
		python autograder.py -t test_cases/q2/pacman_1 >> ../result/$filename
		echo "*End Q2" >> ../result/$filename

		python autograder.py -t test_cases/q3/graph_manypaths >> ../result/$filename
		python autograder.py -t test_cases/q3/ucs_0_graph >> ../result/$filename
		python autograder.py -t test_cases/q3/ucs_1_problemC >> ../result/$filename
		python autograder.py -t test_cases/q3/ucs_4_testSearch >> ../result/$filename
		python autograder.py -t test_cases/q3/ucs_5_goalAtDequeue >> ../result/$filename
		echo "*End Q3" >> ../result/$filename

		python autograder.py -t test_cases/q4/astar_0 >> ../result/$filename
		python autograder.py -t test_cases/q4/astar_1_graph_heuristic >> ../result/$filename
		python autograder.py -t test_cases/q4/astar_2_manhattan >> ../result/$filename
		python autograder.py -t test_cases/q4/graph_backtrack >> ../result/$filename
		python autograder.py -t test_cases/q4/graph_manypaths >> ../result/$filename
		echo "*End Q4" >> ../result/$filename

		python autograder.py -t test_cases/q5/corner_tiny_corner >> ../result/$filename
		echo "*End Q5" >> ../result/$filename

		python autograder.py -t test_cases/q6/corner_sanity_1 >> ../result/$filename
		python autograder.py -t test_cases/q6/corner_sanity_2 >> ../result/$filename
		python autograder.py -t test_cases/q6/corner_sanity_3 >> ../result/$filename
		python autograder.py -t test_cases/q6/medium_corners >> ../result/$filename
		echo "*End Q6" >> ../result/$filename

		python autograder.py -t test_cases/q7/food_heuristic_1 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_2 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_3 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_4 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_5 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_6 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_12 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_13 >> ../result/$filename
		python autograder.py -t test_cases/q7/food_heuristic_0grade_tricky >> ../result/$filename
		echo "*End Q7" >> ../result/$filename

		mv search.py ../Check_Honesty/$filename2-search.py 
		mv searchAgents.py ../Check_Honesty/$filename2-searchAgents.py

		cd ..
		python grading_hw1.py ./result/$filename $2

	
		
