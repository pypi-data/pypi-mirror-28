"""Implement the TELL command."""

from __future__ import absolute_import

import oa.protocol
import oa.protocol.base


class TellCommand(oa.protocol.base.BaseProtocol):
    """Report of revoke spam/ham messages.
    """
    has_options = True
    has_message = True

    def handle(self, msg, options):
        spam = options.get("message-class", "spam").lower() == "spam"
        response = []
        if "set" in options:
            targets = options.get("set").split(",")
            local = "local" in targets
            remote = "remote" in targets
            self.ruleset.ctxt.hook_report(msg, spam, local, remote)
            response.append("DidSet: %s\r\n" % options.get("set"))
        if "remove" in options:
            targets = options.get("remove").split(",")
            local = "local" in targets
            remote = "remote" in targets
            self.ruleset.ctxt.hook_revoke(msg, spam, local, remote)
            response.append("DidRemove: %s\r\n" % options.get("remove"))
        for action in response:
            yield action
