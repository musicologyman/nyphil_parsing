# coding: utf-8
from itertools import groupby
import json
import re
from collections.abc import Iterable, Mapping
from more_itertools import flatten
from toolz.functoolz import pipe
from typing import Any, NamedTuple

class Work(NamedTuple):
    composer:str
    title:str

def get_all_programs() -> Iterable[Mapping[str, Any]]:
    with open("nyphil.json") as fp:
        data_root = json.load(fp)
        return data_root["programs"]

def get_concerts_in_programs(programs:Iterable[Mapping[str, Any]]):
    for program in programs:
        for concert in program["concerts"]:
            yield concert

def get_event_types(concerts):
    return sorted(list(set([concert['eventType'] for concert in concerts])),
                  key=str.upper)

def get_programs_by_event_type(programs, event_type):
    return (program for program in all_programs 
               if len([concert for concert in program["concerts"]]) > 0)

def get_all_works(programs):
    works = (Work(work["composerName"], work["workTitle"]) 
                for program in programs 
                for work in program['works'] 
                if 'composerName' in work
                and not isinstance(work["workTitle"], dict))
    return list(set(works))

def get_works_for_composer(works: Iterable[Work], composer: str) \
        -> Iterable[Work]:
    return sorted((work.title for work in works
                   if re.search(composer, work.composer, re.IGNORECASE)))

def get_programs_for_composer(programs, composer):
    return [program for program in programs
                    for work in program["works"] 
                    if 'composerName' in work 
                    and re.search(composer, work["composerName"], 
                        re.IGNORECASE)]

all_programs = get_all_programs()

all_concerts = get_concerts_in_programs(all_programs)

all_event_types = get_event_types(all_concerts)

all_subscription_programs = list(get_programs_by_event_type(all_programs, 
                                                       "Subscription Season"))

all_works = get_all_works(all_subscription_programs)

sibelius_works = get_works_for_composer(all_works, "Sibelius")

sibelius_programs = get_programs_for_composer(all_subscription_programs, 
                                              "sibelius")

# print(len(sibelius_programs))

# with open("sibelius_programs.json", mode="w") as fp:
#     json.dump(sibelius_programs, fp, indent=4)

# with open("sibelius_works.txt", mode="w") as fp:
#     for work in sibelius_works:
#         fp.write(f"{work}\n")

with open("sibelius_major_works.txt") as fp:
    sibelius_major_works = [line[:-1] for line in fp]

import io
import hashlib

def get_program_hash_digest(program):
    with io.StringIO() as sp:
        json.dump(program, sp, indent=4)
        contents = sp.getvalue()
    m = hashlib.sha256()
    m.update(contents.encode())
    return m.hexdigest()

class ProgramDigest(NamedTuple):
    hexdigest:str
    program:dict

# Filter programs by major works:
programs_with_major_works = [ProgramDigest(get_program_hash_digest(program),
                                program) 
                             for program in sibelius_programs
                             for work in program["works"]
                             if "workTitle" in work 
                             and work["workTitle"] in sibelius_major_works]

programs_with_major_works.sort(key=lambda pd:pd.hexdigest)

deduped_programs_with_major_works \
    = [list(values)[0].program for _, values 
       in groupby(programs_with_major_works, key=lambda pd:pd.hexdigest)]
    
print(len(deduped_programs_with_major_works))

with open("deduped_sibelius_programs.json", mode="w") as fp:
    json.dump(deduped_programs_with_major_works, fp, indent=4)

# with open("programs_with_major_works.json", mode="w") as fp:
#     json.dump(programs_with_major_works, fp, indent=4)