from math import floor
from turtle import left


def parent(index):
    return floor((index + 1) / 2) - 1

def left_child(index):
    return ((index + 1) * 2) - 1

def right_child(index):
    return ((index + 1) * 2)

def swap(arr, l, r):
    arr[l], arr[r] = (arr[r], arr[l])

def min_heapify(arr):
    for index in range(floor(len(arr) / 2), -1, -1):
        outer_index = index
        heap = False
        while not heap and outer_index * 2 < len(arr):
            inner_index = left_child(outer_index) 
            if inner_index < len(arr) - 1:
                if arr[inner_index] > arr[inner_index + 1]:
                    inner_index += 1
            if arr[outer_index] <= arr[inner_index]:
                heap = True
            else:
                swap(arr, outer_index, inner_index)
                outer_index = inner_index

def heap_insert(heap: list, item):
    heap.append(item)
    item_index = len(heap) - 1
    while heap[item_index] < parent(item_index):
        swap(item_index, parent(item_index))
        item_index = parent(item_index)

def extract_min(heap: list):
    r = heap[0]
    heap[0] = heap.pop()
    outer_index = 0
    heap = False
    while not heap and outer_index * 2 < len(heap):
        inner_index = left_child(outer_index)
        if inner_index < len(heap) - 1:
            if heap[inner_index] > heap[inner_index + 1]:
                inner_index += 1
        if heap[outer_index] > heap[inner_index]:
            swap(heap, outer_index, inner_index)
            outer_index = inner_index
        else:
            heap = True
    return r