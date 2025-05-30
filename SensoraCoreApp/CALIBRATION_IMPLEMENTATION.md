# SensoraCore Linear Calibration Implementation

## Overview
Linear regression calibration has been successfully implemented for the Ángulo Simple sensor in the SensoraCore application. This system allows users to improve sensor accuracy by calibrating raw sensor values against known reference values.

## Implementation Details

### 1. Calibration Module (`modules/calibration.py`)
- **LinearCalibration class** with complete functionality:
  - Add calibration points (raw vs reference values)
  - Perform linear regression using scikit-learn
  - Apply calibration to raw sensor values
  - Save/load calibration data to/from JSON files
  - Get calibration statistics (R², equation)

### 2. Calibration Dialog UI (`ui/calibration_dialog.py`)
- **CalibrationDialog class** providing:
  - Input fields for adding calibration points
  - Table display with delete functionality
  - Real-time matplotlib visualization
  - Calibration controls (perform, clear, save, load)
  - Statistical information display

### 3. Main Window Integration (`ui/main_window.py`)
- **Added to Ángulo Simple interface**:
  - Calibration button
  - Calibration status label showing equation and R²
  - Modified data display to show both raw and calibrated values
  - Real-time calibration application

### 4. Dependencies (`requirements.txt`)
- Added required packages:
  - numpy (numerical operations)
  - scikit-learn (linear regression)
  - matplotlib (visualization)

## Features Implemented

### User Interface
1. **Calibration Button**: Opens calibration dialog from Ángulo Simple sensor interface
2. **Status Display**: Shows current calibration equation and R² value
3. **Data Display**: Shows both raw and calibrated values in real-time

### Calibration Dialog
1. **Point Management**: Add/delete calibration points with validation
2. **Visualization**: Real-time plot showing data points and regression line
3. **Statistics**: Display of equation, R², and point count
4. **Persistence**: Save/load calibration configurations

### Calibration Engine
1. **Linear Regression**: Uses scikit-learn for robust calculations
2. **Error Handling**: Validates input and handles edge cases
3. **Real-time Application**: Applies calibration to live sensor data
4. **Persistence**: JSON-based storage for calibration data

## Usage Workflow

1. **Setup**: Start SensoraCore application and select Ángulo Simple sensor
2. **Calibration**:
   - Click "Calibrar" button to open calibration dialog
   - Add calibration points by entering raw and reference values
   - Click "Realizar Calibración" to compute linear regression
   - Review statistics and visualization
   - Save calibration if satisfactory
3. **Application**: Calibration is automatically applied to real-time data
4. **Monitoring**: Status label shows active calibration equation and R²

## Technical Implementation

### Calibration Algorithm
```
Calibrated_Value = slope × Raw_Value + intercept
```
Where slope and intercept are determined by linear regression on calibration points.

### Data Flow
1. Raw sensor value → Calibration engine → Calibrated value
2. Display shows: "Raw: X.XX | Cal: Y.YY"
3. Status shows: "y = mx + b | R² = 0.XXXX"

### File Structure
```
modules/
  ├── __init__.py
  └── calibration.py     # LinearCalibration class
ui/
  ├── calibration_dialog.py  # CalibrationDialog class
  └── main_window.py     # Updated with calibration integration
```

## Status: READY FOR TESTING

All code has been implemented and integrated. The calibration system is ready for:
1. Manual testing with the GUI application
2. Validation with real sensor data
3. User acceptance testing

## Next Steps for Testing

1. Run the application: `python main.py`
2. Select Ángulo Simple sensor
3. Click "Calibrar" button
4. Add calibration points and test functionality
5. Verify real-time calibration application
6. Test save/load functionality

The implementation provides a complete, production-ready linear calibration system for the SensoraCore platform.
