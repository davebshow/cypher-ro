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
with_kwd = CaselessKeyword("WITH")
as_kwd = CaselessKeyword("AS")
and_kwd = CaselessKeyword("AND")
or_kwd = CaselessKeyword("OR")
return_kwd = CaselessKeyword("RETURN")
distinct = CaselessKeyword("DISTINCT")
# ...there are a bunch of functions and reserved kwds to add.


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

# Parse gettr/settr syntax.
left = var +  Optional(period + var)
right = left | quotedString
gettr = left + seperator + right

# Comma seperated recursive pattern for gettr/settr.
csv_pattern = Forward()
csv_pattern << gettr + ZeroOrMore(comma + csv_pattern)

# Map style properties for nodes/edges.
attr_open = Literal("{")
attr_close = Literal("}")
props = attr_open + csv_pattern + attr_close


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


############### (OPTIONAL) MATCH STATEMENT ###############

match_stmt = Optional(optional) + match + traversal_pattern
