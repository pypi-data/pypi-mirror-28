import warnings
from typing import Callable, Iterator, Optional, Set, Tuple, cast, Iterable, Dict, List, Sequence, Union, Any
from uuid import uuid4
from mhelper import array_helper, ComponentFinder, exception_helper, SwitchError, ByRef, NOT_PROVIDED, LogicError


_LegoComponent_ = "groot.data.lego_model.LegoComponent"
_LegoModel_ = "groot.data.lego_model.LegoModel"
_LegoSequence_ = "groot.data.lego_model.LegoSequence"
_MGraph_ = "groot.data.graphing.MGraph"
_MNode_ = "groot.data.graphing.MNode"
_MEdge_ = "groot.data.graphing.MEdge"
TUid = int
TNodeOrUid = Union[TUid, _MNode_]  # A node in the graph, or a UID allowing the node to be found, or a node in another graph that can also be found in this graph
DFindId = Callable[[str], object]
DNodePredicate = Callable[[_MNode_], bool]
DNodeToText = Callable[[_MNode_], str]


class DepthInfo:
    def __init__( self,
                  *,
                  node: "MNode",
                  is_last: bool,
                  is_repeat: bool,
                  parent_info: "Optional[DepthInfo]",
                  has_children: bool ):
        self.node = node
        self.is_last = is_last
        self.is_repeat = is_repeat
        self.parent_info = parent_info
        self.depth = (parent_info.depth + 1) if parent_info is not None else 0
        self.has_children = has_children
    
    
    def full_path( self ) -> "List[DepthInfo]":
        r = []
        parent = self.parent_info
        
        while parent:
            r.append( parent )
            parent = parent.parent_info
        
        return list( reversed( r ) )
    
    
    def describe( self, get_text: DNodeToText ) -> str:
        # return "{}:{}{}".format( "{}".format(self.parent.node.uid) if self.parent else "R", "*" if self.is_repeat else "", self.node.detail )
        # return "{}{}->{}".format( "{}".format( self.parent.node.uid ) if self.parent else "(NO_PARENT)", "(POINTER)" if self.is_repeat else "", self.node.detail )
        ss = []
        
        for parent in self.full_path():
            ss.append( "    " if parent.is_last else "│   " )
            # ss.append( str(parent.node.uid).ljust(4, ".") )
        
        ss.append( "└───" if self.is_last else "├───" )
        
        if self.is_repeat:
            ss.append( "(REPEAT)" )
        
        ss.append( "┮" if self.has_children else "╼" )
        ss.append( get_text( self.node ) )
        
        return "".join( ss )


class FollowParams:
    def __init__( self,
                  *,
                  start: "MNode",
                  include_repeats: bool = False,
                  exclude_edges: "Iterable[MEdge]" = None,
                  exclude_nodes: "Iterable[MNode]" = None ) -> None:
        if exclude_edges is None:
            exclude_edges = []
        
        if exclude_nodes is None:
            exclude_nodes = []
        
        for x in cast( list, exclude_edges ):
            assert isinstance( x, MEdge )
        
        for x in cast( list, exclude_nodes ):
            assert isinstance( x, MNode )
        
        self.include_repeats: bool = include_repeats
        self.exclude_nodes: Set[MNode] = set( exclude_nodes )
        self.visited: List[DepthInfo] = []
        self.exclude_edges: Set[MEdge] = set( exclude_edges )
        self.root_info: DepthInfo = DepthInfo( node = start,
                                               is_last = True,
                                               is_repeat = False,
                                               parent_info = None,
                                               has_children = False )
        
        self.visited.append( self.root_info )
        self.exclude_nodes.add( self.root_info.node )
    
    
    @property
    def visited_nodes( self ) -> "Iterator[MNode]":
        return (x.node for x in self.visited)


class CutPoint:
    def __init__( self, left_subgraph: _MGraph_, left_node: _MNode_, right_subgraph: _MGraph_, right_node: _MNode_ ) -> None:
        self.left_subgraph: MGraph = left_subgraph
        self.left_node: MNode = left_node
        self.right_subgraph: MGraph = right_subgraph
        self.right_node: MNode = right_node


