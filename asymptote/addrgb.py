#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
	print("usage: %s countrymap_rgb.csv" % sys.argv[0])
	sys.exit(1)

countrymap = dict()
for l in open(sys.argv[1]):
	v = [x.strip() for x in l.split(";")]
	countrymap[v[0]] = (v[1], v[2], v[3])
print(countrymap)

count = 0
out = open('mapdata1_rgb.csv', 'w')
for l in open('mapdata1.csv'):
	v = l.split('\t');
	# if v[2] not in countrymap:
	if v[1] not in countrymap:
		# print("%s not found" % v[2])
		print("%s not found" % v[1])
		rgb = (1, 1, 1)
	else:
		# rgb = countrymap[v[2]]
		rgb = countrymap[v[1]]
		count += 1
	out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (v[0], v[1], v[2], str(rgb[0]), str(rgb[1]), str(rgb[2]), v[3], "\t".join(v[4:])))
out.close()

print("found %d countries" % (count))
