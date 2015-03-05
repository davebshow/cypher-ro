from pyparsing import (Word, alphanums, ZeroOrMore, nums,
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
where_opts = (and_not | or_not | and_kwrd | or_kwrd | not_kwrd)

############### Generics ###############

# Some basic symbols.
var = Word(alphanums, "_" + alphanums)
period = Literal(".")
integer = Word(nums)
flt = integer + period + integer
comma = Literal(",")
paren_open = Literal("(")
paren_close = Literal(")")

# Operators
equals = Literal("=")
gt = Literal(">")
geq = Literal(">=")
lt = Literal("<")
leq = Literal("<=")
neq = Literal("<>")

comparison_operators = (equals | geq | leq | gt | lt | neq)

# Build node/edge alias and label.
seperator = Literal(":")
label = seperator + var
alias_label = var + Optional(label) | label

# Left and right side of property operations.
gettr = var + period + var
right = gettr | quotedString | integer

# Parse property dict style syntax.
keyval = var + seperator + right

# Comma seperated recursive pattern for property.
keyval_csv_pattern = Forward()
keyval_csv_pattern << keyval + ZeroOrMore(comma + keyval_csv_pattern)

# Parse comparison style syntax.
comparison = gettr + comparison_operators + right

# Comma seperated recursive pattern for WHERE style syntax
comparison_csv_pattern = Forward()
comparison_csv_pattern << comparison + ZeroOrMore(where_opts + comparison_csv_pattern)

# Map style properties for nodes/edges.
prop_open = Literal("{")
prop_close = Literal("}")
props = prop_open + keyval_csv_pattern + prop_close


############### Nodes ###############

node = paren_open + Optional(alias_label) + Optional(props)+ paren_close


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


############### MATCH/WHERE STATEMENTS ###############

match_stmt = Optional(optional) + match + traversal_pattern
where_stmt = where + comparison_csv_pattern


############### Aggregation ###############

count = CaselessKeyword("count")
sum = CaselessKeyword("sum")
disc_per = CaselessKeyword("percentileDisc")
standard_dev = CaselessKeyword("stdev")

# Count function
astrx = Literal("*")
dist_iden = (distinct + gettr) | (distinct + var)
count_opts = dist_iden | gettr | var | astrx
count_fn = count + paren_open + count_opts + paren_close

# Sum function
sum_fn = sum + paren_open + gettr + paren_close

# Discrete percentile function
disc_per_fn = disc_per + paren_open + gettr + comma + flt + paren_close

# Standard deviation function
std_dev_fn = standard_dev + paren_open + gettr + paren_close

# Aggregates
aggr_fn = (count_fn | sum_fn | disc_per_fn | std_dev_fn)
