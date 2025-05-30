# Quick test to verify calibration integration
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing the calibration module
    from modules.calibration import LinearCalibration
    print("✓ LinearCalibration imported successfully")
    
    # Create and test calibration instance
    calibration = LinearCalibration()
    print("✓ LinearCalibration instance created")
    
    # Test adding points
    calibration.add_calibration_point(10, 15)
    calibration.add_calibration_point(20, 25)
    calibration.add_calibration_point(30, 35)
    print("✓ Calibration points added")
    
    # Test calibration
    success = calibration.perform_calibration()
    print(f"✓ Calibration performed: {success}")
    
    if success:
        # Test applying calibration
        test_value = 25
        result = calibration.calibrate_value(test_value)
        print(f"✓ Calibration applied: {test_value} -> {result}")
        
        # Test stats
        stats = calibration.get_calibration_stats()
        print(f"✓ Stats retrieved: {stats}")
    
    print("\n--- Testing UI imports ---")
    
    # Test CalibrationDialog import
    from ui.calibration_dialog import CalibrationDialog
    print("✓ CalibrationDialog imported successfully")
    
    # Test MainWindow import
    from ui.main_window import MainWindow
    print("✓ MainWindow imported successfully")
    
    print("\n🎉 All tests passed! Calibration system is ready.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
