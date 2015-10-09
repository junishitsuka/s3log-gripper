# coding: utf-8

import sys
import const, command, validator
from optparse import OptionParser
from datetime import datetime as dt

def gripper(argv=sys.argv[1:]):
    parser = make_parser()
    (options, args) = parser.parse_args(argv)

    if options.list:
        return command.exec_list()

    # validate options
    if not validator.collection_validate(options.collection):
        return "invalid collection option"
    if not validator.date_validate(options.date_from):
        return "invalid date_from option"
    if not validator.date_validate(options.date_to):
        return "invalid date_to option"

    return command.exec_grip(
        options.collection,
        options.date_from,
        options.date_to,
        options.profile
    )

def make_parser():
    parser = OptionParser()
    default_date = dt.now().strftime("%Y-%m-%d")

    # set options
    parser.add_option("-l", "--list", action="store_true", dest="list", default=False,
        help="output the list of all possible logs"
    )
    parser.add_option("-c", "--collection", dest="collection",
        help="the target log collection"
    )
    parser.add_option("-f", "--from", dest="date_from", default=default_date,
        help="the date of start, format is YYYY-mm-dd"
    )
    parser.add_option("-t", "--to", dest="date_to", default=default_date,
        help="the date of end, format is YYYY-mm-dd"
    )
    parser.add_option("-p", "--profile", dest="profile", default="default",
        help="aws profile"
    )
    return parser
