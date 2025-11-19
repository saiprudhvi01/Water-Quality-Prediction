from flask import Flask, render_template, request, jsonify
from waste_water_detector import WasteWaterDetector

app = Flask(__name__)
detector = WasteWaterDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get data from form
        sample = {
            'ph': float(request.form.get('ph', 0)),
            'turbidity': float(request.form.get('turbidity', 0)),
            'tss': float(request.form.get('tss', 0)),
            'cod': float(request.form.get('cod', 0)),
            'bod': float(request.form.get('bod', 0)),
            'oil_grease': float(request.form.get('oil_grease', 0)),
            'heavy_metals': float(request.form.get('heavy_metals', 0))
        }
        
        # Analyze the sample
        results = detector.analyze_water_sample(sample)
        
        # Add parameter details to results
        results['parameter_details'] = {
            'ph': {'name': 'pH', 'unit': '', 'safe_range': f"{detector.thresholds['ph']['min']} - {detector.thresholds['ph']['max']}"},
            'turbidity': {'name': 'Turbidity', 'unit': 'NTU', 'safe_range': f"≤ {detector.thresholds['turbidity']}"},
            'tss': {'name': 'Total Suspended Solids', 'unit': 'mg/L', 'safe_range': f"≤ {detector.thresholds['tss']}"},
            'cod': {'name': 'Chemical Oxygen Demand', 'unit': 'mg/L', 'safe_range': f"≤ {detector.thresholds['cod']}"},
            'bod': {'name': 'Biological Oxygen Demand', 'unit': 'mg/L', 'safe_range': f"≤ {detector.thresholds['bod']}"},
            'oil_grease': {'name': 'Oil & Grease', 'unit': 'mg/L', 'safe_range': f"≤ {detector.thresholds['oil_grease']}"},
            'heavy_metals': {'name': 'Heavy Metals', 'unit': 'mg/L', 'safe_range': f"≤ {detector.thresholds['heavy_metals']}"}
        }
        
        return render_template('result.html', results=results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
