class Memory_Object:
    #The name of the camera:
    cam_name = ""
    #The bounding box of the image obtained:
    coords = ()

    def __init__(self, cam_name, coords):
        self.cam_name = cam_name
        self.coords = coords

    def get_name(self):
        return self.cam_name

    def get_coords(self):
        return self.coords

    def to_string(self):
        to_ret = self.cam_name + " "
        for x in self.coords:
            to_ret += str(x) + " "

        return to_ret

    #TODO: Add hooks for writing to file if needed:
    def write(self):
        return

    def read(self):
        return
    
