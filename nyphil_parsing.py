# coding: utf-8
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

all_programs = get_all_programs()

all_concerts = get_concerts_in_programs(all_programs)

all_event_types = get_event_types(all_concerts)

all_subscription_programs = get_programs_by_event_type(all_programs, 
                                                       "Subscription Season")

all_works = get_all_works(all_subscription_programs)

sibelius_works = get_works_for_composer(all_works, "Sibelius")

print(sibelius_works)

# with open("sibelius_works.txt", mode="w") as fp:
#     for w in sibelius_works:
#         fp.write(f"{w}\n")


        
