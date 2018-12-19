"""
Author: yu zhang
use different constrain function to test. each constrain reflect each word change.
if the constrain does not fit. it means it append nothing in the temp list. we just need to call previous word.

"""
def dict():
    return {1:['LASER','STEER','SAILS','SHEET','HOSES'],2:['HOSES','LASER','STEER','SHEET','SAILS'],3:['STEER','LASER','SAILS','SHEET','LASER'],4:['HEEL','HIKE','KNOT','KEEL','LINE'],5:['HEEL','HIKE','KNOT','KEEL','LINE'],6:['AFT','EEL','ALE','LEE','TIE'],7:['AFT','EEL','ALE','LEE','TIE'],8:['HOSES','STEER','SAILS','SHEET','LASER']}
worddict= dict()
#set up temp list to contain search result, if it is fit for constrain, save temp list to result.
templist1=[]
templist2=[]
templist3=[]
templist4=[]
templist5=[]
templist6=[]
templist7=[]
result={}
#set up flag and index to define position of search in each node
flag3=0
flag6=0
index2=0
flag5=0
flag4=0
index1=0
def word1():
    global index1
    result[1] = worddict[1][index1]
    word2()

def word2():
    global index1
    global index2
    global flag3
    templist1=[]
    for k in range(0,5):
        if (worddict[2][k][0]==result[1][2]):
            templist1.append(worddict[2][k])
    if not templist1:
        index1=index1+1
        word1()
    else:
        result[2]=templist1[index2]
        flag3=0
        word3()
		
def word3():
    global flag4
    global index2
    global flag5
    global index1
    global templist2
    if (flag3 < len(templist2) or flag3 == 0):
        templist2=[]
        for l in range(0,5):
            if (worddict[3][l][0]==result[1][4]):
                templist2.append(worddict[3][l])
        if not templist2:
            index1=index1+1
            word1()
        else:
            flag4=0
            flag5=0
            result[3]=templist2[flag3]
            word4(flag4)
    else:
        index2=index2+1
        word2()
def word4(flag4):
    global flag3
    global flag6
    global flag5
    global templist3
    if (flag4 < len(templist3) or flag4 == 0):
        templist3=[]
        for m in range(0,5):
            if(worddict[4][m][1]==result[2][2] and worddict[4][m][3]==result[3][2]):
                templist3.append(worddict[4][m])
        if not templist3:

            flag3=flag3+1
            word3()
        else:
            if (flag6 >4):
                del result[flag6]
                flag6=0	
            result[4]=templist3[flag4]
            word5(flag5)
    else:
        flag3=flag3+1
        word3()


def word5(dummyflag5):

    global flag6
    global templist4
    global flag4
    global flag5

    if (flag5 < len(templist4) or flag5 == 0):
        templist4=[]
        for n in range(0,5):
            if(worddict[5][n][0]==result[4][2]):
                templist4.append(worddict[5][n])
        if not templist4:
            del result[4]
            del (flag4)
        else:
            result[5]=templist4[flag5]
            word6(flag6)
    else:
        flag4=flag4+1
        word4(flag4)

def word6(flag6):
    global templist5
    global flag5
    if (flag6 < len(templist5) or flag6 == 0):
        templist5=[]
        for o in range(0,5):
            templist5.append(worddict[6][o])

        result[6]=templist5[flag6]
        word7()
    else:
        flag5=flag5+1
        word5(flag5)

def word7():
    global templist6
    global flag4
    global flag5
    global flag6
    templist6=[]
    for p in range(0,5):
        if(worddict[7][p][0]==result[2][3] and worddict[7][p][1]==result[5][1] and worddict[7][p][2]==result[3][3]):
            templist6.append(worddict[7][p])

    if not templist6:
        flag5=flag5+1
        flag6=0
        word5(flag5)
    else:
        result[7]=templist6[0]
        flag5=0
        word8()
def word8():
    global flag6
    global flag5
    for q in range(0,5):	
        if (worddict[8][q] not in result.values()):
            if(worddict[8][q][0]==result[6][1] and worddict[8][q][2]==result[2][4] and worddict[8][q][3]== result[5][2] and worddict[8][q][4]== result[3][4]):
                templist7.append(worddict[8][q])
    if not templist7:
        flag6=flag6+1
        del result[6]
        del result[7]
        flag5=flag5+1	
        word6(flag6)
    else:
        print ("result is")
        result[8]=templist7[0]
        print (result)


word1()	
