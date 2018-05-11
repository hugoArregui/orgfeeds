#!/usr/bin/env python

from orgfeeds.feeds import OrgFeeds

import argparse

parser = argparse.ArgumentParser(description='Refresh an org feeds file')
parser.add_argument('--mark-as-new',
                    action='store_true',
                    help='mark new entries with NEW tag')
parser.add_argument('--forget-new',
                    action='store_true',
                    help='revemo NEW tag from existent entries')
parser.add_argument('file',
                    help='the org feeds file')

args = parser.parse_args()

OrgFeeds(args.file).refresh(mark_as_new=args.mark_as_new,
                            forget_new=args.forget_new)
