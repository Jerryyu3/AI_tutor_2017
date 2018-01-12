import sys
from os import listdir
from os.path import isfile, join

K = 500

def getid(filename, n=-1):
    ids = []
    with open(filename, 'r') as f:
        lines = list(f)
        if n == -1 or n > len(lines) - 1:
            for l in lines[1:]:
                ids.append(int(l))
        else:
            for l in lines[1:n+1]:
                ids.append(int(l))
    return ids

def ap8k(test, ans, k):
    count = 0
    ap = 0
    for i in range(k):
        if testid[i] in testans:
            count += 1
        ap += count / (i + 1)
    return ap/k

#testid = getid(sys.argv[1], K)
#print(len(testid))
testans = getid("../Test_Ans_Public.csv")
#ap = ap8k(testid, testans, K)

filepath = sys.argv[1]
filenames = [fn for fn in listdir(filepath) if isfile(join(filepath, fn))]
total = {}
for filename in filenames:
    if filename.endswith(".csv"):
        student = filename.split("-")[0]
        testid = getid(filepath+"/"+filename)
        #testid.reverse()
        ap = ap8k(testid, testans, K)
        total[student] = ap
        #print(student, ap)

sort_total = [(k, total[k]) for k in sorted(total, key=total.get, reverse=True)]
for s in sort_total:
    #if s[1] == 0:
    #    print("{}@ntu.edu.tw;".format(s[0]), s[1])
    print("{},{}".format(s[0], s[1]))
