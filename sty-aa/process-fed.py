
source_file = open("federalist-all", 'r')

dest_file = None

paper = 0

for line in source_file :
    if line.startswith('FEDERALIST') :
        if dest_file :
            dest_file.close()
        paper += 1
        dest_file = open("federalist" + str(paper), 'w')
    if dest_file and all([not line.startswith(x) for x in ["HAMILTON", "MADISON", "JAY"]]) :
        dest_file.write(line)

if dest_file :
    dest_file.close()
