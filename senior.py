validarrows = ["A", "B", "C", "D", "E", "F", "G", "H"]
arrowdirs=["←","↑","→","↓","↖","↗","↘","↙"] # corresponding indexes for later replacement in final output

def checkarrow(grid, arrow): # check what arrow hits, including all targets and potentially other arrows
    row = int(arrow[0]); col = int(arrow[1]); dir=arrow[2]
    hits = []
    if dir == "A": # step-by-step (replicated throughout with slight variations)
        for j in range(col): # iterate through all items up to location of arrow
            i = col-j-1 # inverse to sort closest -> nearest (subtract 1 to prevent iterating over itself)
            if "T" == grid[row][i]: # check if hit target
                #print(f"Hit at {row}, {i}")
                hits.append([row,i,False]) # if so, append target location and mark it as not being an arrow
            if grid[row][i] in validarrows: # check if hit arrow
                hits.append([row,i,True]) # if so, append arrow location and mark it as being an arrow (marking location isn't necessary but helps with keeping it consistent for later processing)
    if dir == "B":
        for j in range(row):
            i = row-j-1
            if "T" == grid[i][col]:
                #print(f"Hit at {i}, {col}")
                hits.append([i,col,False])
            if grid[i][col] in validarrows:
                hits.append([i,col,True])
    if dir == "C":
        for i in range(len(grid)-(col+1)): # change order of iteration and amount of items iterated to count left -> right
            if "T" == grid[row][i+(col+1)]:
                #print(f"Hit at {row}, {i+(col+1)}")
                hits.append([row, i+(col+1),False])
            if grid[row][i+(col+1)] in validarrows:
                hits.append([row,i+(col+1),True])
    if dir == "D":
        for i in range(len(grid)-(row+1)):
            if "T" == grid[i+(row+1)][col]:
                #print(f"Hit at {i+(row+1)}, {col}")
                hits.append([i+(row+1),col,False])
            if grid[i+(row+1)][col] in validarrows:
                hits.append([i+(row+1),col,True])
    if dir == "E":
        small=min([col,row]) # iterate the amount of times it takes to get to the nearest edge of the grid
        for j in range(small):
            i = j+1 # add one to range to prevent iterating over itself
            if "T" == grid[row-i][col-i]: # [row-i][col-i] is used for the diagonal arrows; simply replace the sign for which direction (- is up and to the left, + is down and to the right)
                #print(f"Hit at {row-i}, {col-i}")
                hits.append([row-i,col-i,False])
            if grid[row-i][col-i] in validarrows:
                hits.append([row-i,col-i,True])
    if dir == "F":
        small=min([len(grid)-(col+1),row])
        for j in range(small):
            i = j+1
            if "T" == grid[row-i][col+i]:
                #print(f"Hit at {row-i}, {col+i}")
                hits.append([row-i,col+i,False])
            if grid[row-i][col+i] in validarrows:
                hits.append([row-i,col+i,True])
    if dir == "G":
        small=min([len(grid)-(col+1),len(grid)-(row+1)])
        for j in range(small):
            i = j+1
            if "T" == grid[row+i][col+i]:
                #print(f"Hit at {row+i}, {col+i}")
                hits.append([row+i,col+i,False])
            if grid[row+i][col+i] in validarrows:
                hits.append([row+i,col+i,True])
    if dir == "H":
        small=min([col,len(grid)-(row+1)])
        for j in range(small):
            i = j+1
            if "T" == grid[row+i][col-i]:
                #print(f"Hit at {row+i}, {col-i}")
                hits.append([row+i,col-i,False])
            if grid[row+i][col-i] in validarrows:
                hits.append([row+i,col-i,True])
    return(hits)

def genGrid(size,targets,numbers, arrows):
    tsize = int(size)

    grid = []
    for i in range(tsize):
        grid.append([" " for l in range(tsize)]) # create grid of empty spaces in rows

    ttargets = targets.split(" ")
    for i in ttargets: # place targets ("T") on grid
        row = int(i[0]); col = int(i[1])
        grid[row][col] = "T"
    
    
    tnumbers = numbers.split()
    for i,e in enumerate(tnumbers): # covert numbers into two lists of numbers
        e = list(e.strip(""))
        tnumbers[i] = e

    tarrows = arrows.split(" ")
    for i in tarrows:
        row = int(i[0]); col = int(i[1]); dir=i[2] # place arrows on grid
        grid[row][col] = dir
    
    truerow=[];truecol=[]
    for i,row in enumerate(grid): # for rows, and then columns: get the known number of arrows in each 
        c=0
        for item in row:
            if item in validarrows:
                c+=1
        truerow.append(c)
    for i in range(tsize):
        c=0
        for row in grid:
            if row[i] in validarrows:
                c+=1
        truecol.append(c)


    for i in tarrows:
        tarloc=checkarrow(grid, i)
        grid[tarloc[0][0]][tarloc[0][1]] = "X" # mark targets being hit by arrows with "X"

    for x,e in enumerate(tnumbers[0]): # for rows, and then columns: find where there is a difference between the actual and known number of arrows in each, and use that to find where the hidden arrow should be
        if int(e)-truerow[x] != 0:
            alocrow=x
    for x,e in enumerate(tnumbers[1]):
        if int(e)-truecol[x] != 0:
            aloccol=x
    #print(alocrow,aloccol)
    for i in validarrows: # iterate through each arrow direction
        if len(checkarrow(grid,f"{alocrow}{aloccol}{i}")) > 0 and not(checkarrow(grid,f"{alocrow}{aloccol}{i}")[0][2]): # if the arrow hits something, and if the first object the arrow hits is not another arrow,
            #print(f"{alocrow}{aloccol}{i}")
            grid[alocrow][aloccol] = i
            founddir=i

    for i,row in enumerate(grid):
        for j,item in enumerate(row):
              if item in validarrows:
                  grid[i][j] = arrowdirs[validarrows.index(item)] # for each arrow, convert letter to arrow character
    grid[alocrow][aloccol] = f"|{grid[alocrow][aloccol]}|" # surround solution arrow with | |
    
    return(f"{alocrow}{aloccol}{founddir}",grid)

size = "6"
targets="15 23 24 32 33 34 42 43 51"
numbers="401211 401211"
arrows="00G 20G 40G 53B 02G 03D 04G 35A"
solution=genGrid(size,targets,numbers,arrows)
print(solution[0])
for i in solution[1]: # outputs completed grid in proper formatting
    print(i) 