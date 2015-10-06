# coding: utf-8

import const, subprocess


def exec_list():
    for l in const.COLLECTION_LIST:
        print l
    return


def exec_grip(collection, date_from, date_to):
    file_list = _fetch_file_list(collection, date_from, date_to)
    for fname in file_list:
       _fetch_log_files(fname, collection)

    list_str = " ".join([x[:-3] for x in file_list])
    _export_csv_files(list_str)
    _remove_log_files(list_str)
    return


def _fetch_file_list(collection, date_from, date_to):
    # TODO: awscliのprofileをオプションで指定できるようにする
    cmd = "aws s3 ls s3://%s%s/ | awk '{date = substr($4, 0, 10); if (date >= \"%s\" && date <= \"%s\") print $4}'" % (
       const.BUCKET_DIR, 
       collection,
       date_from,
       date_to
    )

    stdout_data, stderr_data = _exec_command(cmd)

    if stderr_data:
        raise Exception(stderr_data)

    return [x for x in stdout_data.split("\n") if x != ""]


def _fetch_log_files(fname, collection):
    # TODO: awscliのprofileをオプションで指定できるようにする
    cmd = "aws s3 cp s3://%s%s/%s ./" % (
        const.BUCKET_DIR,
        collection,
        fname
    )

    stdout_data, stderr_data = _exec_command(cmd)

    if stderr_data:
        raise Exception(stderr_data)

    stdout_data, stderr_data = _exec_command("gzip -d -f %s" % fname)

    if stderr_data:
        raise Exception(stderr_data)

    return True


def _export_csv_files(list_str):
    cmd = "cat %s | cut -f 3- | jq -r 'to_entries | [.[].key] | @csv' | head -n 1 > %s" % (
        list_str,
        const.OUT_FILE
    )
    stdout_data, stderr_data = _exec_command(cmd)

    cmd = "cat %s | cut -f 3- | jq -r 'to_entries | [.[].value] | @csv' >> %s" % (
        list_str,
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
