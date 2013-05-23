#!/usr/bin/env python

import sys, os, shutil
import argparse
import ConfigParser

def usage():
	print "help"

def create(srcdir, dstdir, name, ambient, diffuse, specular, emission, shininess, maps, shader):
	try:
		os.makedirs(os.path.join(dstdir, name))
	except:
		pass

	config = ConfigParser.ConfigParser()
	config.optionxform=str

	config.add_section('Model')
	config.set('Model', 'ambientRed', ambient['red'])
	config.set('Model', 'ambientGreen', ambient['green'])
	config.set('Model', 'ambientBlue', ambient['blue'])
	config.set('Model', 'ambientAlpha', ambient['alpha'])

	config.set('Model', 'diffuseRed', diffuse['red'])
	config.set('Model', 'diffuseGreen', diffuse['green'])
	config.set('Model', 'diffuseBlue', diffuse['blue'])
	config.set('Model', 'diffuseAlpha', diffuse['alpha'])

	config.set('Model', 'specularRed', specular['red'])
	config.set('Model', 'specularGreen', specular['green'])
	config.set('Model', 'specularBlue', specular['blue'])
	config.set('Model', 'specularAlpha', specular['alpha'])

	config.set('Model', 'emissionRed', emission['red'])
	config.set('Model', 'emissionGreen', emission['green'])
	config.set('Model', 'emissionBlue', emission['blue'])
	config.set('Model', 'emissionAlpha', emission['alpha'])

	config.set('Model', 'shininess', shininess)

	config.add_section('Textures')
	config.set('Textures', 'diffuseMap', maps['diffuse'])
	shutil.copyfile(os.path.join(srcdir, maps['diffuse']), os.path.join(dstdir, name, maps['diffuse']))

	config.add_section('Shader')
	config.set('Shader', 'defaultShader', shader['default'])
	config.set('Shader', 'blobbingShader', shader['blobbing'])

	with open(os.path.join(dstdir, name, 'material.ini'), 'wb') as configfile:
		config.write(configfile)	

def parseMtl(srcdir, srcfile, dstdir):
	file = open(os.path.join(srcdir, srcfile), 'r')

	name = None
	ambient = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	diffuse = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	specular = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	emission = {'red':0, 'green':0, 'blue':0, 'alpha':1}
	shininess = 80
	maps = {}
	shader = {'default':'versatile', 'blobbing':'versatileBlob'}

	for line in file.readlines():
		line = line.rstrip()
		fields = line.split(" ")
		keyword = fields.pop(0)

		if not line or line.startswith("#"):
			continue
		
		if keyword == "newmtl":
			if name:
				create(srcdir, dstdir, name, ambient, diffuse, specular, emission, shininess, maps, shader)
				
			name = os.path.splitext(srcfile)[0]+'_'+fields[0]
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

	create(srcdir, dstdir, name, ambient, diffuse, specular, emission, shininess, maps, shader)
		

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--material', required=True, help='Material filepath.')
	parser.add_argument('--outdir', required=True, help='Output directory.')
	args = parser.parse_args()

	srcdir = os.path.dirname(args.material)
	srcfile = os.path.basename(args.material)
	
	parseMtl(srcdir, srcfile, args.outdir)

if __name__ == "__main__":
	main()