#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Provides utilities to post values to the display software, dopplerganger.
"""
from optparse import OptionParser
import socket


def connect_to_dopplerganger(host, port):
    """Connects to a host at `host` running dopplerganger on `port`.

    Returns a socket which can be used with ``.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def send_point(sock, x, y, z, t):
    """Sends a given point to the dopplerganger that `sock` is connected to.
    """
    message = _format_point(x, y, z, t)
    sock.sendall(message)


def _format_point(x, y, z, t):
    """Given a point to store (x, y, z, t), formats a message which can be
    sent over the wire to a dopplerganger service.
    """
    return "".join(("\t".join((x, y)), "\n"))


def define_options():
    parser = OptionParser()
    parser.add_option('--host', default='127.0.0.1', help="Host")
    parser.add_option('-p', '--port', default=12345, type=int, help="Port")
    return parser


if __name__ == "__main__":
    parser = define_options()
    options, _ = parser.parse_args()

    


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
