.. api.rst
.. Copyright (c) 2013-2018 Pablo Acosta-Serafini
.. See LICENSE for details
.. py:module:: putil.tree

###
API
###

************
Pseudo-types
************

.. _NodeName:

NodeName
--------

String where hierarchy levels are denoted by node separator characters
(:code:`'.'` by default). Node names cannot contain spaces, empty hierarchy
levels, start or end with a node separator character.

For this example tree:

.. include:: ./support/tree.txt

The node names are ``'root'``, ``'root.branch1'``, ``'root.branch1.leaf1'``,
``'root.branch1.leaf2'`` and ``'root.branch2'``

.. _NodesWithData:

NodesWithData
-------------

Dictionary or list of dictionaries; each dictionary must contain exactly two
keys:

* **name** (*NodeName*) Node name. See `NodeName`_ pseudo-type specification

* **data** (*any*) node data

The node data should be an empty list to create a node without data, for
example: :code:`{'name':'a.b.c', 'data':[]}`

*****
Class
*****

.. autoclass:: ptrie.Trie
    :members: add_nodes, collapse_subtree, copy_subtree, delete_prefix,
              delete_subtree, flatten_subtree, get_children, get_data,
              get_leafs, get_node, get_node_children, get_node_parent,
			  get_subtree, is_root, in_tree, is_leaf, make_root, print_node,
			  rename_node, search_tree, nodes, node_separator, root_node,
			  root_name, __nonzero__, __str__
    :show-inheritance:
