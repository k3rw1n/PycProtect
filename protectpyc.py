from __future__ import print_function


is2 = True

import sys
import os
import random
import py_compile
import string

if len(sys.argv) != 3:
    print('Usage: python protectpyc.py <filename> [2|3]')
elif not os.path.exists(sys.argv[1]):
    print('Error, file not found')
else:
    filename = sys.argv[1]
    f = open(filename, 'r')
    content = f.read()
    if len(content) < 1243:
        rest = 1243 - len(content)
        for i in range(rest):
            if i == 0:
                content += '#'
            else:
                content += random.choice(string.ascii_lowercase+string.ascii_uppercase)
    if sys.argv[2] == '2':
        out, special = 'exec str(', False
    else:
        out, special = 'exec(str(', False
    print(content)

    for caract in content:
        if caract == '\\':
            out += '\'\\'
            special = True
        elif special:
            out += caract + '\'+'
            special = False
        else:
            if sys.argv[2] == '2':
                out += 'unichr({})+'.format(str(ord(caract)))
            else:
                out += 'chr({})+'.format(str(ord(caract)))
    if sys.argv[2] == '2':
        out = out[:-1] + ')'
    else:
        out = out[:-1] + '))'
    output = open('protected-'+filename,'w')
    output.write(out)
    output.close()
    py_compile.compile('protected-'+filename)
    print('Success ! your python script protected file is "{}"'.format('protected-'+filename))