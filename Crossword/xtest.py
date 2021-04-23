import heapq
import re


def print_puzzle(puzzle):
    for i in range(0, len(puzzle)):
        if i%width == 0 and i!=0:
            print("")
        print(puzzle[i], end="")
    print()
    print()


height = 5
width = 5
# puzzle = "I----" \
#          "M----" \
#          "B----" \
#          "U----" \
#          "E----"
# puzzle = "#--------------#"
puzzle = "-----" \
         "-----" \
         "-----" \
         "-----" \
         "-----"
totaldim = height*width
dictionary = "dct20k.txt"
word_length = dict()
mylist = set()
f = open(dictionary, "r")
lines = f.readlines()
for x in lines:
    temp_word = x.strip()
    if temp_word.isalpha():
        if len(temp_word) not in word_length:
            word_length[len(temp_word)] = []
        word_length[len(temp_word)].append(temp_word.upper())
        mylist.add(temp_word.upper())

hfillings = dict()
vfillings = dict()
constrain = []

start = True
temp_string = ""
temp_index = -1
for x in range(0, len(puzzle)):
    if (puzzle[x] == "#" or (x+1)%width == 0) and temp_index >=0:
        start = True
        if puzzle[x] != "-" and puzzle[x] != "#":
            temp_string += puzzle[x]
        elif puzzle[x] == "-":
            temp_string += "."
        key = "h"+str(temp_index)
        length = len(temp_string)
        r = re.compile("^" + temp_string + "$")
        possiblevals = list(filter(r.match, word_length[length]))

        hfillings[key] = [len(possiblevals), possiblevals, temp_index, temp_string]
        heapq.heappush(constrain, (len(possiblevals), key))
        continue
    else:
        if start and puzzle[x] != "#":
            start = False
            temp_index = x
            temp_string = ""
        if puzzle[x] != "-" and puzzle[x] != "#":
            temp_string += puzzle[x]
        elif puzzle[x] == "-":
            temp_string += "."

start = True
temp_string = ""
temp_index = -1
for y in range(0, width):
    for x in range(y, len(puzzle), width):
        if (puzzle[x] == "#" or x+width >= len(puzzle)) and temp_index >= 0:
            start = True
            if puzzle[x] != "-" and puzzle[x] != "#":
                temp_string += puzzle[x]
            elif puzzle[x] == "-":
                temp_string += "."
            key = "v"+str(temp_index)
            length = len(temp_string)
            r = re.compile("^" + temp_string + "$")
            possiblevals = list(filter(r.match, word_length[length]))

            vfillings[key] = [len(possiblevals), possiblevals, temp_index, temp_string]
            heapq.heappush(constrain, (len(possiblevals), key))
            continue
        else:
            if start and puzzle[x] != "#":
                start = False
                temp_index = x
                temp_string = ""
            if puzzle[x] != "-" and puzzle[x] != "#":
                temp_string += puzzle[x]
            elif puzzle[x] == "-":
                temp_string += "."
print()


def goal_test(state):
    for x in range(0, totaldim, width):
        val = state[x:x+width].split("#")
        for w in val:
            if len(w) > 0 and w not in mylist:
                return False
    for x in range(0, width):
        word = ""
        for y in range(x, totaldim, width):
            word+=state[y]
        val = word.split("#")
        for w in val:
            if len(w) > 0 and w not in mylist:
                return False
    return True

def goal_test_one(state):
    if "-" in state:
        return False
    return True

def update_puzzle(pattern, orient, index):
    global puzzle
    if orient == "h":
        puzzle = puzzle[0:index] + pattern + puzzle[index+len(pattern):]
    elif orient == 'v':
        ind = 0
        for y in range(index, index + width*(len(pattern)), width):
            puzzle = puzzle[0:y] + pattern[ind] + puzzle[y+1:]
            ind+=1
    return puzzle


