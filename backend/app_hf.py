from flask import Flask, request, jsonify
from flask_cors import CORS
from models.advanced_ensemble import AdvancedEnsembleHumanizer
from utils.advanced_metrics_v2 import AdvancedTextMetrics
from utils.enhanced_preprocessor import EnhancedPreprocessor
from config_v2 import Config
import os

app = Flask(__name__)

# Allow CORS for all origins (Hugging Face Spaces)
CORS(app, origins='*')

# Initialize advanced ensemble (lazy loading)
advanced_ensemble = None

def get_advanced_ensemble():
    """Lazy load advanced ensemble to avoid loading models on import"""
    global advanced_ensemble
    if advanced_ensemble is None:
        print("Initializing ADVANCED Ensemble Humanizer (Hugging Face GPU)...")
        advanced_ensemble = AdvancedEnsembleHumanizer(
            device=Config.DEVICE,
            use_bart=True,
            use_t5=True,
            use_pegasus=True
        )
        print("Advanced Ensemble ready on Hugging Face!")
    return advanced_ensemble

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'name': 'AI Humanizer v2.0',
        'version': '2.0',
        'status': 'running',
        'hosting': 'huggingface',
        'gpu': Config.DEVICE,
        'endpoints': {
            'health': '/health',
            'humanize': '/api/humanize',
            'humanize_ultra': '/api/humanize/ultra',
            'metrics': '/api/metrics',
            'compare': '/api/compare',
            'batch': '/api/batch',
            'analyze': '/api/analyze',
            'models_info': '/api/models/info'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    ensemble = get_advanced_ensemble()
    return jsonify({
        'status': 'healthy',
        'models_loaded': ensemble is not None,
        'device': Config.DEVICE,
        'gpu_available': Config.DEVICE == 'cuda',
        'version': '2.0-huggingface'
    })

@app.route('/api/humanize', methods=['POST'])
def humanize_text():
    """
    Advanced humanization endpoint with multiple strategies
    
    Request body:
    {
        "text": "Text to humanize",
        "strategy": "adaptive" | "cascade" | "style_transfer" | "mixed",
        "num_variations": 3,
        "return_all": false,
        "use_gpt2": true
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
        
        strategy = data.get('strategy', 'adaptive')
        num_variations = data.get('num_variations', 3)
        return_all = data.get('return_all', False)
        use_gpt2 = data.get('use_gpt2', True)
        
        valid_strategies = ['adaptive', 'cascade', 'style_transfer', 'mixed', 'advanced_blend', 'weighted', 'diverse', 'best']
        if strategy not in valid_strategies:
            return jsonify({
                'error': f'Invalid strategy. Must be one of: {valid_strategies}'
            }), 400
        
        ens = get_advanced_ensemble()
        
        result = ens.humanize(
            text=text,
            strategy=strategy,
            num_variations=num_variations,
            return_all=return_all,
            max_length=Config.MAX_LENGTH
        )
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in humanize_text: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/humanize/ultra', methods=['POST'])
def humanize_text_ultra():
    """
    ULTRA advanced humanization - Maximum detection evasion
    Uses all advanced techniques with aggressive parameters
    
    Request body:
    {
        "text": "Text to humanize",
        "strategy": "adaptive"
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
        
        strategy = data.get('strategy', 'adaptive')
        
        ens = get_advanced_ensemble()
        
        # Apply enhanced preprocessing first
        preprocessor = EnhancedPreprocessor()
        preprocessed = preprocessor.comprehensive_enhancement(text)
        
        # Humanize with ultra settings
        result = ens.humanize(
            text=preprocessed,
            strategy=strategy,
            num_variations=Config.ULTRA_NUM_VARIATIONS,
            return_all=False,
            max_length=Config.MAX_LENGTH
        )
        
        # Apply final enhancement
        final_text = preprocessor.comprehensive_enhancement(result['text'])
        
        # Recalculate metrics
        metrics_calculator = AdvancedTextMetrics()
        final_metrics = metrics_calculator.calculate_comprehensive_score(final_text, use_gpt2=True)
        
        result['text'] = final_text
        result['metrics'] = final_metrics
        result['score'] = final_metrics['composite_score']
        result['mode'] = 'ultra'
        result['description'] = 'Maximum detection evasion with multi-stage enhancement'
        result['hosting'] = 'huggingface-gpu'
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in humanize_text_ultra: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics', methods=['POST'])
def get_metrics():
    """
    Get advanced metrics for text without humanizing
    
    Request body:
    {
        "text": "Text to analyze",
        "use_gpt2": true (optional, default true for accuracy)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        use_gpt2 = data.get('use_gpt2', True)
        
        metrics_calculator = AdvancedTextMetrics()
        metrics = metrics_calculator.calculate_comprehensive_score(text, use_gpt2=use_gpt2)
        
        return jsonify(metrics)
    
    except Exception as e:
        print(f"Error in get_metrics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_texts():
    """
    Compare two texts (original vs humanized) with advanced metrics
    
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
        
        ens = get_advanced_ensemble()
        comparison = ens.compare_texts(data['original'], data['humanized'])
        
        return jsonify(comparison)
    
    except Exception as e:
        print(f"Error in compare_texts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def batch_humanize():
    """
    Humanize multiple texts in batch with advanced processing
    
    Request body:
    {
        "texts": ["text1", "text2", ...],
        "strategy": "adaptive"
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
        
        strategy = data.get('strategy', 'adaptive')
        
        ens = get_advanced_ensemble()
        preprocessor = EnhancedPreprocessor()
        
        results = []
        for text in texts:
            if len(text.strip()) < 10:
                results.append({'error': 'Text too short'})
                continue
            
            # Apply preprocessing
            preprocessed = preprocessor.comprehensive_enhancement(text)
            
            # Humanize
            result = ens.humanize(
                text=preprocessed,
                strategy=strategy,
                num_variations=3,
                return_all=False,
                max_length=Config.MAX_LENGTH
            )
            
            results.append(result)
        
        return jsonify({'results': results})
    
    except Exception as e:
        print(f"Error in batch_humanize: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Deep text analysis for optimization recommendations
    
    Request body:
    {
        "text": "Text to analyze"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        ens = get_advanced_ensemble()
        
        # Analyze text characteristics
        text_analysis = ens._analyze_text_characteristics(text)
        
        # Calculate metrics
        metrics_calculator = AdvancedTextMetrics()
        metrics = metrics_calculator.calculate_comprehensive_score(text, use_gpt2=True)
        
        # Generate recommendations
        recommendations = []
        
        if text_analysis['vocabulary_diversity'] < 0.5:
            recommendations.append('Increase vocabulary diversity - use more varied words and synonyms')
        
        if text_analysis['avg_sentence_length'] > 25:
            recommendations.append('Sentence length too long - break down into shorter sentences')
        
        if metrics['perplexity'] < 40:
            recommendations.append('Text too predictable - add more variety and unexpected elements')
        
        if metrics['burstiness'] < 40:
            recommendations.append('Burstiness too low - vary sentence lengths dramatically')
        
        if metrics['repetitive_patterns']['repetition_score'] > 50:
            recommendations.append('Too much repetition - vary phrasing and sentence structure')
        
        # Suggest optimal strategy
        optimal_strategy = 'adaptive'
        if text_analysis['category'] == 'academic':
            optimal_strategy = 'style_transfer'
        elif text_analysis['vocabulary_diversity'] > 0.6:
            optimal_strategy = 'cascade'
        
        recommendations.append(f'Optimal strategy: {optimal_strategy}')
        
        return jsonify({
            'text_analysis': text_analysis,
            'metrics': metrics,
            'recommendations': recommendations,
            'overall_score': metrics['composite_score'],
            'detection_risk': 'LOW' if metrics['composite_score'] > 75 else 'MEDIUM' if metrics['composite_score'] > 50 else 'HIGH',
            'hosting': 'huggingface-gpu'
        })
    
    except Exception as e:
        print(f"Error in analyze_text: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/info', methods=['GET'])
def get_models_info():
    """Get information about loaded models and capabilities"""
    ens = get_advanced_ensemble()
    info = ens.get_model_info()
    info['hosting'] = 'huggingface-gpu'
    info['gpu_available'] = Config.DEVICE == 'cuda'
    return jsonify(info)

if __name__ == '__main__':
    # Hugging Face Spaces uses port 7860
    port = int(os.getenv('PORT', 7860))
    
    # Auto-detect GPU in Hugging Face environment
    import torch
    if torch.cuda.is_available():
        Config.DEVICE = 'cuda'
        print("GPU detected! Using CUDA for acceleration.")
    else:
        Config.DEVICE = 'cpu'
        print("No GPU detected. Using CPU.")
    
    print("=" * 70)
    print("Starting Advanced AI Humanization API v2.0 (Hugging Face)")
    print(f"Server running on port {port}")
    print(f"Device: {Config.DEVICE}")
    print(f"Strategies: adaptive, cascade, style_transfer, mixed")
    print(f"Special endpoints: /api/humanize/ultra for maximum evasion")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=port)
