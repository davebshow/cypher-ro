"""
This module implements a Cypher query language parser for read only queries.

The parser will perform the following:

* Verification that a query is read only.

* Liberal evaluation of Cypher syntax. It is probable that this parser is
consierable more permissive than Neo4j's parser, but that is ok for our purposes.

* Injectable parse actions on any major part of the grammar, for example,
mapping an new style label to a legacy Neo4j index.

############### CYPHER READ QUERY STRUCTURE ###############
#http://neo4j.com/docs/stable/cypher-refcard/

# [MATCH WHERE]
# [OPTIONAL MATCH WHERE]
# [WITH [ORDER BY] [SKIP] [LIMIT]]
# RETURN [ORDER BY] [SKIP] [LIMIT]

"""
from pyparsing import (Word, alphanums, ZeroOrMore, OneOrMore, nums, stringEnd, Literal,
    CaselessKeyword, Optional, Forward, quotedString, White)

#############################################################################
############### KWRDS #######################################################
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
xor = CaselessKeyword("XOR") + White()
not_kwrd = CaselessKeyword("NOT") + White()
return_kwrd = CaselessKeyword("RETURN") + White()
distinct = CaselessKeyword("DISTINCT") + White()
has = CaselessKeyword("HAS") + White()
in_kwrd = CaselessKeyword("IN") + White()
is_kwrd = CaselessKeyword("IS") + White()
null = CaselessKeyword("NULL") + Optional(White())
asc = CaselessKeyword("ASC") + Optional(White())
desc = CaselessKeyword("DESC") + Optional(White())
skip = CaselessKeyword("SKIP") + Optional(White())

type_kwrd = CaselessKeyword("type")  # Literal?


#############################################################################
############### KWRD Groups ###############

and_not = and_kwrd + not_kwrd
or_not = or_kwrd + not_kwrd
xor_not = xor + not_kwrd
where_opts = (and_not | or_not | xor_not | and_kwrd | or_kwrd | xor | not_kwrd)


#############################################################################
############### Generics ####################################################

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

operators = (equals | geq | leq | gt | lt | neq)

# Useful combos
gettr = var + "." + var
right = gettr | quotedString | integer


#############################################################################
############### Misc. Functions #############################################
simple_param = "(" + var + ")"
type_fn = type_kwrd + simple_param


#############################################################################
############### Path Functions ##############################################
### UNTESTED
length = CaselessKeyword("length")
nodes = CaselessKeyword("nodes")
rels = CaselessKeyword("rels")

length_fn = length + simple_param
nodes_fn = nodes + simple_param
rels_fn = rels + simple_param


#############################################################################
############### Collection Functions ########################################


#############################################################################
############### Mathematical Functions ######################################

#############################################################################
############### Aggregation #################################################

# Kwrds
count = CaselessKeyword("count")  # Literal?
sum = CaselessKeyword("sum")  # Literal?
disc_per = CaselessKeyword("percentileDisc")  # Literal?
standard_dev = CaselessKeyword("stdev")  # Literal?

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


#############################################################################
############### Functions ###################################################

fns = (aggr_fn | type_fn)


#############################################################################
############### Collections #################################################

lst = "[" + right + ZeroOrMore("," + Optional(White()) + right) + "]"


#############################################################################
############### Nodes/Edges #################################################

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
cardinality = "*" + integer + ".." + integer | "*"
edge_content = ("[" + Optional(alias_label) + Optional(prop_map) +
    Optional(cardinality) + "]")
undir_edge = "-" + Optional(edge_content) + "-"
out_edge = undir_edge + ">"
in_edge = "<" + undir_edge
edge = out_edge | in_edge | undir_edge


#############################################################################
############### Traversal pattern ###########################################

traversal_pattern = Forward()
traversal_pattern << node + ZeroOrMore(edge + traversal_pattern)

traversal_csv_pattern = Forward()
traversal_csv_pattern << traversal_pattern + ZeroOrMore("," +
    traversal_csv_pattern)


#############################################################################
############### WHERE pattern ###############################################

# This is pretty permissive, but fine for our purposes. For now anyway, can
# make stricter if necessary
has_comp = has + "(" + gettr + ")"
full_left = gettr | type_fn | var

# operator + right combos
simple_comp = operators + right
in_comp = in_kwrd + lst
isnull_comp = is_kwrd + null
reg_comp = reg + quotedString
op_right = isnull_comp | simple_comp | in_comp | reg_comp

comp = (has_comp | full_left + op_right | (var + OneOrMore(label)))

comp_obj = not_kwrd + comp | comp
traversal_pattern_obj = not_kwrd + traversal_pattern | traversal_pattern

# Comma seperated recursive pattern for comp_obj style syntax
comparison_pattern = Forward()
comparison_pattern << Optional("(") + comp_obj + ZeroOrMore(White() +
    where_opts + comparison_pattern) + Optional(")")

multi_comparison_pattern = Forward()
multi_comparison_pattern << ((traversal_pattern_obj | comparison_pattern) +
    ZeroOrMore(White() + where_opts + multi_comparison_pattern))


#############################################################################
############### WITH pattern ################################################

as_left = aggr_fn | type_fn | gettr | var
as_stmt =  as_left + White() + as_kwrd + var

with_obj = as_stmt | var

with_pattern = Forward()
with_pattern << with_obj + ZeroOrMore("," + Optional(White()) + with_pattern)


#############################################################################
############### ORDER BY pattern ############################################

orderby_obj = (gettr | var) + Optional(White() + (asc | desc))

orderby_pattern = Forward()
orderby_pattern << orderby_obj + ZeroOrMore("," + Optional(White()) +
    orderby_pattern)


#############################################################################
############### RETURN pattern ##############################################

return_obj = (quotedString | as_stmt | fns | multi_comparison_pattern | flt |
    var)

return_pattern = Forward()
return_pattern << return_obj + ZeroOrMore("," + Optional(White()) +
    return_pattern)


#############################################################################
############### STATEMENTS ##################################################

match_stmt = ((Optional(optional) + match + traversal_csv_pattern |
    match + var + "=" + traversal_pattern) + Optional(White()))

where_stmt = where + multi_comparison_pattern + Optional(White())

with_stmt = with_kwrd + with_pattern + Optional(White())

order_stmt = order_by + orderby_pattern + Optional(White())

limit_stmt = limit + integer + Optional(White())

skip_stmt = skip + integer + Optional(White())

return_stmt = return_kwrd + return_pattern + Optional(White())
