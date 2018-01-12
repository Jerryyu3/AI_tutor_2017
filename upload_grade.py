import csv

def main():
	f = open('Upload.csv','w',newline='');
	w = csv.writer(f);
	data = list(); 
	with open('成績統計.csv','r')as file2:
		for row in csv.DictReader(file2):
			tempdata = [row['學號'],row['第十七週分數']];
			str1 = "\"選擇題:"+row['第十七週選擇']+"\n手寫題:"+row['第十七週手寫']+"\n作業總分:"+row['第十七週作業']+"\n交換改出席:"+row['第十七週交換改']+"\"";
			tempdata.append(str1);
			data.append(tempdata);
	w.writerows(data);
	f.close();
if __name__ == '__main__':
	main();