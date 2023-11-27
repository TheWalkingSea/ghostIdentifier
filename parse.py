import pyperclip
# import os
# l = list()
# while True:
#     text = input("waiting: ")
#     if text == "s":
#         break
#     if text:
#         l.append(text)
# os.system("cls")
# pyperclip.copy(str(l)[1:-1])
# print(str(l)[1:-1])

e = input("ENTER: ")
l = list()
convert = {"Fingerprints": "fingerprints", "Ghost Writing": "book", "Freezing Temperatures": "thermometer"}
for i in e:
    l.append(convert[e])
print(l)
