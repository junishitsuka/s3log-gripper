# coding: utf-8

import const
import subprocess

def exec_list():
    for l in const.COLLECTION_LIST:
        print l

def exec_grip(collection, date_from, date_to):
    file_list = get_file_list(collection, date_from, date_to)
    for fname in file_list:
        print fname

    return ""

def get_file_list(collection, date_from, date_to):
    cmd = "aws s3 ls s3://%s%s/ --profile cryptract | awk '{date = substr($4, 0, 10); if (date >= \"%s\" && date <= \"%s\") print $4}'" % (
       const.BUCKET_DIR, 
       collection,
       date_from,
       date_to
    )

    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    stdout_data, stderr_data = proc.communicate()
    return stdout_data.split("\n")
