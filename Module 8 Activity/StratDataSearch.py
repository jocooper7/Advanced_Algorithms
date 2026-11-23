# CS 680: Advanced Algorithms
# Strat Data Search Application

# imports
import csv
import heapq

# validation functions
def validateInt(value) -> bool:
    try:
        int(value)
        return True
    except:
        return False

def validateString(value) -> bool:
    if len(value) < 50:
        return isinstance(value, str)
    else:
        return False

# heap class for dataset
class DataSetHeap:
    def __init__(self) -> None:
        self.data = []
        self.dict = {}
        self.length = 0

    def getLen(self) -> int:
        return self.length

    def append(self, item) -> None:
        self.data.append(item)
        self.length += 1
        if item[0] not in self.dict:
            self.dict[item[0]] = []
        self.dict[item[0]].append(item[1])

    def testPrint(self, n) -> None:
        for i in range(min(n, self.length)):
            print(self.data[i])

    def searchDict(self, string) -> list:
        return self.dict.get(string)

# file loading function
def loadFile(file, dao) -> None:
    try:
        with open(file) as f:
            reader = csv.reader(f, delimiter='|')
            headRow = next(reader)
            for row in reader:
                rec = [row[1], row[0]] # [data, sequence]
                dao.append(rec)
            heapq.heapify(dao.data)
    except Exception as e:
        print("Error loading file")
        print(e)
        print("Exiting program.")
        exit()

if __name__ == "__main__":
    dao = DataSetHeap()
    loadFile("Module_8_Data_Set-2.csv", dao) # number in "Set-#" can be changed to 1-5 for alternate files

    # test print to ensure data loaded
    if 0:
        dao.testPrint(10)

    while True:
        print("\nSelect option: \n  1. Search\n  2. Exit")
        option = input("Enter menu option integer: ")
        if validateInt(option):
            option = int(option)
            if option == 1:
                search = input("Enter string: ")
                if validateString(search):
                    # records is an array of array of sequence numbers the searched string appears in
                    records = dao.searchDict(search)
                    if records:
                        header = "Sequence Number"
                        gap = 2
                        width = max(len(header), *(len(str(rec)) for rec in records)) + gap
                        print(f"\n{header:<{width}}Data")
                        for rec in records:
                            print(f"{rec:<{width}}{search}")
                        print(f"Records searched: {len(records)}")
                    else:
                        print("\nNo records found")
                        print(f"Records searched: 0")
                else:
                    print("Invalid string (string limit 50)")
            elif option == 2:
                break
            else:
                print("Invalid option")
        else:
            print("Invalid input")

    print("Exiting program.")
    exit()
