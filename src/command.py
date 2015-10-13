# coding: utf-8

import const, subprocess
import sys, os

def exec_list():
    for l in const.COLLECTION_LIST:
        print l
    return

def exec_grip(collection, date_from, date_to, profile):
    if os.path.exists(const.OUT_FILE):
        try:
            os.remove(const.OUT_FILE)
        except Exception, e:
            raise Exception(e)

    file_list = _fetch_file_list(collection, date_from, date_to, profile)
    for fname in file_list:
       _fetch_log_files(fname, collection, profile)

    list_str = " ".join([x[:-3] for x in file_list])
    _export_csv_files(list_str)
    _remove_log_files(list_str)
    return

def _fetch_file_list(collection, date_from, date_to, profile):
    cmd = "aws s3 ls s3://%s%s/ --profile %s | awk '{date = substr($4, 0, 10); if (date >= \"%s\" && date <= \"%s\") print $4}'" % (
       const.BUCKET_DIR,
       collection,
       profile,
       date_from,
       date_to
    )

    stdout_data, stderr_data = _exec_command(cmd)

    if stderr_data:
        raise Exception(stderr_data)

    return [x for x in stdout_data.split("\n") if x != ""]

def _fetch_log_files(fname, collection, profile):
    cmd = "aws s3 cp s3://%s%s/%s ./ --profile %s" % (
        const.BUCKET_DIR,
        collection,
        fname,
        profile
    )

    stdout_data, stderr_data = _exec_command(cmd)

    if stderr_data:
        raise Exception(stderr_data)

    stdout_data, stderr_data = _exec_command("gzip -d -f %s" % fname)

    if stderr_data:
        raise Exception(stderr_data)

    return True

def _export_csv_files(list_str):
    # 先頭のレコードのキーを信頼する（配列, オブジェクトは除く）
    cmd = "cat %s | head -n 1 | cut -f 3- | jq -r 'to_entries | [.[].key] | select(map(type) != \"array\" and map(type) != \"object\") | @csv' | sed -e 's/\"//g'" % list_str
    stdout_data, stderr_data = _exec_command(cmd)

    # Headerを書き込み
    f = open(const.OUT_FILE, "w")
    f.write(stdout_data)
    f.close()

    keys = ["\(.%s)" % str(x.rstrip()) for x in stdout_data.split(",")]
    key_query = ",".join(keys)

    cmd = "cat %s | cut -f 3- | jq \\\"\"%s\"\\\" | sed -e 's/\"//g' >> %s" % (
        list_str,
        key_query,
        const.OUT_FILE
    )
    stdout_data, stderr_data = _exec_command(cmd)

    return True

def _remove_log_files(list_str):
    stdout_data, stderr_data = _exec_command("rm -rf %s" % list_str)

    if stderr_data:
        raise Exception(stderr_data)

    return True

def _exec_command(cmd):
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    return proc.communicate()
