import sys
import re
import heapq

dimensions = sys.argv[1]
total_blocks = sys.argv[2]
dictionary = sys.argv[3]
starters = []
puzzle = ""
blocks = []
for x in range(4, len(sys.argv)):
    starters.append(sys.argv[x])

# print(starters)

dim = dimensions.split("x")
for x in range(0, int(dim[0]) * int(dim[1])):
    puzzle = puzzle[0:x] + "-" + puzzle[x+1:]

total_dim = int(dim[1]) * int(dim[0])
width = int(dim[1])
height = int(dim[0])

def print_puzzle(puzzle):
    for i in range(0, len(puzzle)):
        if i%width == 0 and i!=0:
            print("")
        print(puzzle[i], end="")
    print()
    print()
#
for x in starters:
    num1 = re.search(r'\d.*$', x)
    num2 = re.search(r'x\d', x)
    ending_pos = re.search(r'(\d)[^\d]*$', x)
    starting_pos = ending_pos.start() + 1
    start_num1 = num1.start()
    end_num1 = num2.start() - 1
    start_num2 = num2.start() + 1
    end_num2 = ending_pos.start()
    start_word = starting_pos
    start_index = (int(x[start_num1:end_num1 + 1])) * int(dim[1]) + int(x[start_num2:end_num2 + 1])

    tmp = start_word
    for i in range(start_index, total_dim, 1 if x[0] == "H" or x[0] == "h" else int(dim[1])):
        # print("Index",i)
        if start_word >= len(x):
            break
        puzzle = puzzle[0:i] + x[start_word:start_word+1].upper() + puzzle[i+1:]
        if x[start_word:start_word+1] == "#":
            blocks.append(i)
        # print(len(puzzle))
        start_word+=1

num_blocks = len(blocks)

visited = set()

def split_board(puzzle):
    start = 0
    while puzzle[start] == "#":
        start+=1
    q = []
    v = set()
    q.append((start, start))
    while len(q) > 0:
        hi = q.pop(0)
        tmp = hi[1]
        tmp1 = hi[0]
        if tmp in v:
            continue
        v.add(tmp)
        # print(tmp,'from',tmp1)
        if tmp+width < total_dim and puzzle[tmp+width] != "#":
            q.append((tmp, tmp+width))
        if tmp-width >= 0 and puzzle[tmp-width] != "#":
            q.append((tmp, tmp-width))
        if tmp+1 < total_dim and puzzle[tmp+1] != "#" and (tmp+1)%width != 0:
            q.append((tmp, tmp+1))
        if tmp-1 >= 0 and puzzle[tmp-1] != "#" and tmp%width != 0:
            q.append((tmp, tmp-1))
    return len(visited) + len(v) == total_dim


def propogate_blocks(puzzle):
    while len(blocks) != 0:
        val = blocks.pop()
        # print("Val:", val)
        if val in visited:
            continue
        visited.add(val)
        # print(len(puzzle))
        if puzzle[val].isalpha():
            # print("a")
            return False
        if len(visited) > int(total_blocks):
            # print("b")
            return False
        puzzle = puzzle[0:val] + "#" + puzzle[val+1:]

        if (val+1)%width >= width - 2:
            # print(True)
            tval = val + 1
            while tval < total_dim:
                if tval%width == 0:
                    break
                else:
                    blocks.append(tval)
                tval += 1
        if val % width <= 2:
            # print(True)
            tval = val
            while tval >= 0:
                if tval % width == 0:
                    break
                else:
                    blocks.append(tval)
                tval -= 1
        if val+1 <= width * 3:
            # print(True)
            tval = val - width
            while tval >= 0:
                blocks.append(tval)
                tval -= width
        if val + 3*width >= total_dim:
            tval = val+width
            while tval < total_dim:
                blocks.append(tval)
                tval+=width
        x = val
        if x-1 > 0 and x-2>0 and x-3>0 and puzzle[x-3] == "#" and puzzle[x-2] != "#" and puzzle[x-1] != "#":
            blocks.append(x-1)
            blocks.append(x-2)
        if x-1 > 0 and x-2 > 0 and puzzle[x-2] == "#" and puzzle[x-1] != "#":
            blocks.append(x-1)
        if x-width>0 and x-2*width>0 and x-3*width>0 and puzzle[x-3*width] == "#" and puzzle[x-2*width] != "#" and puzzle[x-width] != "#":
            blocks.append(x-width)
            blocks.append(x-2*width)
        if x-width>0 and x-2*width>0 and puzzle[x-2*width] == "#" and puzzle[x-width] != "#":
            blocks.append(x-width)

        cheight = int(val/width)
        cwidth = val%width
        nheight = height - cheight - 1
        nwidth = width - cwidth - 1
        nval = nheight*width + nwidth
        # print(cheight)
        # print(cwidth)
        # print(nheight)
        # print(nwidth)
        blocks.append(nval)
    return puzzle


