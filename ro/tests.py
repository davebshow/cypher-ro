import unittest
from pyparsing import ParseException, stringEnd
from grammar import (node, edge_meta, undir_edge, edge, traversal_pattern,
    match_stmt)



class CypherRO(unittest.TestCase):

    def setUp(self):
        # Traversal pattern matches recursively with ZeroOrMore, therefore
        # we need string end to test in an isolated environment.
        self.traversal_pattern = traversal_pattern + stringEnd
        self.match_stmt = match_stmt + stringEnd

    def test_node(self):
        # Legal nodes
        empty = "()"
        try:
            node.parseString(empty)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        alias = "(p)"
        try:
            node.parseString(alias)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        label = "(p:Person)"
        try:
            node.parseString(label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        props = "(p {name: 'dave'})"
        try:
            node.parseString(props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multi_props = "(p {name: 'dave', age: 34})"
        try:
            node.parseString(multi_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        label_props = "(p:Person {name: 'dave', age: 34})"
        try:
            node.parseString(label_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        # Illegal nodes
        bad_alias = "(p"
        try:
            node.parseString(bad_alias)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_props = "(p {name: 'dave })"
        try:
            node.parseString(bad_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multi_props = "(p {name: 'dave' age: 34})"
        try:
            node.parseString(bad_multi_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_label_props = "(p:Person {name: 'dave', age: 34)"
        try:
            node.parseString(bad_label_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_edge_meta(self):
        # Legal edge meta
        empty = "[]"
        try:
            edge_meta.parseString(empty)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        alias = "[k]"
        try:
            edge_meta.parseString(alias)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        label = "[k:KNOWS]"
        try:
            edge_meta.parseString(label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        props = "[k {from: 'school'}]"
        try:
            edge_meta.parseString(props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multi_props = "[k {from: 'school', how_long: 10}]"
        try:
            edge_meta.parseString(multi_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        label_props = "[k:KNOWS {from: 'school', how_long: 10}]"
        try:
            edge_meta.parseString(label_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        # Illegal edge meta
        bad_alias = "[k"
        try:
            edge_meta.parseString(bad_alias)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_props = "[k {from: 'school }]"
        try:
            edge_meta.parseString(bad_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multi_props = "[k {from: 'school' how_long: 10}]"
        try:
            edge_meta.parseString(bad_multi_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_label_props = "[k:KNOWS {from: 'school', how_long: 10]"
        try:
            edge_meta.parseString(bad_label_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_undir_edge(self):
        simple = "--"
        try:
            undir_edge.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_meta = "-[:KNOWS]-"
        try:
            undir_edge.parseString(simple_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple_meta = "[:KNOWS]-"
        try:
            undir_edge.parseString(bad_simple_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_out_meta = "-:KNOWS]-"
        try:
            undir_edge.parseString(bad_out_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_edge(self):
        simple = "--"
        try:
            edge.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        out_edge = "-->"
        try:
            edge.parseString(out_edge)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        in_edge = "<--"
        try:
            edge.parseString(in_edge)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_meta = "-[:KNOWS]-"
        try:
            edge.parseString(simple_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        out_meta = "-[:KNOWS]->"
        try:
            edge.parseString(out_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        in_meta = "<-[:KNOWS]-"
        try:
            edge.parseString(in_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_out_edge = "->"
        try:
            edge.parseString(bad_out_edge)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_in_edge = "<-"
        try:
            edge.parseString(bad_in_edge)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_meta = "[:KNOWS]-"
        try:
            edge.parseString(bad_simple_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_out_meta = "-[:KNOWS]>"
        try:
            edge.parseString(bad_out_meta)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_out_meta2 = "-:KNOWS]-"
        try:
            edge.parseString(bad_out_meta2)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_traversal(self):
        traversal_pattern = self.traversal_pattern
        one_node = "(n:Node)"
        try:
            traversal_pattern.parseString(one_node)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple = "(n)--(m)"
        try:
            traversal_pattern.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        labels = "(n:Person)--(m:Place)"
        try:
            traversal_pattern.parseString(labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_labels = "(n:Person)-[:BORN_IN]-(m:Place)"
        try:
            traversal_pattern.parseString(full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        long_full_labels = "(n:Person)-[:BORN_IN]-(m:Place)-[:LIVED_IN]-(m:Person)"
        try:
            traversal_pattern.parseString(long_full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        long_full_labels_dir = "(n:Person)-[:BORN_IN]->(m:Place)<-[:LIVED_IN]-(m:Person)"
        try:
            traversal_pattern.parseString(long_full_labels_dir)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_labels_out = "(n:Person)-[:BORN_IN]->(m:Place)"
        try:
            traversal_pattern.parseString(full_labels_out)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_labels_in = "(n:Person)<-[:BORN_IN]-(m:Place)"
        try:
            traversal_pattern.parseString(full_labels_in)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        attrs = "(n:Person {name: 'Dave'})-[k:BORN_IN]-(m:Place)"
        try:
            traversal_pattern.parseString(attrs)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_attrs = "(n:Person {name: 'Dave'})-[k:LIVED_IN]-(m:Place {name: 'Iowa City'})"
        try:
            traversal_pattern.parseString(full_attrs)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "(n:Node)---(m)"
        try:
            traversal_pattern.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_one_node = "(n:Node"
        try:
            traversal_pattern.parseString(bad_one_node)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_labels = "(n:Person--(m:Place)"
        try:
            traversal_pattern.parseString(bad_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_labels = "(n:Person)-:BORN_IN]-(m:Place)"
        try:
            traversal_pattern.parseString(bad_full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_labels_out = "(n:Person)<-[:BORN_IN]->(m:Place)"
        try:
            traversal_pattern.parseString(bad_full_labels_out)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_labels_in = "(n:Person)<[:BORN_IN]-(m:Place)"
        try:
            traversal_pattern.parseString(bad_full_labels_in)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_attrs = "(n:Person {name: 'Dave')-[k:BORN_IN]-(m:Place)"
        try:
            traversal_pattern.parseString(bad_attrs)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_attrs = "(n:Person {name: Dave'})-[k:LIVED_IN]-(m:Place {name: 'Iowa City'})"
        try:
            traversal_pattern.parseString(bad_full_attrs)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_match_statement(self):
        match = self.match_stmt
        one_node = "MATCH (n:Node)"
        try:
            match.parseString(one_node)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple = "MATCH (n)--(m)"
        try:
            match.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        labels = "MATCH (n:Person)--(m:Place)"
        try:
            match.parseString(labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_labels = "OPTIONAL MATCH (n:Person)-[:BORN_IN]-(m:Place)"
        try:
            match.parseString(full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        long_full_labels = "MATCH (n:Person)-[:BORN_IN]-(m:Place)-[:LIVED_IN]-(m:Person)"
        try:
            match.parseString(long_full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        long_full_labels_dir = "MATCH (n:Person)-[:BORN_IN]->(m:Place)<-[:LIVED_IN]-(m:Person)"
        try:
            match.parseString(long_full_labels_dir)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_attrs = "MATCH (n:Person {name: 'Dave'})-[k:LIVED_IN]-(m:Place {name: 'Iowa City'})"
        try:
            match.parseString(full_attrs)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_one_node = "MATC (n:Node)"
        try:
            match.parseString(bad_one_node)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_labels = "MATCH ugly (n:Person)--(m:Place)"
        try:
            match.parseString(bad_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_labels = "MATCH (n:Person)-[:BORN_IN]-(m:Place) to much"
        try:
            match.parseString(bad_full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)


if __name__ == "__main__":
    unittest.main()
