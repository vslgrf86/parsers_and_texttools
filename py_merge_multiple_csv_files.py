# merge multiple csv files with pandas
# https://stackoverflow.com/questions/2512386/how-to-merge-200-csv-files-in-python
# define/create export file
fout=open("out3.csv","a")
# define first file to be exported:
for line in open("20220425_absence_mrr_development_1.csv"):
    fout.write(line)
# range for the rest files, based on name convention:    
for num in range(1,27):
    f = open("20220425_absence_mrr_development_"+str(num)+".csv")

    for line in f:
         fout.write(line)
 fout.close()