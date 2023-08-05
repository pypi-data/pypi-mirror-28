import random
import math

class MeanSort():

    def __init__(self):
        pass

    def bubblesort(self, array):
        a = array[:]
        length = len(a)
        for i in range(length):
            for i,v in enumerate(a[:-1]):
                if a[i] > a[i+1]:
                    x = a[i]
                    a[i] = a[i+1]
                    a[i+1] = x
        return a

    def bubblesort_test(self, array):
        from tqdm import tqdm
        a = array[:]
        length = len(a)
        for i in tqdm(range(length)):
            for i,v in enumerate(a[:-1]):
                if a[i] > a[i+1]:
                    x = a[i]
                    a[i] = a[i+1]
                    a[i+1] = x
        return a

    def meansplit(self,array):

        result = []

        if type(array) != list:
            return [array]

        for i,v in enumerate(array):
            if len(v) < 1:
                del array[i]

        if len(array) < 1:
            return []
        else:
            for i in array:
                arr = i[:]
                x = 0
                for i in arr:
                    x+=i
                x = x/len(arr)
                a = [i for i in arr if i > x]
                b = [i for i in arr if i <= x]

                result.append(b)
                result.append(a)

            for i,v in enumerate(result):
                if len(v) < 1:
                    del result[i]

            return result

            if len(a) > 0 and len(b) > 0:
                return result

            #elif len(a) > 0 and len(b) < 1:
            #    return a

            #elif len(b) > 0 and len(a) < 1:
            #    return b

    def meansort(self,array,order='asc'):
        if type(array[0]) != list:
            array = [array]

        arr = array[:]
        length = 7
        for i in range(length):
            arr = MeanSort().meansplit(arr)
        for i,v in enumerate(arr):
            if v[0] > v[-1]:
                arr[i] = arr[i][::-1]
        res = []
        for i in arr:
            res+=i
        if order == 'desc':
            return res[::-1]
        elif order == 'asc':
            return res

    def meansort_test(self,array,order='asc'):
        from tqdm import tqdm
        if type(array[0]) != list:
            array = [array]

        arr = array[:]
        length = 7
        for i in tqdm(range(length)):
            arr = MeanSort().meansplit(arr)
        for i,v in enumerate(arr):
            if v[0] > v[-1]:
                arr[i] = arr[i][::-1]
        res = []
        for i in arr:
            res+=i
        if order == 'desc':
            return res[::-1]
        elif order == 'asc':
            return res


def mmax(array):
    res = []
    res.insert(0,array[0])
    for i,v in enumerate(array):
        if i == 0:
            continue
        if array[i] > res[0]:
            res.insert(0,v)
    return res[0]

def mmin(array):
    res = []
    res.insert(0,array[0])
    for i,v in enumerate(array):
        if i == 0:
            continue
        if array[i] < res[0]:
            res.insert(0,v)
    return res[0]

def bound(array,order='asc'):
    from tqdm import tqdm
    res = []
    floats = [x for x in array if type(x) == float]
    array = [x for x in array if type(x) != float]
    inc = 1

    if len(array) > 0:

        upper = int(mmax(array)+1)
        lower = int(mmin(array)-1)

        for i in tqdm(range(lower-1,upper+1)):
            if upper not in array:
                upper -= inc
            else:
                for i in array:
                    if i == upper:
                        res.append(upper)
                upper -= inc

        res = res[::-1]

    if len(floats) > 0:
        length = len(res)
        for flt in tqdm(floats):
            for i in range(1,length):
                if flt < res[i] and flt > res[i-1]:
                    res.insert(i,flt)
                elif flt > res[-1]:
                    res.insert(-1,flt)
                elif flt < res[0]:
                    res.insert(0,flt)

    if len(floats) > 0 and len(res) < 1:
        res = MeanSort().meansort(floats)


    if order == 'asc':
        return res
    elif order == 'desc':
        return res[::-1]


#ms = MeanSort()

#test = [random.randint(0,10000) for x in range(100000)]
