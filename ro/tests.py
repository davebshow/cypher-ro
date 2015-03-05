import unittest
from pyparsing import ParseException, stringEnd
from grammar import (node, edge_meta, undir_edge, edge, traversal_pattern,
    match_stmt, where_stmt, count_fn, sum_fn, disc_per_fn, std_dev_fn)



class CypherRO(unittest.TestCase):

    def setUp(self):
        # Traversal pattern matches recursively with ZeroOrMore, therefore
        # we need string end to test in an isolated environment.
        self.match_stmt = match_stmt + stringEnd
        self.where_stmt = where_stmt + stringEnd

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

        bad_out_meta2 = "-:KNOWS]->"
        try:
            edge.parseString(bad_out_meta2)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_match(self):
        match_stmt = self.match_stmt
        one_node = "MATCH (n:Node)"
        try:
            match_stmt.parseString(one_node)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        labels = "OPTIONAL MATCH (n:Person)--(m:Place)"
        try:
            match_stmt.parseString(labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_labels = "MATCH (n:Person)-[:BORN_IN]-(m:Place)"
        try:
            match_stmt.parseString(full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        long_full_labels = "OPTIONAL MATCH (n:Person)-[:BORN_IN]-(m:Place)-[:LIVED_IN]-(m:Person)"
        try:
            match_stmt.parseString(long_full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        long_full_labels_dir = "MATCH (n:Person)-[:BORN_IN]->(m:Place)<-[:LIVED_IN]-(m:Person)"
        try:
            match_stmt.parseString(long_full_labels_dir)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_labels_out = "OPTIONAL MATCH (n:Person)-[:BORN_IN]->(m:Place)"
        try:
            match_stmt.parseString(full_labels_out)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_labels_in = "MATCH (n:Person)<-[:BORN_IN]-(m:Place)"
        try:
            match_stmt.parseString(full_labels_in)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        full_attrs = "OPTIONAL MATCH (n:Person {name: 'Dave'})-[k:LIVED_IN]-(m:Place {name: 'Iowa City'})"
        try:
            match_stmt.parseString(full_attrs)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "MATCH (n:Node)---(m)"
        try:
            match_stmt.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_one_node = "OPTIONAL MATCH(n:Node"
        try:
            match_stmt.parseString(bad_one_node)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_labels = "MATCH (n:Person--(m:Place)"
        try:
            match_stmt.parseString(bad_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_labels = "OPTIONAL MATCH (n:Person)-:BORN_IN]-(m:Place)"
        try:
            match_stmt.parseString(bad_full_labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_labels_out = "MATCH (n:Person)<-[:BORN_IN]->(m:Place)"
        try:
            match_stmt.parseString(bad_full_labels_out)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_full_labels_in = "OPTIONAL MATCH (n:Person)<[:BORN_IN]-(m:Place)"
        try:
            match_stmt.parseString(bad_full_labels_in)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_kwrd = "MATC (n:Person)-[:BORN_IN]->(m:Place)<-[:LIVED_IN]-(m:Person)"
        try:
            match_stmt.parseString(bad_kwrd)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_opt_kwrd = "OPTIONA MATCH (n:Person)-[:BORN_IN]->(m:Place)<-[:LIVED_IN]-(m:Person)"
        try:
            match_stmt.parseString(bad_opt_kwrd)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_where(self):
        where_stmt = self.where_stmt
        simple = "WHERE n.name = 'David'"
        try:
            where_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_and = "WHERE n.name = 'David' AND n.age=34"
        try:
            where_stmt.parseString(where_and)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_or = "WHERE n.name = 'David' OR n.age=34"
        try:
            where_stmt.parseString(where_or)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_and_not = "WHERE n.name = 'David' AND NOT n.age=34"
        try:
            where_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_or_not = "WHERE n.name = 'David' OR NOT n.age=34"
        try:
            where_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "WHER n.name = 'David'"
        try:
            where_stmt.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_op = "WHERE n.name  'David'"
        try:
            where_stmt.parseString(bad_op)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_quote = "WHERE n.name = David'"
        try:
            where_stmt.parseString(bad_quote)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_op = "WHERE n.name = 'David' OR AND n.age=10"
        try:
            where_stmt.parseString(bad_op)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_count(self):
        simple = "count(*)"
        try:
            count_fn.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        alias = "count(n)"
        try:
            count_fn.parseString(alias)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        distinct = "count(DISTINCT n)"
        try:
            count_fn.parseString(distinct)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        distinct_prop = "count(DISTINCT n.name)"
        try:
            count_fn.parseString(distinct_prop)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        prop = "count(n.name)"
        try:
            count_fn.parseString(prop)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "coun(name)"
        try:
            count_fn.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_lparen = "count name)"
        try:
            count_fn.parseString(bad_lparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_rparen = "count(name"
        try:
            count_fn.parseString(bad_rparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_quotes = "count('name')"
        try:
            count_fn.parseString(bad_quotes)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_sum(self):
        simple = "sum(n.name)"
        try:
            sum_fn.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "su(n.name)"
        try:
            sum_fn.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_lparen = "sum n.name)"
        try:
            sum_fn.parseString(bad_lparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_rparen = "sum(n.name"
        try:
            sum_fn.parseString(bad_rparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_quotes = "sum('n.name')"
        try:
            sum_fn.parseString(bad_quotes)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_discret_percentile(self):
        simple = "percentileDisc(n.name, 0.5)"
        try:
            disc_per_fn.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "percentilDisc(n.name, 0.5)"
        try:
            disc_per_fn.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_lparen = "percentileDisc n.name, 0.5)"
        try:
            disc_per_fn.parseString(bad_lparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_rparen = "percentileDisc(n.name, 0.5"
        try:
            disc_per_fn.parseString(bad_rparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_quotes = "percentileDisc(n.name, '0.5')"
        try:
            disc_per_fn.parseString(bad_quotes)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        missing_first = "percentileDisc('0.5')"
        try:
            disc_per_fn.parseString(missing_first)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        missing_second = "percentileDisc(n.name)"
        try:
            disc_per_fn.parseString(missing_second)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        missing_comma = "percentileDisc(n.name 0.5)"
        try:
            disc_per_fn.parseString(missing_comma)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)


    def test_std_dev(self):
        simple = "stdev(n.name)"
        try:
            std_dev_fn.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "stde(n.name)"
        try:
            std_dev_fn.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_lparen = "stdev n.name)"
        try:
            std_dev_fn.parseString(bad_lparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_rparen = "stdev(n.name"
        try:
            std_dev_fn.parseString(bad_rparen)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_quotes = "stdev('n.name')"
        try:
            std_dev_fn.parseString(bad_quotes)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)


if __name__ == "__main__":
    unittest.main()
