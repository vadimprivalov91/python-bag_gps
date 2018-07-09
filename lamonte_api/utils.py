__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"


import random
import string


def random_string():
    n = 6
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def random_email():
    account = random_string().lower()
    server = random_string().lower()
    return "%s@%s.com" % (account, server)
