from PyAndor import ShamRockController

if __name__ == "__main__":
    sc = ShamRockController()
    try:
        sc.Initialize()
        print("nr of devices:", sc.GetNumberDevices())
        
        s = sc.Connect()
        
        print("Serial:", s.GetSerialNumber())
        print("Optical params:", s.EepromGetOpticalParams())
        
        print("Gratings")
        print("GetGrating", s.GetGrating())
        print("GetNumberGratings", s.GetNumberGratings())
        print("GetDetectorOffset", s.GetDetectorOffset())
        print("GetDetectorOffsetPort2", s.GetDetectorOffsetPort2())
        print("GetTurret", s.GetTurret())
        
        for grating in range(1, s.GetNumberGratings() + 1):
            print("Grating #", grating)
            print("GetGratingInfo", grating, s.GetGratingInfo(grating))
            print("GetGratingOffset", grating, s.GetGratingOffset(grating))
            print("GetWavelengthLimits", s.GetWavelengthLimits(grating))

        print("GetWavelength", s.GetWavelength())
        print("AtZeroOrder", s.AtZeroOrder())
        print("WavelengthIsPresent", s.WavelengthIsPresent())
        
        for slit in range(1, 5):
            print("Slit #", slit)
            print("AutoSlitIsPresent", s.AutoSlitIsPresent(slit))
            if not s.AutoSlitIsPresent(slit):
                continue
            print("GetAutoSlitWidth", s.GetAutoSlitWidth(slit))
            if slit == 1:
                print("GetAutoSlitCoefficients", s.GetAutoSlitCoefficients(slit))
         
        print("ShutterIsPresent", s.ShutterIsPresent())
        print("GetShutter", s.GetShutter())
        
        print("FilterIsPresent", s.FilterIsPresent())
        print("GetFilter", s.GetFilter())
        print("GetFilterInfo", s.GetFilterInfo(s.GetFilter()))

        print("GetPixelWidth", s.GetPixelWidth())
        print("GetNumberPixels", s.GetNumberPixels())
        print("GetCalibration", s.GetCalibration())
        
        print("GetInfo")
        print("\n".join(["%s: %s" % (k, v) for k, v in s.GetInfo().items()]))
        print()
         
    finally:
        sc.Close()
        print("done")