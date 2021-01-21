import argparse
import logging
import sys
from os.path import splitext

from ..core.conf import log_levels_dict as log_lvl
from ..docs import TopologyGrapher
from ..docs import generate

log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(
    description='The missing docs generator for F Prime projects.')


def build_parser(parser):
    """Builds the parser for the docs cli.  Formulating this as a
    function allows this cli to be built either as a standalone callable
    or as a subcommand in a collection of callables.
    """
    parser.add_argument('-o', '--output', dest="output",
                        help='Documentation file to generate')
    parser.add_argument('-g', '--graph', action='store_true',
                        help='Graph a topology file')


def docs_main(args=None, parser=None):
    if args is None and parser is not None:
        args = parser
    else:
        args = parser.parse_args(args=args)

    root_log = logging.getLogger('')
    console_handler = logging.StreamHandler(sys.stderr)
    root_log.addHandler(console_handler)
    root_log.setLevel(log_lvl[args.log_level])

    invalid_flag = False
    filename, file_extension = splitext(args.base_file)
    ai_file_type = None
    output_file = "graphviz.txt"
    if file_extension != '.xml':
        log.error('This version only works with XML input files.')
        invalid_flag = True
    if filename[-2:] != 'Ai':
        log.error('Autocoder input files must have the suffix "Ai".')
        invalid_flag = True
    elif filename[-11:-2] == "Component":
        ai_file_type = "Component"
    elif filename[-13:-2] == "TopologyApp":
        ai_file_type = "TopologyApp"
        if not args.graph and (args.fprime_root is None or len(args.fprime_root) < 1):
            log.error("Topology parsing requires fprime root directory argument")
            invalid_flag = True
    else:
        log.info(filename)
        log.error('This version can only handle Component and Topology files.')
        invalid_flag = True
    if args.graph and ai_file_type != "TopologyApp":
        log.warning("Graphing is only supported for topology files")
        invalid_flag = True
    if args.output is not None:
        output_file = args.output

    if invalid_flag:
        exit(1)

    log.info('Loading file {}'.format(args.base_file))
    # Ignore the rest of this file, its a hack, and probably needs
    # to be removed since it was written to auto-code files that are
    # actively being removed from F Prime.
    log.info(ai_file_type)
    if ai_file_type == "Component":
        generate.generate_component_documentation(args.base_file)
    elif ai_file_type == "TopologyApp" and not args.graph:
        generate.generate_topology_documentation(
            args.base_file, args.fprime_root)
    elif ai_file_type == "TopologyApp" and args.graph:
        TopologyGrapher.make_graph(args.base_file, output_file)
