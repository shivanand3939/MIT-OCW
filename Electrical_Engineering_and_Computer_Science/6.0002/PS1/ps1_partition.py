# From codereview.stackexchange.com                    
def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        #print 'mahi', i
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
            #print 'virat', i
        #print 'virat', parts[1], parts[0]
        for b in partitions(parts[1]):
            #print 'kohli' , b   
            #print b, parts[1]
            yield [parts[0]]+b

def get_partitions(set_):
    for partition in partitions(set_):
        #print partition, 'ssss'
        yield [list(elt) for elt in partition]
