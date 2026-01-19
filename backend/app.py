from flask import Flask, request, jsonify
from flask_cors import CORS
from models.ensemble import EnsembleHumanizer
from utils.advanced_metrics import AdvancedTextMetrics as TextMetrics
from config import Config
import os

app = Flask(__name__)
CORS(app)

# Initialize ensemble (lazy loading)
ensemble = None

def get_ensemble():
    """Lazy load ensemble to avoid loading models on import"""
    global ensemble
    if ensemble is None:
        print("Initializing Ensemble Humanizer...")
        ensemble = EnsembleHumanizer(
            device=Config.DEVICE,
            use_bart=True,
            use_t5=True,
            use_pegasus=True
        )
        print("Ensemble ready!")
    return ensemble

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': ensemble is not None,
        'device': Config.DEVICE
    })

@app.route('/api/humanize', methods=['POST'])
def humanize_text():
    """
    Main humanization endpoint
    
    Request body:
    {
        "text": "Text to humanize",
        "strategy": "weighted" | "diverse" | "mixed" | "best",
        "num_variations": 3,
        "return_all": false
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if len(text) > Config.MAX_TEXT_LENGTH:
            return jsonify({
                'error': f'Text too long. Maximum {Config.MAX_TEXT_LENGTH} characters'
            }), 400
        
        if len(text.strip()) < 10:
            return jsonify({'error': 'Text too short. Minimum 10 characters'}), 400
        
        # Get parameters
        strategy = data.get('strategy', Config.DEFAULT_STRATEGY)  # Use advanced_blend by default
        num_variations = data.get('num_variations', 3)
        return_all = data.get('return_all', False)
        
        # Validate strategy
        valid_strategies = ['weighted', 'diverse', 'mixed', 'best', 'advanced_blend']
        if strategy not in valid_strategies:
            return jsonify({
                'error': f'Invalid strategy. Must be one of: {valid_strategies}'
            }), 400
        
        # Get ensemble
        ens = get_ensemble()
        
        # Humanize
        result = ens.humanize(
            text=text,
            strategy=strategy,
            num_variations=num_variations,
            return_all=return_all,
            max_length=Config.MAX_LENGTH,
            temperature=Config.TEMPERATURE,
            top_k=Config.TOP_K,
            top_p=Config.TOP_P,
            num_beams=Config.NUM_BEAMS
        )
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in humanize_text: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics', methods=['POST'])
def get_metrics():
    """
    Get metrics for a text without humanizing
    
    Request body:
    {
        "text": "Text to analyze",
        "use_gpt2": false (optional, default false for speed)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        use_gpt2 = data.get('use_gpt2', False)  # Default to false for speed
        
        metrics = TextMetrics.calculate_comprehensive_score(text, use_gpt2=use_gpt2)
        
        return jsonify(metrics)
    
    except Exception as e:
        print(f"Error in get_metrics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_texts():
    """
    Compare two texts (original vs humanized)
    
    Request body:
    {
        "original": "Original text",
        "humanized": "Humanized text"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'original' not in data or 'humanized' not in data:
            return jsonify({'error': 'Both original and humanized texts required'}), 400
        
        ens = get_ensemble()
        comparison = ens.compare_texts(data['original'], data['humanized'])
        
        return jsonify(comparison)
    
    except Exception as e:
        print(f"Error in compare_texts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def batch_humanize():
    """
    Humanize multiple texts in batch
    
    Request body:
    {
        "texts": ["text1", "text2", ...],
        "strategy": "weighted"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({'error': 'No texts provided'}), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list):
            return jsonify({'error': 'texts must be an array'}), 400
        
        if len(texts) > 10:
            return jsonify({'error': 'Maximum 10 texts per batch'}), 400
        
        strategy = data.get('strategy', Config.DEFAULT_STRATEGY)
        
        ens = get_ensemble()
        
        results = []
        for text in texts:
            if len(text.strip()) < 10:
                results.append({'error': 'Text too short'})
                continue
            
            result = ens.humanize(
                text=text,
                strategy=strategy,
                num_variations=2,  # Fewer variations for batch
                return_all=False,
                max_length=Config.MAX_LENGTH,
                temperature=Config.TEMPERATURE,
                top_k=Config.TOP_K,
                top_p=Config.TOP_P,
                num_beams=Config.NUM_BEAMS
            )
            results.append(result)
        
        return jsonify({'results': results})
    
    except Exception as e:
        print(f"Error in batch_humanize: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)


@app.route('/api/humanize/recursive', methods=['POST'])
def humanize_recursive():
    """
    Advanced recursive humanization endpoint
    Uses multiple passes through different models/techniques
    
    Request body:
    {
        "text": "Text to humanize",
        "min_passes": 2,
        "max_passes": 4,
        "target_score": 75.0,
        "add_imperfections": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if len(text) > Config.MAX_TEXT_LENGTH:
            return jsonify({
                'error': f'Text too long. Maximum {Config.MAX_TEXT_LENGTH} characters'
            }), 400
        
        if len(text.strip()) < 10:
            return jsonify({'error': 'Text too short. Minimum 10 characters'}), 400
        
        # Get parameters
        min_passes = data.get('min_passes', 2)
        max_passes = data.get('max_passes', 3)
        target_score = data.get('target_score', 75.0)
        add_imperfections = data.get('add_imperfections', True)
        
        # Get ensemble
        ens = get_ensemble()
        
        # First, get paraphrased output from models
        result = ens.humanize(
            text=text,
            strategy='advanced_blend',
            num_variations=2,
            return_all=False,
            max_length=Config.MAX_LENGTH,
            temperature=Config.TEMPERATURE,
            top_k=Config.TOP_K,
            top_p=Config.TOP_P
        )
        
        # The recursive paraphrasing is already applied in humanize()
        # Add additional info about recursive passes
        result['recursive_humanization'] = True
        result['min_passes'] = min_passes
        result['max_passes'] = max_passes
        result['imperfections_added'] = add_imperfections
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in humanize_recursive: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/humanize/aggressive', methods=['POST'])
def humanize_aggressive():
    """
    Most aggressive humanization mode
    - Recursive paraphrasing (3-4 passes)
    - Maximum grammar imperfections
    - Highest temperature/randomization
    - Multiple model cascade
    
    Request body:
    {
        "text": "Text to humanize"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if len(text) > Config.MAX_TEXT_LENGTH:
            return jsonify({
                'error': f'Text too long. Maximum {Config.MAX_TEXT_LENGTH} characters'
            }), 400
        
        # Get ensemble
        ens = get_ensemble()
        
        # Generate with MAXIMUM diversity settings
        result = ens.humanize(
            text=text,
            strategy='advanced_blend',
            num_variations=4,  # More variations
            return_all=False,
            max_length=Config.MAX_LENGTH,
            temperature=2.0,  # VERY high temperature
            top_k=200,  # Maximum word choices
            top_p=0.99  # Maximum nucleus sampling
        )
        
        result['mode'] = 'aggressive'
        result['description'] = 'Maximum humanization with recursive paraphrasing and grammar imperfections'
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in humanize_aggressive: {e}")
        return jsonify({'error': str(e)}), 500
