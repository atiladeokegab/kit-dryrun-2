# /// script
# requires-python = ">=3.11"
# dependencies = ["diagrams"]
# ///
"""C4 diagrams for <SYSTEM>. Copy this file, replace the example nodes, run it.

    uv run c4.py            # writes c4_context.png ... c4_code.png beside this file
    uv run c4.py context    # just one level

While planning it lives at ~/hub/projects/<repo>/c4.py and draws the PLANNED system,
levels 1-3 only. After the build it moves to docs/architecture/c4.py in the repo and
draws the REAL code, level 4 included. The inline dependency above means nothing is
added to the repo's pyproject.
"""

import shutil
import sys
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.c4 import Container, Database, Person, Relationship, System, SystemBoundary
from functools import partial

# diagrams.c4 wraps text at 40 characters but draws 2.6in boxes, which fit about 34:
# lines of 35-40 characters were cut off, silently. 3.3in fits the full wrap width.
Container, Database, Person, System = (partial(f, width="3.3") for f in (Container, Database, Person, System))
from diagrams.programming.language import Python

SYSTEM = "expenses"  # <- the system's name
# Look at every PNG before showing it to anyone.
OUT = Path(__file__).parent
GRAPH = {"splines": "spline", "nodesep": "0.8", "ranksep": "1.1"}


def draw(level, title):
    return Diagram(f"{SYSTEM} - {title}", filename=str(OUT / f"c4_{level}"), outformat="png",
                   show=False, direction="TB", graph_attr=GRAPH)


def context():
    """Level 1: who uses it and what it depends on. The system is ONE box."""
    with draw("context", "System Context"):
        user = Person("Person with receipts", "Wants a correct monthly total")
        system = System(SYSTEM, "Turns a folder of messy receipt text into a summary")
        src = System("Receipt folder", "Text dumps of receipts, one per file", external=True)
        user >> Relationship("runs on a folder") >> system
        system >> Relationship("reads") >> src


def container():
    """Level 2: the separately running or deployed pieces, and how they talk."""
    with draw("container", "Containers"):
        user = Person("Person with receipts", "")
        with SystemBoundary(SYSTEM):
            cli = Container("expenses CLI", "Python 3 stdlib", "python3 -m expenses FOLDER [--json]")
        src = System("Receipt folder", "samples/ or any folder of .txt receipts", external=True)
        user >> Relationship("runs") >> cli
        cli >> Relationship("reads") >> src


def component():
    """Level 3: inside ONE container. Name the container in the title."""
    with draw("component", "Components of the expenses CLI"):
        with SystemBoundary("expenses CLI"):
            main = Container("CLI", "expenses/__main__.py (core)", "Reads files, prints table or JSON")
            model = Container("Receipt model", "expenses/model.py (core)", "Receipt, Summary dataclasses")
            parse = Container("Parse", "expenses/parse/", "Text -> merchant, date, total, currency")
            totals = Container("Totals", "expenses/totals/", "Category, GBP subtotals, not-counted list")
        main >> Relationship("parse(text)") >> parse
        main >> Relationship("summarise(receipts)") >> totals
        parse >> Relationship("builds") >> model
        totals >> Relationship("returns Summary") >> model


def code():
    """Level 4: modules and key signatures, from the real code."""
    with draw("code", "Code"):
        with Cluster("expenses/"):
            main = Python("__main__.py\n——\n+ main(argv) → int\n+ render_table(Summary)\n+ render_json(Summary)")
            model = Python("model.py\n——\nReceipt(source, merchant,\n  date, total, currency)\nSummary(by_category,\n  grand_total, not_counted)")
            parse = Python("parse/__init__.py\n——\n+ parse(source, text)\n  → Receipt")
            totals = Python("totals/__init__.py\n——\n+ category(\\n  merchant) → str\n+ summarise(receipts)\n  → Summary")
        main >> Edge(label="parse") >> parse
        main >> Edge(label="summarise") >> totals
        parse >> Edge(label="builds") >> model
        totals >> Edge(label="returns") >> model


# Only the levels defined above: while planning, code() is deleted, not stubbed.
LEVELS = {n: globals()[n] for n in ("context", "container", "component", "code") if n in globals()}

if __name__ == "__main__":
    if not shutil.which("dot"):
        sys.exit("c4: Graphviz is not installed (no `dot` on PATH). Run: sudo apt install -y graphviz")
    for name in sys.argv[1:] or LEVELS:
        LEVELS[name]()
        print(OUT / f"c4_{name}.png")
