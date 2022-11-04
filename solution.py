import search

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
        ##switch the cells given by the action
        state=list(state)
        state[action[0][0]]=list(state[action[0][0]])
        state[action[1][0]]=list(state[action[1][0]])
        state[action[0][0]][action[0][1]]=state[action[1][0]][action[1][1]]
        state[action[1][0]][action[1][1]]="empty-cell"
        state[action[0][0]]=tuple(state[action[0][0]])
        state[action[1][0]]=tuple(state[action[1][0]])
        state=tuple(state)
        return state
    
    def actions(self,state):
        actions=[]
        n=0
        ## for to find empty cells
        for i in range(0,self.N):
            for j in range(0,self.N):
                if ((state[i][j])[0]=='e'): ## found an empty cell
                    actions.extend(checkmoves((i,j),state,self.N)) ## append available moves for the cell
                    n+=1
                    pass
                if(n==self.ecell): ## if every empty cell has been found
                    return actions
                pass
            if(n==self.ecell): ## if every empty cell has been found
                return actions
            pass
        return actions

    def goal_test(self,state): 
        xi=self.beg[0]
        yi=self.beg[1]
        answer=True
        
        ## Defines the next move from the initial cell coordinates
        nextm=(state[xi][yi].split('-'))[1]
        
        ## Loop that evaluates the cells from the initial cell to the goal cell
        ## and feedbacks it according to its coordinates
        while (xi,yi)!=(self.end):
            
            ## Checks if the move is valid, gets next cell coordinates and condition to be valid (nextm)
            (nextm,xi,yi,answer) = movevalid(nextm,xi,yi,self.N)
            if(answer==True): 
                ## Evaluates if the cell is the goal cell
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

        ## Initialize the longest possible path in the goal state (every cell connected)
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
                    ## Saves the coordinates of the initial cell
                    self.beg=(i,j)
                    pass
                elif(((self.initial)[i][j])[0]=='g'):
                    ## Saves the coordinates of the goal cell
                    self.end=(i,j)
                    pass
                elif(((self.initial)[i][j])[0]=='e'):
                    self.ecell+=1
                    self.hi-=1      ## Subtracts the found empty cell to the longest possible path of the puzzle
                    pass
                elif(((self.initial)[i][j])[0]=='n'):
                    self.hi-=1      ## Subtracts the no passage cell to the longest possible path of the puzzle
                    pass
                pass
            self.initial[i]=tuple(self.initial[i])
            pass
        self.initial=tuple(self.initial)
        
        pass
    
    def h(self,node):
        """This heurisitic works like this:
        Takes into account:
        1) the longest path possible of the solution, obtained in load (#longest <=> self.hi)
        2) the length of the path from the root node of the tree to that node. (depth <=> node.depth)
        3) the number of connections to the initial cell and the goal cell. (#connections <=> c obtained in countconnect)
        
        So, the heuristic function, h(n) is defined by doing: h(n) = (#longest * depth)/(2*#connections + 1)
        
        It is not admissable because it estimates a cost that is higher than the true cheapest cost to reach the goal state.
        Any state in which is one move away from completion and solution path is much smaller than #longest,
        the heuristic will overestimate the true cost to the goal state.
        
        It is not consistent because the heuristic difference cost overestimates the actual step cost when going from any
        neighboring node to the goal, plus the cost of reaching that neighbour. Since the admissibility is not guaranteed,
        an overestimation of the of the true cost can lead to inconsistency. An example of a state with multiple cells
        connected but with 2 breaks near the goal and initial cell proves inconsistency, because the connecting those breaks
        will lead to a big drop int the heuristic function, meaning that the h(n)> path_cost(=1) + h(n'), being n the parent
        node and n' the child node.
        
        Although the heuristic function doesn't have this essencial characteristics, we can often obtain optimal solutions.
        The heuristic function can lead to these solutions because it is proportional with the depth of the node, meaning
        nodes with higher depth are less prioritized and is inversely proportional to the connections, meaning that the
        amount of connections takes a big part in reducing the heuristic as it is closer to the solution.
        Therefore, for most problems it can give good values that allow to reach a good solution.
        """
        c=countconnect(self,node.state)    

        return self.hi*node.depth/(2*c+1)
    
    def setAlgorithm(self):
        self.algorithm=search.astar_search  
        pass
    
    def solve(self):
        return self.algorithm(self)
    