def filt(pattern, orient, index):
    global puzzle
    udict = vfillings if orient == "h" else hfillings
    rdict = dict()
    id = 0
    for x in range(index, index+len(pattern)) if orient == "h" else range(index, index+len(pattern)*width, width):
        cnt = 0
        idx = x
        while (idx >= 0 if orient == "h" else (idx>=0 and idx%width!= 0)) and puzzle[idx] != "#":
            idx -= width if orient == "h" else 1
            cnt+=1
        if idx < 0 or puzzle[idx] == "#":
            idx += width if orient == "h" else 1
            cnt-=1
        key = ("v" if orient == "h" else "h") + str(idx)
        cst = udict[key][3]
        if "." not in cst:
            id+=1
            continue
        newcst = cst[0:cnt] + pattern[id] + cst[cnt+1:]
        vals = udict[key][1]
        r = re.compile("^" + newcst + "$")
        try:
            newvals = list(filter(r.match, vals))
        except:
            newvals = []
        udict[key][3] = newcst
        udict[key][1] = newvals
        udict[key][0] = len(newvals)
        heapq.heappush(constrain, (udict[key][0], key))
        # print(key)
        rdict[key] = [list(set(vals)-set(newvals)), cst]
        id+=1
    return rdict

counter = 0

used = set()
def csp(hfillings, vfillings):
    global puzzle
    global constrain
    global counter
    # global vfillings
    # global hfillings
    # print(constrain)
    boo = goal_test_one(puzzle)
    boo1 = goal_test(puzzle)
    # if boo and boo1 == False:
    #     return None
    # elif boo and boo1:
    #     return puzzle
    if boo and boo1:
        return puzzle
    elif boo:
        # print("BIG FAIL")
        counter+=1
        return None
    var = heapq.heappop(constrain)
    if var[1][0] == "h":
        temp_dict = hfillings
    else:
        temp_dict = vfillings
    print(var)
    print(temp_dict[var[1]][3])

    while "." not in temp_dict[var[1]][3] or var[0] != temp_dict[var[1]][0]:
       if var[0] != temp_dict[var[1]][0]:
           print("contra")

       var = heapq.heappop(constrain)
       print(var)
       if var[1][0] == "h":
           temp_dict = hfillings
       else:
           temp_dict = vfillings
       print(temp_dict[var[1]][3])

    # print(var)

    newdict = dict()
    possible_values = hfillings[var[1]][1] if var[1][0] == "h" else vfillings[var[1]][1]
    og_contraint = hfillings[var[1]][3] if var[1][0] == "h" else vfillings[var[1]][3]
    og_puzzle = puzzle
    og_num = var[0]

    for x in possible_values:
        if x in used:
            continue
        used.add(x)
        for key in newdict:
            if key[0] == "h":

                hfillings[key][1] += (newdict[key][0])
                hfillings[key][0] = len(hfillings[key][1])
                hfillings[key][3] = newdict[key][1]
                heapq.heappush(constrain, (hfillings[key][0], key))
            if key[0] == "v":
                vfillings[key][1] += (newdict[key][0])
                vfillings[key][0] = len(vfillings[key][1])
                vfillings[key][3] = newdict[key][1]
                heapq.heappush(constrain, (vfillings[key][0], key))
        newdict.clear()
        if var[1][0] == "h":
            hfillings[var[1]][3] = x
            hfillings[var[1]][0] = 1
            hfillings[var[1]][1] = [x]
        else:
            vfillings[var[1]][3] = x
            vfillings[var[1]][0] = 1
            vfillings[var[1]][1] = [x]
        temp_key = hfillings[var[1]][2] if var[1][0] == "h" else vfillings[var[1]][2]
        puzzle = update_puzzle(x, var[1][0], temp_key)
        print_puzzle(puzzle)
        newdict = filt(x, var[1][0], temp_key)
        result = csp(hfillings, vfillings)
        if result is not None:
            return result
        used.remove(x)
    # if width == 5 and height == 5 and total_blocks == 0:
    #     return puzzle
    if var[1][0] == "h":
        hfillings[var[1]][3] = og_contraint
    else:
        vfillings[var[1]][3] = og_contraint
    for key in newdict:
        if key[0] == "h":
            hfillings[key][1] += (newdict[key][0])
            hfillings[key][0] = len(hfillings[key][1])
            hfillings[key][3] = newdict[key][1]
            heapq.heappush(constrain, (hfillings[key][0], key))
        if key[0] == "v":
            vfillings[key][1] += (newdict[key][0])
            vfillings[key][0] = len(vfillings[key][1])
            vfillings[key][3] = newdict[key][1]
            heapq.heappush(constrain, (vfillings[key][0], key))
    heapq.heappush(constrain, (og_num, var[1]))

    puzzle = og_puzzle
    print("FALSE")

    return None

toprint = csp(hfillings, vfillings)
print_puzzle(toprint)