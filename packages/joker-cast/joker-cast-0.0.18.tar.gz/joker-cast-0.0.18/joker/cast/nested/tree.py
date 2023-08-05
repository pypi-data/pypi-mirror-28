#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, unicode_literals

from copy import deepcopy

from joker.cast.iterative import reusable


def get_parent_from_ascendants(ascendants):
    return ([0] + ascendants)[-1]


def compact_tree_assemble(records):
    """
    flat -> nested
    :param records: a list of dicts
    :return: (tree, tmap), both are dicts
    """
    records = reusable(records)
    tmap = {rec['id']: dict() for rec in records}
    tree = {}
    for rec in records:
        i = rec['id']
        p = rec['parent']
        pnode = tmap.get(p, tree)
        inode = tmap[i]
        pnode[i] = inode
    return tree, tmap


def standard_tree_assemble(records, setnone=False):
    """
    flat -> nested
    :param records: a list of dicts
    :param setnone: bool, default False
    :return: (tree, tmap), both are dicts
    """
    records = reusable(records)
    ids = [rec['id'] for rec in records]
    tmap = {i: {'id': i, 'children': list()} for i in ids}
    tree = {'id': 0, 'children': list()}
    for rec in records:
        i = rec['id']
        p = rec['parent']
        pnode = tmap.get(p, tree)
        inode = tmap[i]
        pnode['children'].append(inode)
    if setnone:
        for val in tmap.values():
            if not val['children']:
                val['children'] = None
    return tree, tmap


def standard_tree_dissemble(tree):
    """
    nested structure -> flat records
    :param tree: a nested dict
    :return: a list of dicts
    """
    tree = deepcopy(tree)
    tree['ascendants'] = []
    stack = [tree]
    collect = []
    while stack:
        node = stack.pop()
        collect.append(node)
        ascendants = node['ascendants'] + [node['id']]
        for child in node.get('children', []):
            child['ascendants'] = ascendants
            stack.append(child)
    for node in collect:
        try:
            del node['children']
        except KeyError:
            pass
    return collect


def compact_tree_dissemble(tree):
    """
    nested -> flat
    :param tree: a nested dict
    :return: a list of dicts
    """
    tree = deepcopy(tree)
    # tree['ascendants'] = []
    stack = [(i, list(), node) for (i, node) in tree.items()]
    collect = list()
    while stack:
        i, ascendants, node = stack.pop()
        collect.append({'id': i, 'ascendants': ascendants})
        ascendants = ascendants + [i]
        if node is None:
            continue
        for k, child in node.items():
            stack.append((k, ascendants, child))
    return collect
