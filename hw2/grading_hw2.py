import sys 
import csv

def main():
    with open(sys.argv[1], 'r') as parse_file:
        sentences = parse_file.readlines()
    
    score_str = ""
    prob = 1
    PASS_num = 0
    score = 0
    q1 = 0; q5 = 0

    for sentence in sentences:
        words = sentence.split();
        #print (words)
        if(len(words) == 0): continue;

        if(prob >= 2 and prob <= 4):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                if(PASS_num == 1):
                    score += 1.5
                    score_str += "Pass Question " + str(prob) + "!\n"
                    score_str += "q" + str(prob) + ": " + str('%.1f' % (PASS_num * 1.5)) + "\n\n"
                    PASS_num = 0; prob += 1;
                else:
                    score += 1.2
                    score_str += "Some error on question" + str(prob) + "!\n"
                    score_str += "q" + str(prob) + ": 1.2\n\n"
                    prob += 1
 

        elif(prob == 5):
            if(len(words) >= 3):
                if(words[0] == "Average"):
                    score_str += sentence
                    q5_pacman_score = float(words[2])
                    
                    if(q5_pacman_score >= 1450): q5 += 1.6
                    elif(q5_pacman_score >= 1350): q5 += 1.4
                    elif(q5_pacman_score >= 1200): q5 += 1.2
                    elif(q5_pacman_score >= 1000): q5 += 0.8
                    elif(q5_pacman_score >= 750): q5 += 0.4

                elif(words[0] == "Win"): 
                    score_str += sentence
                    q5_win = words[2].split('/'); q5_win = int(q5_win[0])
                    
                    if(q5_win >= 15): q5 += 0.9
                    elif(q5_win >= 1): q5 += 0.4

            if(words[0] == "*End"): 
                score_str += "q" + str(prob) + ": " + str(q5) + "\n\n"
                PASS_num = 0; prob += 1; score += q5


        elif(prob == 1):
            if(len(words) >= 3):
                if(words[0] == "Average"):
                    score_str += sentence
                    q1_pacman_score = float(words[2])
                    
                    if(q1_pacman_score >= 1200): q1 += 1
                    elif(q1_pacman_score >= 1000): q1 += 0.75
                    elif(q1_pacman_score >= 800): q1 += 0.5
                    elif(q1_pacman_score >= 600): q1 += 0.25

                elif(words[0] == "Win"): 
                    score_str += sentence
                    q1_win = words[2].split('/'); q1_win = int(q1_win[0])
                    
                    if(q1_win >= 8): q1 += 0.7
                    elif(q1_win >= 5): q1 += 0.4

            if(words[0] == "*End"): 
                score_str += "q" + str(prob) + ": " + str(q1) + "\n\n"
                PASS_num = 0; prob += 1; score += q1

    grading_split = sys.argv[1].split('_')
    student_ID = grading_split[1].split('.'); student_ID = student_ID[0].lower()

    csv_file = csv.reader(open('HW2_Documentation.csv', "r"), delimiter=",")
    for row in csv_file:
        if student_ID == row[0]:
            score += float(row[1])
            score_str += "The documentation score is " + row[1] + "!\n\n"

    if(sys.argv[2] == '1'): 
        score += 0.1
        score_str += "Format +0.1\n\n"

    score_str += "Total score is " + str(score) + "\n"
     
    with open("./result/" + grading_split[1], 'w') as grading_file:
        grading_file.writelines(score_str)



def if_pass(word, PASS_num):
    if(word == "PASS:"): PASS_num += 1
    return (PASS_num)
    

if __name__ == '__main__':
    main()



