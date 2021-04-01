'''
IDChecker

Usage:
    idchecker login <1password_url> <useranme>
    idchecker check [--vault=<vault_name>] [--dir=<path>] [--notes]
    idchecker -h | --help
    idchecker -v | --version

Options:
    --vault=<vault_name>            The name of the 1Password vault where the IDs are stored (it is better to frame the name with quotation marks)
    --dir=<path>                    The path to the folder where the report_<datetime>.csv file will be saved
    --notes                         Add notes from the ID record to the report
    -h, --help                      Show this help message.
    -v, --version                   Show the version.
'''

from docopt import docopt
from datetime import datetime

import subprocess
import platform
import json
import csv
import sys
import os


DEFAULT_VAULT = "SE&TS Shared OPs"
DEFAULT_FILTER_TAG = "IDChecker"
DEFAULT_W3_FILTER_TAG = "w3 IDs"
DEFAULT_OWNER = "L2 Support"


def get_exec_path():
    sys_case = {
        "Linux": "op_linux",
        "Darwin": "op_darwin"
    }
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        sys_case[platform.system()]
    )


def safe_print(text):
    print("\x1b[2K\r{}".format(text))


def exec_cmd(command, **kwargs):
    out = subprocess.run(command, shell=True, **kwargs)
    r_msg = out.stdout
    if out.returncode:
        r_msg = out.stderr
        if "TLS handshake timeout" in r_msg:
            return exec_cmd(command, **kwargs)
    if not r_msg is None:
        return out.returncode, r_msg.decode()
    return r_msg


def check_err(r_code, result):
    if r_code:
        if "You are not currently signed in" in result:
            print("You should log in before start using idchecker.\nPlease run `idchecker --help` for instructions")
        else:
            print(" ".join(result.split(" ")[3:]))
        return
    return result


def print_format(json):
    for item in json:
        for _, k in enumerate(item):
            print("{}: {}".format(k, item[k]))
        print("{}".format("—" * int(os.popen('stty size', 'r').read().split(" ")[1])))


def json_to_csv(json, path):
    path = os.path.abspath(os.path.join(
        path,
        "report_{}.csv".format(str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")))
    ))
    with open(path, "w") as file:
        wr = csv.writer(file)
        wr.writerow(json[0].keys())
        for item in json:
            wr.writerow(item.values())
    file.close()


def get_record_title(object):
    return object.get("overview").get("title")


def get_record_exp(object):
    section = [item for item in object["details"]["sections"] if "expiry" in item["title"].lower() and not item.get("fields") is None]
    if len(section) == 0:
        safe_print("WARNING: this record does not match the expected format - '{}'\n".format(object["overview"]["title"]))
        return None
    section = section[0]

    field = [item for item in section["fields"] if "expiry date" in item["t"].lower()]
    if len(field) == 0:
        return None
    field = field[0]
    exp = field.get("v")
    if not type(exp) is int:
        safe_print("WARNING: this record does not match the expected format - '{}'\n".format(object["overview"]["title"]))
    return exp


def get_record_owner(object):
    global DEFAULT_OWNER
    global DEFAULT_W3_FILTER_TAG
    owner = DEFAULT_OWNER
    w3_tag = DEFAULT_W3_FILTER_TAG

    if not w3_tag in object["overview"]["tags"]:
        return owner

    section = [item for item in object["details"]["sections"] if "OWNER" in item["title"]]
    if len(section) == 0:
        safe_print("WARNING: this record does not match the expected format - '{}'\n".format(object["overview"]["title"]))
        return None
    section = section[0]

    field = section.get("fields")
    if field is None or len(field) == 0:
        return None
    field = field[0]
    owner = "{} ({})".format(field.get("t"), field.get("v"))
    return owner


def get_record_notes(object):
    return object.get("details").get("notesPlain")


def sort_list(records):
    broken = []
    idxs = []
    for i, record in enumerate(records):
        if record["expire"] is None or not type(record["expire"]) is int:
            broken.append(record)
            idxs.append(i)
    idxs.reverse()
    for i in idxs:
        records.pop(i)

    if not len(records) == 0:
        records.sort(key = lambda record:record["expire"])
    for record in records:
        record["expire"] = str(datetime.utcfromtimestamp(record["expire"]).strftime('%Y/%m/%d'))
    records = broken + records
    return records


def filter_by_tag(items, notes):
    global DEFAULT_FILTER_TAG
    tag = DEFAULT_FILTER_TAG
    print("2. Filtering the list by the '{}' tag".format(tag))
    items = [item["uuid"] for item in items if tag in item["overview"]["tags"]]
    print("Done. The number of filtered records: {}".format(len(items)))
    return items


def get_full_list(items, notes):
    print("3. Getting full information about filtered records")
    records = []
    # added visualization of the process to make it not so boring
    width = int(os.popen('stty size', 'r').read().split(" ")[1])
    n = len(items)
    for i, item in enumerate(items):
        idx = i + 1
        prefix = " {}% | ".format(round(idx / n * 100))
        sys.stdout.write("\r{}{}".format(prefix, "█" * int((width - len(prefix)) / n * idx)))
        ###

        r_code, result = exec_cmd(
            "{} get item {}".format(get_exec_path(), item), capture_output=True
        )
        result = check_err(r_code, result)
        if result is None: return result
        obj = json.loads(result)

        record = {
            "title": get_record_title(obj),
            "expire": get_record_exp(obj),
            "ID revalidation owner": get_record_owner(obj)
        }
        if notes:
            record["notes"] = get_record_notes(obj)
        records.append(record)
    print("\n")
    return records


def get_list(vault, notes):
    print("1. Getting a list of all records")
    r_code, result = exec_cmd(
        "{} list items --vault \"{}\"".format(get_exec_path(), vault),
        capture_output=True
    )
    result = check_err(r_code, result)
    if result is None: return result
    result = json.loads(result)
    print("Done")
    result = filter_by_tag(result, notes)
    result = get_full_list(result, notes)
    result = sort_list(result)
    return result


def login(url, username):
    exec_cmd(
        "{} signin {} {}".format(get_exec_path(), url, username)
    )


def main():
    args = docopt(__doc__, version='1.1.2')
    if args["login"]:
        login(args["<1password_url>"], args["<useranme>"])
    elif args["check"]:
        if not args["--dir"] is None:
            if not os.path.exists(args["--dir"]):
                print("The provided path don't exists")
                sys.exit(1)
            if not os.path.isdir(args["--dir"]):
                print("The provided path is not a directory")
                sys.exit(1)

        vault = DEFAULT_VAULT
        notes = False
        if not args["--vault"] is None:
            vault = args["--vault"]
        if args["--notes"]:
            notes = True
        result = get_list(vault, notes)

        if not result is None:
            if not args["--dir"] is None:
                json_to_csv(result, args["--dir"])
            else:
                print_format(result)
