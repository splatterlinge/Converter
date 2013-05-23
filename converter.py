#!/usr/bin/env python

import getopt, sys

def usage():
	print "help"

def createIni(name, ambient, diffuse, specular, emission, shininess, maps, shader):
	print name
	print ambient
	print diffuse
	print specular
	print emission
	print shininess
	print maps
	print shader

def parseMtl(filename):
	file = open(filename, 'r')

	name = None
	ambient = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	diffuse = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	specular = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	emission = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	shininess = 80
	maps = {}
	shader = {'default':'versatile'}

	for line in file.readlines():
		line = line.rstrip()
		fields = line.split(" ")
		keyword = fields.pop(0)

		if not line or line.startswith("#"):
			continue
		
		if keyword == "newmtl":
			if name:
				createIni(name, ambient, diffuse, specular, emission, shininess, maps, shader)
				
			name = fields[0]
		elif keyword == "Ka":
			ambient['red'] = fields[0]
			ambient['green'] = fields[1]
			ambient['blue'] = fields[1]
		elif keyword == "Kd":
			diffuse['red'] = fields[0]
			diffuse['green'] = fields[1]
			diffuse['blue'] = fields[1]
		elif keyword == "Ks":
			specular['red'] = fields[0]
			specular['green'] = fields[1]
			specular['blue'] = fields[1]
		elif keyword == "map_Ka":
			maps['diffuse'] = fields[0]
		elif keyword == "map_Kd":
			maps['diffuse'] = fields[0]
		elif keyword == "map_Ks":
			maps['diffuse'] = fields[0]

	createIni(name, ambient, diffuse, specular, emission, shininess, maps, shader)
		

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["help", "material="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False

    for o, a in opts:
    	if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m", "--material"):
            parseMtl(a)
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()