import sys

public_score = {}
public_rank = {}
private_score = {}
private_rank = {}

with open("public.csv", 'r') as f:
    for l in list(f):
        cols = l.split(",")
        public_score[cols[1]] = float(cols[-1])
        public_rank[cols[1]] = int(cols[0])

with open("private.csv", 'r') as f:
    for l in list(f):
        cols = l.split(",")
        private_score[cols[1]] = float(cols[-1])
        private_rank[cols[1]] = int(cols[0])

names = list(public_rank.keys())

if sys.argv[1] == "rank":
    ns = [k for k in sorted(public_rank, key=public_rank.get)]
    for n in ns:
        if n not in private_rank:
            private_rank[n] = "--"
        print(public_rank[n], n, private_rank[n])
elif sys.argv[1] == "score":
    ns = list(public_score)
    total = {}
    for n in ns:
        if n not in private_score:
            private_score[n] = 0
        total[n] = (public_score[n] + private_score[n]) / 2
    ns = [k for k in sorted(total, key=total.get, reverse=True)]
    for n in ns:
        print(n, total[n])