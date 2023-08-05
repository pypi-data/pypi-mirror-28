"""Expose some eval rules that do checks on the headers."""

from __future__ import absolute_import
from __future__ import division

import re
import time
import datetime
import itertools
import email.utils
import email.header

from dateutil import relativedelta

import oa.locales
import oa.plugins.base
from oa.received_parser import IP_ADDRESS
from oa.regex import Regex


class HeaderEval(oa.plugins.base.BasePlugin):
    hotmail_addr_with_forged_hotmail_received = 0
    hotmail_addr_but_no_hotmail_received = 0
    tocc_sorted_count = 7
    tocc_similar_count = 5
    tocc_similar_length = 2

    eval_rules = (
        "check_for_fake_aol_relay_in_rcvd",
        "check_for_faraway_charset_in_headers",
        "check_for_unique_subject_id",
        "check_illegal_chars",
        "check_for_forged_hotmail_received_headers",
        "check_for_no_hotmail_received_headers",
        "check_for_msn_groups_headers",
        "check_for_forged_eudoramail_received_headers",
        "check_for_forged_yahoo_received_headers",
        "check_for_forged_juno_received_headers",
        "check_for_matching_env_and_hdr_from",
        "sorted_recipients",
        "similar_recipients",
        "check_for_missing_to_header",
        "check_for_forged_gw05_received_headers",
        "check_for_shifted_date",
        "subject_is_all_caps",
        "check_for_to_in_subject",
        "check_outlook_message_id",
        "check_messageid_not_usable",
        "check_header_count_range",
        "check_unresolved_template",
        "check_ratware_name_id",
        "check_ratware_envelope_from",
        "gated_through_received_hdr_remover",
        "check_equal_from_domains",
        "received_within_months"
    )

    options = {
        "util_rb_tld": ("append_split", []),
        "util_rb_2tld": ("append_split", []),
        "util_rb_3tld": ("append_split", []),
    }

    def check_for_fake_aol_relay_in_rcvd(self, msg, target=None):
        """Check for common AOL fake received header."""
        for recv in msg.get_decoded_header("Received"):
            if not Regex(r" rly-[a-z][a-z]\d\d\.", re.I).search(recv):
                continue
            if Regex(r"\/AOL-\d+\.\d+\.\d+\)").search(recv):
                continue
            if Regex(r"ESMTP id (?:RELAY|MAILRELAY|MAILIN)").search(recv):
                continue
            return True
        return False

    def check_for_faraway_charset_in_headers(self, msg, target=None):
        """Check if the Subject/From header is in a NOT ok locale.

        This eval rule requires the ok_locales setting configured,
        and not set to ALL.
        """
        ok_locales = self.ctxt.conf.get_global("ok_locales")
        if not ok_locales or ok_locales.lower() == "all":
            return False
        ok_locales = ok_locales.split()

        # XXX We should really be checking ALL headers here,
        # XXX not just Subject and From.
        for header_name in ("Subject", "From"):
            for header in msg.get_raw_header(header_name):
                try:
                    decoded_header = email.header.decode_header(header)
                except (ValueError, email.header.HeaderParseError):
                    continue

                for value, charset in decoded_header:
                    if not oa.locales.charset_ok_for_locales(
                            charset, ok_locales):
                        return True

        return False

    def check_for_unique_subject_id(self, msg, target=None):
        """Check if in subject appears an unique id"""
        subject = "".join(msg.get_decoded_header("Subject"))
        id = None
        unique_id_re_list = [
            r"[-_\.\s]{7,}([-a-z0-9]{4,})$",
            r"\s{10,}(?:\S\s)?(\S+)$",
            r"\s{3,}[-:\#\(\[]+([-a-z0-9]{4,})[\]\)]+$",
            r"\s{3,}[-:\#]([a-z0-9]{5,})$",
            r"[\s._]{3,}([^0\s._]\d{3,})$",
            r"[\s._]{3,}\[(\S+)\]$",

            # (7217vPhZ0-478TLdy5829qicU9-0@26) and similar
            r"\(([-\w]{7,}\@\d+)\)$",
            r"\b(\d{7,})\s*$",

            # stuff at end of line after "!" or "?" is usually an id
            r"[!\?]\s*(\d{4,}|\w+(-\w+)+)\s*$",

            # 9095IPZK7-095wsvp8715rJgY8-286-28 and similar
            # excluding 'Re:', etc and the first word
            r"(?:\w{2,3}:\s)?\w+\s+(\w{7,}-\w{7,}(-\w+)*)\s*$",

            # #30D7 and similar
            r"\s#\s*([a-f0-9]{4,})\s*$"
        ]
        for rgx in unique_id_re_list:
            match = Regex(rgx, re.I).search(subject)
            if match:
                id = match.group()
                break
        if not id:
            return False
        comercial_re = Regex(r"(?:item|invoice|order|number|confirmation)"
                             r".{1,6}%s\s*$" % id, re.X | re.I)
        if Regex(r"\d{5,}").search(id) and comercial_re.search(subject):
            return False
        return True

    def check_illegal_chars(self, msg, header, ratio, count, target=None):
        """look for 8-bit and other illegal characters that should be MIME
        encoded, these might want to exempt languages that do not use
        Latin-based alphabets, but only if the user wants it that way
        """
        try:
            ratio = float(ratio)
        except ValueError:
            self.ctxt.log.warn("HeaderEval::Plugin check_illegal_chars "
                                  "invalid option: %s", ratio)
            return False
        try:
            count = int(count)
        except ValueError:
            self.ctxt.log.warn("HeaderEval::Plugin check_illegal_chars "
                                  "invalid option: %s", count)
            return False
        if header == 'ALL':
            raw_headers = msg.raw_headers
            key_headers = []
            for keys in raw_headers.keys():
                key_headers.append(keys)
            for key in key_headers:
                if key.lower() in ("subject", "from"):
                    try:
                        del raw_headers[key]
                    except KeyError:
                        pass
        else:
            raw_headers = {header: msg.get_raw_header(header)}

        # count illegal substrings (RFC 2045)
        # (non-ASCII + C0 controls except TAB, NL, CR)

        raw_str = ''.join([''.join(value) for value in raw_headers.values()])
        try:
            raw_str = raw_str.decode("utf-8")
        except AttributeError:
            # in Python 3 all string is unicode object
            pass
        clean_hdr = ''.join([i if ord(i) < 128 else '' for i in raw_str])
        illegal = len(raw_str) - len(clean_hdr)
        if illegal > 0 and header.lower() == "subject":
            exempt = 0
            # only exempt a single cent sign, pound sign, or registered sign
            for except_chr in (u'\xa2', u'\xa3', u'\xae'):
                if except_chr in raw_str:
                    exempt += 1
            if exempt == 1:
                illegal -= exempt
        if raw_str:
            return (illegal / len(raw_str)) >= ratio and illegal >= count
        else:
            return False

    def check_for_forged_hotmail_received_headers(self, msg, target=None):
        """Check for forged hotmail received headers"""
        self._check_for_forged_hotmail_received_headers(msg)
        return self.hotmail_addr_with_forged_hotmail_received

    def check_for_no_hotmail_received_headers(self, msg, target=None):
        """Check for no hotmail received headers"""
        self._check_for_forged_hotmail_received_headers(msg)
        return self.hotmail_addr_but_no_hotmail_received

    def _check_for_forged_hotmail_received_headers(self, msg):
        self.hotmail_addr_but_no_hotmail_received = 0
        self.hotmail_addr_with_forged_hotmail_received = 0
        rcvd = msg.msg.get("Received")
        if not rcvd:
            return False
        pickup_service_regex = Regex(r"from mail pickup service by hotmail"
                                     r"\.com with Microsoft SMTPSVC;")
        if pickup_service_regex.search(rcvd):
            return False
        if self.check_for_msn_groups_headers(msg):
            return False
        ip_header = msg.msg.get("X-ORIGINATING-IP")
        if ip_header and IP_ADDRESS.search(ip_header):
            FORGED_REGEX = Regex(
                r"from\s+(?:\S*\.)?hotmail.com\s+\(\S+\.hotmail("
                r"?:\.msn)?\.com[\)]|"
                r"from\s+\S*\.hotmail\.com\s+\(\[{IP_ADDRESS}\]|"
                r"from\s+\S+\s+by\s+\S+\.hotmail(?:\.msn)?\.com\s+with\s+ "
                r"HTTP\;|"
                r"from\s+\[66\.218.\S+\]\s+by\s+\S+\.yahoo\.com"
                r"".format(IP_ADDRESS=IP_ADDRESS.pattern), re.I | re.X)
            if FORGED_REGEX.search(rcvd):
                return False
        if self.gated_through_received_hdr_remover(msg):
            return False

        helo_hotmail_regex = Regex(r"(?:from |HELO |helo=)\S*hotmail\.com\b")
        if helo_hotmail_regex.search(rcvd):
            self.hotmail_addr_with_forged_hotmail_received = 1
        else:
            from_address = msg.msg.get("From")
            if not from_address:
                from_address = ""
            if "hotmail.com" not in from_address:
                return False
            self.hotmail_addr_but_no_hotmail_received = 1

    def check_for_msn_groups_headers(self, msg, target=None):
        """Check if the email's destination is a msn group"""
        to = ''.join(msg.get_decoded_header('To'))
        if not Regex(r"<(\S+)\@groups\.msn\.com>").search(to):
            return False
        listname = Regex(r"<(\S+)\@groups\.msn\.com>").match(to).groups()[0]
        server_rgx = Regex(r"from mail pickup service by "
                           r"((?:p\d\d\.)groups\.msn\.com)\b")
        server = ''
        for rcvd in msg.get_decoded_header('Received'):
            if server_rgx.search(rcvd):
                server = server_rgx.search(rcvd).groups()[0]
                break
        if not server:
            return False
        message_id = ''.join(msg.get_decoded_header('Message-Id'))
        if listname == "notifications":
            if not Regex(r"^<\S+\@{0}".format(server)).search(message_id):
                return False
        else:
            msn_addr = Regex(r"^<{0}-\S+\@groups\.msn\.com>".format(listname))
            if not msn_addr.search(message_id):
                return False
            msn_addr = "{0}-bounce@groups.msn.com".format(listname)
            if msg.sender_address != msn_addr:
                return False
        return True

    def check_for_forged_eudoramail_received_headers(self, msg, target=None):
        """Check if the email has forged eudoramail received header"""
        from_addr = ''.join(msg.get_all_addr_header("From"))
        if from_addr.rsplit("@", 1)[-1] != "eudoramail.com":
            return False
        rcvd = ''.join(msg.get_decoded_header("Received"))
        ip = ''.join(msg.get_decoded_header("X-Sender-Ip"))
        if ip and IP_ADDRESS.search(ip):
            ip = True
        else:
            ip = False
        if self.gated_through_received_hdr_remover(msg):
            return False
        if Regex(r"by \S*whowhere.com\;").search(rcvd) and ip:
            return False
        return True

    def check_for_forged_yahoo_received_headers(self, msg, target=None):
        """Check for forged yahoo received headers"""
        from_addr = ''.join(msg.get_all_addr_header("From"))
        rcvd = ''.join(msg.get_decoded_header("Received"))
        if "yahoo.com" not in from_addr:
            return False
        if (msg.get_decoded_header("Resent-From") and
                msg.get_decoded_header("Resent-To")):
            xrcvd = ''.join(msg.get_decoded_header("X-Received"))
            rcvd = xrcvd if xrcvd else rcvd

        if self.gated_through_received_hdr_remover(msg):
            return False
        for relay in msg.untrusted_relays + msg.trusted_relays:
            rdns = relay.get("rdns")
            if rdns and "yahoo.com" in rdns:
                return False
        if Regex(r"by web\S+\.mail\S*\.yahoo\.com via HTTP").search(rcvd):
            return False
        if Regex(r"by smtp\S+\.yahoo\.com with SMTP").search(rcvd):
            return False
        yahoo_ip_re = Regex(
            r"from\s+\[{}\]\s+by\s+\S+\."
            r"(?:groups|scd|dcn)\.yahoo\.com\s+with\s+NNFMP".format(
                IP_ADDRESS.pattern), re.X)
        if yahoo_ip_re.search(rcvd):
            return False
        if (Regex(r"\bmailer\d+\.bulk\.scd\.yahoo\.com\b").search(rcvd) and
                    from_addr.rsplit("@", 1)[-1] == "reply.yahoo.com"):
            return False
        if Regex("by \w+\.\w+\.yahoo\.com \(\d+\.\d+\.\d+\/\d+\.\d+\.\d+\)"
                 "(?: with ESMTP)? id \w+").search(rcvd):
            return False
        return True

    def check_for_forged_juno_received_headers(self, msg, target=None):
        from_addr = ''.join(msg.get_all_addr_header("From"))
        if not from_addr.rsplit("@", 1)[-1].endswith("juno.com"):
            return False
        if self.gated_through_received_hdr_remover(msg):
            return False
        xorig = ''.join(msg.get_decoded_header("X-Originating-IP"))
        xmailer = ''.join(msg.get_decoded_header("X-Mailer"))
        rcvd = ''.join(msg.get_decoded_header("Received"))
        if xorig != "":
            juno_re = Regex(r"from.*\b(?:juno|untd)\.com.*"
                            r"[\[\(]{0}[\]\)].*by".format(IP_ADDRESS.pattern), re.X)
            cookie_re = Regex(r" cookie\.(?:juno|untd)\.com ")
            if not juno_re.search(rcvd) and not cookie_re.search(rcvd):
                return True
            if "Juno " not in xmailer:
                return True
        else:
            mail_com_re = Regex(r"from.*\bmail\.com.*\[{}\].*by".format(
                IP_ADDRESS.pattern), re.X)
            untd_com_re = Regex(r"from\s+(webmail\S+\.untd"
                                r"\.com)\s+\(\1\s+\[{}\]\)\s+by".format(
                IP_ADDRESS.pattern), re.X)
            if mail_com_re.search(rcvd) and not Regex(r"\bmail\.com").search(
                    xmailer):
                return True
            elif untd_com_re.search(rcvd) and not Regex(
                    r"^Webmail Version \d").search(xmailer):
                return True
            else:
                return True
        return False

    def check_for_matching_env_and_hdr_from(self, msg, target=None):
        from_addr = ''.join(msg.get_all_addr_header("From"))
        envfrom = ""
        for relay in msg.trusted_relays + msg.untrusted_relays:
            if relay.get('envfrom'):
                envfrom = relay.get('envfrom')
                break
        return envfrom in from_addr

    def _parse_rcpt(self, addr):
        user = addr[:self.tocc_similar_count]
        try:
            fqhn = addr.rsplit("@", 1)[1]
        except IndexError:
            fqhn = addr
        host = fqhn[:self.tocc_similar_length]
        return user, fqhn, host

    def _check_recipients(self, msg):
        """Check for similar recipients addresses.

        Return the ratio of possibly similar recipient of
        the total number of possible combinations.
        """
        try:
            return self.get_local(msg, "tocc_similar")
        except KeyError:
            pass

        recipients = []
        for header_name in ("To", "Cc", "Bcc", "ToCc"):
            recipients.extend(msg.get_all_addr_header(header_name))

        if not recipients:
            self.set_local(msg, "tocc_similar", 0)
            self.set_local(msg, "tocc_sorted", False)
            return

        sorted_recipients = sorted(recipients)
        self.set_local(msg, "tocc_sorted", sorted_recipients == recipients)
        # Remove dupes IF they are next to each other
        addresses = [recipients[0]]
        for rcpt1, rcpt2 in zip(recipients, recipients[1:]):
            if rcpt1 == rcpt2:
                continue
            addresses.append(rcpt2)

        if len(addresses) < self.tocc_similar_count:
            self.set_local(msg, "tocc_similar", 0)
            return

        hits = 0
        combinations = 0
        for rcpt1, rcpt2 in itertools.combinations(addresses, 2):
            user1, fqhn1, host1 = self._parse_rcpt(rcpt1)
            user2, fqhn2, host2 = self._parse_rcpt(rcpt2)
            combinations += 1
            if user1 == user2:
                hits += 1
            if host1 == host2 and fqhn1 != fqhn2:
                hits += 1
        ratio = hits / combinations
        self.set_local(msg, "tocc_similar", ratio)
        return ratio

    def sorted_recipients(self, msg, target=None):
        """Matches if the recipients are sorted"""
        self._check_recipients(msg)
        return self.get_local(msg, "tocc_sorted")

    def similar_recipients(self, msg, minr=None, maxr=None,
                           target=None):
        """Matches if the similar recipients ratio is in the
        specified .

        :param minr: The minimum for the ratio
        :param maxr: The maximum for the ratio
        """
        ratio = self._check_recipients(msg)
        try:
            return (
                (minr is None or float(minr) < ratio) and
                (maxr is None or ratio < float(maxr))
            )
        except (TypeError, ValueError):
            return False

    def check_for_missing_to_header(self, msg, target=None):
        """Check if the To header is missing."""
        if msg.get_raw_header("To"):
            return False
        if msg.get_raw_header("Apparently-To"):
            return False
        return True

    def check_for_forged_gw05_received_headers(self, msg, target=None):
        gw05_re = Regex(r"from\s(\S+)\sby\s(\S+)\swith\sESMTP\;\s+\S\S\S,"
                        r"\s+\d+\s+\S\S\S\s+\d{4}\s+\d\d:\d\d:\d\d\s+[-+]*"
                        r"\d{4}", re.X | re.I)
        for rcv in msg.get_decoded_header("Received"):
            h1 = ""
            h2 = ""
            try:
                match = gw05_re.match(rcv)
                if match:
                    h1, h2 = match.groups()
                if h1 and h2 and h2 != ".":
                    return True
            except IndexError:
                continue
        return False

    def _parse_rfc822_date(self, date):
        try:
            parsed_date = email.utils.parsedate(date)
            time_in_seconds = time.mktime(parsed_date)
            date_time = datetime.datetime.utcfromtimestamp(
                time_in_seconds)
        except ValueError:
            return
        return date_time

    def _get_date_header_time(self, msg):
        try:
            return self.get_local(msg, "date_header_time")
        except KeyError:
            pass

        date_time = None
        for header in ["Resent-Date", "Date"]:
            dates = msg.get_decoded_header(header)
            for date in dates:
                date_time = self._parse_rfc822_date(date)
                if date_time:
                    break
        if date_time:
            self.set_local(msg, "date_header_time", date_time)
        else:
            self.set_local(msg, "date_header_time", -1)
        return date_time

    def _get_received_header_times(self, msg):
        try:
            return self.get_local(msg, "received_header_times")
        except KeyError:
            pass

        received_times = []
        self.set_local(msg, "received_header_times", received_times)

        date_re = Regex(r"(\s.?\d+ \S\S\S \d+ \d+:\d+:\d+ \S+)")
        for rcvd in msg.get_decoded_header("Received"):
            try:
                date = date_re.search(rcvd).group()
            except (AttributeError, TypeError):
                date = None
            if not date:
                continue
            self.ctxt.log.debug("eval: trying Received header date for "
                                "real time: %s", date)
            received_time = self._parse_rfc822_date(date)
            if received_time:
                received_times.append(received_time)
        return received_times

    def _check_date_diff(self, msg):
        try:
            return self.get_local(msg, "date_diff")
        except KeyError:
            pass

        self.set_local(msg, "date_diff", datetime.timedelta(0))

        date_header_time = self._get_date_header_time(msg)
        received_header_times = self._get_received_header_times(msg)

        diffs = []
        for received_header_time in received_header_times:
            diff = abs(received_header_time - date_header_time)
            if diff:
                diffs.append(diff)

        try:
            date_diff = sorted(diffs)[0]
            self.set_local(msg, "date_diff", date_diff)
            return date_diff
        except IndexError:
            self.set_local(msg, "date_diff", datetime.timedelta(0))
            return datetime.timedelta(0)

    def subject_is_all_caps(self, msg, target=None):
        """Checks if the subject is all capital letters.

        This eval rule ignore short subjects, one word subject and
        the prepended notations. (E.g. ``Re:``)
        """
        for subject in msg.get_decoded_header("Subject"):
            # Remove the Re/Fwd notations in the subject
            subject = Regex(r"^(Re|Fwd|Fw|Aw|Antwort|Sv):", re.I).sub("",
                                                                     subject)
            subject = subject.strip()
            if len(subject) < 10:
                # Don't match short subjects
                continue
            if len(subject.split()) == 1:
                # Don't match one word subjects
                continue
            if subject.isupper():
                return True
        return False

    def check_for_to_in_subject(self, msg, test, target=None):
        """
        Check if to address is in Subject field.

        If it is called with 'address', check if full address is in subject,
        else if the parameter is 'user', then check if user name is in subject.
        """
        full_to = msg.get_all_addr_header('To')
        if not full_to:
            return False
        subject = msg.msg.get('Subject', "")
        for to in full_to:
            if test == "address":
                subject_regex = Regex(r".*" + re.escape(to) + r".*", re.I)
                if subject_regex.search(subject):
                    return True
            elif test == "user":
                regex = re.match("(\S+)@.*", to)
                if regex:
                    to = regex.group(1)
                    if Regex(r"^" + re.escape(to) + "$").search(subject):
                        return True
                    if Regex(r"(?:re|fw):\s*(?:\w+\s+)?" + re.escape(to) + "$")\
                            .search(subject):
                        return True
                    if Regex(r"\s*" + re.escape(to) + "[,:;!?-]$")\
                            .search(subject):
                        return True
                    if Regex(r"^" + re.escape(to) + "\s*[,:;!?-](\s).*")\
                            .search(subject):
                        return True
        return False

    def check_outlook_message_id(self, msg, target=None):
        message_id = msg.msg.get("Message-ID")
        if not message_id:
            return
        msg_regex = Regex(r"^<[0-9a-f]{4}([0-9a-f]{8})\$[0-9a-f]{8}\$["
                          r"0-9a-f]{8}\@")
        regex = msg_regex.search(message_id)
        if not regex:
            return False
        timetocken = int(regex.group(1), 16)

        date = msg.msg.get("Date")
        x = 0.0023283064365387
        y = 27111902.8329849
        mail_date = time.mktime(email.utils.parsedate(date))
        expected = int((mail_date * x) + y)
        if abs(timetocken - expected) < 250:
            return False
        received = msg.msg.get("Received")
        received_regex = Regex(r"(\s.?\d+ \S\S\S \d+ \d+:\d+:\d+ \S+).*?$")
        regex = received_regex.search(received)
        received_date = 0
        if regex:
            received_date = time.mktime(email.utils.parsedate(regex.group()))
        expected = int((received_date * x) + y)
        return abs(timetocken - expected) >= 250

    def check_messageid_not_usable(self, msg, target=None):
        list_unsubscribe = msg.msg.get("List-Unsubscribe")
        if list_unsubscribe:
            if Regex(r"<mailto:(?:leave-\S+|\S+-unsubscribe)\@\S+>$").search(
                    list_unsubscribe):
                return True
        if self.gated_through_received_hdr_remover(msg):
            return True
        received = msg.msg.get("Received")
        if Regex(r"/CWT/DCE\)").search(received):
            return True
        if Regex(r"iPlanet Messaging Server").search(received):
            return True
        return False

    def check_header_count_range(self, msg, header, minr, maxr, target=None):
        """Check if the count of the header is withing the given range.
        The range is inclusive in both ranges.

        :param header: the header name
        :param minr: the minimum number of headers with the same name
        :param maxr: the minimum number of headers with the same name
        :return: True if the header count is withing the range.
        """
        raw_headers = set(msg.get_raw_header(header))
        return int(minr) <= len(raw_headers) <= int(maxr)

    def check_unresolved_template(self, msg, target=None):
        message = msg.raw_msg
        headers = message.split("\n")
        for header in headers:
            if Regex(r"%[A-Z][A-Z_-]").search(header) and not \
                    Regex(r"^(?:x-vms-to|x-uidl|x-face|to|cc|from|subject|"
                          r"references|in-reply-to|(?:x-|resent-|"
                          r"x-original-)?message-id):").search(header.lower()):
                return True
        return False

    def check_ratware_name_id(self, msg, target=None):
        """Check if message-id is ratware or not."""
        message_id = msg.msg.get("Message-Id")
        from_header = msg.msg.get("From")
        if not message_id and not from_header:
            return False
        regex = Regex(r"<[A-Z]{28}\.([^>]+?)>").search(message_id)
        if regex:
            if Regex(r"\"[^\"]+\"\s*<" + regex.group(1) + ">").search(
                    from_header):
                return True
        return False

    def check_in_TL_TLDS(self, address):
        if address in self["util_rb_tld"]:
            return True
        if address in self["util_rb_2tld"]:
            return True
        if address in self["util_rb_3tld"]:
            return True
        return False

    def is_domain_valid(self, domain):
        domain = domain.lower()
        if " " in domain:
            return False
        parts = domain.split(".")
        if len(parts) <= 1:
            return False
        elif not self.check_in_TL_TLDS(".".join(parts[1:])):
            return False
        return True

    def check_ratware_envelope_from(self, msg, target=None):
        """Check if envelope-from address is ratware or not."""
        to_header = msg.msg.get("To")
        envelope_from = msg.sender_address
        if not to_header or not envelope_from:
            return False
        if Regex(r"^SRS\d=").search(envelope_from):
            return False
        regex = Regex(r"^([^@]+)@(.+)$").search(to_header)
        if regex:
            user = regex.group(1)
            dom = regex.group(2)
            if not self.is_domain_valid(dom):
                return False
            if Regex(r"\b" + dom + "." + user + "@").search(envelope_from):
                return True
        return False

    def gated_through_received_hdr_remover(self, msg, target=None):
        """Check if the email is gated through ezmlm"""
        txt = ''.join(msg.get_decoded_header("Mailing-List"))
        rcvd = ''.join(msg.get_decoded_header("Received"))
        if Regex(r"^contact \S+\@\S+\; run by ezmlm$").search(txt):
            dlto = ''.join(msg.get_decoded_header("Delivered-To"))
            mailing_list_re = Regex(r"^mailing list \S+\@\S+")
            qmail_re = Regex(r"qmail \d+ invoked (?:from "
                             r"network|by .{3,20})\); \d+ ... \d+")
            if mailing_list_re.search(dlto) and qmail_re.search(rcvd):
                return True
        if not rcvd:
            return True
        if Regex(r"from groups\.msn\.com \(\S+\.msn\.com ").search(rcvd):
            return True
        return False

    def check_equal_from_domains(self, msg, target=None):
        """Check if the domain from `From` header and `EnvelopeFrom` header
        are different."""
        from_addr = ''.join(msg.get_all_addr_header("From"))
        envfrom = msg.sender_address
        if not envfrom or not from_addr:
            return False
        try:
            fromdomain = from_addr.rsplit("@", 1)[-1]
        except (IndexError, AttributeError):
            return False
        try:
            envfromdomain = envfrom.rsplit("@", 1)[-1]
        except (IndexError, AttributeError):
            return False
        self.ctxt.log.debug("eval: From 2nd level domain: %s, "
                            "EnvelopeFrom 2nd level domain: %s", fromdomain,
                            envfromdomain)
        if envfromdomain.lower() not in fromdomain.lower():
            return True
        return False

    def _check_date_received(self, msg):
        try:
            return self.get_local(msg, "date_received")
        except KeyError:
            pass

        all_times = self._get_received_header_times(msg) + [
            self._get_date_header_time(msg)
        ]
        median = int(len(all_times)/2)
        date_received = sorted(all_times, reverse=True)[median]
        self.set_local(msg, "date_received", date_received)
        return date_received

    def received_within_months(self, msg, min, max, target=None):
        """Check if the date from received is in past"""
        if min == "undef":
            min = None
        if max == "undef":
            max = None
        try:
            if min:
                min = int(min)
            if max:
                max = int(max)
        except ValueError:
            self.ctxt.log.warn("HeaderEval::Plugin received_within_months "
                               "min and max should be integer values")
            return False

        diff = relativedelta.relativedelta(
            datetime.datetime.utcnow(),
            self._check_date_received(msg)
        )

        number_months = (diff.year or 0) * 12 + (diff.months or 0)

        if ((not min or number_months >= min) and
                (not max or number_months < max)):
            return True
        return False

    def check_for_shifted_date(self, msg, min=None, max=None, target=None):
        """Check if the difference between Date header and date from received
        headers its between min,max interval

        * min: minimum time express in hours
        * max: maximum time express in hours
        """
        if min == "undef":
            min = None
        if max == "undef":
            max = None
        try:
            if min:
                min = int(min)
            if max:
                max = int(max)
        except ValueError:
            self.ctxt.log.warn("HeaderEval::Plugin check_for_shifted_date "
                               "min and max should be integer values")
            return False
        diff = int(self._check_date_diff(msg).total_seconds() / 3600)
        if ((not min or diff >= min) and
                (not max or diff < max)):
            return True
        return False