# print(blocks)
if int(total_blocks) % 2 == 1:
    blocks.append(int(width/2) + int(height/2)*width)
# print_puzzle(puzzle)
new_puzzle = propogate_blocks(puzzle)
if new_puzzle != False:
    puzzle = new_puzzle
print()

counter = 0
vertical_cont = []
if int(total_blocks) == 0:
    xval = width
    yval = width
else:
    xval = width/5
    yval = width/5
for x in range(0, width):
    vertical_cont.append(height)
for x in range(0, int(total_dim/4)):
    if x!=0:
        blocks.clear()
    if puzzle[x] == "#":
        counter = 0
        vertical_cont[x % width] = 0
    if puzzle[x] == "-":
        if x-1 >= 0 and x-2>=0 and x-3>=0 and puzzle[x-3] == "#" and puzzle[x-2] != "#" and puzzle[x-1] != "#":
            continue
        if x-1 >= 0 and x-2 >= 0 and puzzle[x-2] == "#" and puzzle[x-1] != "#":
            continue
        if x-width>=0 and x-2*width>=0 and puzzle[x-2*width] == "#" and puzzle[x-width] != "#":
            continue
        if x-width>=0 and x-2*width>=0 and x-3*width>=0 and puzzle[x-3*width] == "#" and puzzle[x-2*width] != "#" and puzzle[x-width] != "#":
            continue
        blocks.append(x)
        boo = visited.copy()
        newpuzzle = propogate_blocks(puzzle)
        # and vertical_cont[x % width] >= height / yval
        if newpuzzle != False and split_board(newpuzzle) and (counter >= width/xval and len(visited) - len(boo) < width/2.5 \
                ):
            puzzle = newpuzzle
            counter = 0
            vertical_cont[x%width] = 0
        else:
            visited = boo
            # print()
            # print_puzzle(puzzle)
        counter += 1
        vertical_cont[x%width] += 1
if len(visited) < int(total_blocks):
    for x in range(int(total_dim/4), int(total_dim/1.5)):
        if x != 0:
            blocks.clear()
        if puzzle[x] == "#":
            counter = 0
            vertical_cont[x % width] = 0
        if puzzle[x] == "-":
            if x - 1 >= 0 and x - 2 >= 0 and x - 3 >= 0 and puzzle[x - 3] == "#" and puzzle[x - 2] != "#" and puzzle[x - 1] != "#":
                continue
            if x - 1 >= 0 and x - 2 >= 0 and puzzle[x - 2] == "#" and puzzle[x - 1] != "#":
                continue
            if x - width >= 0 and x - 2 * width >= 0 and puzzle[x - 2 * width] == "#" and puzzle[x - width] != "#":
                continue
            if x - width >= 0 and x - 2 * width >= 0 and x - 3 * width >= 0 and puzzle[x - 3 * width] == "#" and puzzle[
                x - 2 * width] != "#" and puzzle[x - width] != "#":
                continue
            blocks.append(x)
            boo = visited.copy()
            newpuzzle = propogate_blocks(puzzle)
            if newpuzzle != False and split_board(newpuzzle):
                puzzle = newpuzzle
                counter = 0
                vertical_cont[x % width] = 0
            else:
                visited = boo
                # print()
                # print_puzzle(puzzle)
            counter += 1
            vertical_cont[x % width] += 1
