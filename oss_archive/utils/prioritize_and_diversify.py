"""Prioritize and Diversify is an algorithm tailored to go over a bunch operations groups/lists,
It works to prioritize the most important operations to a certain point, then it switch to other group of operation to diversify the work,
then it goes back to the start of the cycle to finish the first group to a certain point, then it diversify the work again,
and it goes around this cycle untill it finishes all groups.

Every group/list of operation have metadata, containing a priority value and a list of items/operations. Each item/operation have a priority value.
The prioritiy paradigm is seperate into levels, for example:
priority is an integer from 0 to 10
Level Minus -> priority = -1 (only assigned dynamically by the user to ignore a certain operation for the current run) 
Level Zero -> priority = 0  (only assigned dynamically by the user to push an operation into the top)
Level 1 -> priority = 1
Level 2 -> priority = [2,3,4]
level 3 -> priority = [5,6,7]
level 4- -> priority = [8,9,10]

The algorithm filter groups into levels, then it starts with level 1 then 2...etc
then the algo filter the group operation into levels and starts with level 1 then 2...etc
The diversifying works like goes on level 1 groups and do all level 1 opretaion of each of them first,
then do all operations in level 2 of all of them...etc. Then it goes to level 2 groups and starts with level 1 operations...etc

Main Data Structure that can be used:
- Cache (Hashmap or LRU/MRU): for fast access and to be able to edit
- Doubly Linkedlist (to be able to): used with the cache to to able to delete something from the working queue
- Red-Black Tree or AVL Trees: used for fairness of work and priorities
"""
from pydantic import Field, BaseModel
from typing import Annotated, TypedDict, Literal


class PriorityField(BaseModel):
    priority: Annotated[int, Field(ge=-1, le=10)]



class Level(BaseModel):
    order: int
    values: list[int]

class PriorityLevelsType(TypedDict):
    Minus: Level
    Zero: Level
    One: Level
    Two: Level
    Three: Level
    Four: Level

PriorityLevels = PriorityLevelsType(
    Minus=Level(order=-1, values=[-1]),
    Zero=Level(order=0, values=[0]),
    One=Level(order=1, values=[1]),
    Two=Level(order=1, values=[2,3,4]),
    Three=Level(order=1, values=[5,6,7]),
    Four=Level(order=1, values=[8,9,10])
)
    
def get_level(value: int) -> Level | None:
    pass