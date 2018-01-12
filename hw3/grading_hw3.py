import sys 
import csv

def main():
    with open(sys.argv[1], 'r') as parse_file:
        sentences = parse_file.readlines()
    
    score_str = ""
    prob = 1
    PASS_num = 0
    score = 0
    q3 = 0

    for sentence in sentences:
        words = sentence.split();
        #print (words)
        if(len(words) == 0): continue;

        if(prob != 3 and prob <= 6):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                score += PASS_num * 0.25
                score_str += "Pass " + str(PASS_num) + " cases!\n"
                score_str += "q" + str(prob) + ": " + str('%.2f' % (PASS_num * 0.25)) + "\n\n"
                PASS_num = 0; prob += 1;
        
        elif(prob == 7):
            if(len(words) >= 2): PASS_num = if_pass(words[1], PASS_num)
            
            if(words[0] == "*End"): 
                PASS_num += 1
                score += PASS_num * 0.25
                score_str += "Pass " + str(PASS_num) + " cases!\n"
                score_str += "q" + str(prob) + ": " + str('%.2f' % (PASS_num * 0.25)) + "\n\n"
                PASS_num = 0; prob += 1;


        elif(prob == 3):
            if(len(words) >= 3):
                if(words[0] == "Average"):
                    score_str += sentence
                    q3_pacman_score = float(words[2])
                    
                    if(q3_pacman_score >= 700): q3 += 1.0
                    elif(q3_pacman_score >= 500): q3 += 0.5


            if(words[0] == "*End"): 
                score_str += "q" + str(prob) + ": " + str(q3) + "\n\n"
                PASS_num = 0; prob += 1; score += q3


    grading_split = sys.argv[1].split('_')
    #student_ID = grading_split[1].split('.'); student_ID = student_ID[0].lower()

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



