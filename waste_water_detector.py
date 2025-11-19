class WasteWaterDetector:
    def __init__(self):
        # Define water quality thresholds (example values - can be adjusted)
        self.thresholds = {
            'ph': {'min': 6.5, 'max': 8.5},  # Standard pH range for water
            'turbidity': 5.0,  # NTU (Nephelometric Turbidity Units)
            'tss': 30.0,  # mg/L (Total Suspended Solids)
            'cod': 250.0,  # mg/L (Chemical Oxygen Demand)
            'bod': 30.0,   # mg/L (Biological Oxygen Demand)
            'oil_grease': 10.0,  # mg/L
            'heavy_metals': 0.1  # mg/L (for individual heavy metals)
        }
        
    def check_ph(self, ph_value):
        """Check if pH is within acceptable range."""
        return self.thresholds['ph']['min'] <= ph_value <= self.thresholds['ph']['max']
    
    def check_turbidity(self, turbidity_value):
        """Check if turbidity is below threshold."""
        return turbidity_value <= self.thresholds['turbidity']
    
    def check_tss(self, tss_value):
        """Check Total Suspended Solids."""
        return tss_value <= self.thresholds['tss']
    
    def check_cod(self, cod_value):
        """Check Chemical Oxygen Demand."""
        return cod_value <= self.thresholds['cod']
    
    def check_bod(self, bod_value):
        """Check Biological Oxygen Demand."""
        return bod_value <= self.thresholds['bod']
    
    def check_oil_grease(self, oil_grease_value):
        """Check oil and grease levels."""
        return oil_grease_value <= self.thresholds['oil_grease']
    
    def check_heavy_metals(self, heavy_metal_value):
        """Check heavy metal concentration."""
        return heavy_metal_value <= self.thresholds['heavy_metals']
    
    def analyze_water_sample(self, sample):
        """
        Analyze a water sample and return results.
        
        Args:
            sample (dict): Dictionary containing water quality parameters
                          Example: {'ph': 7.0, 'turbidity': 4.0, 'tss': 20.0, ...}
        
        Returns:
            dict: Analysis results with status for each parameter and overall status
        """
        results = {
            'parameters': {},
            'is_safe': True,
            'contaminants': []
        }
        
        # Check each parameter
        for param, value in sample.items():
            if param in self.thresholds:
                if param == 'ph':
                    is_safe = self.check_ph(value)
                elif param == 'turbidity':
                    is_safe = self.check_turbidity(value)
                elif param == 'tss':
                    is_safe = self.check_tss(value)
                elif param == 'cod':
                    is_safe = self.check_cod(value)
                elif param == 'bod':
                    is_safe = self.check_bod(value)
                elif param == 'oil_grease':
                    is_safe = self.check_oil_grease(value)
                elif param == 'heavy_metals':
                    is_safe = self.check_heavy_metals(value)
                
                results['parameters'][param] = {
                    'value': value,
                    'is_safe': is_safe
                }
                
                if not is_safe:
                    results['is_safe'] = False
                    results['contaminants'].append(param)
        
        return results

def main():
    # Example usage
    detector = WasteWaterDetector()
    
    # Example water sample
    sample = {
        'ph': 7.2,
        'turbidity': 4.5,  # NTU
        'tss': 25.0,      # mg/L
        'cod': 200.0,     # mg/L
        'bod': 25.0,      # mg/L
        'oil_grease': 8.0, # mg/L
        'heavy_metals': 0.05  # mg/L
    }
    
    # Analyze the sample
    results = detector.analyze_water_sample(sample)
    
    # Print results
    print("Water Quality Analysis Results:")
    print("-" * 50)
    
    for param, data in results['parameters'].items():
        status = "✓ SAFE" if data['is_safe'] else "✗ UNSAFE"
        print(f"{param.upper():<15}: {data['value']:<10} {status}")
    
    print("\nOverall Water Quality:", "SAFE" if results['is_safe'] else "UNSAFE")
    
    if not results['is_safe']:
        print("\nContaminants detected:")
        for contam in results['contaminants']:
            print(f"- {contam}")

if __name__ == "__main__":
    main()