def countconnect(self,state): 
    xi=self.beg[0]
    yi=self.beg[1]
    steps=0
    answer=True
    ## Defines the next move from the initial cell coordinates
    nextm=(state[xi][yi].split('-'))[1]
    
    ## Loop that evaluates the cells from the initial cell to the goal cell
    ## and feedbacks it according to its coordinates
    while (xi,yi)!=(self.end):
        
        ## Checks if the move is valid, gets next cell coordinates and condition to be valid (nextm)
        (nextm,xi,yi,answer) = movevalid(nextm,xi,yi,self.N)
        if(answer==True): 
            ## Evaluates if the cell is the goal state
            if(xi,yi)==self.end:
                if((state[xi][yi].split('-'))[1] == nextm):
                    return steps
                else:
                    break
            
            ## Evaluates if the next cell is valid
            ## If valid, advances to the next cell, if not, stops
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
        ## Detected a valid move, adds one more connected cell
        steps+=1
        pass
    
    ## The initial and goal cells aren't connected and there was no more connected cells since the beginning
    ## Repeats the search starting from the goal cell
    xi=self.end[0]
    yi=self.end[1]
    answer=True
    nextm=(state[xi][yi].split('-'))[1]

    while (xi,yi)!=(self.beg):
        
        ## Checks if the move is valid, gets next cell coordinates and condition to be valid (nextm)
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
        ## Detected a valid move, adds one more connected cell
        steps+=1
        pass
    
    ## After counting running the search starting from both the initial and goal cells
    ## Returns the number of already connected cells
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
        ## For each move, checks if the cell is able to move, adding the action (both coordinates to switch) in case it is
        if (move=="left"): 
            if((board[x][y-1])[-3]!='n' and (board[x][y-1])[0]!='g' and (board[x][y-1])[0]!='e' and (board[x][y-1])[0]!='i'): 
                actions.append(((x,y),(x,y-1)))
        elif (move=="right"): 
            if((board[x][y+1])[-3]!='n' and (board[x][y+1])[0]!='g' and (board[x][y+1])[0]!='e' and (board[x][y+1])[0]!='i'): 
                actions.append(((x,y),(x,y+1)))
        elif (move=="down"): 
            if((board[x+1][y])[-3]!='n' and (board[x+1][y])[0]!='g' and (board[x+1][y])[0]!='e' and (board[x+1][y])[0]!='i'): 
                actions.append(((x,y),(x+1,y)))
        elif (move=="up"): 
            if((board[x-1][y])[-3]!='n' and (board[x-1][y])[0]!='g' and (board[x-1][y])[0]!='e' and (board[x-1][y])[0]!='i'): 
                actions.append(((x,y),(x-1,y)))
        pass
    
    return tuple(actions)

## This function checks if a move its valid or invalid according to its coordinates
## and returns the cell if False,
## or, if True, returns the next cell coordinates and condition to check (for a left move, the next cell has to have right)
def movevalid(move,xi,yi,N):
    if(move=="left"):
        if (yi-1)<0: # Invalid
            return (move,xi,yi,False)
        else:
            return ("right",xi,yi-1,True)
    elif(move=="right"):
        if (yi+1)<N: # Valid
            return ("left",xi,yi+1,True)
        else:
            return (move,xi,yi,False)
    elif(move=="down"):
        if (xi+1)<N: # Valid
            return ("top",xi+1,yi,True)
        else:
            return (move,xi,yi,False)
    elif(move=="top"):
        if (xi-1)<0: # Invalid
            return (move,xi,yi,False)
        else:
            return ("down",xi-1,yi,True)

    return (move,xi,yi,False)