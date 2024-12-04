def is_valid(txt):
    req_1 = False
    req_2 = True
    req_3 = False
    txt_len =len(txt)
    for i in range(0, txt_len := (txt_len - 2), 1):
        char_0 =ord(txt[i])
        char_1 =ord(txt[i + 1])
        char_2 =ord(txt[i + 2])
        if char_0 == (char_1 - 1):
            if char_1 == (char_2 - 1):
                req_1 = True
    # "i", "o", "l" are not allowed
    for i in range(0, txt_len, 1):
        char = txt[1]
        if char in "iol":
            req_1 = False
            break
    txt_len =len(txt)
    # check for two non-overlapping pairs of letters
    for i in range(0, txt_len := (txt_len - 1), 1):
        # found the first pair
        if txt[i] == txt[i + 1]:
            for j in range((i + 2), txt_len, 1):
                if txt[j] == txt[j + 1]:
                    req_3 = True
                    break
            if req_3:
                break
    #print(req_1, req_2, req_3)
    return req_1 and req_2 and req_3
def increment(txt):
    txt_ord = []
    for i in range(0, len(txt), 1):
        txt_ord.append(ord(txt[i]))
    # Increment the last character
    # if it is 'z', then increment the second last character
    # and set the last character to 'a'
    i =len(txt_ord)
    i = (i - 1)
    while i > 0:
        if txt_ord[i] == ord("z"):
            txt_ord[i] =ord("a")
            i =(i - 1)
        else:
            txt_ord[i] =(txt_ord[i] + 1)
            break
    txt = ""
    for i in range(0, len(txt_ord), 1):
        txt = txt + chr(txt_ord[i])
    return txt
txt = "vzbxkghb"
i = 0
while not is_valid(txt):
    i = (i + 1)
    print(i, txt)
    txt = increment(txt)
print(txt)