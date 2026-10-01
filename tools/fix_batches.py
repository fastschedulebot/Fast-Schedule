# -*- coding: utf-8 -*-
"""Repair ru_batches .py files: a bad mass-replace put REAL newlines inside
single-quoted string literals. Join those lines back and re-escape the
newlines as backslash-n so every string is a proper Python literal again."""
import io, glob

def file_ok(path):
    try:
        compile(io.open(path, encoding='utf-8').read(), path, 'exec')
        return True
    except SyntaxError:
        return False

def repair(s):
    out = []
    pending = None
    for line in s.split('\n'):
        if pending is not None:
            line = pending + '\\n' + line
            pending = None
        # an unterminated single-quoted literal: odd number of ' on the line
        if line.count("'") % 2 == 1:
            pending = line
            continue
        out.append(line)
    if pending is not None:
        out.append(pending)
    return '\n'.join(out)

fixed_any = 0
for f in glob.glob('tools/ru_batches/*.py'):
    if file_ok(f):
        continue
    s = io.open(f, encoding='utf-8').read()
    r = repair(s)
    try:
        compile(r, f, 'exec')
    except SyntaxError as e:
        print('STILL BROKEN', f, e)
        continue
    io.open(f, 'w', encoding='utf-8', newline='\n').write(r)
    fixed_any += 1
    print('repaired', f)
print('done, repaired', fixed_any)
