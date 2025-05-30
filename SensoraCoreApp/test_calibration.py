# Test script for calibration functionality
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.calibration import LinearCalibration

def test_calibration():
    print("Testing Linear Calibration...")
    
    # Create calibration instance
    calibration = LinearCalibration()
    
    # Add some test points
    calibration.add_point(10, 12)  # Raw value 10 should be 12
    calibration.add_point(20, 24)  # Raw value 20 should be 24
    calibration.add_point(30, 36)  # Raw value 30 should be 36
    
    print(f"Added {len(calibration.get_points())} calibration points")
    
    # Perform calibration
    success = calibration.perform_calibration()
    print(f"Calibration successful: {success}")
    
    if success:
        # Test calibration
        test_value = 25
        calibrated_value = calibration.apply_calibration(test_value)
        print(f"Raw value {test_value} -> Calibrated value {calibrated_value}")
        
        # Get equation
        equation = calibration.get_equation_string()
        print(f"Calibration equation: {equation}")
        
        # Get R²
        r_squared = calibration.get_r_squared()
        print(f"R² value: {r_squared:.4f}")
        
        # Save calibration
        calibration.save_calibration("test_calibration.json")
        print("Calibration saved to test_calibration.json")
        
        # Load calibration
        new_calibration = LinearCalibration()
        if new_calibration.load_calibration("test_calibration.json"):
            print("Calibration loaded successfully")
            test_loaded = new_calibration.apply_calibration(test_value)
            print(f"Loaded calibration result: {test_loaded}")
        else:
            print("Failed to load calibration")
    
    print("Calibration test completed!")

if __name__ == "__main__":
    test_calibration()
