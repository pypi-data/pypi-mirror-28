#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import hashlib
import os
import sys

CHUNK_SIZE = 2**12

def compute_hashs(file_path_list, algorithm):
    """TODO
    """
    if algorithm not in ["md5", "sha1", "sha256", "sha512"]:
        print("Unknown algorithm", file=sys.stderr)
        sys.exit(1)

    for file_path in file_path_list:
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as fd:
                try:
                    if algorithm == "md5":
                        hash_generator = hashlib.md5()
                    elif algorithm == "sha1":
                        hash_generator = hashlib.sha1()
                    elif algorithm == "sha256":
                        hash_generator = hashlib.sha256()
                    elif algorithm == "sha512":
                        hash_generator = hashlib.sha512()
                    else:
                        raise ValueError("Unknown algorithm")

                    data = fd.read(CHUNK_SIZE)
                    while len(data) > 0:
                        hash_generator.update(data)
                        data = fd.read(CHUNK_SIZE)
                except:
                    print("{}: unknown error".format(file_path), file=sys.stderr)
                finally:
                    fd.close()

                hash_str = hash_generator.hexdigest()
                print("{}  {}".format(hash_str, file_path))
        else:
            if os.path.isdir(file_path):
                print('"{}" is a directory'.format(file_path), file=sys.stderr)
            else:
                print("unable to read {}".format(file_path), file=sys.stderr)

def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Print or check MD5 or SHA checksums.')

    parser.add_argument("--algorithm", "-a", required=True, metavar="STRING",
            help='the algorithm to use ("md5", "sha1", "sha256" or "sha512")')
    parser.add_argument("filepaths", nargs='+', metavar="FILE",
            help="the file(s) to check")

    args = parser.parse_args()

    compute_hashs(args.filepaths, algorithm=args.algorithm)

def md5():
    """Main MD5 function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Print or check MD5 checksums.')

    parser.add_argument("filepaths", nargs='+', metavar="FILE",
            help="the file(s) to check")

    args = parser.parse_args()

    compute_hashs(args.filepaths, algorithm="md5")

def sha1():
    """Main SHA1 function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Print or check SHA1 checksums.')

    parser.add_argument("filepaths", nargs='+', metavar="FILE",
            help="the file(s) to check")

    args = parser.parse_args()

    compute_hashs(args.filepaths, algorithm="sha1")

def sha256():
    """Main SHA256 function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Print or check SHA256 checksums.')

    parser.add_argument("filepaths", nargs='+', metavar="FILE",
            help="the file(s) to check")

    args = parser.parse_args()

    compute_hashs(args.filepaths, algorithm="sha256")

def sha512():
    """Main SHA512 function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='Print or check SHA512 checksums.')

    parser.add_argument("filepaths", nargs='+', metavar="FILE",
            help="the file(s) to check")

    args = parser.parse_args()

    compute_hashs(args.filepaths, algorithm="sha512")

if __name__ == '__main__':
    main()

