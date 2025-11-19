import random
import time
from datetime import datetime
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class WaterQualitySensor:
    """
    Class to interface with water quality sensors.
    This is a simulation version that generates random values.
    For real hardware, uncomment and implement the appropriate sensor code.
    """
    
    def __init__(self, simulate=True):
        self.simulate = simulate
        self.sensor_init = False
        
        if not self.simulate:
            self._initialize_hardware()
    
    def _initialize_hardware(self):
        """Initialize I2C and sensor connections"""
        try:
            # Initialize I2C bus
            self.i2c = busio.I2C(board.SCL, board.SDA)
            
            # Create ADS1115 ADC (16-bit) instance
            self.ads = ADS.ADS1115(self.i2c)
            
            # Create single-ended input for each sensor
            self.channels = [
                AnalogIn(self.ads, ADS.P0),  # pH sensor
                AnalogIn(self.ads, ADS.P1),  # Turbidity sensor
                AnalogIn(self.ads, ADS.P2),  # TSS sensor
                AnalogIn(self.ads, ADS.P3)   # Other sensors through multiplexer
            ]
            
            self.sensor_init = True
            print("Hardware sensors initialized successfully")
            
        except Exception as e:
            print(f"Error initializing hardware: {e}")
            print("Falling back to simulation mode")
            self.simulate = True
    
    def _read_ph(self):
        """Read pH value from sensor or generate simulated value"""
        if self.simulate or not self.sensor_init:
            # Simulate pH between 4.0 and 10.0
            return round(random.uniform(4.0, 10.0), 2)
        else:
            # Real sensor reading (example for ADS1115)
            # Note: This needs calibration for your specific pH sensor
            voltage = self.channels[0].voltage
            # Convert voltage to pH (this is an example calibration - adjust for your sensor)
            ph_value = 7 - ((voltage - 1.5) / 0.18)
            return max(0, min(14, ph_value))  # Clamp between 0-14
    
    def _read_turbidity(self):
        """Read turbidity in NTU"""
        if self.simulate or not self.sensor_init:
            # Simulate turbidity between 0.5 and 10.0 NTU
            return round(random.uniform(0.5, 10.0), 2)
        else:
            # Real sensor reading (example)
            voltage = self.channels[1].voltage
            # Convert voltage to NTU (calibrate for your sensor)
            turbidity = (voltage * 1000) / 4.0  # Example conversion
            return max(0, turbidity)
    
    def _read_tss(self):
        """Read Total Suspended Solids in mg/L"""
        if self.simulate or not self.sensor_init:
            # Simulate TSS between 5 and 50 mg/L
            return round(random.uniform(5.0, 50.0), 2)
        else:
            # Real sensor reading would go here
            return 0.0
    
    def _read_cod(self):
        """Read Chemical Oxygen Demand in mg/L"""
        if self.simulate or not self.sensor_init:
            # Simulate COD between 50 and 500 mg/L
            return round(random.uniform(50.0, 500.0), 2)
        else:
            # Real sensor reading would go here
            return 0.0
    
    def _read_bod(self):
        """Read Biological Oxygen Demand in mg/L"""
        if self.simulate or not self.sensor_init:
            # Simulate BOD between 10 and 100 mg/L
            return round(random.uniform(10.0, 100.0), 2)
        else:
            # Real sensor reading would go here
            return 0.0
    
    def _read_oil_grease(self):
        """Read Oil & Grease in mg/L"""
        if self.simulate or not self.sensor_init:
            # Simulate Oil & Grease between 0.1 and 20.0 mg/L
            return round(random.uniform(0.1, 20.0), 2)
        else:
            # Real sensor reading would go here
            return 0.0
    
    def _read_heavy_metals(self):
        """Read Heavy Metals in mg/L"""
        if self.simulate or not self.sensor_init:
            # Simulate Heavy Metals between 0.01 and 0.5 mg/L
            return round(random.uniform(0.01, 0.5), 3)
        else:
            # Real sensor reading would go here
            return 0.0
    
    def read_all_sensors(self):
        """Read all sensor values and return as a dictionary"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            'timestamp': timestamp,
            'ph': self._read_ph(),
            'turbidity': self._read_turbidity(),
            'tss': self._read_tss(),
            'cod': self._read_cod(),
            'bod': self._read_bod(),
            'oil_grease': self._read_oil_grease(),
            'heavy_metals': self._read_heavy_metals()
        }


def test_sensor_interface():
    """Test function to demonstrate the sensor interface"""
    print("Testing Water Quality Sensor Interface")
    print("====================================")
    
    # Create sensor interface in simulation mode
    sensor = WaterQualitySensor(simulate=True)
    
    # Read and display sensor values
    print("\nSimulated Sensor Readings:")
    print("-" * 40)
    readings = sensor.read_all_sensors()
    for param, value in readings.items():
        print(f"{param:>12}: {value}")
    
    # Try to initialize hardware (will fail if not on a Pi with proper hardware)
    print("\nAttempting to initialize hardware...")
    sensor_hw = WaterQualitySensor(simulate=False)
    
    if sensor_hw.sensor_init:
        print("\nHardware Sensor Readings:")
        print("-" * 40)
        readings_hw = sensor_hw.read_all_sensors()
        for param, value in readings_hw.items():
            print(f"{param:>12}: {value}")
    else:
        print("Hardware initialization failed. Running in simulation mode.")


if __name__ == "__main__":
    test_sensor_interface()
