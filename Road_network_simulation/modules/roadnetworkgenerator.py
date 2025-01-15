from modules.custom_types import *
from modules.loggers import *
from modules.utils import Utils as utils
import numpy as np
import random

class AsymmetricRoadNetwork():
    """
    Generates a general road network with no restrictions apart from that segments are oriented in cardinal directions
    and that graph edges are asymmetric.
    """
    def __init__(self):
        """
        Initializes the asymmetric road network object.
        """
        self.outgoing: Graph = {}
        self.incoming: Dict[Node, List[Node]] = {}
        self.entry_gates: List[Node] = []
        self.exit_gates: List[Node] = []
    
    def _add_segment(self, segment: Segment) -> None:
        """
        Adds a segment to the road network, if the segment or its inverse is not already in the network.
        The segment is added both to the outgoing and incoming dictionaries.
        
        Args:
            segment (Segment): A segment that is to be added to the road network.
            
        Returns:
            None (None): If no errors occur during the addition of the segment.
            
        Side effects:
            Adds the segment to the outgoing and incoming dictionaries. 
            Also ensures that the start and end nodes are in the network.
            
        Raises:
            ValueError: If the segment is diagonal, a null vector or if the segment is already in the network.
        """

        startnode, endnode = segment
        direction = self.get_unit_vector(segment)

        #Endnode is added to outgoing, as it makes random generation easier and adds no complexity.
        self._ensure_node_in_network(startnode)
        self._ensure_node_in_network(endnode)

        #Validate that the road is not already in the network.
        self._ensure_asymmetric_road(startnode, endnode, direction)
        
        self.outgoing[startnode].append((direction, endnode))
        self.incoming[endnode].append(startnode)

    def _ensure_node_in_network(self, node: Node) -> None:
        """
        Ensures that a node is in the network, if not it's added to the network.
        
        Args:
            node (Node): A node that is to be added to the network.

        Side effects:
            Adds the node to the outgoing and incoming dictionaries, if they are not already there.
        """
        if node not in self.outgoing:
            self.outgoing[node] = []
        if node not in self.incoming:
            self.incoming[node] = []
    
    def _ensure_asymmetric_road(self, startnode: Node, endnode: Node, direction: Unit_Vector) -> None:
        """
        Ensures that the road is not already in the network, as the graph is asymmetric.
        This test only works for cardinal directions.
        It is not necessary to validate self.incoming, as both outgoing and incoming are updated simultaneously.
        
        Args:
            startnode (Node): The starting node of the segment.
            endnode (Node): The end node of the segment.
            direction (Unit_Vector): The direction of the segment.
            
        Returns:
            None (None): If the road is not already in the network.
            
        Raises:
            ValueError: If the asymmetric property is violated.
        """
        inverse_direction = (-direction[0], -direction[1])

        if any(direction == edge[0] for edge in self.outgoing[startnode]) or \
           any(inverse_direction == edge[0] for edge in self.outgoing[endnode]):
            raise ValueError(f"Attempting to add an already existing direction to the road_network.")


    def convert_to_segments(self) -> List[Segment]:
        """
        Converts the road network to a list of segments.

        Returns:
            List[Segment]: A list of segments where each segment is a tuple of two points ((x1, y1), (x2, y2)).
        """
        segments = []
        for startnode in self.outgoing:
            for _, endnode in self.outgoing[startnode]:
                segments.append((startnode, endnode))
        return segments

    @staticmethod
    def get_unit_vector(segment: Segment) -> Unit_Vector:
        """
        Returns the unit vector of a segment.
        
        Args:
            segment (Segment): A segment that is to be converted to a unit vector.
            
        Returns:
            Unit_Vector: A unit vector of the segment.
            
        Raises:
            ValueError: If the segment is empty, diagonal or has no direction.
        """
        if not segment:
            raise ValueError("Segment is empty")
        (x1, y1), (x2, y2) = segment

        vector = np.array([x2-x1,y2-y1])
        norm = np.linalg.norm(vector)

        if norm == 0:
            raise ValueError("Segments with no direction are disallowed")
        if x1 != x2 and y1 != y2:
            raise ValueError("Diagonal segments are disallowed")

        unit_vector = tuple((vector / norm).tolist())
        return unit_vector
    
    def search_for_invalid_intersections(self) -> None:
        """
        Validates that every intersection has an entrance and exit.
        The function must be ran after exit and entry gates are generated.

        Returns:
            None (None): If no errors occur during the validation of the intersections.
            
        Raises:
            ValueError: If an intersection has no entrance or exit.
        """

        #Search for intersection with no exit
        for node in self.outgoing:
            if self.outgoing[node] == [] and node not in self.exit_gates:
                raise ValueError(f"intersection at {node} has no exit")
        
        #Search for intersection with no entrance
        for node in self.incoming:
            if self.incoming[node] == [] and node not in self.entry_gates:
                raise ValueError(f"intersection at {node} has no entrance")

                
    def _generate_gates(self) -> None:
        """
        Generates entry and exit gates for the road network. 
        The function must be ran after the road network is generated.
        An entry gate is a node with only one outgoing direction and no incoming directions.
        An exit gate is a node with only one incoming direction and no outgoing directions.

        Returns:
            None (None): If no errors occur during the generation of the gates.
            
        Side effects:
            Adds the entry and exit gates to the entry_gates and exit_gates lists respectively.
        """
        
        #If the road network has only one outgoing direction and no incoming direction, it's an entry gate.
        self.entry_gates = [node for node in self.outgoing if len(self.outgoing[node]) == 1 \
                             and len(self.incoming.get(node, [])) == 0]

        #If the road network has only one incoming direction and no outgoing direction, it's an exit gate.
        self.exit_gates  = [node for node in self.incoming if len(self.incoming[node]) == 1 \
                             and len(self.outgoing.get(node, [])) == 0]

 

    def enforce_reachability(self) -> None:
        """
        Validates if every node is reachable from any entry gate.

        Raises:
            RunTimeError: If a node is not reachable from an entry gate
        """
        visited = set()
        stack = list(self.entry_gates)
 
        while stack:
            node = stack.pop()
            visited.add(node)

            for _,neighbour in self.outgoing[node]:
                if neighbour not in visited:
                    stack.append(neighbour)

        if len(visited) != len(self.outgoing):
            raise RuntimeError("Not all nodes are reachable from an entry gate")

 

