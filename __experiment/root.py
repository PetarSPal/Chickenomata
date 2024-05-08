from typing import Self
import dis

# Need to flesh this out better, conceptually


class Node:
    def __init__(
        self,
        value: int,
        next: Self | None = None,
        prev: Self | None = None
    ) -> None:
        self.value: int = value
        self.next: Self | None = next
        self.prev: Self | None = prev


class FakeData:
    def __init__(self, num_sys: int) -> None:
        if num_sys < 2:
            raise ValueError("Num sys < 2")
        self.num_sys = num_sys
        self.data = [Node(i) for i in range(num_sys)]
        for i in range(1, num_sys-1):
            self.data[i].prev = self.data[i-1]
            self.data[i].next = self.data[i+1]
        self.data[0].next = self.data[1]
        self.data[-1].prev = self.data[-2]
        self.data[0].prev = self.data[-1]
        self.data[-1].next = self.data[0]


class FakeInt:
    def __init__(self, value, source):
        true_value = abs(value % source.num_sys)
        self.data = source.data[true_value]

    def __add__(self, other):
        # TODO: add check for going over/under
        if other > 0:
            for _ in range(other):
                self.data = self.data.next
        elif other < 0:
            for _ in range(abs(other)):
                self.data = self.data.prev
        return self

    def __sub__(self, other):
        self.__add__(-other)
        return self

    def __mul__(self, other):
        self.__add__(self.data.value * (other-1))
        return self

    def __truediv__(self, other):
        self.__sub__(self.data.value - (self.data.value // other))
        return self

    def __str__(self):
        return "%d" % int(self.data.value)

    def __repr__(self):
        return "%d" % int(self.data.value)


class Root:
    # Testing with dis.dis makes this seem at lest semi-redundant (ints get cached by parser already)
    # TODO: Test with actual automata to confirm
    def __init__(self, values, source):
        self.source = source
        if len(values) != source.num_sys:
            raise Exception(
                "count of values {values} does not match in_sys {source.num_sys}")
        true_values = [abs(value % source.num_sys) for value in values]
        self.data = [FakeInt(value, source) for value in true_values]

    def __getitem__(self, key):
        return self.data[key].data.value

    def __testitem__(self, key):
        return self.data[key].data

    def __setitem__(self, key, value):
        self.data[key] = FakeInt(value, self.source)


# def testfunc(val):
#     a = [val for i in range(val)]
#     a[0] +=1
#     a[1] -=1
#     a[0] = 450
#     a[2] +=1
#     a[3] = 99
#     import resource
#     print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
#     print(a)

# def altfunc(val):
#     dat = FakeData(val)
#     rtrt = Root([val-1 for i in range(val)], dat)
#     rtrt[0] +=1
#     rtrt[1] -=1
#     rtrt[0] = 450
#     rtrt[2] +=1
#     rtrt[3] = 99
#     import resource
#     print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
#     print(rtrt.data)

# # testfunc(999)
# # dis.distb()
# # dis.dis("a = testfunc(999)", depth=100, show_caches=True)
# altfunc(1000)
# dis.dis("altfunc(1000)", depth=1000, show_caches=True)

# dat = FakeData(5)
# rtrt = Root([1,0,2,2,3], dat)
# # rtrt[2] += 5
# # rtrt[2] += 5
# # rtrt[2] += 5
# # rtrt[2] += 5
# # rtrt[2] += 5


# dis.dis("dat = FakeData(5)")
# dis.dis("rtrt = Root([1,0,2,2,3], dat)")
# dis.dis("rtrt[2] += 5")
# dis.dis("rtrt[2] += 5")
# dis.dis("rtrt[2] += 5")
# dis.dis("rtrt[2] += 5")
# dis.dis("rtrt[2] += 5")


# print(rtrt[2])
# print(rtrt[3])

# print(rtrt[2] + 1)

# print(rtrt[2])
# print(rtrt[3])


# dat = FakeData(5)
# inte = FakeInt(3, dat)
# inte2 = FakeInt(4, dat)

# print(inte.data)
# print(inte)
# print(inte2.data.prev)
# print(inte2)


# print(inte)
# print(inte.data)
# print(inte + 1)
# print(inte.data.prev)
# inte += 2
# print(inte)
# print(inte.data.prev.prev.prev)
# print(inte)
# inte *3
# print(inte)

# class Node:
#     def __init__(
#         self,
#         value: int,
#         next: Self | None = None,
#         prev: Self | None = None
#     ) -> None:
#         self.value: int = value
#         self.next: Self | None = next
#         self.prev: Self | None = prev

# class FakeData:
#     def __init__(self, value: int, num_sys: int) -> None:
#         if num_sys < 2:
#             raise ValueError("Num sys < 2")
#         if value >= num_sys:
#             raise ValueError("value too high")
#         # self.cur = None
#         first = Node(0)
#         last = Node(num_sys-1, next=first)
#         first.prev = last
#         true_value = abs(value % num_sys)

#         if true_value == 0:
#             self.cur = first
#         elif true_value == num_sys-1:
#             self.cur = last
#         else:
#             self.cur = Node(true_value)
#         if num_sys == 2:
#             first.next = last
#             last.prev = first
#         elif num_sys == 3:
#             first.next = self.cur
#             last.prev = self.cur
#             self.cur.prev = first
#             self.cur.next = last
#         else:
#             temp = first

#             def make_node(old, new):
#                 old.next = new
#                 new.prev = old
#                 return new
#             for val in range(1, true_value):
#                 temp = make_node(temp, Node(val))
#             if true_value not in (0, num_sys-1):
#                 temp = make_node(temp, self.cur)
#                 # temp.next = self.cur
#                 # self.cur.prev = temp
#                 # temp = self.cur
#             for val in range(true_value+1, num_sys-1):
#                 temp = make_node(temp, Node(val))
#             temp.next = last
#             last.prev = temp

#     def __add__(self, other):
#         if other > 0:
#             for _ in range(other):
#                 assert self.cur is not None
#                 next = self.cur.next
#                 self.cur = next
#         elif other < 0:
#             for _ in range(abs(other)):
#                 assert self.cur is not None
#                 prev = self.cur.prev
#                 self.cur = prev
#         return self

#     def __sub__(self, other):
#         self.__add__(-other)
#         return self

#     def __mul__(self, other):
#         assert self.cur is not None
#         self.__add__(self.cur.value * (other-1))
#         return self

#     def __truediv__(self, other):
#         assert self.cur is not None
#         self.__sub__(self.cur.value - (self.cur.value // other))
#         return self

#     def __str__(self):
#         assert self.cur is not None
#         return "%d" % int(self.cur.value)


# a = FakeData(7, 8)
# # print(a.cur.next.next.next.next.next.prev.prev.prev.prev.prev.value)

# b = a


# print(a.cur)
# print(b.cur.next)


# class FakeInt:
#     def __init__(self, value, num_sys):
#         self._value = FakeData(value, num_sys)

#     def __add__(self, other):
#         out = self._value.cur
#         if other > 0:
#             for _ in range(other):
#                 out = out.next
#         elif other < 0:
#             for _ in range(abs(other)):
#                 out = out.prev
#         return out

    # def __sub__(self, other):
    #     res = super(positive, self).__sub__(other)
    #     return self.__class__(max(res, 0))

    # def __mul__(self, other):
    #     res = super(positive, self).__mul__(other)
    #     return self.__class__(max(res, 0))

    # def __div__(self, other):
    #     res = super(positive, self).__div__(other)
    #     return self.__class__(max(res, 0))

    # def __str__(self):
    #     return "%d" % int(self)

    # def __repr__(self):
    #     return "positive(%d)" % int(self)


# a = FakeData(1,3)

# next.next.next.next.next.prev.prev.prev.prev.prev.prev
# print(a.cur.next.value)


# class positive(int):
#     def __new__(cls, value, num_sys, *args, **kwargs):
#         cls.num_sys = num_sys
#         if value < 0:
#             raise ValueError("positive types must not be less than zero")
#         return super(cls, cls).__new__(cls, value)

#     def __add__(self, other):
#         res = super(positive, self).__add__(other)
#         return self.__class__(max(res, 0))

#     def __sub__(self, other):
#         res = super(positive, self).__sub__(other)
#         return self.__class__(max(res, 0))

#     def __mul__(self, other):
#         res = super(positive, self).__mul__(other)
#         return self.__class__(max(res, 0))

#     def __div__(self, other):
#         res = super(positive, self).__div__(other)
#         return self.__class__(max(res, 0))

#     def __str__(self):
#         return "%d" % int(self)

#     def __repr__(self):
#         return "positive(%d)" % int(self)

# a = positive(5, 2)
# b = positive(5, 3)

# # b = 2 * a
# # print(b)
# print(a.num_sys)


# 0 1
# 0 1

# 0 1 2
# 0 1 01

# 0 1 2 3
# 0 1 01 11
