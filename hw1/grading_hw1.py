import sys 
import csv


def main():
    with open(sys.argv[1], 'r') as parse_file:
        sentences = parse_file.readlines()
    
    score_str = ""
    prob = 1
    PASS_num = 0
    score = 0
    q5_eval = 0; q6 = 0; q7 = 0

    for sentence in sentences:
        words = sentence.split();
        #print (words)
        if(len(words) == 0): continue;

        if(prob >= 1 and prob <= 4):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                score += PASS_num * 0.2
                score_str += "Pass " + str(PASS_num) + " cases!\n"
                score_str += "q" + str(prob) + ": " + str('%.1f' % (PASS_num * 0.2)) + "\n\n"
                PASS_num = 0; prob += 1;

        elif(prob == 5):
            if(len(words) >= 3):
                if(words[1] == "PASS:"):
                    score += 1; score_str += "Pass question 5!\nq5: 1.0\n\n"; q5_eval = 1

                elif(words[2] == "length:" and q5_eval == 0):
                    length = int(words[3])
                    if(abs(length-28) <= 1):
                        score += 0.8; score_str += "Correct tiny corner solution length is 28, yours is " + words[3] + ".\nq5: 0.8\n\n"
                    elif(abs(length-28) <= 2):
                        score += 0.5; score_str += "Correct tiny corner solution length is 28, yours is " + words[3] + ".\nq5: 0.5\n\n"
                    else:
                        score += 0; score_str += "Correct tiny corner solution length is 28, yours is " + words[3] + ".\nq5: 0.0\n\n"
                    q5_eval = 1
 
            if(words[0] == "*End"):
                if (q5_eval == 0): score_str += "Test Fail!\nq5: 0\n\n"
                prob += 1

        elif(prob == 6):
            if(len(words) >= 2):
                if(words[1] == "length:"):
                    length = int(words[2])
                    if(length == 106):
                        q6 -= 0  
                    elif(abs(length-106) <= 1):
                        q6 -= 0.3; score_str += "Path length is 106, yours is " + words[2] + ".\n"
                    elif(abs(length-106) <= 2):
                        q6 -= 0.5; score_str += "Path length is 106, yours is " + words[2] + ".\n"
                    else:
                        q6 -= 1; score_str += "Path length is 106, yours is " + words[2] + ".\n"

                elif(words[-1] != "nodes"): PASS_num = if_pass(words[1], PASS_num)

                else:
                    nodes_count = int(words[-2])
                    if(nodes_count <= 850 and nodes_count > 200):
                        if(PASS_num >= 2): q6 += 1.8
                        else: q6 += 1.2
                    elif(nodes_count <= 1100 and nodes_count > 200):
                        if(PASS_num >= 2): q6 += 1.35
                        else: q6 += 0.9
                    elif(nodes_count <= 1350 and nodes_count > 200):
                        if(PASS_num >= 2): q6 += 0.9
                        else: q6 += 0.6
                    elif(nodes_count <= 1600 and nodes_count > 200):
                        if(PASS_num >= 2): q6 += 0.45
                        else: q6 += 0.3
                    score_str += "Expand " + str(nodes_count) + " nodes! \n"

            if(words[0] == "*End"): 
                q6 += (0.2 if PASS_num * 0.08 >= 0.16 else PASS_num * 0.08)
                q6 = (q6 if q6 >= 0 else 0)
                score_str += "Admissibility and consistence test: pass " + str((3 if PASS_num >= 2 else PASS_num)) + " layouts!\n"
                score_str += "q" + str(prob) + ": " + str(q6) + "\n\n"
                PASS_num = 0; prob += 1; score += q6
        else:
            if(len(words) >= 3):
                if(words[2] == "nodes:"):
                    nodes_count = int(words[3])

                    if(nodes_count <= 9000):
                        if(PASS_num >= 5): q7 += 1.8
                        else: q7 += 1.05
                    elif(nodes_count <= 12000):
                        if(PASS_num >= 5): q7 += 1.35
                        else: q7 += 0.7
                    elif(nodes_count <= 15000):
                        if(PASS_num >= 5): q7 += 0.9
                        else: q7 += 0.35
                    else:
                        if(PASS_num >= 5): q7 += 0.45
                        else: q7 += 0.0
                    score_str += "Expand " + str(nodes_count) + " nodes! \n"

                elif(words[-1] != "test_cases/q7/food_heuristic_0grade_tricky.test"): PASS_num = if_pass(words[1], PASS_num)

            if(words[0] == "*End"):
                PASS_num = (5 if PASS_num >= 5 else PASS_num)
                q7 += PASS_num * 0.04
                score_str += "Admissibility and consistence test: pass " + str(PASS_num) + " layouts!\n"
                score_str += "q" + str(prob) + ": " + str(q7) + "\n\n"
                PASS_num = 0; prob += 1; score += q7

    if(sys.argv[2] == '1'): 
        score += 0.1
        score_str += "Format +0.1\n\n"

    score_str += "Total score is " + str(score) + "\n"

    grading_split = sys.argv[1].split('_')
     
    with open("./result/" + grading_split[1], 'w') as grading_file:
        grading_file.writelines(score_str)

def if_pass(word, PASS_num):
    if(word == "PASS:"): PASS_num += 1
    return (PASS_num)
    

if __name__ == '__main__':
    main()