if len(visited) < int(total_blocks):
    for x in range(0, total_dim):
        if x != 0:
            blocks.clear()
        if puzzle[x] == "#":
            counter = 0
            vertical_cont[x % width] = 0
        if puzzle[x] == "-":
            if x - 1 >= 0 and x - 2 >= 0 and x - 3 >= 0 and puzzle[x - 3] == "#" and puzzle[x - 2] != "#" and puzzle[x - 1] != "#":
                continue
            if x - 1 >= 0 and x - 2 >= 0 and puzzle[x - 2] == "#" and puzzle[x - 1] != "#":
                continue
            if x - width >= 0 and x - 2 * width >= 0 and puzzle[x - 2 * width] == "#" and puzzle[x - width] != "#":
                continue
            if x - width >= 0 and x - 2 * width >= 0 and x - 3 * width >= 0 and puzzle[x - 3 * width] == "#" and puzzle[
                x - 2 * width] != "#" and puzzle[x - width] != "#":
                continue
            blocks.append(x)
            boo = visited.copy()
            newpuzzle = propogate_blocks(puzzle)
            if newpuzzle != False and split_board(newpuzzle):
                puzzle = newpuzzle
                counter = 0
                vertical_cont[x % width] = 0
            else:
                visited = boo
                # print()
                # print_puzzle(puzzle)
            counter += 1
            vertical_cont[x % width] += 1
ogpuzzle = puzzle
# print_puzzle(puzzle)
# print(len(visited))
# print(puzzle)
# print(split_board(puzzle))
# print(len(visited))
# print(int(dim[1]) * int(dim[0]))

