def genPascal(rows):
    main=[[1]] # first row to kickstart
    for i in range(rows-1):
        prev = main[i]
        nl = []
        for i in range(len(prev)+1): # every row increases in size by 1
            if i == 0 or i == len(prev):
                nl.append(1) # set value to 1 if the first or last value in the row
            else:
                nl.append(prev[i]+prev[i-1]) # otherwise, add the value directly above it and up and to the left one of it (like left-aligning on a square grid)
        main.append(nl)
    return(main)

def genFibonacci(iters):
    main = [1,1] # first two values to kickstart
    for i in range(iters-2):
        indx = len(main)
        main.append(main[indx-1]+main[indx-2]) # add previous two values together
    return(main)

fibs = genFibonacci(46) # longest the fibonacci sequence can go without exceeding the 32-bit integer limit

def getdiag(val):
    if val not in fibs: # check if value is a valid input
        return("Invalid Input")
    else:
        indx = fibs.index(val)+1
        pasc = genPascal(indx) # get pascal's triangle with same size as length of the inputted fibonacci number
        dg = []
        j=0
        for i in reversed(pasc): # start at longest row and consistently move up and to the right one until no longer possible
            try:
                dg.append(i[j])
                j+=1
            except:
                break
        return(dg)

def main(val):
    diag = getdiag(val)
    even = 0; odd = 0
    for i in diag: # if divisible by 2, add to even ,otherwise add to odd
        if i%2 == 0:
            even+=1
        else:
            odd+=1
    return(f"{odd} {even} {max(diag)}") # format final output

testval = 317811 # insert value to test here
print(main(testval))