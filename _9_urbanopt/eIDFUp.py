#generated one text file, name as 22-2-0To23-1-0.lst
#there are 38 lines, each line is `in_uwyo_1.idf`, `in_uwyo_2.idf`, etc.

savefile = open("22-2-0To23-1-0-Linux.lst", "w")
for i in range(38, 0, -1):
    savefile.write("/home/xxx/fortran_experiments/_9_urbanopt/la38-22-2-0/in_uwyo_" + str(i) + ".idf\n")
savefile.close()