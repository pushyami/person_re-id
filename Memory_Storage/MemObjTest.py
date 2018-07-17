from memory_object import Memory_Object
from memory_storage import Memory_Storage


def Main():

    cam_name = input("Camera Name: ")

    arr = []
    for i in range(4):
        arr.append(input("Please input coordinate"))

    tuple(arr)

    MO = Memory_Object(cam_name, arr)
    print(MO.to_string())

    print("Inserting")

    MS = Memory_Storage()

    MS.insert(MO)

    print(MS.to_string())
    

if __name__ == "__main__":
    Main()
