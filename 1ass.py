#import search
import numpy as np

## This class provides three functions to solve the RTBProblem
# 1. init: method to instantiate the class
# 2. load: loads the puzzle from a file object fh
# 3. isSolution: returns 1 if the loaded puzzle is a solution, 0 otherwise
class RTBProblem (): 
    def __init__ (self): 
        self.map=[]
        self.N=0
        self.beg=(-1,-1)
        self.end=(-1,-1)
        
    def load (self,fh):
        ## Reads the comment lines and stores the size of the puzzle
        a=fh.readline()
        while a[0]=='#':
            a=fh.readline()
            pass
        self.N=int(a[0:-1])
     
        ## For each line of text saves it to the map matrix and make some verifications 
        for i in range (0,self.N):
            l=fh.readline()
            (self.map).append(l.split(' '))
            
            ## Removes the character \n of the line
            if ((self.map)[i][-1])[-1] =='\n': 
                (self.map)[i][-1]= ((self.map)[i][-1])[0:-1]
                pass
            
            ## Checks if the initial state exists and stores its coordinates 
            if (self.beg == (-1,-1)): 
                j=0
                while (j<self.N and ((self.map)[i][j])[0]!='i'):
                    j+=1
                    pass
                if j<self.N:
                    self.beg=(i,j)
                    pass
                pass
            
            ## Checks if the goal state exists and stores its coordinates
            if (self.end == (-1,-1)):
                j=0
                while (j<self.N and ((self.map)[i][j])[0]!='g'):
                    j+=1
                    pass
                if j<self.N:
                    self.end=(i,j)
                    pass
                pass
            pass
        return self
    
    def isSolution (self):
        xi=self.beg[0]
        yi=self.beg[1]
        answer=True
        
        ## Defines the next move from the initial state coordinates
        nextm=(self.map[xi][yi].split('-'))[1]
        print(xi,yi,self.map[xi][yi])
        
        ## Loop that evaluates the cells from the initial state to the goal state
        ## and feedbacks it according to its coordinates
        while (xi,yi)!=(self.end):
            
            ## Checks if the move is valid
            (nextm,xi,yi,answer) = movevalid(nextm,xi,yi,self)
            if(answer==True): 
                
                ## Returns True if the cell is the goal state
                if(xi,yi)==self.end:
                    if((self.map[xi][yi].split('-'))[1] == nextm):
                        return True
                    else:
                        return False
                
                ## Evaluates if the cell is not the goal state or an empty one    
                if((self.map[xi][yi].split('-'))[0] == nextm):
                    nextm=(self.map[xi][yi].split('-'))[1]
                    pass
                elif((self.map[xi][yi].split('-'))[1] == nextm):
                    nextm=(self.map[xi][yi].split('-'))[0]
                    pass
                
                ## Returns False if it is none of the above
                else:
                    print("bad move",xi,yi,self.map[xi][yi])
                    return False
                pass
            else:
                return False
            pass
        
        ## Returns True if the puzzle is already a solution
        return answer

## This function checks if a move its valid or invalid according to its coordinates and return it.
def movevalid(move,xi,yi,prob):
    if(move=="left"):
        if (yi-1)<0: # Invalid
            xf=xi
            yf=yi
            return (move,xf,yf,False)
        else:
            xf=xi
            yf=yi-1
            move="right"
    elif(move=="right"):
        if (yi+1)<prob.N: # Valid
            xf=xi
            yf=yi+1
            move="left"
        else:
            xf=xi
            yf=yi
            return (move,xf,yf,False)
    elif(move=="down"):
        if (xi+1)<prob.N: # Valid
            xf=xi+1
            yf=yi
            move="top"
        else:
            xf=xi
            yf=yi
            return (move,xf,yf,False)
    elif(move=="top"):
        if (xi-1)<0: # Invalid
            xf=xi
            yf=yi
            return (move,xf,yf,False)
        else:
            xf=xi-1
            yf=yi
            move="down"

    return (move,xf,yf,True)

## This function defines the main function
def main():
    fh=open("Arquivos/pub05.dat")
    prob=RTBProblem()
    prob=RTBProblem.load(prob,fh)
    result=RTBProblem.isSolution(prob)
    print("deu certo? ->",result)
    
## Executes the main function
if __name__ == "__main__":
    main()
