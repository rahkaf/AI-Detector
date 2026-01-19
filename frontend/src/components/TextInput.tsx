import React, { useState } from 'react';
import { Strategy } from '../types';

interface Props {
  onHumanize: (text: string, strategy: Strategy, aggressiveMode?: boolean) => void;
  isProcessing: boolean;
}

const TextInput: React.FC<Props> = ({ onHumanize, isProcessing }) => {
  const [text, setText] = useState('');
  const [strategy, setStrategy] = useState<Strategy>('advanced_blend');
  const [aggressiveMode, setAggressiveMode] = useState(false);
  
  const wordCount = text.trim().split(/\s+/).filter(w => w.length > 0).length;
  const charCount = text.length;
  
  const handleSubmit = () => {
    if (text.trim().length < 10) {
      alert('Please enter at least 10 characters');
      return;
    }
    onHumanize(text, strategy, aggressiveMode);
  };
  
  const strategies = [
    { value: 'advanced_blend', label: 'Advanced Blend', icon: 'fa-wand-magic-sparkles', desc: 'Recursive paraphrasing (Best)' },
    { value: 'weighted', label: 'Weighted', icon: 'fa-balance-scale', desc: 'Balanced approach' },
    { value: 'diverse', label: 'Diverse', icon: 'fa-shuffle', desc: 'Maximum variation' },
    { value: 'mixed', label: 'Mixed', icon: 'fa-layer-group', desc: 'Sentence blending' },
    { value: 'best', label: 'Best', icon: 'fa-trophy', desc: 'Highest score' },
  ];
  
  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-in">
      <div className="text-center space-y-4 mb-12">
        <div className="inline-block">
          <div className="flex items-center gap-2 bg-red-50 text-red-600 px-4 py-2 rounded-full text-xs font-black uppercase tracking-wider border border-red-200">
            <i className="fas fa-shield-halved"></i>
            <span>AI Detection Bypass</span>
          </div>
        </div>
        <h1 className="text-5xl md:text-6xl font-black text-gray-900 tracking-tight">
          Make AI Text <span className="gradient-text">Undetectable</span>
        </h1>
        <p className="text-xl text-gray-600 font-medium max-w-2xl mx-auto">
          Transform AI-generated content into human-like writing that bypasses GPTZero, Originality.ai, and all major detectors.
        </p>
      </div>
      
      <div className="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
        <div className="p-6 border-b border-gray-100 bg-gradient-to-r from-indigo-50 to-purple-50">
          <div className="flex flex-wrap justify-between items-center gap-4">
            <div>
              <h3 className="text-sm font-black text-gray-900 uppercase tracking-wider mb-1">
                <i className="fas fa-paste mr-2 text-indigo-600"></i>
                Input Text
              </h3>
              <p className="text-xs text-gray-500 font-medium">Paste your AI-generated content below</p>
            </div>
            <div className="flex gap-4 text-xs">
              <div className="bg-white px-3 py-1.5 rounded-lg border border-gray-200">
                <span className="font-bold text-gray-900">{wordCount}</span>
                <span className="text-gray-500 ml-1">words</span>
              </div>
              <div className="bg-white px-3 py-1.5 rounded-lg border border-gray-200">
                <span className="font-bold text-gray-900">{charCount}</span>
                <span className="text-gray-500 ml-1">chars</span>
              </div>
            </div>
          </div>
        </div>
        
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={isProcessing}
          placeholder="Paste your AI-generated text here... (minimum 10 characters)"
          className="w-full p-8 text-lg leading-relaxed outline-none resize-none font-serif text-gray-800 placeholder:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
          rows={12}
        />
        
        <div className="p-6 border-t border-gray-100 bg-gray-50">
          <div className="flex flex-col gap-4">
            {/* Aggressive Mode Toggle */}
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-red-50 to-orange-50 rounded-xl border-2 border-red-200">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-red-100 text-red-600 rounded-lg flex items-center justify-center">
                  <i className="fas fa-fire text-lg"></i>
                </div>
                <div>
                  <h4 className="text-sm font-black text-gray-900 uppercase tracking-wider">
                    Aggressive Mode
                  </h4>
                  <p className="text-xs text-gray-600 font-medium">
                    Maximum humanization: 3-4 recursive passes + grammar imperfections
                  </p>
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={aggressiveMode}
                  onChange={(e) => setAggressiveMode(e.target.checked)}
                  disabled={isProcessing}
                  className="sr-only peer"
                />
                <div className="w-14 h-7 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-red-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-red-600"></div>
              </label>
            </div>
            
            <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
              <div className="flex-1">
                <label className="text-xs font-black text-gray-700 uppercase tracking-wider mb-3 block">
                  <i className="fas fa-sliders mr-2"></i>
                  Humanization Strategy
                </label>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                  {strategies.map((s) => (
                    <button
                      key={s.value}
                      onClick={() => setStrategy(s.value as Strategy)}
                      disabled={isProcessing}
                      className={`p-3 rounded-xl border-2 transition-all text-left ${
                        strategy === s.value
                          ? 'border-indigo-600 bg-indigo-50'
                          : 'border-gray-200 bg-white hover:border-gray-300'
                      } disabled:opacity-50 disabled:cursor-not-allowed`}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <i className={`fas ${s.icon} text-sm ${strategy === s.value ? 'text-indigo-600' : 'text-gray-400'}`}></i>
                        <span className={`text-xs font-bold ${strategy === s.value ? 'text-indigo-600' : 'text-gray-700'}`}>
                          {s.label}
                        </span>
                      </div>
                      <p className="text-[10px] text-gray-500 font-medium">{s.desc}</p>
                    </button>
                  ))}
                </div>
              </div>
              
              <button
                onClick={handleSubmit}
                disabled={isProcessing || text.trim().length < 10}
                className={`w-full md:w-auto px-10 py-4 font-black rounded-2xl hover:shadow-2xl hover:-translate-y-1 active:translate-y-0 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-lg ${
                  aggressiveMode
                    ? 'bg-gradient-to-r from-red-600 to-orange-600 text-white'
                    : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                }`}
              >
                {isProcessing ? (
                  <span className="flex items-center justify-center gap-3">
                    <i className="fas fa-spinner fa-spin"></i>
                    Processing...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-3">
                    <i className={`fas ${aggressiveMode ? 'fa-fire' : 'fa-wand-magic-sparkles'}`}></i>
                    {aggressiveMode ? 'Aggressive Humanize' : 'Humanize Text'}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        {[
          { icon: 'fa-robot', title: 'Ensemble AI', desc: 'BART + T5 + PEGASUS' },
          { icon: 'fa-chart-line', title: 'Smart Metrics', desc: 'Perplexity & Burstiness' },
          { icon: 'fa-shield-check', title: '100% Bypass', desc: 'All Major Detectors' },
        ].map((feature, i) => (
          <div key={i} className="bg-white p-6 rounded-2xl border border-gray-100 hover:shadow-lg transition-shadow">
            <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center mx-auto mb-3">
              <i className={`fas ${feature.icon} text-xl`}></i>
            </div>
            <h4 className="font-black text-gray-900 mb-1">{feature.title}</h4>
            <p className="text-xs text-gray-500 font-medium">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TextInput;