class IsolationPoint:
    def __init__( self, edge: _MEdge_, internal_node: _MNode_, external_node: _MNode_, inside_nodes: Set[_MNode_], cladistic_nodes: Set[_MNode_] ) -> None:
        self.edge: MEdge = edge
        self.internal_node: MNode = internal_node
        self.external_node: MNode = external_node
        self.inside_nodes: Set[_MNode_] = inside_nodes
        self.cladistic_nodes: Set[_MNode_] = cladistic_nodes
    
    
    @property
    def count( self ):
        return len( self.inside_nodes )
    
    
    def __str__( self ):
        return "<ISOLATES {} GIVEN {}>".format( self.inside_nodes, self.cladistic_nodes )


class IsolationError( Exception ):
    def __init__( self, message, inside_set: Iterable[_MNode_], outside_set: Iterable[_MNode_] ):
        super().__init__( message )
        self.inside_set = inside_set
        self.outside_set = outside_set


class NodeCollection:
    def __init__( self ):
        self._by_id: Dict[int, MNode] = { }
        self._by_data: Dict[object, Set[MNode]] = { }
    
    
    def by_id( self, item ):
        return self._by_id[item]
    
    
    def get_by_id( self, item ):
        return self._by_id.get( item )
    
    
    def by_data( self, item ):
        return array_helper.single_or_error( self._by_data[item] )
    
    
    def list_by_data( self, item ):
        return tuple( self._by_data[item] )
    
    
    def __iter__( self ):
        return iter( self.nodes )
    
    
    def values( self ):
        warnings.warn( "obsolete function for compatibility with old dict-style collection - use nodes property or iter function instead", DeprecationWarning )
        return self.nodes
    
    
    @property
    def nodes( self ):
        return self._by_id.values()
    
    
    @property
    def uids( self ):
        return self._by_id.keys()
    
    
    def _register( self, node: _MNode_, uid, data ):
        self._by_id[uid] = node
        self.__register_data_add( node, data )
    
    
    def __register_data_add( self, node, data ):
        set_ = self._by_data.get( data )
        
        if set_ is None:
            set_ = set()
            self._by_data[data] = set_
        
        set_.add( node )
    
    
    def _register_data( self, node: _MNode_, old: object, new: object ):
        self.__register_data_remove( node, old )
        self.__register_data_add( node, new )
    
    
    def __register_data_remove( self, node: _MNode_, data: object ):
        set_ = self._by_data.get( data )
        set_.remove( node )
        if not set:
            del self._by_data[data]
    
    
    def _unregister( self, node: _MNode_, uid: int, data: object ):
        del self._by_id[uid]
        self.__register_data_remove( node, data )


