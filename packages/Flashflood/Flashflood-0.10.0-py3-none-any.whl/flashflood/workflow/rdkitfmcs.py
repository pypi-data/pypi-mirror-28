#
# (C) 2014-2017 Seiji Matsuoka
# Licensed under the MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import functools
import traceback

from chorus import rdkit

from flashflood import static
from flashflood.core.concurrent import ConcurrentFilter
from flashflood.core.container import Container, Counter
from flashflood.core.workflow import Workflow
from flashflood.interface import sqlite
from flashflood.node.chem.descriptor import AsyncMolDescriptor
from flashflood.node.chem.molecule import AsyncMoleculeToJSON, UnpickleMolecule
from flashflood.node.field.number import AsyncNumber
from flashflood.node.monitor.count import AsyncCountRows
from flashflood.node.reader.sqlite import SQLiteReader
from flashflood.node.writer.container import ContainerWriter


def rdfmcs_calc(qmol, timeout, row):
    try:
        res = rdkit.fmcs(row["__molobj"], qmol, timeout=timeout)
    except:
        print(traceback.format_exc())
        return
    row["fmcs_sim"] = res["similarity"]
    row["fmcs_edges"] = res["mcs_edges"]
    return row


def thld_filter(thld, measure, row):
    if row is None:
        return
    type_ = {"sim": "fmcs_sim", "edge": "fmcs_edges"}
    return row[type_[measure]] >= thld


class RDKitFMCS(Workflow):
    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.query = query
        self.results = Container()
        self.done_count = Counter()
        self.input_size = Counter()
        self.data_type = "nodes"
        measure = query["params"]["measure"]
        thld = float(query["params"]["threshold"])
        timeout = int(query["params"]["timeout"])
        self.append(SQLiteReader(
            [sqlite.find_resource(t) for t in query["targets"]],
            fields=sqlite.merged_fields(query["targets"]),
            counter=self.input_size
        ))
        self.append(UnpickleMolecule())
        qmol = sqlite.query_mol(query["queryMol"])
        self.append(ConcurrentFilter(
            functools.partial(thld_filter, thld, measure),
            func=functools.partial(rdfmcs_calc, qmol, timeout),
            residue_counter=self.done_count,
            fields=[
                {"key": "fmcs_sim", "name": "MCS similarity",
                 "d3_format": ".2f"},
                {"key": "fmcs_edges", "name": "MCS size", "d3_format": "d"}
            ]
        ))
        self.append(AsyncMolDescriptor(static.MOL_DESC_KEYS))
        self.append(AsyncMoleculeToJSON())
        self.append(AsyncNumber("index", fields=[static.INDEX_FIELD]))
        self.append(AsyncCountRows(self.done_count))
        self.append(ContainerWriter(self.results))
