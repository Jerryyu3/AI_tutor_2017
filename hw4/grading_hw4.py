import sys 
import csv

def main():
    with open(sys.argv[1], 'r') as parse_file:
        sentences = parse_file.readlines()
    
    score_str = ""
    prob = 1
    PASS_num = 0
    score = 0
    q7 = 0; q8 = 0; 

    for sentence in sentences:
        words = sentence.split();
        #print (words)
        if(len(words) == 0): continue;

        if(prob == 1):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                score += PASS_num * 0.375
                score_str += "Pass " + str(PASS_num) + " cases!\n"
                score_str += "q" + str(prob) + ": " + str('%.2f' % (PASS_num * 0.375)) + "\n\n"
                PASS_num = 0; prob += 1;

        elif(prob == 2 or prob == 6):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                score += PASS_num * 0.5
                if (PASS_num == 1): score_str += "Pass the case!\n"
                else: score_str += "Fail on the case!\n"
                score_str += "q" + str(prob) + ": " + str('%.2f' % (PASS_num * 0.5)) + "\n\n"
                PASS_num = 0; prob += 1;

        elif(prob == 3):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                score += PASS_num * 0.30
                score_str += "Pass " + str(PASS_num) + " cases!\n"
                score_str += "q" + str(prob) + ": " + str('%.2f' % (PASS_num * 0.30)) + "\n\n"
                PASS_num = 0; prob += 1;

        elif(prob == 4):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                score += PASS_num * 0.25
                score_str += "Pass " + str(PASS_num) + " cases!\n"
                score_str += "q" + str(prob) + ": " + str('%.2f' % (PASS_num * 0.25)) + "\n\n"
                PASS_num = 0; prob += 1;

        elif(prob == 5):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                score += 0.4
                score += PASS_num * 0.15
                score_str += "Pass " + str(PASS_num) + " cases and crawler.py!\n"
                score_str += "q" + str(prob) + ": " + str('%.2f' % (0.4 + PASS_num * 0.15)) + "\n\n"
                PASS_num = 0; prob += 1;

        elif(prob == 7):
            if(len(words) >= 3):
                if(words[0] == "Win"):
                    score_str += sentence
                    q7_win = words[2].split('/'); q7_win = int(q7_win[0])
                    
                    if(q7_win >= 16): q7 += 0.5

            if(words[0] == "*End"): 
                score_str += "q" + str(prob) + ": " + str(q7) + "\n\n"
                PASS_num = 0; prob += 1; score += q7

        elif(prob == 8):
            if(len(words) >= 3):
                if(words[0] == "Win"):
                    score_str += sentence
                    q8_win = words[2].split('/'); q8_win = int(q8_win[0])
                    
                    if(q8_win >= 16): q8 += 1.5
                    elif(q8_win >= 10): q8 += 1.0
                    elif(q8_win >= 1): q8 += 0.5

            if(words[0] == "*End"): 
                score_str += "q" + str(prob) + ": " + str(q8) + "\n\n"
                PASS_num = 0; prob += 1; score += q8

    grading_split = sys.argv[1].split('_')
    #student_ID = grading_split[1].split('.'); student_ID = student_ID[0].lower()

    if(sys.argv[2] == '1'): 
        score += 0.1
        score_str += "Format +0.1\n\n"

    score_str += "Total score is " + str(score) + "\n"
     
    with open("./result/" + grading_split[1], 'w') as grading_file: #Use the student's ID as the score file name
        grading_file.writelines(score_str)


def if_pass(word, PASS_num):
    if(word == "PASS:"): PASS_num += 1
    return (PASS_num)
    

if __name__ == '__main__':
    main()



