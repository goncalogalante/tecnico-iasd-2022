#import search
import numpy as np

class RTBProblem (): #class RTBProblem (search.problem):
    def __init__ (self): 
        self.map=[]
        self.N=0
        self.beg=(-1,-1)
        self.end=(-1,-1)
    def load (self,fh):
        a=fh.readline()

        while a[0]=='#':
            a=fh.readline()
            pass
        self.N=int(a[0])
        #print(self.N)
        for i in range (0,self.N): #tirar as linhas de texto para o mapa (matriz)
            l=fh.readline()
            #print(l)
            (self.map).append(l.split(' '))
            if ((self.map)[i][-1])[-1] =='\n':  #tirar \n
                (self.map)[i][-1]= ((self.map)[i][-1])[0:-1]
                pass
            if (self.beg == (-1,-1)): #início not found
                j=0
                while (j<self.N and ((self.map)[i][j])[0]!='i'):
                    #print("i->",i,"j->",j,"((self.map)[i][j])[0]",((self.map)[i][j])[0],"self.beg =",self.beg)
                    j+=1
                    pass
                if j<self.N:
                    self.beg=(i,j)
                    pass
                pass
            if (self.end == (-1,-1)): #fim not found
                j=0
                while (j<self.N and ((self.map)[i][j])[0]!='g'):
                    #print("i->",i,"j->",j,"((self.map)[i][j])[0]",((self.map)[i][j])[0],"self.end =",self.end)
                    j+=1
                    pass
                if j<self.N:
                    self.end=(i,j)
                    pass
                pass
            pass
        return self
    
    def isSolution (self) :
        xi=self.beg[0]
        yi=self.beg[1]
        answer=True
        
        nextm=(self.map[xi][yi].split('-'))[1]
        #print(nextm)
        print(xi,yi,self.map[xi][yi])
        answer=movevalid(nextm,xi,yi,self)
#         while (movevalid(nextm,xi,yi,prob)!= (-1,-1) or movevalid(nextm,xi,yi,prob)!= (self.end[0],self.end[1])):
#                 nextm=(self.map[xi][yi].split('-'))[1]
#             pass
        return answer

def movevalid(move,xi,yi,prob):
    if(move=="left"):
        if (yi-1)<0: #inválido
            xf=-1
            yf=-1
            return False
        else:
            xf=xi
            yf=yi-1
            move="right"
    elif(move=="right"):
        if (yi+1)<prob.N: #válido
            xf=xi
            yf=yi+1
            move="left"
        else:
            xf=-1
            yf=-1
            return False
    elif(move=="down"):
        if (xi+1)<prob.N: #válido
            xf=xi+1
            yf=yi
            move="top"
        else:
            xf=-1
            yf=-1
            return False
    elif(move=="top"):
        if (xi-1)<0: #inválido
            xf=-1
            yf=-1
            return False
        else:
            xf=xi-1
            yf=yi
            move="down"

    return checkcell(move,xf,yf,prob)

def checkcell(move,xf,yf,prob):
    print(xf,yf,prob.map[xf][yf])
    
    if(xf,yf)==prob.end:
        return True
    
    if((prob.map[xf][yf].split('-'))[0] == move):
        return movevalid((prob.map[xf][yf].split('-'))[1],xf,yf,prob)
    elif((prob.map[xf][yf].split('-'))[1] == move):
        return movevalid((prob.map[xf][yf].split('-'))[0],xf,yf,prob)
    else:
        print("bad move")
        return False

def main():
    fh=open("Fig8-T.txt")
    prob=RTBProblem()
    prob=RTBProblem.load(prob,fh)
#     print(prob.map)
#     print(prob.N)
#     print(prob.beg)
#     print((prob.map)[prob.beg[0]][prob.beg[1]])
#     print(prob.end)
#     print((prob.map)[prob.end[0]][prob.end[1]])
    
    result=RTBProblem.isSolution(prob)
    

if __name__ == "__main__":
    main()