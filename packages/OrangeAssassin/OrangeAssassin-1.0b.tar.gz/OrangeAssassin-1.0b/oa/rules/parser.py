"""Parse OA rule sets.

The general syntax for OA rules is (on one line):

<type> <name> <value>

Various options can be defined for a rule and they get bundled up using
the name as unique identifier.
"""

from __future__ import absolute_import

from builtins import dict
from builtins import object

import re
import os
import warnings
import contextlib
import collections
import locale

import oa.config
import oa.errors
import oa.context
import oa.plugins
import oa.rules.uri
import oa.rules.body
import oa.rules.meta
import oa.rules.full
import oa.rules.eval_
import oa.rules.header
import oa.rules.ruleset

from oa.regex import Regex

# Simple protection against recursion with "include".
MAX_RECURSION = 10

# Rules that require 2 arguments
KNOWN_2_RTYPE = frozenset(
    (
        "score",  # Specifies the score adjustment if the rule matches
        "priority",  # Specifies the priority of the rule
        "describe",  # Specifies a comment describing the rule
        "full",  # Specifies a FullRule
        "body",  # Specifies a BodyRule
        "rawbody",  # Specifies a RawBodyRule
        "uri",  # Specifies a URIRule
        "header",  # Specifies a HeaderRule
        "mimeheader",  # Specifies a MimeHeaderRule
        "meta",  # Specifies a MetaRule
        "eval",  # Specifies a EvalRule
        "lang",  # Specifies a language
        "tflags",  # Specifies a TflagRule
    )
)
# Rules that require 1 arguments
KNOWN_1_RTYPE = frozenset(
    (
        "report",  # Add some text to the report template
        "unsafe_report",  # Add some text to the unsafe report template
        "add_header",  # Adds a header to the message
        "remove_header",  # Remove header from message
        "include",  # Include another file in the current one
        "ifplugin",  # Check if plugin is loaded.
        "loadplugin",  # Load a plugin.
        "require_version",  # Only load this file if the version matches
        "required_score",  # Set the required score for this ruleset
        "report_safe",  # Set the method of reporting spam
        "report_contact",  # Set the contact address
        "required_score",  # Set the required score (default 5)
    )
)

# These are the types of rules that we know how to interpret, ignore anything
# else. These include rule types and option types.
KNOWN_RTYPE = KNOWN_1_RTYPE | KNOWN_2_RTYPE

# These types define rules and not options. Map against their specific class.
RULES = {
    "full": oa.rules.full.FullRule,
    "body": oa.rules.body.BodyRule,
    "rawbody": oa.rules.body.RawBodyRule,
    "uri": oa.rules.uri.URIRule,
    "meta": oa.rules.meta.MetaRule,
    "header": oa.rules.header.HeaderRule,
    "mimeheader": oa.rules.header.MimeHeaderRule,
    "eval": oa.rules.eval_.EvalRule,
}

_COMMENT_P = Regex(r"((?<=[^\\])#.*)")


