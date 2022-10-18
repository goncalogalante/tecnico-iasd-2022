import search
import numpy as np

class RTBProblem (search.Problem):
    def __init__ (self):
        self.initial=[]
        self.N=0
        self.beg=(-1,-1)
        self.end=(-1,-1)
        self.ecell=0 
        self.algorithm=None
        pass

    def result (self,state,action): #action->((xi,yi),(xf,yf))
#         cell,move -> switch
        state=list(state)
        state[action[0][0]]=list(state[action[0][0]])
        state[action[1][0]]=list(state[action[1][0]])
        state[action[0][0]][action[0][1]]=state[action[1][0]][action[1][1]]
        state[action[1][0]][action[1][1]]="empty-cell"
        state[action[0][0]]=tuple(state[action[0][0]])
        state[action[1][0]]=tuple(state[action[1][0]])
        state=tuple(state)
        #print(action)
        return state
    
    def actions(self,state):
        actions=[]
        #found=[]
        n=0
#         for find empty cell
        for i in range(0,self.N):
            for j in range(0,self.N):
                if ((state[i][j])[0]=='e'):
                    actions.extend(checkmoves((i,j),state,self.N))
                    #found.append((i,j))
                    n+=1
                    pass
                if(n==self.ecell):
                    return actions
                pass
            if(n==self.ecell):
                return actions
            pass
                    
#             check moves#             append moves

#         n=0
#         for n in range (0,self.ecell): #isto pode ir para lá para cima
#             actions.extend(checkmoves(found[n],state,self.N))
#             pass       

#         return lista moves
        return actions

    def goal_test(self,state): 
        xi=self.beg[0]
        yi=self.beg[1]
        answer=True
        
        ## Defines the next move from the initial state coordinates
        nextm=(state[xi][yi].split('-'))[1]
        #print(xi,yi,state[xi][yi])
        
        ## Loop that evaluates the cells from the initial state to the goal state
        ## and feedbacks it according to its coordinates
        while (xi,yi)!=(self.end):
            
            ## Checks if the move is valid
            (nextm,xi,yi,answer) = movevalid(nextm,xi,yi,self.N)
            if(answer==True): 
                ## Evaluates if the cell is the goal state
                if(xi,yi)==self.end:
                    if((state[xi][yi].split('-'))[1] == nextm):
                        return True
                    else:
                        return False
                
                ## Evaluates if the next cell is valid    
                if((state[xi][yi].split('-'))[0] == nextm):
                    nextm=(state[xi][yi].split('-'))[1]
                    pass
                elif((state[xi][yi].split('-'))[1] == nextm):
                    nextm=(state[xi][yi].split('-'))[0]
                    pass
                
                ## Returns False if it is none of the above
                else:
                    #print("bad move",xi,yi,state[xi][yi])
                    return False
                pass
            else:
                return False

            pass
        ## Returns True if the puzzle is already a solution
        return answer
    
    def load (self,fh):
        ## Ignores the comment lines and stores the size of the puzzle
        a=fh.readline()
        while a[0]=='#':
            a=fh.readline()
            pass
        self.N=int(a[0:-1])
     
        ## For each line of text saves it to the map matrix and makes some verifications 
        for i in range (0,self.N):
            l=fh.readline()
            (self.initial).append(l.split(' '))
            
            ## Removes the character \n of the line
            if ((self.initial)[i][-1])[-1] =='\n': 
                (self.initial)[i][-1]= ((self.initial)[i][-1])[0:-1]
                pass
            

            for j in range(0,self.N):
                if(((self.initial)[i][j])[0]=='i'):
                    self.beg=(i,j)
                    pass
                if(((self.initial)[i][j])[0]=='g'):
                    self.end=(i,j)
                    pass
                if(((self.initial)[i][j])[0]=='e'):
                    self.ecell+=1
                    pass
                pass
            self.initial[i]=tuple(self.initial[i])
            pass
        self.initial=tuple(self.initial)
        #print(type(self.initial),self.initial)
        pass
    
    def setAlgorithm(self):
        self.algorithm=search.breadth_first_graph_search
        pass
    
    def solve(self):
        return self.algorithm(self)

def checkmoves(ecell,board,N):
    x=ecell[0]
    y=ecell[1]
    moves=["left","right","down","up"]
    actions=[] 
     
    if (y-1)<0: # Invalid left
        moves.remove("left")
        
    elif (y+1)>=N: # Invalid right
        moves.remove("right")

    if (x+1)>=N: # Invalid down
        moves.remove("down")
        
    elif (x-1)<0: # Invalid up
        moves.remove("up")
    
    for move in (moves):
        if (move=="left"): 
            if((board[x][y-1])[-3]=='n' or (board[x][y-1])[0]=='g' or (board[x][y-1])[0]=='e' or (board[x][y-1])[0]=='i'): 
                pass
            else:
                actions.append(((x,y),(x,y-1)))
        elif (move=="right"): 
            if((board[x][y+1])[-3]=='n' or (board[x][y+1])[0]=='g' or (board[x][y+1])[0]=='e' or (board[x][y+1])[0]=='i'): 
                pass
            else:
                actions.append(((x,y),(x,y+1)))
        elif (move=="down"): 
            if((board[x+1][y])[-3]=='n' or (board[x+1][y])[0]=='g' or (board[x+1][y])[0]=='e' or (board[x+1][y])[0]=='i'): 
                pass
            else:
                actions.append(((x,y),(x+1,y)))
        elif (move=="up"): 
            if((board[x-1][y])[-3]=='n' or (board[x-1][y])[0]=='g' or (board[x-1][y])[0]=='e' or (board[x-1][y])[0]=='i'): 
                pass
            else:
                actions.append(((x,y),(x-1,y)))
        pass
    
    return tuple(actions)

## This function checks if a move its valid or invalid according to its coordinates and return it.
def movevalid(move,xi,yi,N):
    if(move=="left"):
        if (yi-1)<0: # Invalid
#             xf=xi
#             yf=yi
#             return (move,xf,yf,False)
            return (move,xi,yi,False)
        else:
#             xf=xi
#             yf=yi-1
#             move="right"
            return ("right",xi,yi-1,True)
    elif(move=="right"):
        if (yi+1)<N: # Valid
#             xf=xi
#             yf=yi+1
#             move="left"
            return ("left",xi,yi+1,True)
        else:
#             xf=xi
#             yf=yi
            return (move,xi,yi,False)
    elif(move=="down"):
        if (xi+1)<N: # Valid
#             xf=xi+1
#             yf=yi
#             move="top"
            return ("top",xi+1,yi,True)
        else:
#             xf=xi
#             yf=yi
            return (move,xi,yi,False)
    elif(move=="top"):
        if (xi-1)<0: # Invalid
#             xf=xi
#             yf=yi
            return (move,xi,yi,False)
        else:
#             xf=xi-1
#             yf=yi
#             move="down"
            return ("down",xi-1,yi,True)

    return (move,xi,yi,False)


## This function defines the main function
def main():
    problem=RTBProblem()
    fh=open("Arquivo2/pub10.dat")
    problem.load(fh)
    problem.setAlgorithm()
    result=problem.solve()
    print(list(result.state))
    print(problem.goal_test(result.state))

## Executes the main function
if __name__ == "__main__":
    main()

