with open("hi.txt", "r") as f:
  l = f.readlines()
  lines=""
  for line in l:
    line = line.split(' ')[0]
    if ":" in line and "@" in line:
      lines+=line+"\n"
  with open("accounts.txt", "w") as f2:
    f2.write(lines)
