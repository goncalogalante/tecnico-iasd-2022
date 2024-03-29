import search
from os import listdir
import time


class RTBProblem (search.Problem):
    def __init__ (self):
        self.initial=[]
        self.N=0
        self.beg=(-1,-1)
        self.end=(-1,-1)
        self.ecell=0
        self.hi=0
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
        n=0
#         for find empty cell
        for i in range(0,self.N):
            for j in range(0,self.N):
                if ((state[i][j])[0]=='e'):
                    actions.extend(checkmoves((i,j),state,self.N))
                    n+=1
                    pass
                if(n==self.ecell):
                    return actions
                pass
            if(n==self.ecell):
                return actions
            pass
                    
#             check moves
#             append moves
#        n=0
#        for n in range (0,self.ecell): #isto pode ir para lá para cima
#            actions.extend(checkmoves(found[n],state,self.N))
#            pass       

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

        ## Calculates and stores the number of places in the puzzle to afterwards calculate the heuristic
        self.hi=(self.N)**2
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
                elif(((self.initial)[i][j])[0]=='g'):
                    self.end=(i,j)
                    pass
                elif(((self.initial)[i][j])[0]=='e'):
                    self.ecell+=1
                    self.hi-=1      ## Subtracts the found empty cell to the number of blocks in the puzzle
                    pass
                elif(((self.initial)[i][j])[0]=='n'):
                    self.hi-=1      ## Subtracts the no passage cell to the number of blocks in the puzzle
                    pass
                # elif(((self.initial)[i][j])[-3:]=='not'):
                #     self.hi-=1      ## Subtracts the not movable block to the number of blocks in the puzzle
                #     pass
                pass
            self.initial[i]=tuple(self.initial[i])
            pass
        self.initial=tuple(self.initial)
        
        pass
    
    def h(self,node):
        
        h=goal_test1(self,node.state)    

        return self.hi*node.depth/(2*h+1)
    
    def setAlgorithm(self):
        self.algorithm=search.astar_search  #astar_search  breadth_first_graph_search iterative_deepening_search
        pass
    
    def solve(self):
        return self.algorithm(self)
    
def goal_test1(self,state): 
    xi=self.beg[0]
    yi=self.beg[1]
    steps=0
    answer=True
    ## Defines the next move from the initial state coordinates
    nextm=(state[xi][yi].split('-'))[1]
    
    ## Loop that evaluates the cells from the initial state to the goal state
    ## and feedbacks it according to its coordinates
    while (xi,yi)!=(self.end):
        
        ## Checks if the move is valid
        (nextm,xi,yi,answer) = movevalid(nextm,xi,yi,self.N)
        if(answer==True): 
            ## Evaluates if the cell is the goal state
            if(xi,yi)==self.end:
                if((state[xi][yi].split('-'))[1] == nextm):
                    return steps #goal 0
                else:
                    break
            
            ## Evaluates if the next cell is valid    
            if((state[xi][yi].split('-'))[0] == nextm):
                nextm=(state[xi][yi].split('-'))[1]
                pass
            elif((state[xi][yi].split('-'))[1] == nextm):
                nextm=(state[xi][yi].split('-'))[0]
                pass            

            else:
                break
            pass
        else:
            break
        steps+=1
        pass
    
    xi=self.end[0]
    yi=self.end[1]
    answer=True
    nextm=(state[xi][yi].split('-'))[1]

    while (xi,yi)!=(self.beg):
        
        ## Checks if the move is valid
        (nextm,xi,yi,answer) = movevalid(nextm,xi,yi,self.N)
        if(answer==True):             
            ## Evaluates if the next cell is valid    
            if((state[xi][yi].split('-'))[0] == nextm):
                nextm=(state[xi][yi].split('-'))[1]
                pass
            elif((state[xi][yi].split('-'))[1] == nextm):
                nextm=(state[xi][yi].split('-'))[0]
                pass

            else:
                break
            pass
        else:
            break
        steps+=1
        pass
    
    
    ## Returns True if the puzzle is already a solution
    return steps
    
def checkmoves(ecell,board,N):
    x=ecell[0]
    y=ecell[1]
    moves=["up","left","down","right"]
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
            if((board[x][y-1])[-3]!='n' and (board[x][y-1])[0]!='g' and (board[x][y-1])[0]!='e' and (board[x][y-1])[0]!='i'): 
#                pass
#            else:
                actions.append(((x,y),(x,y-1)))
        elif (move=="right"): 
            if((board[x][y+1])[-3]!='n' and (board[x][y+1])[0]!='g' and (board[x][y+1])[0]!='e' and (board[x][y+1])[0]!='i'): 
#                pass
#            else:
                actions.append(((x,y),(x,y+1)))
        elif (move=="down"): 
            if((board[x+1][y])[-3]!='n' and (board[x+1][y])[0]!='g' and (board[x+1][y])[0]!='e' and (board[x+1][y])[0]!='i'): 
#                pass
#            else:
                actions.append(((x,y),(x+1,y)))
        elif (move=="up"): 
            if((board[x-1][y])[-3]!='n' and (board[x-1][y])[0]!='g' and (board[x-1][y])[0]!='e' and (board[x-1][y])[0]!='i'): 
#                pass
#            else:
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
#     problem=RTBProblem()
#     fh=open("Arquivo2/pub10.dat")
#     problem.load(fh)
#     problem.setAlgorithm()
#     result=problem.solve()
#     print(list(result.state))
#     print(problem.goal_test(result.state))
    for files in listdir("tests_ass3"):
        if files[-3:] == "dat":
#         if files == "pub02.dat":
            #files
            with open("tests_ass3/"+files,"r") as fh:
                #print(files)
                start_time = time.time()
                teste = RTBProblem()
                teste.setAlgorithm()
                teste.load(fh)
                a=teste.solve()
                if(a!=None):
                    print(f"No ficheiro {files} demorou {time.time()-start_time} | path cost {a.depth} | hi = {teste.hi} \n") #{a.state}
#                     print(f"No ficheiro {files} demorou {time.time()-start_time}\n")
                    pass
# problem1 = Coun tCall s ( s o l u t i o n . RTBProblem ( ) )
# t10 = time . p r o c e s s tim e ( )
# with open(input ) a s f h :
# problem1 . loa d ( f h )
# r e s u l t 1 = u nif o rm c o s t s e a r c h g r a p h ( problem1 )
# t11 = time . p r o c e s s tim e ( )
# problem2 = Coun tCall s ( s o l u t i o n . RTBProblem ( ) )
# t20 = time . p r o c e s s tim e ( )
# with open(input ) a s f h :
# problem2 . loa d ( f h )
# r e s u l t 2 = a s t a r s e a r c h g r a p h ( problem2 )
# t21 = time . p r o c e s s tim e ( )
    
    
    
## Executes the main function
if __name__ == "__main__":
    main()

