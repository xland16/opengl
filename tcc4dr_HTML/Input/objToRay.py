import sys

#Method to get texture coordinates
def getTexCoords(texcoords):
	if (texcoords == ''):
		return '0 0'

	tokens = texcoords.split()
	coords = '0 0'
	
	if (len(tokens) == 2):
		coords = tokens[0] + ' ' + tokens[1]

	return coords

#Get files to read/write
name = sys.argv[1]
obj_file = '%s.obj' % name
ray_file = '%s.ray' % name

f = open(obj_file,'r');
out = open(ray_file,'w');

#Default material to be printed to the ray file
out.write('#material_num 1\n#material\n\t0.000000 0.000000 0.000000\n\t0.200000 0.200000 0.200000\n\t0.500000 0.300000 0.000000\n\t0.250000 0.250000 0.250000 2.000000\n\t0.000000 0.000000 0.000000\n\t0.000000\n\t-1\n\t!!\n')

#Lists for storage
points = []
faces = []
texcoords = []
normals = []
vertices = []
triangles = []
d = {}

#Read each line and store coordinate information
for line in f:
	tokens = line.split(' ',1)
	if (tokens[0] == 'v'):
		points += [tokens[1]]
	if (tokens[0] == 'vn'):
		normals += [tokens[1]]
	if (tokens[0] == 'vt'):
		texcoords += [tokens[1]]
	if (tokens[0] == 'f'):
		faces += [tokens[1]]

count = 0

#Go through each face and make a triangle from the vertex information
for line in faces:
	tokens = line.split()
	sides = len(tokens)
	t_line = '\n#shape_triangle 0\n\t'

	#Go through each vertex, collect information to declare vertices in .ray format
	for i in range(0,3):
		num = tokens[i].split('/')
		pc = points[int(num[0].strip())-1].strip()
		if (num[1].strip() != ''):
			tc = texcoords[int(num[1].strip())-1].strip()
			tc = getTexCoords(tc)
		else:
			tc = '0 0'
		nc = normals[int(num[2].strip())-1].strip()
		v_line = '#vertex\n\t%s\n\t%s\n\t%s\n' % (pc,nc,tc)

		if d.has_key(v_line):
			t_line += str(d.get(v_line)) + ' '
		else:
			d[v_line] = count
			vertices += [v_line]

			t_line += str(count) + ' '
			count = count + 1

	triangles += [t_line]

	t_line = '\n#shape_triangle 0\n\t'

	#Make other triangle if current face is a quadrilateral
	if (sides == 4):
		for i in range(0,4):
			if i != 1:
				num = tokens[i].split('/')

				pc = points[int(num[0].strip())-1].strip()

				if (num[1].strip() != ''):
					tc = texcoords[int(num[1].strip())-1].strip()
					tc = getTexCoords(tc)
				else:
					tc = '0 0'

				nc = normals[int(num[2].strip())-1].strip()
				v_line = '#vertex\n\t%s\n\t%s\n\t%s\n' % (pc,nc,tc)

				if d.has_key(v_line):
					t_line += str(d.get(v_line)) + ' '
				else:
					d[v_line] = count
					vertices += [v_line]

					t_line += str(count) + ' '
					count = count + 1

		triangles += [t_line]


#Declare vertices in .ray file
out.write('#vertex_num ' + str(len(vertices)) + '\n')
for line in vertices:
	out.write(line)

out.write('#group_begin\n\t1 0 0 0\n\t0 1 0 0\n\t0 0 1 0\n\t0 0 0 1\n');

#Declare triangles in .ray file
for line in triangles:
	out.write(line)
out.write('\n#group_end\n')

out.close()


f.close()
