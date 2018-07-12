#!/usr/bin/env python

import transmissionrpc
import pdb
import argparse


class TransmissionAutomation(object):
    """docstring for automation."""

    def __init__(self, host, user, password):
        super(TransmissionAutomation, self).__init__()
        self.transmissionClient = transmissionrpc.Client(
            host,
            user=user,
            password=password
        )
    def __getUnfinishedTorrents(self):
        notFinishedTorrentList = []
        trList = self.transmissionClient.get_torrents()
        for tr in trList:
            if tr.progress < 100:
                notFinishedTorrentList.append(tr)
        return notFinishedTorrentList
    def unfinishedTorrents(self):
        for tr in self.__getUnfinishedTorrents():
            print("%s --- %s" %(tr.name, tr.progress))

    def startUnfinishedTorrents(self):
        for tr in self.__getUnfinishedTorrents():
            print("starting ... \n%s --- %s" %( tr.name, tr.progress))
            self.transmissionClient.start_torrent(tr.id)

    def stopAllTorrent(self):
        for tr in self.transmissionClient.get_torrents():
            print("stoping ... \n%s --- %s" %( tr.name, tr.progress))
            self.transmissionClient.stop_torrent(tr.id)
        pass

class TrNamespace:
    def init(self):
        self.tr = TransmissionAutomation(self.address,
             self.user,
            self.passwd)
    def list(self):
        self.init()
        self.tr.unfinishedTorrents()
    def start(self):
        self.init()
        self.tr.startUnfinishedTorrents()
    def stop(self):
        self.init()
        self.tr.stopAllTorrent()



if __name__ == '__main__':
    trn = TrNamespace()
    parser = argparse.ArgumentParser(
        description="Start and Stop Torrnts",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument(
        "--address",'-a',
        default="127.0.0.1",
        help="transmission address"
        )
    parser.add_argument("--user",'-u')
    parser.add_argument("--passwd",'-p')
    subParser = parser.add_subparsers()
    startParser = subParser.add_parser("start")
    startParser.set_defaults(func=trn.start)
    stopParser = subParser.add_parser("stop")
    stopParser.set_defaults(func=trn.stop)
    listParser = subParser.add_parser("list")
    listParser.set_defaults(func=trn.list)
    listParser.add_argument("--all")

    args = parser.parse_args(namespace=trn)
    args.func()