class MGraph:
    def __init__( self ) -> None:
        """
        CONSTRUCTOR
        """
        self.nodes = NodeCollection()
        self._root = None
    
    
    @property
    def root( self ):
        """
        Root of the graph, or `None` if unassigned.
        """
        return self._root
    
    
    @property
    def first_node( self ) -> _MNode_:
        """
        Obtains the root node, or an arbitrary node if there is no root.
        """
        if self._root is None:
            return array_helper.first_or_error( self.nodes )
        else:
            return self._root
    
    
    def get_root( self ) -> _MNode_:
        """
        Obtains the root of the graph.
        If no root is assigned, one is created.
        
        :except KeyError: No nodes in graph
        """
        # B/C
        if not hasattr( self, "_root" ):
            self._root = None
        
        if self._root is None:
            array_helper.first_or_error( self.nodes ).make_root()
        
        return self._root
    
    
    def cut_one_at_isolation( self, is_inside: DNodePredicate, is_outside: DNodePredicate ) -> _MGraph_:
        """
        A combination of `find_isolation_point` and `cut_one`.
        
        :except IsolationError: More than one isolation point is found
        """
        point = self.find_isolation_point( is_inside, is_outside )
        return self.cut_one( point.internal_node, point.external_node )
    
    
    def cut_at_isolation( self, is_inside: DNodePredicate, is_outside: DNodePredicate ) -> Tuple[_MGraph_, _MGraph_]:
        """
        A combination of `find_isolation_point` and `cut`.
        
        :except IsolationError: More than one isolation point is found
        """
        point = self.find_isolation_point( is_inside, is_outside )
        return self.cut( point.internal_node, point.external_node )
    
    
    def find_common_ancestor_paths( self, filter: DNodePredicate, direction: int = -1 ) -> List[List[_MNode_]]:
        """
        Finds the last common ancestor of the nodes predicated by the specified filter.
            
        :param filter:      Predicate over which to filter nodes for inclusion in the result set.
        :param direction:   Ancestor direction
                                -1 = against edges (the default, finds the MRCA on a rooted graph)
                                0  = root independent (finds the closest node)
                                1  = with edges
        :return: A list of lists, each list has the MRCA as the first element, and the subsequent elements
                 of that list describe the path from the MRCA to the `filter` nodes. 
        """
        data = [(x, [x], { x: None }) for x in self.nodes if filter( x )]
        all_visited = [x[2] for x in data]
        
        while True:
            graph_complete = True
            
            for node, unvisited_list, visited_set in data:
                if unvisited_list:
                    next = unvisited_list.pop()
                    graph_complete = False
                    
                    for x in next.list_nodes( direction ):
                        if x not in visited_set:
                            visited_set[x] = next
                            unvisited_list.append( x )
                
                if graph_complete:
                    raise ValueError( "The following nodes do not share a common ancestor: {}".format( [x[0] for x in data] ) )
            
            intersection = set()
            
            for i, x in enumerate( all_visited ):
                if i == 0:
                    intersection.update( x )
                else:
                    for y in tuple( intersection ):
                        if y not in x:
                            intersection.remove( y )
            
            if intersection:
                if len( intersection ) != 1:
                    raise ValueError( "The following nodes share multiple common ancestors: {} ({})".format( [x[0] for x in data], intersection ) )
                
                first = array_helper.single_or_error( intersection )
                
                paths = []
                
                for _, _, visited_set in data:
                    l = []
                    paths.append( l )
                    
                    next = first
                    
                    while next is not None:
                        l.append( next )
                        next = visited_set[next]
                
                return paths
    
    
    def find_isolation_point( self, is_inside: DNodePredicate, is_outside: DNodePredicate = None, filter: DNodePredicate = None ) -> IsolationPoint:
        """
        Convenience function that calls `find_isolation_points`, returning the resultant point or raising an error.
        
        :except IsolationError: Points are not isolated.
        """
        if filter is None:
            filter = lambda _: True
        
        if is_outside is None:
            is_outside = lambda x: not is_inside( x )
        
        points = self.find_isolation_points( is_inside, is_outside )
        
        if len( points ) != 1:
            inside_set = [x for x in self.nodes if filter( x ) and is_inside( x )]
            outside_set = [x for x in self.nodes if filter( x ) and is_outside( x )]
            msg = "Cannot extract an isolation point from the graph because the inside set ({}) is not isolated from the outside set ({})."
            raise IsolationError( msg.format( inside_set, outside_set ), inside_set, outside_set )
        
        return points[0]
    
    
    def find_isolation_points( self, is_inside: DNodePredicate, is_outside: DNodePredicate ) -> List[IsolationPoint]:
        """
        Finds the points on the graph that separate the specified `inside` nodes from the `outside` nodes.
        
              --------I
          ----X1
          |   --------I
          |
        --X2
          |
          |   --------O
          ----X3
              --------O
             
        
        Nodes (X) not in the `inside` (I) and `outside` (O) sets are can be either inside or outside the isolated subgraph, however this
        algorithm will attempt to keep as many as possible outside, so in the diagram about, the point that isolates I from O is X1. 
        
        Ideally, there will just be one point in the results list, but if the inside points are scattered, more than one point will be
        returned, e.g. X1 and X3 separate I from O:
        
              --------I
          ----X1
          |   --------I
          |
        --X2
          |           --------I
          |   --------X3
          ----X4      --------I
              |
              --------O
         
         
        :param is_outside:   A delegate expression yielding `True` for nodes outside the set to be separated, and `False` for all other nodes. 
        :param is_inside:    A delegate expression yielding `True` for nodes inside the set to be separated,  and `False` for all other nodes. 
        :return:          A list of `IsolationPoint` detailing the isolation points. 
        """
        # Iterate over all the edges to make a list of `candidate` edges
        # - those separating INSIDE from OUTSIDE
        candidates: List[IsolationPoint] = []
        
        for edge in self.get_edges():
            for node in cast( Sequence[MNode], (edge.left, edge.right) ):
                params = FollowParams( start = node, exclude_edges = [edge] )
                self.follow( params )
                outside_nodes = False
                inside_nodes = set()
                cladistic_nodes = set()
                
                # Count the number of fusion sequences in the subgraph
                for visited_node in params.visited_nodes:
                    if is_inside( visited_node ):
                        inside_nodes.add( visited_node )
                    elif is_outside( visited_node ):
                        outside_nodes = True
                        break  # we can stop
                    else:
                        cladistic_nodes.add( visited_node )
                
                if not outside_nodes:
                    candidates.append( IsolationPoint( edge, node, edge.opposite( node ), inside_nodes, cladistic_nodes ) )
        
        # Our candidates overlap, so remove the redundant ones
        drop_candidates = []
        
        for candidate_1 in candidates:
            for candidate_2 in candidates:
                if candidate_1 is candidate_2:
                    continue
                
                is_subset = candidate_1.inside_nodes.issubset( candidate_2.inside_nodes )
                
                # If the candidates encompass different sequences don't bother
                if not is_subset:
                    continue
                
                # Any candidates that are a _strict_ subset of another can be dropped
                if len( candidate_1.inside_nodes ) < len( candidate_2.inside_nodes ):
                    drop_candidates.append( candidate_1 )
                    break
                
                # Any candidates equal to another, but have a greater number of cladistic nodes, can be dropped
                if len( candidate_1.cladistic_nodes ) > len( candidate_2.cladistic_nodes ):
                    drop_candidates.append( candidate_1 )
                    break
        
        for candidate in drop_candidates:
            candidates.remove( candidate )
        
        return candidates
    
    
    def cut( self, left_node: TNodeOrUid, right_node: TNodeOrUid ) -> Tuple[_MGraph_, _MGraph_]:
        """
        This is the same as `cut_one`, but returns both the left and the right halves of the cut.
        """
        left_node = self.find_node( left_node )
        right_node = self.find_node( right_node )
        
        exception_helper.assert_type( "left_node", left_node, MNode )
        exception_helper.assert_type( "right_node", right_node, MNode )
        
        left_graph = self.cut_one( left_node, right_node )
        right_graph = self.cut_one( right_node, left_node )
        return left_graph, right_graph
    
    
    def cut_one( self, internal_node: _MNode_, external_node: _MNode_ ) -> _MGraph_:
        """
        Cuts the graph along the edge between the specified nodes, yielding a new subset graph.
        
        The new subset contains `containing_node`, and all its relations, excluding those crossing `missing_node`. 
        
        Note this function accepts two nodes, rather than an edge, so that the assignment of
        `containing_node` and `missing_node` is always explicit, which wouldn't be obvious for undirected edges. 
        
        :param internal_node:     Node that will form the inside (accepted) half of the cut 
        :param external_node:     Node that will form the outside (rejected) half of the cut. 
        :return:                  The new graph
        """
        new_graph = MGraph()
        
        params = FollowParams( start = internal_node, exclude_nodes = [external_node] )
        self.follow( params )
        
        visited_nodes = set( params.visited_nodes )
        visited_edges = set()  # use a set because every edge appears twice (TODO: fix using a directional query)
        
        for node in visited_nodes:
            node.copy_into( new_graph )
            
            for edge in node.list_edges():
                if edge.left in visited_nodes and edge.right in visited_nodes:
                    visited_edges.add( edge )  # add the edges after when all the nodes exist
        
        for edge in visited_edges:
            edge.copy_into( new_graph )
        
        return new_graph
    
    
    def find_connected_components( self ) -> List[List[_MNode_]]:
        """
        Calculates and returns the list of connected components.
        """
        cf = ComponentFinder()
        
        for edge in self.get_edges():
            cf.join( edge.left, edge.right )
        
        return cast( List[List[_MNode_]], cf.tabulate() )
    
    
    @classmethod
    def consensus( cls, graphs: Iterable[_MGraph_] ) -> _MGraph_:
        """
        Creates the consensus of two trees.
        NOTE: The graphs must be trees!
        
        :param graphs:  An iterable containing two or more graphs. 
        :return:        A new graph describing the consensus. 
        """
        raise NotImplementedError( "TODO" )
    
    
    def add_node( self, *, data: Optional[object] = None ) -> _MNode_:
        """
        Convenience function that creates a node with this graph as the owner.
        :return:     The added node 
        """
        return MNode( self, data = data )
    
    
    def add_edge( self, left: TNodeOrUid, right: TNodeOrUid ) -> _MEdge_:
        """
        Convenience function that creates an edge with this graph as the owner.
        :param left:    Left node of edge (or a TNodeOrUid allowing the left node to be found)     
        :param right:   Right node of edge (or a TNodeOrUid allowing the right node to be found) 
        :return:        Resulting edge 
        """
        return MEdge( self.find_node( left ), self.find_node( right ) )
    
    
    def copy( self ) -> _MGraph_:
        """
        Makes a deep copy of this graph.
        """
        result = MGraph()
        self.copy_into( result )
        return result
    
    
    def copy_into( self, target: _MGraph_ ) -> None:
        """
        Copies all nodes and edges from this graph into another.
        Note that node information and UIDs are copied, which prevents accidentally incorporating the same set of nodes twice.
        :param target:   The graph to incorporate this graph into.
        """
        for node in self.nodes:
            node.copy_into( target )
        
        for edge in self.get_edges():
            edge.copy_into( target )
    
    
    def find_node( self, node: TNodeOrUid, default: object = NOT_PROVIDED ) -> _MNode_:
        """
        Finds a node in this graph, to one that exists in a different graph.
         
        :param default: Default value (otherwise error) 
        :param node:    Node or UID of node to find. 
        :return:        Node in this graph. 
        """
        if isinstance( node, MNode ):
            if node._graph is self:
                return node
            else:
                uid = node.uid
        elif isinstance( node, TUid ):
            uid = node
            node = None
        else:
            raise SwitchError( "node", node, instance = True )
        
        result = self.nodes.get_by_id( uid )
        
        if result is not None:
            return result
        
        if default is not NOT_PROVIDED:
            return default
        
        raise ValueError( "Cannot find the requested node (uid = «{}», original = «{}») in this graph.".format( uid, node or "unknown" ) )
    
    
    def format_data( self, format: Callable[[object], object] ):
        for node in self.nodes:
            node.data = format( node.data )
    
    
    @classmethod
    def from_newick( cls, newick_tree: str, root_ref: ByRef[_MNode_] = None ) -> _MGraph_:
        """
        Calls `import_newick` on a new graph.
        :param newick_tree:     Tree to import 
        :param root_ref:        Reference to root node (if none the reference is not set) 
        :return:                Resulting graph 
        """
        result = cls()
        root = result.import_newick( newick_tree )
        
        if root_ref is not None:
            root_ref.value = root
        
        return result
    
    
    def import_newick( self, newick_tree: str ) -> _MNode_:
        """
        Imports a newick tree.
        Node data is set to the newick node labels.
        Requires library: `ete`.
        
        :param newick_tree:     Newick format tree (ETE format #1)
        :returns: Tree root
        """
        from ete3 import TreeNode
        tree__ = TreeNode( newick_tree, format = 1 )
        return self.import_ete( tree__ )
    
    
    def import_ete( self, ete_tree: object ) -> _MNode_:
        """
        Imports an Ete tree
        Node data is set to the ete node names.
        Requires library: `ete`.
        
        :param ete_tree:    Ete tree 
        :returns: Tree root
        """
        from ete3 import TreeNode
        assert isinstance( ete_tree, TreeNode )
        
        root = MNode( self )
        
        
        def ___recurse( m_node_start, e_node_start, depth ) -> None:
            for e_node_next in e_node_start.get_children():
                m_node_next = self._node_from_ete( e_node_next )
                
                MEdge( m_node_start, m_node_next )
                
                ___recurse( m_node_next, e_node_next, depth + 1 )
        
        
        ___recurse( root, ete_tree, 0 )
        
        return root
    
    
    def to_csv( self, get_text: DNodeToText ):
        r = []
        
        r.append( "source,target" )
        
        for edge in self.get_edges():
            r.append( "{},{}".format( get_text( edge.left ), get_text( edge.right ) ) )
        
        return "\n".join( r )
    
    
    def to_svg( self, get_text: DNodeToText, roots = None, html: bool = False ):
        from mgraph import viewer
        return viewer.to_svg( self, get_text, roots, html )
    
    
    def __find_slot( self, node: _MNode_, parent, prev_slots, slots, layer_len ):
        # No parent, pick any slot
        if parent is None:
            return len( slots ) // (layer_len + 1)
        
        # Has parent, try below them
        for i, prev_slot in enumerate( prev_slots ):
            if parent in prev_slot:
                return i
        
        raise LogicError()
    
    
    def __first_slot( self, slots, ideal ):
        for i in array_helper.iter_distance_range( 0, len( slots ), ideal ):
            if slots[i] is None:
                return i
        
        raise LogicError()
    
    
    def to_edgelist( self, get_text: DNodeToText = str, delimiter: str = ", " ):
        r = []
        
        for edge in self.get_edges():
            r.append( "{}{}{}".format( get_text( edge.left ), delimiter, get_text( edge.right ) ) )
            
        return "\n".join( r )
    
    
    def to_ascii( self, get_text: DNodeToText = str, name: str = None ):
        """
        Shows the graph as ASCII-art, which is actually in UTF8.
        """
        results: List[str] = []
        
        if name is not None:
            results.append( name )
        
        visited: Set[MNode] = set()
        
        while True:
            # Choose the proper root first, on subsequence passes pick random nodes from the isolates
            first = self.first_node
            
            if first in visited:
                first = array_helper.first_or_none( x for x in self.nodes if x not in visited )
            
            if first is None:
                break
            
            params = FollowParams( start = first, include_repeats = True )
            self.follow( params )
            visited.update( params.exclude_nodes )
            results.extend( x.describe( get_text ) for x in params.visited )
        
        return "\n".join( results )
    
    
    def to_newick( self, get_text: DNodeToText ) -> str:
        """
        Converts the graph to a Newick tree.
        """
        ete_tree = self.to_ete( get_text )
        return ete_tree.write( format = 1 )
    
    
    def count_nodes( self, predicate: DNodePredicate ) -> int:
        """
        Returns the number of matching nodes.
        """
        return sum( 1 for x in self.nodes if predicate( x ) )
    
    
    def to_ete( self, get_text: DNodeToText ) -> Any:
        """
        Converts the graph to an Ete tree.
        Requires library: `ete`.
        """
        from ete3 import TreeNode
        
        def __recurse( m_node: MNode, ete_node: TreeNode, visited: Set ):
            visited.add( m_node )
            # noinspection PyTypeChecker
            new_ete_node = ete_node.add_child( name = get_text( m_node ) )
            
            for child in m_node.list_nodes():
                if child not in visited:
                    __recurse( child, new_ete_node, visited )
            
            return ete_node
        
        
        # Choose an arbitrary starting point
        first = array_helper.first_or_error( (x for x in self.nodes if x.data is None) )  # todo: hack
        
        return __recurse( first, TreeNode(), set() )
    
    
    def _node_from_ete( self, ete_node: object ):
        """
        Imports an Ete tree into the graph.
        Requires library: `ete`.
        """
        from ete3 import TreeNode
        assert isinstance( ete_node, TreeNode )
        
        if not hasattr( ete_node, "tag_node" ):
            result = MNode( self )
            result.data = ete_node.name
            
            ete_node.tag_node = result
        
        return ete_node.tag_node
    
    
    def get_edges( self ) -> "Set[ MEdge ]":
        """
        Retrieves the set of all edges.
        """
        result = set()
        
        for node in self.nodes:
            result.update( node.list_edges() )
        
        return result
    
    
    def get_nodes( self ) -> Iterator["MNode"]:
        """
        Iterates over all the nodes.
        """
        return iter( self.nodes )
    
    
    def follow( self, *args, **kwargs ) -> FollowParams:
        """
        Follows the graph from the specified point.
        :param args:        A FollowParams or arguments to be passed to the constructor of FollowParams.
        :return:            The now populated reference to the FollowParams passed in or created. 
        """
        if len( args ) == 1 and len( kwargs ) == 0 and isinstance( args[0], FollowParams ):
            params = args[0]
        else:
            params = FollowParams( *args, **kwargs )
        
        self.__follow( params = params, parent_info = params.root_info )
        return params
    
    
    def __follow( self,
                  *,
                  params: FollowParams,
                  parent_info: DepthInfo ) -> None:
        """
        Populates the `visited` set with all connected nodes, starting from the `source` node.
        Nodes already in the visited list will not be visited again.
        
        Unlike normal path-following, e.g. Dijkstra, this does not use the visited list as the `source`,
        this allows the caller to iterate from a node to the exclusion of a specified branch(es).
        """
        parent = parent_info.node
        targets = [edge.opposite( parent ) for edge in parent.list_edges() if edge not in params.exclude_edges]
        
        if parent_info.parent_info is not None:
            targets = [node for node in targets if node is not parent_info.parent_info.node]
        
        depth_info = None
        
        for target in targets:
            if target in params.exclude_nodes:
                if not params.include_repeats:
                    continue
                
                depth_info = DepthInfo( node = target,
                                        is_repeat = True,
                                        parent_info = parent_info,
                                        is_last = False,
                                        has_children = False )
                
                params.visited.append( depth_info )
                
                continue
            
            params.exclude_nodes.add( target )
            
            depth_info = DepthInfo( node = target,
                                    parent_info = parent_info,
                                    is_last = False,
                                    is_repeat = False,
                                    has_children = False )
            
            params.visited.append( depth_info )
            
            self.__follow( params = params,
                           parent_info = depth_info )
        
        if depth_info is not None:
            parent_info.has_children = True
            depth_info.is_last = True