class CustomRoadNetwork(AsymmetricRoadNetwork):
    """
    Generates a custom road network with restrictions on the segments.
    The roads must have no overlaps, intersections, or diagonal segments.
    The graph must be connected and have at least one entry and exit gate.
    Each intersection must have an entrance and exit.
    The road network can be generated with or without enforcing that all nodes are reachable from an entry gate.
    """
    def __init__(self, segments: List[Segment], enforce_valid_paths: bool = True) -> None:
        """
        Generates a custom road network with a specified list of segments.
        
        Args:
            segments (List[Segment]): A list of segments. Each segment is a tuple of two points ((x1, y1), (x2, y2)).
            enforce_valid_paths (bool): A flag to determine, if road networks, with nodes that can't be reached from an entry gate, should be allowed.
            
        Returns:
            None (None): If no errors occur during the generation of the road network.
            
        Raises:
            ValueError: If the road network doesn't meet the minimum requirements.
            RuntimeError: If the road network if enforce_valid_paths is set to True and the network is not connected.
        """
        super().__init__()
        #Order matters: generate_roads -> gates -> validate roads.
        self._generate_roads(segments)
        self._generate_gates()
        self.validate_roads()

        if enforce_valid_paths:
            self.enforce_reachability()
        
    def _generate_roads(self, segments: List[Segment]) -> None:
        """
        Converts a list of segments to a road network.
        The road_network is structured as a dictionary where nodes are keys, and their values 
        are lists of associated nodes connected to them and the direction to them.

        Args:
            segments (List[Segment]): A list of segments. Each segment is a tuple of two points ((x1, y1), (x2, y2)).

        Returns:
            None (None): If no errors occur during the generation of the road network.

        Side effects:
            Adds segments to self.outgoing and self.incoming.
        """
        
        for segment in segments:
            self._add_segment(segment)

    def validate_roads(self) -> None:
        """
        Validate that there the road network has no diagonal-, overlapping segments, or intersecting segments.
        Additionally, it validates that all roads are connected, and that every intersection has an entrance and exit.
        Lastly, it verifies that at least one entry and exit gate exists.

        Returns:
            None (None): If no errors occur during the validation of the segments.
        
        Raises:
            ValueError: If any of the restrictions are violated.
        """

        #Custom road network must have atleast one entry and exit gate.
        if not self.entry_gates:
            raise ValueError("At least one entry gate must be defined")
        if not self.exit_gates:
            raise ValueError("At least one exit gate must be defined")
        
        segments = self.convert_to_segments()
        # Sort segments by direction
        vertical_lines, horizontal_lines = self._sort_by_direction(segments)
        terminal_logger.info('Successfully sorted all segments into horizontal and vertical segments')

        # Check for overlap in vertical and horizontal lines
        self._check_adjacent_overlap(vertical_lines, 'vertical')
        self._check_adjacent_overlap(horizontal_lines, 'horizontal')
        terminal_logger.info('No overlapping segments detected')

        # Check for intersections between vertical and horizontal lines
        self._check_intersections(horizontal_lines, vertical_lines)
        terminal_logger.info('No intersections detected between horizontal and vertical segments')

        #validate connectivity and that every intersection has an entry/exit.
        self._check_is_connected_network()
        terminal_logger.info('All roads are connected')

        self.search_for_invalid_intersections()
        terminal_logger.info('All intersections have an entrance and exit')
           
    @staticmethod
    def _sort_by_direction(segments: List[Segment]) -> Tuple[List[Segment], List[Segment]]:
        """
        Sorts a list of segments into two lists of horizontal and vertical segments respectively.
        Only lists containing strictly vertical and horizontal segments are allowed. 

        Args:
            segments: A list of all generated segments.

        Returns:
            List[Segments],List[Segments]: Two different lists, one that contains all vertical segments and one that contains
                            all horizontal segments.

        Raises:
            ValueError: If a segment is a null vector or if a segment is diagonal.  
        """
        vertical_lines, horizontal_lines = [], []
        for segment in segments:
            # Check if the segment is vertical or horizontal
            (x1, y1), (x2, y2) = segment
            if x1 == x2 and y1 != y2:
                vertical_lines.append(segment)
            elif y1 == y2 and x1 != x2:
                horizontal_lines.append(segment)
            else:
                raise ValueError(f"{segment} is invalid, as it's a diagonal segment or null vector.")
            
        return vertical_lines, horizontal_lines
    
    @staticmethod
    def _check_adjacent_overlap(segments: Segments, orientation: str) -> None:
        """
        Takes a sorted list of vertical or horizontal segments.
        The function validates if any two adjacent segments overlap each other.

        Args:
            segments (List[Tuple[StartNode, EndNode]]): A list of segments all with the same vertical or horizontal directionality.
            orientation (str): Can either be "horizontal" or "vertical" to describe the orientation of the list of segments.

        Raises:
            ValueError: If two segments overlap each other.
        """

        # Determine axes based on orientation
        fixed_axis, main_axis = (1, 0) if orientation == 'horizontal' else (0, 1)
        # Sort segments based on the main axis
        sorted_segments = sorted(segments, key=lambda line: line[0][main_axis])

        # Check each adjacent pair for overlap
        for i in range(len(sorted_segments) - 1):
            current_segment, next_segment = sorted_segments[i], sorted_segments[i + 1]

            # Only check if on the same axis.
            if current_segment[0][fixed_axis] == next_segment[0][fixed_axis]:

                #Extracts x values if horizontal and y values if vertical
                A_start, A_end = current_segment[0][main_axis], current_segment[1][main_axis]
                B_start, B_end = next_segment[0][main_axis], next_segment[1][main_axis]

                # Check for overlapping segments, including identical lines
                if (A_start < B_end and B_start < A_end) or (A_start == B_start and A_end == B_end):
                    raise ValueError(f"Error: {orientation.capitalize()} lines overlap: {current_segment}, {next_segment}")
    
    @staticmethod
    def _check_intersections(horizontal_lines: Segments, vertical_lines: Segments) -> None:
        """
        Checks if there are any intersections between horizontal and vertical segments.
        Likewise checks if any segment has a node on another segment.

        Args:
            horizontal_lines (List[Tuple[StartNode, EndNode]]): List of horizontal segments.
            vertical_lines (List[Tuple[StartNode, EndNode]]): List of vertical segments.
        
        Returns:
            None (None): If there are no errors, the function returns None.
        
        Raises:
            ValueError: If there are any intersections or nodes lying on segments.
        """
        for h_seg in horizontal_lines:
            h_min_x, h_max_x = sorted([h_seg[0][0], h_seg[1][0]])
            for v_seg in vertical_lines:
                v_min_y, v_max_y = sorted([v_seg[0][1], v_seg[1][1]])

                #Checks if any vertical segment crosses a horizontal line.
                if (h_min_x <= v_seg[0][0] <= h_max_x) and v_min_y < h_seg[0][1] < v_max_y:
                    raise ValueError(f"Intersection detected between {h_seg} and {v_seg}")

                #Checks if any vertical line starts or ends on the horizontal segment.
                elif (h_min_x < v_seg[0][0] < h_max_x) and ((v_min_y == h_seg[0][1]) or (v_max_y == h_seg[0][1])):
                    raise ValueError(f" {v_seg} has a starting or ending node on {h_seg}")            

    def _check_is_connected_network(self) -> None: 
        """
        Checks if all nodes of the road_network are connected.
        The function generates a symmetric closure of the road network and checks if all nodes are connected.
        Graphs consisting of zero nodes are trivially connected.

        Raises:
            ValueError: If the roads are not completely connected.
        """
        if not self.outgoing:
            return
        
        #Construct a symmetric graph from the road network.
        undirected_graph = {node: [] for node in self.outgoing}
        for node in self.outgoing:
            for _, endnode in self.outgoing[node]:
                undirected_graph[node].append(endnode)
                undirected_graph[endnode].append(node)
        

        #Set a starting node and initiate the search
        start_node = next(iter(undirected_graph)) 
        visited = [start_node]
        queue = [start_node]

        #Terminates if all neighbors have been visited
        while queue:
            node = queue.pop(0)
            for neighbor in undirected_graph[node]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)

        if len(undirected_graph) != len(visited):
            raise ValueError('All roads are not connected')

