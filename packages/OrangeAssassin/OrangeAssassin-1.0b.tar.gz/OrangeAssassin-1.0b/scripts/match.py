#! /usr/bin/env python

"""Testing tool that parses PAD rule set files and runs a match against message.

Prints out any matching rules.
"""

from __future__ import print_function

import os
import sys
import argparse

import dill as pickle

import oa
import oa.common
import oa.config
import oa.errors
import oa.message
import oa.rules.meta
import oa.rules.parser

from future.utils import PY3

class MessageList(argparse.FileType):
    def __call__(self, string):
        if os.path.isdir(string):
            for x in os.listdir(string):
                path = os.path.join(string, x)
                msgf = super(MessageList, self).__call__(path)
                yield msgf
        else:
            yield super(MessageList, self).__call__(string)


def _is_binary_reader(stream, default=False):
    try:
        return isinstance(stream.read(0), bytes)
    except Exception:
        return default


def get_binary_stdin():
    # sys.stdin might or might not be binary in some extra cases.  By
    # default it's obviously non binary which is the core of the
    # problem but the docs recommend changing it to binary for such
    # cases so we need to deal with it.
    is_binary = _is_binary_reader(sys.stdin, False)
    if is_binary:
        return sys.stdin
    buf = getattr(sys.stdin, 'buffer', None)
    if buf is not None and _is_binary_reader(buf, True):
        return buf


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-n", "--nice", type=int, help="set 'nice' level",
                        default=0)
    parser.add_argument("-P", "--paranoid", action="store_true", default=False,
                        help="Die upon user errors")
    parser.add_argument("-se", "--serialize", action="store_true", default=False,
                        help="Allow serialization")
    parser.add_argument("--show-unknown", action="store_true", default=False,
                        help="Show warnings about unknown parsing errors")
    parser.add_argument("-sp", "--serializepath", action="store",
                        help="Path to the file with serialized ruleset",
                        default="~/.spamassassin/serialized_ruleset")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--report", action="store_true",
                       help="Report the message as spam", default=False)
    group.add_argument("-k", "--revoke", action="store_true",
                       help="Revoke the message as spam ", default=False)
    parser.add_argument("-D", "--debug", action="store_true",
                        help="Enable debugging output", default=False)
    parser.add_argument("-dl", "--deactivate-lazy", dest="lazy_mode",
                        action="store_true", default=False,
                        help="Deactivate lazy loading of rules/regex")
    parser.add_argument("-v", "--version", action="version",
                        version=oa.__version__)
    parser.add_argument("-C", "--configpath", action="store",
                        help="Path to standard configuration directory",
                        **oa.config.get_default_configs(site=False))
    parser.add_argument("-S", "--sitepath", "--siteconfigpath", action="store",
                        help="Path to standard configuration directory",
                        **oa.config.get_default_configs(site=True))
    parser.add_argument("-p", "--prefspath", "--prefs-file",
                        default="~/.spamassassin/user_prefs",
                        help="Path to user preferences.")
    parser.add_argument("-t", "--test-mode", action="store_true", default=False,
                        help="Pipe message through and add extra report to the "
                             "bottom")
    parser.add_argument("-R", "--report-only", action="store_true",
                        default=False, help="Only print the report instead of "
                                            "the adjusted message.")
    parser.add_argument("messages", type=MessageList(), nargs="*",
                        metavar="path", help="Paths to messages or "
                                             "directories containing messages",
                        default=[[get_binary_stdin()]])

    return parser.parse_args(args)


def call_post_parsing(ruleset):
    """Run all post processing hooks."""
    ruleset.ctxt.hook_parsing_end(ruleset)
    ruleset.ctxt.log.info("%s rules loaded", len(ruleset.checked))
    ruleset.call_postparsing()


def main():
    options = parse_arguments(sys.argv[1:])
    oa.config.LAZY_MODE = not options.lazy_mode
    logger = oa.config.setup_logging("oa-logger", debug=options.debug)
    config_files = oa.config.get_config_files(options.configpath,
                                              options.sitepath,
                                              options.prefspath)

    if not config_files:
        logger.critical("Config: no rules were found.")
        sys.exit(1)

    serialize = options.serialize

    if serialize and not oa.common.can_compile():
        logger.error("Cannot compile in this environment")
        serialize = False

    if not serialize:
        try:
            ruleset = oa.rules.parser.parse_pad_rules(
                config_files, options.paranoid, not options.show_unknown
            ).get_ruleset()
        except oa.errors.MaxRecursionDepthExceeded as e:
            logger.critical(e.recursion_list)
            sys.exit(1)
        except oa.errors.ParsingError as e:
            logger.critical(e)
            sys.exit(1)
    else:
        try:
            with open(os.path.expanduser(options.serializepath), "rb") as f:
                ruleset = pickle.load(f)
        except EOFError as e:
            logger.critical("Compiled file is empty: %s", e)
            sys.exit(1)
        call_post_parsing(ruleset)

    count = 0
    for message_list in options.messages:
        for msgf in message_list:
            raw_msg = msgf.read()
            if type(raw_msg) is bytes and PY3:
                raw_msg = raw_msg.decode("utf-8", "ignore")
            msgf.close()
            msg = oa.message.Message(ruleset.ctxt, raw_msg)

            if options.revoke:
                ruleset.ctxt.hook_revoke(msg)
            elif options.report:
                ruleset.ctxt.hook_report(msg)
            elif options.report_only:
                ruleset.match(msg)
                print(ruleset.get_report(msg))
            else:
                ruleset.match(msg)
                print(ruleset.get_adjusted_message(msg))
                if options.test_mode:
                    print(ruleset.get_report(msg))
        count += 1
    if options.revoke or options.report:
        print("%s message(s) examined" % count)


if __name__ == "__main__":
    main()
