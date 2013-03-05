#!/usr/bin/python
"""
Provides a command line tool to synchronize web site redirects with an
Amazon S3 bucket.
"""

import os
import sys
import argparse
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError


def set_public_redirect(key, redirect_location):
    """Configure this key to redirect to another location.

    When the bucket associated with this key is accessed from the website
    endpoint, a 301 redirect will be issued to the specified
    `redirect_location`.

    :type redirect_location: string
    :param redirect_location: The location to redirect.

    (originally from boto)
    """
    headers = {'x-amz-website-redirect-location': redirect_location,
               'x-amz-acl': 'public-read',
              }
    response = key.bucket.connection.make_request('PUT', key.bucket.name,
                                                   key.name, headers)
    if response.status == 200:
        return True
    else:
        raise key.provider.storage_response_error(
            response.status, response.reason, response.read())


def clean_key_name(key_name, remove_slash=True, index="index.html"):
    """Remove slash from beginning and append index to end of key"""
    if remove_slash and key_name.startswith("/"):
        key_name = key_name[1:]
    if key_name.endswith("/"):
        key_name = key_name + index
    return key_name

def redirect_pairs(f, **kwargs):
    """Generates pairs (key, redirect) in given file"""
    for i, line in enumerate(f):
        line = line.strip()
        # ignore blank lines and comments
        if not line or line.startswith("#"):
            continue

        words = line.split()
        if len(words) < 2:
            sys.stderr.write(
              "Ignoring line {0}, missing redirect field\n".format(i+1))
            continue

        key, loc = clean_key_name(words[0], **kwargs), words[1]
        if not loc.startswith(('/', 'http://', 'https://')):
            sys.stderr.write(
              "Ignoring line {0}, invalid redirect: {1}\n".format(i+1, loc))
            continue

        if len(words) > 2:
            sys.stderr.write(
              "Ignoring extra fields in line {0}: {1}\n".format(
                i+1, " ".join(words[2:])))

        yield key, loc

def upload_redirects(redirects, bucket, remote_keys, dry=False):
    """Pop redirects from remote_keys and upload"""
    for local_key, location in redirects:
        exists = bool(local_key in remote_keys)
        if exists:
            key = remote_keys.pop(local_key)
        else:
            key = bucket.new_key(local_key)

        # don't re-upload identical redirects
        if exists and location == key.get_redirect():
            continue

        if not dry:
            set_public_redirect(key, location)
        print "{2:<6} {0} {1}".format(
          local_key, location, "update" if exists else "new")

def sync_redirects(redirects, bucket, delete=False, dry=False):
    """Do the syncing"""
    remote_keys = {key.name: key for key in bucket.list()}
    upload_redirects(redirects, bucket, remote_keys, dry=dry)

    if delete:
        for key in remote_keys.values():
            # assume all size-non-zero keys aren't redirects to save requests
            redirect = key.get_redirect() if key.size == 0 else None
            if redirect is None:
                continue
            if not dry:
                key.delete()
            print "delete {0} {1}".format(key.name, redirect)

def connection(filename="~/.awssecret"):
    """Creates a connection to S3 using data stored in text file"""
    with open(os.path.expanduser(filename)) as f:
        access, secret = [s.strip() for s in f.readlines()[:2]]
    return S3Connection(access, secret)

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Sync a list of redirects to an Amazon S3 bucket",
        epilog="Amazon access key and secret key should be stored on\
        the first and second lines of the key file.")
    parser.add_argument("redirects",
        help="file containing list of key names and redirect locations,\
        separated by a space and listed one per line",
        type=argparse.FileType('r'))
    parser.add_argument("bucket", help="name of Amazon S3 bucket")
    parser.add_argument("-d", "--delete", action="store_true",
        help="also delete all redirects not listed in redirects file")
    parser.add_argument("-n", "--dry-run", action="store_true",
        help="display changes to be made without actually making them")
    parser.add_argument("--key", metavar="file", default="~/.awssecret",
        type=str, help="use specified key file (default ~/.awssecret)")

    args = parser.parse_args()
    try:
        conn = connection(filename=args.key)
    except IOError, ValueError:
        sys.exit('Unable to read key file: {0}'.format(args.key))

    try:
        bucket = conn.get_bucket(args.bucket)
    except S3ResponseError as err:
        return '{status} {reason}\n{error_message}'.format(**err.__dict__)

    if args.dry_run:  print "This is a dry run"
    sync_redirects(redirects=redirect_pairs(args.redirects),
                   bucket=bucket,
                   delete=args.delete,
                   dry=args.dry_run)

if __name__ == "__main__":
    sys.exit(main())
