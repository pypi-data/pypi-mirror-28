from operator import itemgetter
from .helpers import * 


class SortingAlgorithms:
    @staticmethod
    def BUBBLE(arr):
        """Bubble sort algorithm for a python list """
        data = arr
        n = len(data)
        for i in range(0, n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

    @staticmethod
    def INSERTION(arr):
        """
        Insertion sort algorithm for a python list
        """
        data = arr
        n = len(data)
        for i in range(1, n):
            key = data[i]
            j = i-1
            while j >= 0 and key < data[j]:
                data[j+1] = data[j]
                j = j - 1
            data[j+1] = key
        return data

    @staticmethod
    def MERGE(arr):
        """merge sort algorithm for a python list """
        data = arr
        if len(data) > 1:
            mid = len(data)//2
            left = data[:mid]
            right = data[mid:]
            SortingAlgorithms.MERGE(left)
            SortingAlgorithms.MERGE(right)
            i = 0
            j = 0
            k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    data[k] = left[i]
                    i += 1
                else:
                    data[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                data[k] = left[i]
                i = i + 1
                k = k + 1
            while j < len(right):
                data[k] = right[j]
                j = j + 1
                k = k + 1
        return data

    @staticmethod
    def LISTOFLISTS(arr, index=None):
        """Algorithm to sort a list of lists"""
        data = arr
        if index is None:
            return sorted(data)
        return sorted(data, key=itemgetter(index))

    @staticmethod
    def LISTOFTUPLES(arr, index=None):
        """"Algorithm to sort a list of tuples"""
        data = arr
        if index is None:
            return sorted(data)
        return sorted(data, key=itemgetter(index))

    @staticmethod
    def APPLYSORT(arr, func):
        """Algorithm to sort a list if func is applied to the elements of the list"""
        data = arr
        return sorted(data, key=func)

    @staticmethod
    def SELECTIONSORT(arr):
        """selection sort algorithm for a python list"""
        data = arr
        for i in range(len(data)):   
            min_idx = i
            for j in range(i+1, len(data)):
                if data[min_idx] > data[j]:
                    min_idx = j
                  
            data[i], data[min_idx] = data[min_idx], data[i]
        return data

    @staticmethod
    def QUICKSORT(arr, low, high):
        """selection sort algorithn for a python list
        """
        data = arr
        if low < high:
            pi = partition(data,low,high)
            SortingAlgorithms.QUICKSORT(data, low, pi-1)
            SortingAlgorithms.QUICKSORT(data, pi+1, high)
        return data

    @staticmethod
    def HEAPSORT(arr):
        """heapsort implementation for a python list"""
        data = arr
        n = len(data)
        for i in range(n, -1, -1):
            heapify(data, n, i)
        for i in range(n-1, 0, -1):
            data[i], data[0] = data[0], data[i]
            heapify(data, i, 0)
        return data
