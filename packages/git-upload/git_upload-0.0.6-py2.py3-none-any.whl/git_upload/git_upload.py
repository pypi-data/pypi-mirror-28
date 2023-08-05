#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from builtins import input
from os import path
import subprocess
import sys

args = sys.argv


def main(argv=sys.argv):
    if path.isfile('.gitreview'):
        # Gerrit
        git_review = ['git', 'review']
        git_review.extend(argv[1:])
        subprocess.call(git_review, stdout=sys.stdout)
    else:
        # GitHub or the other repositories
        if len(argv) == 1:
            # Assume that pushing the current branch to a origin repo
            git_rev_parse = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
            current_branch = subprocess.check_output(git_rev_parse)
            current_branch = current_branch.decode('utf-8').strip()
            query = "Do you really want to push '%s' to 'origin'? [Y/n] " \
                    % current_branch
            answer = input(query).lower()
            if answer.startswith('y') or answer.strip() == '':
                # Push the branch
                subprocess.call(['git', 'push', 'origin', current_branch],
                                stdout=sys.stdout)
            else:
                print('Canceled')
        else:
            git_push = ['git', 'push']
            git_push.extend(argv[1:])
            subprocess.call(git_push, stdout=sys.stdout)


if __name__ == '__main__':
    main()
