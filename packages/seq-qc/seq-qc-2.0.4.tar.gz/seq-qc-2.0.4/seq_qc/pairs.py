class UnpairedReadsError(ValueError):
    def __init__(self, msg, r1, r2):
        super(ValueError, self).__init__(msg)
        self.r1 = r1
        self.r2 = r2


def verify_paired(record1, record2):
    """Check if the two sequence records belong to the same fragment.

    In an matching pair the records are left and right pairs
    of each other, respectively.  Returns True or False as appropriate.

    Handles both Casava formats: seq/1 and seq/2, and 'seq::... 1::...'
    and 'seq::... 2::...'.
    """
    l_name, l_desc = (record1.id, record1.description)
    r_name, r_desc = (record2.id, record2.description)

    # handle 'name/1'
    if l_name.endswith('/1') and r_name.endswith('/2'):
        subpart1 = l_name.split('/', 1)[0]
        subpart2 = r_name.split('/', 1)[0]

        if subpart1 and (subpart1 == subpart2):
            return True

    # handle '@name 1:rst'
    elif l_name == r_name and l_desc.startswith('1:') and \
        r_desc.startswith('2:'):
        return True

    # handle no description
    elif l_name == r_name:
        return True

    return False
