import unittest

from mgraph import MGraph


__id = 0


def _next_id():
    global __id
    __id += 1
    return __id


class MyTestCase( unittest.TestCase ):
    def test_mgraph( self ):
        g: MGraph = MGraph.from_newick( "(((A,B),C),(D,(E,(F,G))));" )
        g.format_data( lambda x: x if x else _next_id() )
        
        g.nodes.by_data( 1 ).make_root()
        
        print( g.to_ascii() )
        
        mrca = g.find_common_ancestor_paths( lambda x: x.data in ("E", "F", "G") )
        
        print(mrca)


if __name__ == '__main__':
    unittest.main()
