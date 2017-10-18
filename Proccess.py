import sys
import math
import csv
import operator

f1 = open("input.txt",'r')
f2 = open("router.txt",'r')
B = []
lengths = []
ct=0

def mini(q,w,e):  #Function that takes into account overlapping. And only then finds minimum 
    if(q<0 and w<0 and e<0):
        return min(abs(q),abs(w),abs(e))
    else:
        a = [q,w,e]
        return min(i for i in a if i > 0)   #Finds smallest number greater than 0
    
def eucl_dist(x1,y1,x2,y2):  
    return math.sqrt(pow(int(x2)-int(x1),2)+pow(int(y2)-int(y1),2))

def adjust(Q,i):
    flag =1
    wierd = []
    if(len(Router)==3):
        a1 = float(Q[0]+Q[1])
        a2 = float(Q[0]+Q[2])
        a3 = float(Q[1]+Q[2])
        
        Burst = mini(lengths[0]-a1,lengths[1]-a2,lengths[2]-a3) # Perfect logic
        #Burst = min(abs(a1-lengths[0]),abs(a2-lengths[1]),abs(a3-lengths[2]))  #Also works but is inefficient. Since overlap area is smaller
        while(flag!=(-1)):
            
            if((a1<lengths[0] or a2<lengths[1] or a3<lengths[2]) and flag==1):  # BURST VALUE, Initial jump in adjustment, used to reduce complexity
                #print("CHECK 1")
                a1+=Burst
                a2+=Burst
                a3+=Burst
                flag=0
            elif((a1<lengths[0] or a2<lengths[1] or a3<lengths[2]) and flag==0): # Minor incremental adjustments
                #print("CHECK 2")
                a1+= Burst*0.1
                a2+= Burst*0.1
                a3+= Burst*0.1
            #print(str(Q[i]) + " + "+str(Q[j])+ " < " + str(lengths[i]) + " Are underestimating")
            else:
                flag=-1
                print("adjust seems to be a success....")
                print("Calibrating new length values....")
                wierd.append(max(((Q[0]/(Q[0]+Q[1]))*a1),((Q[0]/(Q[0]+Q[2]))*a2)))
                wierd.append(max(((Q[1]/(Q[0]+Q[1]))*a1),((Q[1]/(Q[1]+Q[2]))*a3)))  #WE SHOULD USE MAXIMUM INSTEAD OF AVERAGING :) 
                wierd.append(max(((Q[2]/(Q[0]+Q[2]))*a2),((Q[2]/(Q[1]+Q[2]))*a3)))
                '''
                wierd.append(((Q[0]/(Q[0]+Q[1])*a1) + (Q[0]/(Q[0]+Q[2])*a2))/2)  ##
                wierd.append(((Q[1]/(Q[0]+Q[1])*a1) + (Q[0]/(Q[1]+Q[2])*a3))/2)  ## 
                wierd.append(((Q[2]/(Q[0]+Q[2])*a2) + (Q[2]/(Q[1]+Q[2])*a3))/2)  ## ^^TURNS OUT IT DOESN't WORK, CAUSE OVERLAP BREAKS IT^^
                '''
    else:
        print("Throwing Router mismatch exception!!")
        return
    #print("ERROR CHECK WIERD IS ")
    print(wierd)
    Q[0] = wierd[0]
    Q[1] = wierd[1]
    Q[2] = wierd[2]
    print ("Calibration success. Changes should be reflected in PARENT CODE")
    Q.insert(i,"x") #Write 'x' wherever router is 
    
    #########^^^^^^^^^^^^ENJOY WRITING COMMENTS FOR THIS SHIT :D  ^^^^^^^^^^^##########

class router:
    def __init__(self):
        x = 0
        y = 0

for line in f1:
    A = line.split()
    for i in range(len(A)):
        A[i]=float(A[i])
    B.append(A)

Router = []
for line in f2:
    C = line.split()
    if((C[0]=='Y' or C[0]=='y') and ct==0):
        ct+=1
        continue
    elif((C[0]=='N' or C[0]=='n') and ct==0):
        ct+=2
        continue
    elif(ct==0):
        print("ERROR DETECTED, [Y / N] not specified, EXITING")
        exit()
    if(ct==1): # THIS CODE REQUIRES x2 for Y axis I guess
        r1 = router()
        r1.x=float(C[0])*2.0558
        r1.y=float(C[1])*1.2
        Router.append(r1)
    if(ct==2): # THIS CODE Does not require x2 for any axis
        r1 = router()
        r1.x=float(C[0])
        r1.y=float(C[1])
        Router.append(r1)
'''
for i in range(len(Router)-1):
    for j in range(i+1,len(Router)):    #Writes lengths between router
        guk = eucl_dist(Router[i].x,Router[i].y,Router[j].x,Router[j].y) #guk stores euclidian distance
        lengths.append(guk)
        #print ("The Euclidean distance between Router " +str(i+1)+" and Router "+str(j+1)+" Is "+str(guk) )
'''


EOF = 0  # Basically EACH LINE STORED IN B
print(B)
while(EOF!=len(B)):
    
    Q = B[EOF]  # Q is just for simplicity sake, HOPEFULLY IT DOESN"T ALTER 'B'
    global lengths
    lengths = []
    index, maxx = max(enumerate(Q), key=operator.itemgetter(1))
    del Q[index]
    temp = Router[index]
    del Router[index]
    for i in range(len(Router)-1):
        for j in range(i+1,len(Router)):    #Writes lengths between router
            guk = eucl_dist(Router[i].x,Router[i].y,Router[j].x,Router[j].y) #guk stores euclidian distance
            lengths.append(guk)
        #print ("The Euclidean distance between Router " +str(i+1)+" and Router "+str(j+1)+" Is "+str(guk) )
    
    '''
    for i in range(len(Router)-1):
        for j in range(i+1,len(Router)):
            if(Q[i]+Q[j]<lengths[i]):
                print(str(Q[i]) + " + "+str(Q[j])+ " < " + str(lengths[i]) + " Are underestimating")  # THIS IS PROBABLY WRONG. Doesn't take 3rd router value at all !!!
                #adjust(Q)
                print(str(Q[i]) + " + "+str(Q[j])+ " < " + str(lengths[i]) + " Are under Checking")
                UEC+=1
                #B[EOF][i],B[EOF][j]=I_D_(Q[i],Q[j],lengths[i])
    '''
    adjust(Q,index) # Performing the algorithm
    Router.insert(index,temp)   # Re-inserting the router.
    EOF+=1      # Next line in B

with open("output.csv", "w") as f:  #When you need to write to a excel file.
    writer = csv.writer(f)
    writer.writerows(B)


print("New List B is")
print(B)
#print("Lengths ARE : ")
#print(lengths)


