#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import functools

from chorus import substructure
from chorus import molutil

from flashflood import static
from flashflood.core.concurrent import ConcurrentFilter
from flashflood.core.container import Container, Counter
from flashflood.core.workflow import Workflow
from flashflood.interface import sqlite
from flashflood.node.chem.descriptor import MolDescriptor, AsyncMolDescriptor
from flashflood.node.chem.molecule import (
    MoleculeToJSON, AsyncMoleculeToJSON, UnpickleMolecule)
from flashflood.node.control.filter import Filter
from flashflood.node.field.number import Number, AsyncNumber
from flashflood.node.monitor.count import CountRows, AsyncCountRows
from flashflood.node.reader.sqlite import SQLiteReader, SQLiteReaderFilter
from flashflood.node.writer.container import ContainerWriter


def exact_filter(qmol, params, row):
    return substructure.equal(
            row["__molobj"], qmol, ignore_hydrogen=params["ignoreHs"])


def substr_filter(qmol, params, row):
    return substructure.substructure(
            row["__molobj"], qmol, ignore_hydrogen=params["ignoreHs"])


def supstr_filter(qmol, params, row):
    return substructure.substructure(
            qmol, row["__molobj"], ignore_hydrogen=params["ignoreHs"])


class ExactStruct(Workflow):
    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.results = Container()
        self.done_count = Counter()
        self.input_size = Counter()
        self.data_type = "nodes"
        qmol = sqlite.query_mol(query["queryMol"])
        pred = functools.partial(exact_filter, qmol, query["params"])
        self.append(SQLiteReaderFilter(
            [sqlite.find_resource(t) for t in query["targets"]],
            "_mw_wo_sw", molutil.mw(qmol), "=",
            fields=sqlite.merged_fields(query["targets"])
        ))
        self.append(CountRows(self.input_size))
        self.append(UnpickleMolecule())
        self.append(Filter(pred, residue_counter=self.done_count))
        self.append(MolDescriptor(static.MOL_DESC_KEYS))
        self.append(MoleculeToJSON())
        self.append(Number("index", fields=[static.INDEX_FIELD]))
        self.append(CountRows(self.done_count))
        self.append(ContainerWriter(self.results))


class Substruct(Workflow):
    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.results = Container()
        self.done_count = Counter()
        self.input_size = Counter()
        self.data_type = "nodes"
        qmol = sqlite.query_mol(query["queryMol"])
        pred = functools.partial(substr_filter, qmol, query["params"])
        self.append(SQLiteReader(
            [sqlite.find_resource(t) for t in query["targets"]],
            fields=sqlite.merged_fields(query["targets"]),
            counter=self.input_size
        ))
        self.append(UnpickleMolecule())
        self.append(ConcurrentFilter(pred, residue_counter=self.done_count))
        self.append(AsyncMolDescriptor(static.MOL_DESC_KEYS))
        self.append(AsyncMoleculeToJSON())
        self.append(AsyncNumber("index", fields=[static.INDEX_FIELD]))
        self.append(AsyncCountRows(self.done_count))
        self.append(ContainerWriter(self.results))


class Superstruct(Workflow):
    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.results = Container()
        self.done_count = Counter()
        self.input_size = Counter()
        self.data_type = "nodes"
        qmol = sqlite.query_mol(query["queryMol"])
        pred = functools.partial(supstr_filter, qmol, query["params"])
        self.append(SQLiteReader(
            [sqlite.find_resource(t) for t in query["targets"]],
            fields=sqlite.merged_fields(query["targets"]),
            counter=self.input_size
        ))
        self.append(UnpickleMolecule())
        self.append(ConcurrentFilter(pred, residue_counter=self.done_count))
        self.append(AsyncMolDescriptor(static.MOL_DESC_KEYS))
        self.append(AsyncMoleculeToJSON())
        self.append(AsyncNumber("index", fields=[static.INDEX_FIELD]))
        self.append(AsyncCountRows(self.done_count))
        self.append(ContainerWriter(self.results))
