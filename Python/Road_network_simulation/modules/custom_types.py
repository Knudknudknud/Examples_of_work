"""
This module contains the custom types used in the project,
to make the code more readable and easier to understand.
"""

from typing import List,Tuple,Dict

Node = Tuple[int,int]
StartNode = Tuple[int,int]
EndNode = Tuple[int,int]
Unit_Vector = Tuple[int,int]
Segment = Tuple[StartNode,EndNode]
Segments = list[Tuple[StartNode,EndNode]]
RGB = Tuple[int,int,int]
Position = Tuple[float,float]
Graph = Dict[StartNode, List[Tuple[Unit_Vector,EndNode]]]

