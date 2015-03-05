from pyparsing import (Word, alphanums, ZeroOrMore,
                       stringEnd, Suppress, Literal, CaselessKeyword,
                       Optional, Forward, quotedString, removeQuotes)


############### CYPHER READ QUERY STRUCTURE ###############
#http://neo4j.com/docs/stable/cypher-refcard/

# [MATCH WHERE]
# [OPTIONAL MATCH WHERE]
# [WITH [ORDER BY] [SKIP] [LIMIT]]
# RETURN [ORDER BY] [SKIP] [LIMIT]


############### KWRDS ###############

match = CaselessKeyword("MATCH")
optional = CaselessKeyword("OPTIONAL")
where = CaselessKeyword("WHERE")
order_by = CaselessKeyword("ORDER BY")
skip = CaselessKeyword("SKIP")
limit = CaselessKeyword("LIMIT")
with_kwrd = CaselessKeyword("WITH")
as_kwrd = CaselessKeyword("AS")
and_kwrd = CaselessKeyword("AND")
or_kwrd = CaselessKeyword("OR")
not_kwrd = CaselessKeyword("NOT")
return_kwrd = CaselessKeyword("RETURN")
distinct = CaselessKeyword("DISTINCT")
# ...there are a bunch of functions and reserved kwds to add.


############### KWRD Groups ###############
and_not = and_kwrd + not_kwrd
or_not = or_kwrd + not_kwrd
where_opts = and_not | or_not | and_kwrd | or_kwrd | not_kwrd


############### Generics ###############

# Some basic symbols.
var = Word(alphanums, "_" + alphanums)
equals = Literal("=")  # Need other operators for where.
comma = Literal(",")
period = Literal(".")

# Build node/edge alias and label.
seperator = Literal(":")
label = seperator + var
alias_label = var + Optional(label) | label

# Left and right side of property operations.
left = var +  Optional(period + var)
right = left | quotedString

# Parse property dict style syntax.
keyval = left + seperator + right

# Comma seperated recursive pattern for property.
keyval_csv_pattern = Forward()
keyval_csv_pattern << keyval + ZeroOrMore(comma + keyval_csv_pattern)

# Parse getter style syntax.
gettr = left + equals + right

# Comma seperated recursive pattern for WHERE style syntax
gettr_csv_pattern = Forward()
gettr_csv_pattern << gettr + ZeroOrMore(where_opts + gettr_csv_pattern)

# Map style properties for nodes/edges.
prop_open = Literal("{")
prop_close = Literal("}")
props = prop_open + keyval_csv_pattern + prop_close


############### Nodes ###############

node_open = Literal("(")
node_close = Literal(")")
node = node_open + Optional(alias_label) + Optional(props)+ node_close


############### Edges ###############

edge = Literal("-")
out_marker = Literal(">")
in_marker = Literal("<")
edge_open = Literal("[")
edge_close = Literal("]")
edge_meta = edge_open + Optional(alias_label) + Optional(props)+ edge_close
undir_edge = edge + Optional(edge_meta) + edge
out_edge = undir_edge + out_marker
in_edge = in_marker + undir_edge
edge = (out_edge | in_edge | undir_edge)


############### Traversal pattern ###############

traversal_pattern = Forward()
traversal_pattern << node + ZeroOrMore(edge + traversal_pattern)


############### STATEMENTS ###############

match_stmt = Optional(optional) + match + traversal_pattern
where_stmt = where + gettr_csv_pattern
