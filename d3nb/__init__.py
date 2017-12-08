from __future__ import print_function
import os
import sys
from subprocess import Popen, PIPE, check_call
from IPython.core.magic import register_cell_magic
from IPython.display import SVG, HTML


__title__ = "d3nb"
__description__ = "d3js"
__uri__ = "https://github.com/jbn/d3js"
__doc__ = __description__ + " <" + __uri__ + ">"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2017 John Bjorn Nelson"
__version__ = "0.0.2"
__author__ = "John Bjorn Nelson"
__email__ = "jbn@abreka.com"


def report_err(msg, exit=False):
    """
    :param msg: the message to print to stderr
    :param exit: if True, raise a runtime error after printing
    """
    print(msg, file=sys.stderr)
    if exit:
        # Failing allows for good batch notebook behavior based on exit-codes.
        # XXX: Hook into Jupyter's exception handling for cleaner results.
        raise RuntimeError("d3nb failure")


def process_line_args(line):
    """
    Process the cell-magic arguments.

    Expected format: [working_directory] [--init]

    The `--init` flag will run `yarn add node-d3` in [working_directory]
    but it will not reinitialize it.
    """
    cwd, init = None, False

    if line:
        # Create will run `yarn add node-d3`.
        init = "--init" in line
        if init:
            line = line.replace("--init", "")
        cwd = line.strip()

    cwd = cwd or os.getcwd()
    node_modules = os.path.join(cwd, "node_modules")

    if not os.path.exists(node_modules):
        if init:
            if not os.path.exists(cwd):
                os.makedirs(cwd)
            report_err("Executing `yarn add d3-node` in `{}`".format(cwd))
            check_call(['yarn', 'add', 'd3-node'], cwd=cwd)
        else:
            report_err("Directory `{}` doesn't exist!".format(cwd))
            report_err("Call with --init to initialize it.".format(cwd),
                       exit=True)
    elif init:
        report_err("`{}` already exists. Won't `--init`!".format(cwd),
                   exit=True)

    return cwd


def portray(line, cell, portrayal):
    """
    Portray the output of the node invocation.

    :param line: the arguments to the cell magic
    :param cell: the cell magic source excluding invocation line
    :param portrayal: the display class in jupyter.
    """
    out, err = run_script(cell, process_line_args(line))
    return err if err else portrayal(out)


def run_script(script, cwd=None):
    """
    :param script: the d3 script
    :param cwd: the node project directory.
    """
    proc = Popen(['node'], stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
    out, err = proc.communicate(script.encode())
    return out.decode(), err


@register_cell_magic
def d3nb_svg(line, cell):
    """
    Cell magic that renders output of d3 script to an SVG.
    """
    return portray(line, cell, SVG)


@register_cell_magic
def d3nb_html(line, cell):
    """
    Cell magic that renders output of d3 script to an HTML.
    """
    return portray(line, cell, HTML)
