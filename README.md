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
