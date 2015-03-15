import unittest
from pyparsing import ParseException, stringEnd
from grammar import (node, edge_content, undir_edge, edge, traversal_pattern,
    match_stmt, where_stmt, count_fn, sum_fn, disc_per_fn, std_dev_fn,
    with_stmt, order_stmt, limit_stmt, skip_stmt, return_stmt)



class CypherRO(unittest.TestCase):

    def setUp(self):
        # Traversal pattern matches recursively with ZeroOrMore, therefore
        # we need string end to test in an isolated environment.
        self.edge_content = edge_content + stringEnd
        self.match_stmt = match_stmt + stringEnd
        self.where_stmt = where_stmt + stringEnd
        self.with_stmt = with_stmt + stringEnd
        self.order_stmt = order_stmt + stringEnd
        self.limit_stmt = limit_stmt + stringEnd
        self.skip_stmt = skip_stmt + stringEnd
        self.return_stmt = return_stmt + stringEnd

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

        multi_label = "(p:Person:Place)"
        try:
            node.parseString(multi_label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_multi_label = "(:Person:Place)"
        try:
            node.parseString(simple_multi_label)
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

        multi_label_props = "(p:Person:Place {name: 'dave'})"
        try:
            node.parseString(multi_label_props)
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

        bad_multi_label = "(p:Person Place)"
        try:
            node.parseString(bad_multi_label)
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
        edge_content = self.edge_content
        empty = "[]"
        try:
            edge_content.parseString(empty)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        alias = "[k]"
        try:
            edge_content.parseString(alias)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        label = "[k:KNOWS]"
        try:
            edge_content.parseString(label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        card = "[*]"
        try:
            edge_content.parseString(label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        label_card = "[k:KNOWS*1..5]"
        try:
            edge_content.parseString(label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multi_label = "[k:KNOWS:WORKS_WITH]"
        try:
            edge_content.parseString(multi_label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_multi_label = "[:KNOWS:WORKS_WITH]"
        try:
            edge_content.parseString(simple_multi_label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        props = "[k {from: 'school'}]"
        try:
            edge_content.parseString(props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_multi_label_props = "[:KNOWS:WORKS_WITH {how_long: 10}]"
        try:
            edge_content.parseString(simple_multi_label_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multi_props = "[k {from: 'school', how_long: 10}]"
        try:
            edge_content.parseString(multi_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        label_props = "[k:KNOWS {from: 'school', how_long: 10}]"
        try:
            edge_content.parseString(label_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        # Illegal edge meta
        bad_alias = "[k"
        try:
            edge_content.parseString(bad_alias)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_multi_label = "[:KNOWS WORKS_WITH]"
        try:
            edge_content.parseString(bad_simple_multi_label)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_props = "[k {from: 'school }]"
        try:
            edge_content.parseString(bad_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multi_props = "[k {from: 'school' how_long: 10}]"
        try:
            edge_content.parseString(bad_multi_props)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_label_props = "[k:KNOWS {from: 'school', how_long: 10]"
        try:
            edge_content.parseString(bad_label_props)
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

        multiple = "MATCH (n:Person)-[:LIVED_IN]-(m:Place), (j:Job)"
        try:
            match_stmt.parseString(labels)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        match_path = "MATCH path = (n)-->(m)"
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

        bad_multiple = "MATCH (n:Person)-[:LIVED_IN]-(m:Place) (j:Job)"
        try:
            match_stmt.parseString(bad_multiple)
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

        where_path = "WHERE n.name = 'David' AND (n)-->(m)"
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
            where_stmt.parseString(where_and_not)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_or_not = "WHERE n.name = 'David' OR NOT n.age=34"
        try:
            where_stmt.parseString(where_or_not)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_or_not = "WHERE n:Name"
        try:
            where_stmt.parseString(where_or_not)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_coll = "WHERE n.name IN ['david', 'javi']"
        try:
            where_stmt.parseString(where_coll)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_or_not = "WHERE has (n.name)"
        try:
            where_stmt.parseString(where_or_not)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_not = "WHERE NOT (persons)-->(peter)"
        try:
            where_stmt.parseString(where_not)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_reg = "WHERE n.name =~ 'asdf'"
        try:
            where_stmt.parseString(where_reg)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_type = "WHERE type(r) = 'person'"
        try:
            where_stmt.parseString(where_type)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        where_isnull = "WHERE n.prop IS NULL"
        try:
            where_stmt.parseString(where_isnull)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multi_where = "WHERE n.name = 'Peter' OR (n.age < 30 AND n.name = 'Tobias') OR NOT (n.name = 'Tobias' OR n.name='Peter')"
        try:
            where_stmt.parseString(multi_where)
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

        bad_where_or_not = "WHERE has n.name)"
        try:
            where_stmt.parseString(bad_where_or_not)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_where_reg = "WHERE n.name =~ 30"
        try:
            where_stmt.parseString(bad_where_reg)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_where_isnull = "WHERE IS NULL"
        try:
            where_stmt.parseString(bad_where_isnull)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_where_path = "WHERE n.name = 'David' AND (n)->(m)"
        try:
            where_stmt.parseString(bad_where_path)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multi_where = "WHERE n.name = 'Peter' (OR n.age < 30 AND n.name = 'Tobias') OR NOT (n.name = 'Tobias' OR n.name='Peter')"
        try:
            where_stmt.parseString(bad_multi_where)
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


    def test_with(self):
        with_stmt = self.with_stmt
        simple = "WITH n"
        try:
            with_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_patt = "WITH n, m"
        try:
            with_stmt.parseString(simple_patt)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_as = "WITH n AS Something"
        try:
            with_stmt.parseString(simple_as)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_mix = "WITH n AS Something, c"
        try:
            with_stmt.parseString(simple_mix)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        two_as = "WITH n AS Something, c AS Col"
        try:
            with_stmt.parseString(two_as)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        gettrs = "WITH n.name AS Something, c.some AS Col"
        try:
            with_stmt.parseString(gettrs)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        tp = "WITH type(n) AS Type"
        try:
            with_stmt.parseString(tp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        count = "WITH count(n) AS Num"
        try:
            with_stmt.parseString(count)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "WITHn"
        try:
            with_stmt.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_patt = "WITH n m"
        try:
            with_stmt.parseString(bad_simple_patt)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_as = "WITH AS Something"
        try:
            with_stmt.parseString(bad_simple_as)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_mix = "WITH n AS Something c"
        try:
            with_stmt.parseString(bad_simple_mix)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_two_as = "WITH n AS Something, c Col"
        try:
            with_stmt.parseString(bad_two_as)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_tp = "WITH type(n) Type"
        try:
            with_stmt.parseString(bad_tp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        count = "WITH count(n AS Num"
        try:
            with_stmt.parseString(count)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_orderby(self):
        order_stmt = self.order_stmt
        simple = "ORDER BY n"
        try:
            order_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_asc = "ORDER BY n ASC"
        try:
            order_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_desc = "ORDER BY n DESC"
        try:
            order_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multiple_simple = "ORDER BY n, m "
        try:
            order_stmt.parseString(multiple_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multiple_simple_asc_desc = "ORDER BY n ASC, m DESC"
        try:
            order_stmt.parseString(multiple_simple_asc_desc)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_attr = "ORDER BY n.name"
        try:
            order_stmt.parseString(simple_attr)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_asc_attr = "ORDER BY n.name ASC"
        try:
            order_stmt.parseString(simple_asc_attr)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_desc_attr = "ORDER BY n.name DESC"
        try:
            order_stmt.parseString(simple_desc_attr)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multiple_attr = "ORDER BY n.name, m.name "
        try:
            order_stmt.parseString(multiple_attr)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multiple_attr_asc_desc = "ORDER BY n.name asc, m.name desc"
        try:
            order_stmt.parseString(multiple_attr_asc_desc)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_multiple_attr = "ORDER BY n.name m.name "
        try:
            order_stmt.parseString(bad_multiple_attr)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multiple_attr_asc_desc = "ORDER BY n.name asc m.name desc"
        try:
            order_stmt.parseString(bad_multiple_attr_asc_desc)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple = "ORDER B n"
        try:
            order_stmt.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_limit(self):
        limit_stmt = self.limit_stmt
        simple = "LIMIT 3"
        try:
            limit_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "LIMIT '3'"
        try:
            limit_stmt.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multiple = "LIMIT 3,4"
        try:
            limit_stmt.parseString(bad_multiple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_skip(self):
        skip_stmt = self.skip_stmt
        simple = "SKIP 3"
        try:
            skip_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "SKIP '3'"
        try:
            skip_stmt.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multiple = "SKIP 3,4"
        try:
            skip_stmt.parseString(bad_multiple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

    def test_return(self):
        return_stmt = self.return_stmt
        simple = "RETURN n"
        try:
            return_stmt.parseString(simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_literal = "RETURN 'yolo'"
        try:
            return_stmt.parseString(simple_literal)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_pattern = "RETURN (m)-->(n)"
        try:
            return_stmt.parseString(simple_pattern)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_comp = "RETURN n > 30"
        try:
            return_stmt.parseString(simple_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_as = "RETURN n as Name"
        try:
            return_stmt.parseString(simple_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        simple_attr_as = "RETURN n.name as Name"
        try:
            return_stmt.parseString(simple_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        compound_comp = "RETURN n > 30 and m ='dave'"
        try:
            return_stmt.parseString(compound_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        multi_compound_comp = "RETURN (n > 30 and m ='dave') or not m > 10"
        try:
            return_stmt.parseString(multi_compound_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        long_return = "RETURN (n>30 AND m='dave') OR NOT g<100, (m)-->(n), 30, 5.5, 'literal', m, n.name AS Name"
        try:
            parsed = return_stmt.parseString(long_return)
            accepted = True
            q = ''.join(parsed.asList())
            self.assertEqual(q, long_return)
        except ParseException:
            accepted = False
        self.assertTrue(accepted)

        bad_simple = "RETUR n"
        try:
            return_stmt.parseString(bad_simple)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_literal = "RETURN yolo'"
        try:
            return_stmt.parseString(bad_simple_literal)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_pattern = "RETURN m)-->(n)"
        try:
            return_stmt.parseString(bad_simple_pattern)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_comp = "RETURN n  30"
        try:
            return_stmt.parseString(bad_simple_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_as = "RETURN n Name"
        try:
            return_stmt.parseString(bad_simple_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_simple_attr_as = "RETURN n.name as "
        try:
            return_stmt.parseString(bad_simple_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_compound_comp = "RETURN n > 30 m ='dave'"
        try:
            return_stmt.parseString(bad_compound_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_multi_compound_comp = "RETURN (n > 30 and m ='dave') or not > 10"
        try:
            return_stmt.parseString(bad_multi_compound_comp)
            accepted = True
        except ParseException:
            accepted = False
        self.assertFalse(accepted)

        bad_long_return = "RETURN (n>30 AND m='dave') OR NOT g<100 (m)-->(n), 30, 5.5, 'literal', m, n.name AS Name"
        try:
            parsed = return_stmt.parseString(bad_long_return)
            accepted = True
            q = ''.join(parsed.asList())
            self.assertEqual(q, long_return)
        except ParseException:
            accepted = False
        self.assertFalse(accepted)


if __name__ == "__main__":
    unittest.main()
