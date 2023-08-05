# MeanSort Documentation

Sorting algorithm by splitting a list by its mean/average.

# Installation

	pip install meansort

# Example

![Alt text](https://github.com/dibsonthis/meansort/blob/master/Meansort/Meansort.PNG "test.py")

# Dependencies

* tqdm (pip install tqdm)

<h1> How to use MeanSort: </h1>

    from meansort import MeanSort
    
    ms = MeanSort
    
    test = [random.randint(0,100) for x in range(100000)]
    
    a = ms.meansort(test)
    
    b = sorted(test)
    
    a==b
    
    >> True
    
    # to test time on sort use *_test train on function
    
    a = ms.meansort_test(test)
    
    # This will initialize a tqdm progress bar in the command line to show sorting progress