# height = 3
# width = 3
totaldim = height*width
# dictionary = "wordlist.txt"
# word_length = dict()
# mylist = []
# f = open(dictionary, "r")
# for x in f:
#     temp_word = f.readline()
#     if len(temp_word) not in word_length:
#         word_length[len(temp_word)] = []
#     word_length[len(temp_word)].append(temp_word)
#     mylist.append(temp_word)
# #
# # for x in word_length:
# #     print(x, len(word_length[x]))
#
# col_words = []
# row_words = []
# for x in range (0, width):
#     col_words.append("")
#
# for y in range (0, height):
#     row_words.append("")
#
# puzzle = "........."
#
# def checkword(puzzle, row, col, index, dtb):
#     r = re.compile(row_words[row] + "\w{%s}" % (dtb,))
#     newlist_row = list(filter(r.match, mylist))
#     r = re.compile(col_words[col] + "\w{%s}" % (dtb,))
#     newlist_col = list(filter(r.match, mylist))
#     if len(newlist_row) != 0 and len(newlist_col) != 0:
#         return True
#     return False
#
#
# def check_horizpos(puzzle, index):
#     start = index
#     end = index
#     while puzzle[start] == "#":
#         start += 1
#     end = start
#     while puzzle[end] != "#" and end % width != 0:
#         end += 1
#     end -= 1
#     return start, end
#
#
# def check_vertpos(puzzle, index):
#     start = index
#     end = index
#     while puzzle[start] == "#":
#         start += width
#     end = start
#     while puzzle[end] != "#" and end < totaldim:
#         end += width
#     end -= width
#     return start, end
#
# original_letters = set()
# horistart = []
# horiend = []
# vertstart = []
# vertend = []
# horipos = []
# vertpos = []
# for x in range (0, width):
#     val = check_vertpos(puzzle, x)
#     vertstart[val[0]] = 0
#     vertend[val[1]] = 0
#     vertpos[x] = 0
# for x in range (0, height):
#     val = check_horizpos(puzzle, x)
#     horistart[val[0]] = 0
#     horiend[val[1]] = 0
#     horipos[x] = 0
#
#
# def csp(puzzle, row, col, index, bt):
#     if puzzle[index] == '#':
#         hc = check_horizpos(puzzle, index)
#         vc = check_vertpos(puzzle, index)
#         horipos[row] = 0
#         vertpos[col] = 0
#         horistart[row] = hc[0]
#         horiend[row] = hc[1]
#         vertstart[col] = vc[0]
#         vertend[col] = vc[1]
#         newindex = index+1
#         newrow = newindex/width
#         newcol = newindex%width
#         return csp(puzzle, newrow, newcol, index, bt)
#     elif puzzle[index] in original_letters:
#         horipos[row] += 1
#         vertpos[col] += 1
#         newindex = index + 1
#         newrow = newindex / width
#         newcol = newindex % width
#         return csp(puzzle, newrow, newcol, index, bt)
#     else:
#         hp = horipos[row]
#         vp = vertpos[col]
#         hs = horistart[row]
#         vs = vertstart[col]
#         he = horiend[row]
#         ve = vertend[col]
#         hr = hs - he - hp
#         vr = vs - ve - vp
#         r = re.compile("^" + puzzle[hs:hs+hp] + "\w{%s}" % (hr,) + "$")
#         hlist = list(filter(r.match, mylist))
#         vcur = ""
#         for y in range(vs, vs+vp, width):
#             vcur += puzzle[y]
#         r = re.compile("^" + vcur + "\w{%s}" % (vr,) + "$")
#         vlist = list(filter(r.match, mylist))
#         ogset = set()
#         newset = set()
#         for h in hlist:
#             ogset.add(h[hp])
#         for v in vlist:
#             if v[vp] in ogset:
#                 newset.add(v[vp])
#         if len(newset) == 0:
#             # backtrack
#             # if hp != 0:
#             #     if not bt:
#             #         bt = set()
#             #     bt.add(puzzle[index-1])
#             #     return csp(puzzle, row, col-1, index-1, bt)
#             return None
#         for letter in newset:
#             # if not bt and letter in bt:
#             #     continue
#             newpuzzle = puzzle[0:index] + letter + puzzle[index+1:]
#             horipos[row] += 1
#             vertpos[col] += 1
#
#             newindex = index + 1
#             newrow = newindex / width
#             newcol = newindex % width
#             result = csp(newpuzzle, newrow, newcol, index, bt)
#             if result is not None:
#                 return result
#         return None
#
#     #word_vis = set()
#
#
# # def prop(puzzle, row, col, index, dtb):
# #     # dtb = distance to block/boundary
# #
# #     if index >= len(puzzle):
# #         return puzzle
# #
# #     if puzzle[index] == "#":
# #         newcol = col+1
# #         newrow = row
# #         if col == width-1:
# #             newcol = 0
# #             newrow = row+1
# #         return prop(puzzle, newrow, newcol, index+1, 0)
# #     if not checkword(puzzle, row, col, index, dtb):
# #         return False
# #
# #     if dtb == 0 and col == 0:
# #         tmpidx = index
# #         if tmpidx == -1:
# #             tmpidx = 0
# #         while puzzle[tmpidx] != "#" and (tmpidx + 1)%width != 0:
# #             tmpidx += 1
# #         dtb = tmpidx
# #
# #     r = re.compile("^" + row_words[row]+"\w{%s}" % (dtb+1,) + "$")
# #     newlist = list(filter(r.match, mylist))
# #     for w in newlist:
# #         newpuzzle = puzzle[0:index+1] + w[col] + puzzle[index+2:]
# #         newcol = col + 1
# #         newrow = row
# #         if col == width - 1:
# #             newcol = 0
# #             newrow = row + 1
# #             dtb = 1
# #         row_words[row] += w[col]
# #         col_words[col] += w[col]
# #         print_puzzle(newpuzzle)
# #         val = prop(newpuzzle, newrow, newcol, index+1, dtb-1)
# #         if val != False:
# #             return val
#
#
# start = 0
# while puzzle[start]!=0:
#     start +=1
# # calc_horizpos(start)
# # calc_vertpoz(start)
#
# print(csp(puzzle, start, start/width, start%width, False))

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
    # print(var)
    # print(temp_dict[var[1]][3])

    while "." not in temp_dict[var[1]][3] or var[0] != temp_dict[var[1]][0]:
       # if var[0] != temp_dict[var[1]][0]:
       #        #     print("contra")

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
        # print_puzzle(puzzle)
        newdict = filt(x, var[1][0], temp_key)
        result = csp(hfillings, vfillings)
        if result is not None:
            return result
        used.remove(x)
    if width == 5 and height == 5 and total_blocks == 0:
        return puzzle
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
    # print("FALSE")

    return None

toprint = csp(hfillings, vfillings)
print_puzzle(toprint)
