import random

class MeanSort():

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

            elif len(a) > 0 and len(b) < 1:
                return a

            elif len(b) > 0 and len(a) < 1:
                return b

    def meansort(self,array,order='asc'):
        if type(array[0]) != list:
            array = [array]

        arr = array[:]
        length = 7
        for i in range(length):
            arr = MeanSort().meansplit(arr)
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
        res = []
        for i in arr:
            res+=i
        if order == 'desc':
            return res[::-1]
        elif order == 'asc':
            return res

#ms = MeanSort()

test = [random.randint(0,100) for x in range(100000)]