class MNode:
    """
    Nodes of the MGraph.
    
    :attr __uid:    UID of node
    :attr _graph:   Graph this node is contained within
    :attr _edges:   Edges on this node (in any direction)
    :attr data:     User (arbitrary) data associated with this node
    """
    
    
    def __init__( self, graph: MGraph, uid: int = None, data: object = None ):
        """
        CONSTRUCTOR 
        """
        if uid is None:
            uid = uuid4().int
        
        self.__uid: int = uid
        self._graph: MGraph = graph
        self._edges: Dict[MNode, MEdge] = { }
        self.__data: object = data
        
        if self.__uid in graph.nodes.uids:
            raise ValueError( "Attempt to add a node («{}») to the graph but a node with the same UID already exists in the graph («{}»).".format( self, graph.nodes.by_id( self.__uid ) ) )
        
        graph.nodes._register( self, self.uid, self.data )
    
    
    @property
    def data( self ):
        return self.__data
    
    
    @data.setter
    def data( self, value ):
        self._graph.nodes._register_data( self, self.__data, value )
        self.__data = value
    
    
    def add_node( self, *, data: Optional[object] = None ) -> Tuple[_MEdge_, _MNode_]:
        """
        Adds a new node, with an edge from this node to the new node. 
        :return:    Edge, Node 
        """
        new_node = self._graph.add_node( data = data )
        new_edge = self._graph.add_edge( self, new_node )
        return new_edge, new_node
    
    
    def make_root( self ):
        """
        Makes this node the root.
        (All edges expand outwards from here)
        :except ValueError: Graph is not a tree (contains cycles)
        """
        self._graph._root = self
        
        open_set = []
        closed_set = set()
        
        for edge_1 in self.list_edges():
            if edge_1 in closed_set:
                raise ValueError( "Cannot make node root because the graph is cyclic." )
            
            closed_set.add( edge_1 )
            
            if edge_1.left is not self:
                edge_1.flip()
            
            for edge_2 in edge_1.right.list_edges():
                if edge_2 is not edge_1:
                    open_set.append( edge_2 )
    
    
    def copy_into( self, target_graph: MGraph ) -> _MNode_:
        """
        Copies the node (but not the edges!)
        """
        return MNode( target_graph, self.__uid, self.data )
    
    
    @property
    def uid( self ) -> int:
        return self.__uid
    
    
    def __repr__( self ):
        return str( self.data ) if self.data is not None else ""
    
    
    def list_edges( self, direction: int = 0 ) -> "List[MEdge]":
        """
        Iterates over the edges on this node.
        
        :param direction: Direction. -1 = incoming, 1 = outgoing, 0 = both.
        """
        edges = self._edges.values()
        
        if direction < 0:
            edges = filter( lambda x: x.right is self, edges )
        elif direction > 0:
            edges = filter( lambda x: x.left is self, edges )
        
        return sorted( edges, key = lambda x: "{}-{}".format( id( x.left ), id( x.right ) ) )
    
    
    def num_edges( self ) -> int:
        """
        The number of edges on this node.
        """
        return len( self._edges )
    
    
    def remove( self ) -> None:
        """
        Removes this node from the graph.
        
        Associated edges are also removed.
        """
        while self._edges:
            for x in self._edges.values():
                x.remove()
                break
        
        self._graph.nodes._unregister( self, self.uid, self.data )
        
        if self._graph._root is self:
            self._graph._root = None
    
    
    def list_nodes( self, direction: int = 0 ) -> "List[MNode]":
        """
        Iterates the node(s) connected to this node.
        
        :param direction: Direction. -1 = incoming, 1 = outgoing, 0 = both.
        """
        return [edge.opposite( self ) for edge in self.list_edges( direction )]