class PADParser(object):
    """Parses PAD ruleset and extracts and combines the relevant data.

    Note that this is not thread-safe.
    """

    def __init__(self, paranoid=False, ignore_unknown=True, lazy_mode=True):
        self.ctxt = oa.context.GlobalContext(paranoid=paranoid,
                                             ignore_unknown=ignore_unknown,
                                             lazy_mode=lazy_mode)
        # XXX This could be a default OrderedDict
        self.results = collections.OrderedDict()
        self.ruleset = oa.rules.ruleset.RuleSet(self.ctxt)
        self._ignore = False

    @contextlib.contextmanager
    def _paranoid(self, *exceptions):
        """If not paranoid ignore the specified exceptions."""
        try:
            yield
        except exceptions as e:
            self.ctxt.err(e)
            if self.ctxt.paranoid:
                raise

    def parse_file(self, filename, _depth=0):
        """Parses a single PAD ruleset file."""
        if _depth > MAX_RECURSION:
            raise oa.errors.MaxRecursionDepthExceeded()
        self.ctxt.log.debug("Parsing file: %s", filename)
        if not os.path.isfile(filename):
            self.ctxt.log.warn("Ignoring %s, not a file", filename)
            return
        with open(filename, "rb") as rulef:
            for line_no, line in enumerate(rulef):
                try:
                    with self._paranoid(oa.errors.InvalidSyntax):
                        self._handle_line(filename, line, line_no + 1, _depth)
                except oa.errors.PluginLoadError as e:
                    warnings.warn(str(e))
                    self.ctxt.log.warn("%s", e)

    def _handle_line(self, filename, line, line_no, _depth=0):
        """Handles a single line."""
        try:
            line = line.decode("iso-8859-1").strip()
        except UnicodeDecodeError as e:
            raise oa.errors.InvalidSyntax(filename, line_no, line,
                                          "Decoding Error: %s" % e)
        # if line.startswith("if can"):
        #     # XXX We don't support for this check, simply
        #     # XXX skip everything for now.
        #     self._ignore = True
        #     return

        if line.startswith("endif"):
            self._ignore = False
            return

        if line.startswith("else"):
            if self._ignore:
                self._ignore = False
            else:
                self._ignore = True
            return

        if line.startswith("require_version"):
            # XXX We don't really have any use for this now
            # XXX Just skip it.
            return

        if not line or line.startswith("#") or self._ignore:
            return

        # Remove any comments
        line = _COMMENT_P.sub("", line).strip()

        try:
            rtype, value = line.split(None, 1)
        except ValueError:
            # Some plugin might know how to handle this line
            rtype, value = line, ""

        if rtype == "include":
            dirname = None
            if os.path.isabs(filename):
                dirname = os.path.dirname(filename)
            self._handle_include(value, line, line_no, _depth,
                                 dirname=dirname)
        elif rtype == "ifplugin":
            self._handle_ifplugin(value)
        elif rtype == "loadplugin":
            self._handle_loadplugin(value)
        elif rtype in KNOWN_2_RTYPE or rtype in self.ctxt.cmds:
            try:
                rtype, name, value = line.split(None, 2)
            except ValueError:
                raise oa.errors.InvalidSyntax(filename, line_no, line,
                                              "Missing argument")
            if rtype == "tflags":
                value = value.split()

            if rtype == "lang":
                locale.setlocale(locale.LC_ALL, '')
                locale_language = locale.getlocale(locale.LC_MESSAGES)[0]
                if not locale_language.startswith(name):
                    self.ctxt.log.debug("Lang argument does not"
                                        "correspond with locales")
                    return

                if "report" in value:
                    try:
                        rtype, value = value.split(None, 1)
                    except ValueError:
                        raise oa.errors.InvalidSyntax(filename, line_no, line,
                                                      "Missing argument")

                    if not self.ctxt.hook_parse_config(rtype, value):
                        self.ctxt.err("%s:%s Ignoring unknown"
                                      "configuration line: %s",
                                      filename, line_no, line)
                    return

                try:
                    rtype, name, value = value.split(None, 2)
                except ValueError:
                    raise oa.errors.InvalidSyntax(filename, line_no, line,
                                                  "Missing argument")

            if name not in self.results:
                self.results[name] = dict()

            if rtype in RULES or rtype in self.ctxt.cmds:
                if value.startswith("eval:"):
                    # This is for compatibility with SA ruleset
                    self.results[name]["target"] = rtype
                    rtype = "eval"
                self.results[name]["type"] = rtype
                self.results[name]["value"] = value
            else:
                if rtype == 'priority':
                    try:
                        int(value)
                    except ValueError:
                        self.ctxt.err("%s:%s Invalid type for priority value "
                                      "in configuration line: %s, setting it "
                                      "by"
                                      " default to 0", filename, line_no, line)
                self.results[name][rtype] = value

        else:
            if not self.ctxt.hook_parse_config(rtype, value):
                self.ctxt.err("%s:%s Ignoring unknown configuration line: %s",
                              filename, line_no, line)

    def _handle_include(self, value, line, line_no, _depth=0,
                        dirname=None):
        """Handles the 'include' keyword."""
        filename = value.strip()
        if not os.path.isabs(filename) and dirname is not None:
            filename = os.path.join(dirname, filename)
        try:
            self.parse_file(filename, _depth=_depth + 1)
        except oa.errors.MaxRecursionDepthExceeded as e:
            e.add_call(filename, line_no, line)
            raise e

    def _handle_ifplugin(self, value):
        """Handles the 'ifplugin' keyword."""
        plugin_name = oa.plugins.REIMPLEMENTED_PLUGINS.get(value, value)
        try:
            plugin_name = plugin_name.rsplit(".", 1)[1]
        except IndexError:
            pass
        if plugin_name not in self.ctxt.plugins:
            self.ctxt.log.debug("Plugin %s not loaded, skipping.", plugin_name)
            self._ignore = True

    def _handle_loadplugin(self, value):
        """Handles the 'loadplugin' keyword."""
        try:
            plugin_name, path = value.split(None, 1)
        except ValueError:
            plugin_name, path = value, None
        if "::" in plugin_name:
            plugin_name = oa.plugins.REIMPLEMENTED_PLUGINS.get(plugin_name)
        if plugin_name:
            self.ctxt.load_plugin(plugin_name, path)
        else:
            self.ctxt.log.warn("Plugin not available: %s", value)

    def get_ruleset(self):
        """Create and return the corresponding ruleset for the parsed files."""
        self.ctxt.hook_parsing_start(self.results)
        for name, data in self.results.items():
            try:
                rule_type = data["type"]
            except KeyError:
                e = oa.errors.InvalidRule(name, "No rule type defined.")
                self.ctxt.err(e)
                if self.ctxt.paranoid:
                    raise e
            else:
                with self._paranoid(oa.errors.InvalidRule,
                                    oa.errors.InvalidRegex):
                    try:
                        rule_class = RULES[rule_type]
                    except KeyError:
                        # A plugin might have been loaded that
                        # can handle this.
                        rule_class = self.ctxt.cmds[rule_type]
                    self.ctxt.log.debug("Adding rule %s with: %s", name, data)
                    rule = rule_class.get_rule(name, data)
                    self.ruleset.add_rule(rule)
        self.ctxt.hook_parsing_end(self.ruleset)
        self.ctxt.log.info("%s rules loaded", len(self.ruleset.checked))
        self.ruleset.post_parsing()
        return self.ruleset


def parse_pad_rules(files, paranoid=False, ignore_unknown=True):
    """Parse a list of PAD rules and returns the corresponding ruleset.

    'files' - a list of file paths.

    Returns a dictionary that maps rule names to a dictionary of rule options.
    Every rule will contain "type" and "value" which corresponds to the
    mandatory line for defining a rule. For example (type, name value):

    body LOCAL_DEMONSTRATION_RULE   /test/

    Other options may be included such as "score", "describe".
    """
    parser = PADParser(paranoid=paranoid, ignore_unknown=ignore_unknown)
    for filename in files:
        parser.parse_file(filename)

    return parser