class RandomRoadNetwork(AsymmetricRoadNetwork):
    """
    Generates a random road network with a specified number of segments, centered around the origin.
    The road network only generates vertical and horizontal segments.
    The road network will not generate overlapping segments, or segments that intersect between endpoints.
    Every intersection will have at least one entrance and exit gate and the road network always contains at least one entry and exit gate.
    By default, the road network will also validate that every segment is reachable from an entry node, this can be disabled.
    """
    def __init__(self, total_segments: int, scalar: int, enforce_valid_paths: bool = True) -> None:
        """
        Generates a random road network with a specified number of segments.
        
        Args:
            total_segments (int): The total number of segments to generate.
            scalar (int): The scalar value to scale the road network with.
            enforce_valid_paths (bool): A flag to determine, if road networks, with nodes that can't be reached from an entry gate, should be allowed.
        """
        super().__init__()
        self.blocked_nodes = set()
        #Road generation rarely fails to generate an entry/exit gate, a try/except block handles this very improbable case.

        if total_segments < 1:
            raise ValueError("Total segments must be a positive integer")
        
        while True:
            try:
                #Order matters: generate_roads -> upscale -> gates -> validate roads.
                self._generate_roads(total_segments)
                self._upscale_road_network(scalar)
                self._generate_gates()

                if not self.exit_gates or not self.entry_gates:
                    raise RuntimeError("Insufficient entry or exit gates")
                
                if enforce_valid_paths:
                    self.enforce_reachability()
                break
            except RuntimeError:
                #Enforce reachability can cause the generation to fail, and will thus retry the generation.
                #Errors are infrequent and should rarely occur.

                self.reset()

    def reset(self) -> None:
        """
        Resets the road network to an empty state.

        Side effects:
            Clears all existing segments, entry/exit gates, and blocked nodes.
        """
        self.outgoing.clear()
        self.incoming.clear()
        self.entry_gates.clear()
        self.exit_gates.clear()
        self.blocked_nodes.clear()

    def _generate_roads(self, total_segments: int) -> None:
        """
        Generates a random road network with a specified number of segments.
        The road network is centered around the origin and only allows cardinal directions.
        The road network generates roads of different orientations and lengths.

        Args:
            total_segments (int): The total number of segments to generate.

        Raises:
            ValueError: If the total segments is not a positive integer.

        Side effects:
            Adds segments to self.outgoing and self.incoming.
        """
        
        if total_segments < 1:
            raise ValueError("Total segments must be a positive integer")
        
        spawn_node = (0,0)
        available_nodes = [spawn_node]

        #For the loop to run an initial segment must be added.
        dx,dy = utils.pick_item(self._get_available_directions(spawn_node))
        self._add_segment(((spawn_node), (spawn_node[0]+dx, spawn_node[1]+dy)))

        #The first segment is added, thus the counter starts at 1.
        generated_segments = 1

        while generated_segments < total_segments:
            startnode = random.choice(available_nodes)
            available_directions = self._get_available_directions(startnode)
            node_direction = utils.pick_item(available_directions)

            #If there exists a direction to move in, find the endnode and add the segment.
            if node_direction:
                endnode = self._find_endnode(startnode, node_direction)
                
                #If the node is reached for the first time add it to the available nodes.
                if not endnode in self.outgoing:
                    available_nodes.append(endnode)
                
                options = []
                #If the startnode has incoming_roads directions, an outgoing segment is allowed
                # IFF the endnode is not in the network or the endnode has outgoing directions.
                if self.incoming.get(startnode, []) and (endnode not in self.outgoing or self.outgoing.get(endnode, []) != []):
                    options.append((startnode, endnode)) 

                # If the startnode has outgoing directions, an incoming_roads segment is allowed
                # IFF the endnode is not in the network or the endnode has incoming_roads directions.
                if self.outgoing.get(startnode, []) and (endnode not in self.outgoing or self.incoming.get(endnode, []) != []):
                    options.append((endnode, startnode))
                
                if options:
                    self._add_segment(random.choice(options))
                    generated_segments += 1

            else:
                available_nodes.remove(startnode)
    

    def _find_endnode(self, node: Node, node_direction: Unit_Vector) -> Node:
            """
            Creates a connecting node to the current node based on the current direction and the available directions.

            Args:
                node (Tuple[int, int]): The starting node segment to which an end node is to be connected.
                node_direction (Tuple[int, int]): The direction of the starting node to the current node
            
            Returns:
                Node (Node): The found end node.
            
            Side effects:
                Assigns a node to the set of blocked nodes, when longer segment generation occurs.
            """
            while True:
                x, y = node
                dx, dy = node_direction
                current_node = (x + dx, y + dy)
                avail_dirs = self._get_available_directions(current_node)
                #Weight movement in the same direction higher to create longer segments more frequently.
                new_direction = utils.pick_item(avail_dirs, weighted_item=node_direction, weight=2)
                
                #If the node is in the network, a longer segment can't generate across it.
                if new_direction == node_direction and current_node not in self.outgoing:
                    self.blocked_nodes.add(current_node)
                    #The loop is repeated from the newly generated node.
                    node = current_node
                else:
                    #If the direction generated differs, the segment is complete.
                    return current_node
    

    def _node_is_obstacle(self, node: Node) -> bool:
        """
        Checks if a given node is an obstructed node.
        
        Args:
            node (Tuple[int, int]): The coordinates of the node that is looked at
        
        Returns:
            True: if the node is already in the list of blocked nodes.
            False: if the node is not in the list of blocked nodes.
        """
        if node in self.blocked_nodes:
            return True
        return False
    
    def _get_available_directions(self, node: Node) -> List[Unit_Vector]:
        """
        Returns the available directions to move to from a given node.

        Args:
            node (Tuple[int, int]): The node to check for available directions.

        Returns:
            List[Tuple[int, int]]: A list of available directions to move to.
        """

        available_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x,y = node

        # If the node is in the road network, get its connections else empty list.
        for direction,_ in self.outgoing.get(node, []):
            available_directions.remove(direction)
      
        for direction in available_directions[:]:
            dx,dy = direction

            #Validate if the node is a valid node to move to.
            new_node = (x+dx,y+dy)
            if self._node_is_obstacle(new_node):
                available_directions.remove(direction)

            #If the new node is in the network, check if the node is already connected to the current node.
            elif new_node in self.outgoing:
                for _, endnode in self.outgoing[new_node]:
                    if endnode == node:
                        available_directions.remove(direction)

        return available_directions
    
    def _upscale_road_network(self, scalar: int) -> None:
        """
        Scales the outgoing and incoming road network by a positive scalar value.    
        The function must be ran after the segments are generated, but before the gates are generated.
        
        Args:
            scalar (int): A positive integer scalar value to scale the road network with.

        Raises:
            ValueError: If the scalar value is not a positive integer.

        Side effects:
            Overwrites the road network with the scaled values
        """

        if scalar < 1 or not isinstance(scalar, int):
            raise ValueError("Scalar value is not a positive integer.")
    
        scaled_outgoing = {}
        scaled_incoming = {}

        for node in self.outgoing:
            scaled_node = (node[0] * scalar, node[1] * scalar)  # Scale the node
            scaled_outgoing[scaled_node] = []

            for unitvector, endnode in self.outgoing[node]:
                scaled_endnode = (endnode[0]*scalar, endnode[1]*scalar)
                scaled_outgoing[scaled_node].append((unitvector,scaled_endnode))


        for node in self.incoming:
            scaled_node = (node[0] * scalar, node[1] * scalar)
            scaled_incoming[scaled_node] = []

            for endnode in self.incoming[node]:
                scaled_endnode = (endnode[0]*scalar, endnode[1]*scalar)
                scaled_incoming[scaled_node].append(scaled_endnode)

            
        # Update the original road_network with the scaled values
        self.outgoing.clear()
        self.incoming.clear()
        self.outgoing.update(scaled_outgoing)
        self.incoming.update(scaled_incoming)
