#!/usr/bin/env python3

'''
This is a script for demostrating how ACL works

THANKS:

- gfwlist: https://github.com/gfwlist/gfwlist
- gfwlist.acl: https://github.com/NateScarlet/gfwlist.acl
- china_ip_list: https://github.com/17mon/china_ip_list
'''

from urllib import request, parse
import logging
import sys
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GFW_TRANSLATED_URL = "https://raw.githubusercontent.com/NateScarlet/gfwlist.acl/master/gfwlist.acl.json"
CHINA_IP_LIST_URL = "https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt"


def fetch_url_content(url):
    logger.info("FETCHING {}".format(url))
    r = request.urlopen(url)
    return r.read()


def write_gfw_list(fp):
    gfw_json = fetch_url_content(GFW_TRANSLATED_URL)
    gfw_obj = json.loads(gfw_json)
    for line in gfw_obj["blacklist"]:
        fp.write(line.encode("utf-8"))
        fp.write(b"\n")


def write_china_ip(fp):
    china_ip_list = fetch_url_content(CHINA_IP_LIST_URL)
    fp.write(china_ip_list)


try:
    output_file_path = sys.argv[1]
except:
    output_file_path = "shadowsocks.acl"

logger.info("WRITING {}".format(output_file_path))

with open(output_file_path, 'wb') as fp:
    now = datetime.now()

    fp.write(b"# Generated by genacl.py\n")
    fp.write("# Time: {}\n".format(now.isoformat()).encode("utf-8"))
    fp.write(b"\n")

    fp.write(b"[proxy_all]\n")
    fp.write(b"\n[proxy_list]\n")
    write_gfw_list(fp)
    fp.write(b"\n[bypass_list]\n")
    write_china_ip(fp)

logger.info("DONE")
