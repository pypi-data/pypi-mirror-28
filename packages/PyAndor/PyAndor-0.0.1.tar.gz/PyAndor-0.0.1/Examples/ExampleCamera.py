import pylab as plt
import logging
from PyAndor import AndorCamera
    
if __name__ == "__main__":
    
    logging.basicConfig(level = logging.DEBUG)
    cam = AndorCamera()
    try:
        cam.Initialize()
        print("GetInfo")
        print("\n".join(["%s: %s" % (k, v) for k, v in cam.GetInfo().items()]))
        print()
        
        cam.SetReadMode("Image")
        cam.SetImage(1, 1)
        cam.SetExposureTime(0.1)
        cam.SetAccumulationCycleTime(0.0)
        cam.GetAcquisitionTimings()
        
        cam.StartAcquisition()
        cam.WaitForAcquisition()
        img = cam.GetMostRecentImage()
         
        # plt.plot(img)
        plt.pcolormesh(img.T)
        plt.colorbar()
        plt.show()
         
    finally:
        cam.ShutDown()