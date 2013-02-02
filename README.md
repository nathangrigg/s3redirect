Provides a command line tool to synchronize web site redirects with an
Amazon S3 bucket.

# Installation

Using pip:

    pip install s3redirect

You can also use `easy_install`, download the source and run
`python setup.py install`, or use `s3redirect.py` as a standalone script.

# Usage

From the command line:

    s3redirect [options] redirects bucket

The script takes two arguments:

- `redirects`: a file containing a list of key names and redirect locations,
separated by a space and listed one per line
- `bucket`: name of Amazon S3 bucket

For more information, run `s3redirect --help`.

# What it does

The S3 bucket is examined, any new redirects are set, and any modified
redirects are updated. With the `--delete` option, all other redirects
are removed from the server. Regular files (that do not send a redirect
header) are not deleted.

If there is already a file in your bucket with the same name as one of
your redirects, the file will be overwritten.


# The redirect file

Each line of the redirect field
should have two fields with a space between them.
The first field contains the S3 key which should contain the redirect.
The second field contains the redirect location, which must begin with
`/`, `http://`, or `https://`.

Example:

    old-blog/ /new-blog/
    google.html http://google.com
    2001/resolutions.html http://en.wikipedia.org/wiki/Resolution

Note that regular expressions and wildcards are not allowed.

# Amazon Credentials

The script reads your Amazon credentials from a file; `~/.awssecret` by default.
The first line should be your access key and the second should be your
secret key.

# Using s3redirect with another sync tool

This script will only add and remove redirects, so it is safe to use alongside
another sync tool. If the other sync tool deletes files from the bucket that
have been removed from the local disk, the redirects may be deleted each time
the other sync tool is used.

One workaround is to create an empty file in the position of each redirect.
Under most circumstances, this will prevent other tools from deleting the
redirects that s3redirect creates.