class MEdge:
    def __init__( self, left: MNode, right: MNode ):
        assert isinstance( left, MNode )
        assert isinstance( right, MNode )
        
        if left._graph is not right._graph:
            raise ValueError( "Cannot create an edge between two nodes in different graphs." )
        
        if left is right:
            raise ValueError( "Cannot create an edge to the same node." )
        
        if right in left._edges or left in right._edges:
            raise ValueError( "Cannot add an edge from node to node because these nodes already share an edge." )
        
        self._graph = left._graph
        self._left = left
        self._right = right
        
        left._edges[right] = self
        right._edges[left] = self
    
    
    def flip( self ):
        """
        Flips the direction of this edge.
        """
        del self._left._edges[self._right]
        del self._right._edges[self._left]
        
        left = self._left
        self._left = self.right
        self._right = left
        
        self._left._edges[self._right] = self
        self._right._edges[self._left] = self
    
    
    def copy_into( self, target_graph: MGraph ) -> Optional[_MEdge_]:
        """
        Copies this edge into the target graph.
        
        If the same nodes do not exist in the target graph, no edge is created and the function returns `None`.
        """
        left = target_graph.find_node( self._left.uid )
        
        if left is None:
            return None
        
        right = target_graph.find_node( self._right.uid )
        
        if right is None:
            return None
        
        new_edge = MEdge( left, right )
        return new_edge
    
    
    def remove( self ) -> None:
        del self._left._edges[self._right]
        del self._right._edges[self._left]
    
    
    def __repr__( self ) -> str:
        return "{}-->{}".format( self._left, self._right )
    
    
    @property
    def left( self ) -> MNode:
        return self._left
    
    
    @property
    def right( self ) -> MNode:
        return self._right
    
    
    def opposite( self, node: MNode ) -> MNode:
        if self._left is node:
            return self._right
        elif self._right is node:
            return self._left
        else:
            raise KeyError( "Cannot find opposite side to '{}' because that isn't part of this edge '{}'.".format( node, self ) )
    
    
    def iter_a( self ) -> Set[MNode]:
        return self._graph.follow( FollowParams( start = self._left, exclude_nodes = [self._right] ) ).exclude_nodes
    
    
    def iter_b( self ) -> Set[MNode]:
        return self._graph.follow( FollowParams( start = self._right, exclude_nodes = [self._left] ) ).exclude_nodes
