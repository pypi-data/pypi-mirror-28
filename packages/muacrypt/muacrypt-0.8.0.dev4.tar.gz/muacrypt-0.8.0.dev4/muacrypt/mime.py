# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab

"""Mime message parsing and manipulation functions for Autocrypt usage. """

from __future__ import unicode_literals, print_function
import email.parser
import base64
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import six


def encode_binary_keydata(keydata):
    assert isinstance(keydata, bytes)
    key = base64.b64encode(keydata)
    if isinstance(key, bytes):
        key = key.decode("ascii")
    return key


def decode_keydata(ascii_keydata):
    return base64.b64decode(ascii_keydata)


def make_ac_header_value(addr, keydata, prefer_encrypt="nopreference", keytype="1"):
    assert keydata
    key = base64.b64encode(keydata) if isinstance(keydata, bytes) else keydata
    if isinstance(key, bytes):
        key = key.decode("ascii")
    l = ["addr=" + addr]
    if prefer_encrypt != "nopreference":
        l.append("prefer-encrypt=" + prefer_encrypt)
    if keytype != "1":
        l.append("type=" + keytype)
    l.append("keydata=\n" + indented_split(key))
    return "; ".join(l)


def indented_split(value, maxlen=78, indent="  "):
    assert "\n" not in value
    l = []
    for i in range(0, len(value), maxlen):
        l.append(indent + value[i:i + maxlen] + "\n")
    return "".join(l).rstrip()


def get_target_emailadr(msg):
    l = []
    tos = msg.get_all("to") + (msg.get_all("cc") or [])
    for realname, emailadr in email.utils.getaddresses(tos):
        l.append(emailadr)
    return l


def parse_email_addr(string):
    """ return a (prefix, emailadr) tuple. """
    prefix, emailadr = email.utils.parseaddr(string)
    if isinstance(emailadr, bytes):
        emailadr = six.text_type(emailadr)
    return prefix, emailadr


def parse_message_from_file(fp):
    return email.parser.Parser().parse(fp)


def parse_message_from_string(string):
    stream = six.StringIO(string)
    return parse_message_from_file(stream)


def parse_one_ac_header_from_string(string):
    msg = parse_message_from_string(string)
    return parse_one_ac_header_from_msg(msg)


def parse_all_ac_headers_from_msg(msg):
    autocrypt_headers = msg.get_all("Autocrypt") or []
    return [parse_ac_headervalue(inb) for inb in autocrypt_headers if inb]


def parse_one_ac_header_from_msg(msg):
    all_results = parse_all_ac_headers_from_msg(msg)
    if len(all_results) == 1:
        return all_results[0]
    if len(all_results) > 1:
        raise ValueError("more than one Autocrypt header\n%s" %
                         "\n".join(msg.get_all("Autocrypt")))
    return {}


def parse_ac_headervalue(value):
    """ return a autocrypt attribute dictionary parsed
    from the specified autocrypt header value.  Unspecified
    default values for prefer-encrypt and the key type are filled in."""
    parts = value.split(";")
    result_dict = {"prefer-encrypt": "nopreference", "type": "1"}
    for x in parts:
        kv = x.split("=", 1)
        name, value = [x.strip() for x in kv]
        if name == "keydata":
            value = "".join(value.split())
        result_dict[name] = value
    return result_dict


def verify_ac_dict(ac_dict):
    """ return a list of errors from checking the autocrypt attribute dict.
    if the returned list is empty no errors were found.
    """
    l = []
    for name in ac_dict:
        if name not in ("keydata", "addr", "type", "prefer-encrypt") and name[0] != "_":
            l.append("unknown critical attr '{}'".format(name))
    # keydata_base64 = "".join(ac_dict["keydata"])
    # base64.b64decode(keydata_base64)
    if "type" not in ac_dict:
        l.append("type missing")
    if "keydata" not in ac_dict:
        l.append("keydata missing")
    if ac_dict["type"] != "1":
        l.append("unknown key type '%s'" % (ac_dict["type"], ))
    if ac_dict["prefer-encrypt"] not in ("nopreference", "mutual"):
        l.append("unknown prefer-encrypt setting '%s'" %
                 (ac_dict["prefer-encrypt"]))
    return l


def gen_mail_msg(From, To, _extra=None, Autocrypt=None, Subject="testmail",
                 Date=None, _dto=False, MessageID=None, body='Autoresponse'):
    assert isinstance(To, (list, tuple))
    if MessageID is None:
        MessageID = make_msgid()

    # prefer plain ascii mails to keep mail files directly readable
    # without base64-decoding etc.
    charset = None
    assert isinstance(body, six.text_type)
    try:
        msg = body.encode("ascii")
    except UnicodeEncodeError:
        charset = "utf-8"
    msg = MIMEText(body, _charset=charset)

    msg['Message-ID'] = MessageID
    msg['From'] = From
    msg['To'] = ",".join(To)
    msg['Subject'] = Subject
    msg['Date'] = Date or formatdate()
    if _extra:
        for name, value in _extra.items():
            msg.add_header(name, value)
    if _dto:
        msg["Delivered-To"] = To[0]
    if Autocrypt:
        msg["Autocrypt"] = Autocrypt
    return msg


def decrypt_message(msg, bingpg):
    # this method is not tested through the test suite
    # currently because we lack a way to generate proper
    # encrypted messages
    ctype = msg.get_content_type()
    assert ctype == "multipart/encrypted"
    parts = msg.get_payload()
    meta, enc = parts
    assert meta.get_content_type() == "application/pgp-encrypted"
    assert enc.get_content_type() == "application/octet-stream"

    dec, err = bingpg.decrypt(enc.get_payload())
    dec_msg = parse_message_from_string(dec)
    for name, val in msg.items():
        if name.lower() in ("content-type", "content-transfer-encoding"):
            continue
        dec_msg.add_header(name, val)
    return dec_msg, err


# adapted from ModernPGP:memoryhole/generators/generator.py which
# was adapted from notmuch:devel/printmimestructure
def render_mime_structure(msg, prefix='└'):
    '''msg should be an email.message.Message object'''
    stream = six.StringIO()
    mcset = str(msg.get_charset())
    fname = '' if msg.get_filename() is None else ' [' + msg.get_filename() + ']'
    cset = '' if mcset is None else ' ({})'.format(mcset)
    disp = msg.get_params(None, header='Content-Disposition')
    if (disp is None):
        disposition = ''
    else:
        disposition = ''
        for d in disp:
            if d[0] in ['attachment', 'inline']:
                disposition = ' ' + d[0]

    if 'subject' in msg:
        subject = ' (Subject: %s)' % msg['subject']
    else:
        subject = ''
    if (msg.is_multipart()):
        print(prefix + '┬╴' + msg.get_content_type() + cset +
              disposition + fname, str(len(msg.as_string())) +
              ' bytes' + subject, file=stream)
        if prefix.endswith('└'):
            prefix = prefix.rpartition('└')[0] + ' '
        if prefix.endswith('├'):
            prefix = prefix.rpartition('├')[0] + '│'
        parts = msg.get_payload()
        i = 0
        while (i < len(parts) - 1):
            print(render_mime_structure(parts[i], prefix + '├'), file=stream)
            i += 1
        print(render_mime_structure(parts[i], prefix + '└'), file=stream)
        # FIXME: show epilogue?
    else:
        print(prefix + '─╴' + msg.get_content_type() + cset + disposition +
              fname, msg.get_payload().__len__().__str__(),
              'bytes' + subject, file=stream)
    return stream.getvalue().rstrip()
