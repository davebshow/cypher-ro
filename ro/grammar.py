from pyparsing import (Word, alphanums, ZeroOrMore, nums, stringEnd, Literal,
    CaselessKeyword, Optional, Forward, quotedString, White)


############### CYPHER READ QUERY STRUCTURE ###############
#http://neo4j.com/docs/stable/cypher-refcard/

# [MATCH WHERE]
# [OPTIONAL MATCH WHERE]
# [WITH [ORDER BY] [SKIP] [LIMIT]]
# RETURN [ORDER BY] [SKIP] [LIMIT]


############### KWRDS ###############

match = CaselessKeyword("MATCH") + White()
optional = CaselessKeyword("OPTIONAL") + White()
where = CaselessKeyword("WHERE") + White()
order_by = CaselessKeyword("ORDER BY") + White()
skip = CaselessKeyword("SKIP") + White()
limit = CaselessKeyword("LIMIT") + White()
with_kwrd = CaselessKeyword("WITH") + White()
as_kwrd = CaselessKeyword("AS") + White()
and_kwrd = CaselessKeyword("AND") + White()
or_kwrd = CaselessKeyword("OR") + White()
not_kwrd = CaselessKeyword("NOT") + White()
return_kwrd = CaselessKeyword("RETURN") + White()
distinct = CaselessKeyword("DISTINCT") + White()
has = CaselessKeyword("HAS") + White()
in_kwrd = CaselessKeyword("IN") + White()
is_kwrd = CaselessKeyword("IS") + White()
null = CaselessKeyword("NULL") + Optional(White())
# ...there are a bunch of functions and reserved kwds to add.

type_func = CaselessKeyword("type")


############### KWRD Groups ###############

and_not = and_kwrd + not_kwrd
or_not = or_kwrd + not_kwrd
where_opts = (and_not | or_not | and_kwrd | or_kwrd | not_kwrd)


############### Generics ###############

# Some basic symbols.
var = Word(alphanums, "_" + alphanums)
integer = Word(nums)
flt = integer + "." + integer

# Operators
equals = Literal("=")
gt = Literal(">")
geq = Literal(">=")
lt = Literal("<")
leq = Literal("<=")
neq = Literal("<>")
reg = Literal("=~")

# Maybe pull the regex out of here later, we'll see.
comparison_operators = (equals | geq | leq | gt | lt | neq)

# Left and right side of property operations.
gettr = var + "." + var
right = gettr | quotedString | integer


############### Aggregation ###############

# Kwrds
count = CaselessKeyword("count")
sum = CaselessKeyword("sum")
disc_per = CaselessKeyword("percentileDisc")
standard_dev = CaselessKeyword("stdev")

# Count function
dist_iden = (distinct + gettr) | (distinct + var)
count_opts = dist_iden | gettr | var | "*"
count_fn = count + "(" + count_opts + ")"

# Sum function
sum_fn = sum + "(" + gettr + ")"

# Discrete percentile function
disc_per_fn = disc_per + "(" + gettr + "," + flt + ")"

# Standard deviation function
std_dev_fn = standard_dev + "(" + gettr + ")"

# Aggregates
aggr_fn = (count_fn | sum_fn | disc_per_fn | std_dev_fn)


############### Collections ###############

lst = "[" + right + ZeroOrMore("," + Optional(White()) + right) + "]"


############### Nodes/Edges ###############

# Labels for nodes/edges
label = ":" + var + Optional(White())
alias_label = var + ZeroOrMore(label) | ZeroOrMore(label)

# Parse property prop_map style syntax.
keyval = var + ":" + Optional(White()) + right

# Comma seperated recursive pattern for property.
keyval_csv_pattern = Forward()
keyval_csv_pattern << keyval + ZeroOrMore("," + Optional(White()) +
    keyval_csv_pattern)

# Property map
prop_map = "{" + keyval_csv_pattern + "}"

# Nodes
node = "(" + Optional(alias_label) + Optional(prop_map) + ")"

# Edges
edge_meta = "[" + Optional(alias_label) + Optional(prop_map)+ "]"
undir_edge = "-" + Optional(edge_meta) + "-"
out_edge = undir_edge + ">"
in_edge = "<" + undir_edge
edge = (out_edge | in_edge | undir_edge)


############### Traversal pattern ###############

traversal_pattern = Forward()
traversal_pattern << node + ZeroOrMore(edge + traversal_pattern)

traversal_csv_pattern = Forward()
traversal_csv_pattern << traversal_pattern + ZeroOrMore("," +
    traversal_csv_pattern)

############### WHERE pattern ###############

# This is pretty permissive, but fine for our purposes. For now anyway, can
# make stricter if necessary
has_comp = has + "(" + gettr + ")"
full_left = gettr | type_func + "(" + var + ")" | var

# operator + right combos
simple_comp = comparison_operators + right
in_comp = in_kwrd + lst
isnull_comp = is_kwrd + null
reg_comp = reg + quotedString
op_right = isnull_comp | simple_comp | in_comp | reg_comp

comp = (has_comp | full_left + op_right | traversal_pattern |
    alias_label)

comparison = not_kwrd + comp | comp

# Comma seperated recursive pattern for comparison style syntax
comparison_pattern = Forward()
comparison_pattern << Optional("(") + comparison + ZeroOrMore(White() +
    where_opts + comparison_pattern) + Optional(")")

multi_comparison_pattern = Forward()
multi_comparison_pattern << comparison_pattern + ZeroOrMore(White() + where_opts
    + multi_comparison_pattern)


############### MATCH/WHERE STATEMENTS ###############

match_stmt = Optional(optional) + match + traversal_csv_pattern
where_stmt = where + multi_comparison_pattern
