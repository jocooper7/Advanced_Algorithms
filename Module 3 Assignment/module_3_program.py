# Module 3 Activity

import csv
import os

# entries saved as [key, data-a, data-b, validation]
data = [] 

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "resources/module_3_dataset_3.csv") 
try:
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter="|")

        header = next(reader)

        for row in reader:
            data.append(row)
except FileNotFoundError:
    print("File not found.")

# validates user input as a 9-digit integer key
def intValidation(value: str) -> int | None:
    try:
        if len(str(value)) != 9:
            raise ValueError("Invalid length")
        val = int(value)
        return val
    except ValueError:
        return None

# sort function using merge sort
def mergeSort(data: list[list]) -> list[list]:
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = mergeSort(data[:mid])
    right = mergeSort(data[mid:])
    return merge(left, right)

def merge(left: list[list], right: list[list]) -> list[list]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if int(left[i][0]) <= int(right[j][0]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# binary search function for searching by integer key field
def binarySearch(data: list[list], key: int) -> int:
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if int(data[mid][0]) == int(key):
            return mid
        elif int(data[mid][0]) < int(key):
            low = mid + 1
        else:
            high = mid - 1
    return -1

# main program
if __name__ == "__main__":
    data = mergeSort(data)

    while True:
        print("Enter 9 digit key to search for: ", end="")
        userInput = intValidation(input())
        if userInput is None:
            print("Invalid input. Please enter a 9 digit key.")
            continue
        break

    # returns -1 if key is not found
    ind = binarySearch(data, userInput)
    if ind != -1:
        print(f"Key found at index {ind}: {data[ind]}")
    else:
        print("Key not found.")