# Simple import test
try:
    from modules.calibration import LinearCalibration
    print("✓ LinearCalibration imported successfully")
except Exception as e:
    print(f"✗ Error importing LinearCalibration: {e}")

try:
    from ui.calibration_dialog import CalibrationDialog
    print("✓ CalibrationDialog imported successfully")
except Exception as e:
    print(f"✗ Error importing CalibrationDialog: {e}")

try:
    from ui.main_window import MainWindow
    print("✓ MainWindow imported successfully")
except Exception as e:
    print(f"✗ Error importing MainWindow: {e}")

print("Import test completed!")
