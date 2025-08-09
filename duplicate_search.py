# coding: utf-8
get_ipython().run_line_magic('ls', '')
import json
with open("programs_with_major_works.json") as fp:
    programs = json.load(fp)o
with open("programs_with_major_works.json") as fp:
    programs = json.load(fp)
    
program_ids = [p["programID"] for p in programs]
len(program_ids)
program_ids[:20]
program_ids.sort()
from itertools import groupby
grouped_ids = groupby(ids, key=lambda id:id)
grouped_ids = groupby(program_ids, key=lambda id:id)
grouped_ids = [(id, list(ids)) for id, ids in groupby(program_ids, key=lambda id:idi)]
grouped_ids = [(id, list(ids)) for id, ids in groupby(program_ids, key=lambda id:id)]
len(grouped_ids)
duplicates = [(id, len(ids)) for id, ids in grouped_ids if len(ids) > 1]
len(duplicates)
duplicates[:10]
duplicates.sort(key=lambda x:-x[1])
duplicates[:10]
x = [program for program in programs if program["programID"] == "6108"]
len(x)
x[:2]
import hashlib
import io
def get_program_hash_digest(program):
    with io.BytesIO() as bp:
        json.dump(program, bp, indent=4)
    contents = bp.getvalue()
    m = hashlib.sha256()
    m.update(contents)
    return m.digest()
    
digests = [get_program_hash_digest(p) for p in x]
import io
def get_program_hash_digest(program):
    with io.StringIO() as bp:
        json.dump(program, bp, indent=4)
    contents = bp.getvalue()
    m = hashlib.sha256()
    m.update(contents.encode())
    return m.digest()
    
    
get_ipython().run_line_magic('rep', '25')
digests = [get_program_hash_digest(p) for p in x]
import io
def get_program_hash_digest(program):
    with io.StringIO() as bp:
        json.dump(program, bp, indent=4)
        contents = bp.getvalue()
    m = hashlib.sha256()
    m.update(contents.encode())
    return m.digest()
    
    
digests = [get_program_hash_digest(p) for p in x]
digests[0]
digests[1]
grouped_digests = [(key, list(values)) for key, values in groupby(digests,key=lambda x:x)]
grouped_digests.keys()
len(grouped_digests)
