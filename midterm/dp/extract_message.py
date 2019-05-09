'''
Created on Oct 27, 2017

@author: tvandrun
'''

#####################
#
# Usage:
#    python extract_message.py msg1 msg2
#
#  where msg1 and msg2 are two multi-word messages delimited by
# quotation marks, for example:
#
#      python extract_message.py "CALL OFF THE ATTACK WAIT AT CURRENT LOCATION TIL DAWN" "ENEMY WILL NOT ATTACK AT POSITION BETWEEN DAWN AND NOON"
#
########################

import sys

msg1 = sys.argv[1].split(' ')
msg2 = sys.argv[2].split(' ')

# The next two lines demonstrats what msg1 and msg2 are.
# You may delete them when you write your solution

print msg1
print msg2


def longest_common_subsequence(a, b) :
    return None

print longest_common_subsequence(msg1, msg2)
