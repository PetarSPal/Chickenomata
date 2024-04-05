# from collections import UserList

class Oumbellatum():
    def __init__(self, nodes, n=2):
        #TODO: add autofill logic (binary,collection -> tree)
        #TODO: add testing framework
        self._n = n
        self.nodes = nodes
        self.next = None
        self.prev = None
        self._depth = 1
        types = set(map(type, nodes))
        leaf, master = types <= {int}, types <= {Oumbellatum}
        if len(self) != n:
            raise ValueError(f"Invalid length {len(self)} for n={n}")
        if not (master or leaf):
            raise ValueError(f"Invalid data types {types}, uniform int or Oumbellatum expected")
        if master and not (ns := set(node._n for node in nodes)) <= {n}:
            raise ValueError(f"Invalid child n values: {ns} for n={n}")
        if master:
            self._depth = nodes[0]._depth + 1
        #Consider separating nodes to separate stem/leaf/bulb types
        branchnodes = nodes
        if self._depth == 2:
            branchnodes[0].next = branchnodes[1]
            branchnodes[-1].prev = branchnodes[-2]
            for idx in range(1, n-1):
                branchnodes[idx].prev = branchnodes[idx-1]
                branchnodes[idx].next = branchnodes[idx+1]
        elif self._depth >= 3:
            # while not branchnodes[0].leaf:
            depthnodes = [branchnodes[0][-1]]
            for idx in range(1, n-1):
                depthnodes.append(branchnodes[idx][0])
                depthnodes.append(branchnodes[idx][-1])
            depthnodes.append(branchnodes[-1][0])
            branchnodes = depthnodes
            while not branchnodes[0]._depth == 1:
                for idx in range(n):
                    branchnodes[idx] = branchnodes[idx][(idx%2)-1]
            for node1, node2 in self._pairwise(branchnodes):
                node1.next = node2
                node2.prev = node1
        if self._depth == 1:
            ##TODO: Important: Add bulb assignment logic (static memory for all possible leaf values)
            ##TODO: Important: Add +1 -1 coalescing logic
            pass

    def _pairwise(self, iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return zip(a, a)
        
    def __len__(self):
        return len(self.nodes)
    
    # def __setattr__(self, name, value):
    #     if len(value) != 3:
    #         raise ValueError(f"Invalid data length {len(self.data)} for n={self._n}")
    #     self.nodes = value
    
    def __getitem__(self, key):
        # if key >= self._n:
        #     raise ValueError(f"Invalid key {key} for n={self._n}")
        return self.nodes[key]
    
    def __setitem__(self, key, value):
        # if key >= self._n:
        #     raise ValueError(f"Invalid key {key} for n={self._n}")
        self.nodes[key] = value


# f = Oumbellatum([3,4,5],3)
# g = Oumbellatum([3,3,3],2)

# a = Oumbellatum([1,2],2)
# b = Oumbellatum([3,4],2)
# c = Oumbellatum([5,6],2)
# d = Oumbellatum([7,8],2)
# # e = Oumbellatum([a,b],2)
# # f = Oumbellatum([c,d],2)
# # g = Oumbellatum([e,f],2)

# a = Oumbellatum([1,2,3],3)
# b = Oumbellatum([4,5,6],3)
# c = Oumbellatum([7,8,9],3)
# d = Oumbellatum([10,11,12],3)
# e = Oumbellatum([13,14,15],3)
# f = Oumbellatum([16,17,18],3)
# g = Oumbellatum([19,20,21],3)
# h = Oumbellatum([22,23,24],3)
# i = Oumbellatum([25,26,27],3)
# j = Oumbellatum([a,b,c],3)
# k = Oumbellatum([d,e,f],3)
# o = Oumbellatum([g,h,i],3)
# m = Oumbellatum([j,k,o],3)

# # print(g.nodes, g._n)

# # for z in c.nodes:
# #     print(z.nodes)

# # print(g[0][0].prev.nodes)

# def subtest(cmd, meth, arg):
#     try:
#         cmd(arg(meth))
#     except Exception as z:
#         print(z)

# def test(tree):
#     pre = lambda x : x.prev.nodes
#     pos = lambda x : x.next.nodes
#     subtest(print, tree[0], pre)
#     subtest(print, tree[1], pre)
#     subtest(print, tree[0], pos)
#     subtest(print, tree[1], pos)

# def test(tree):
#     pre = lambda x : x.prev.nodes
#     pos = lambda x : x.next.nodes
#     subtest(print, tree[0], pre)
#     subtest(print, tree[1], pre)
#     subtest(print, tree[2], pre)
#     subtest(print, tree[0], pos)
#     subtest(print, tree[1], pos)
#     subtest(print, tree[2], pos)
    
    
# test(m[0])
# test(m[1])
# test(m[2])