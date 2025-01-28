import os
files = os.listdir("specific")
gp=[]
st = input("Enter search terms: ").lower()
for file in files:
  if st in file.lower():
    gp.append(file)
s2=open("search_result.txt", "w")
lines=""
for f in gp:
  with open(f"specific/{f}", "r") as s:
    lin = s.read()
    line = f"[{f}]\n{lin}\n\n"
    lines+=line
s2.write(lines)
s2.close()
print("Successfully located accounts. Check search_result.txt")