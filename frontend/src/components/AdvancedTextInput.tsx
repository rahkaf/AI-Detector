import React, { useState } from 'react';
import { Strategy, ProcessMode, PROCESS_MODES, STRATEGY_DESCRIPTIONS } from '../types_v2';

interface Props {
  onHumanize: (text: string, strategy: Strategy, mode: 'standard' | 'ultra') => void;
  isProcessing: boolean;
}

const AdvancedTextInput: React.FC<Props> = ({ onHumanize, isProcessing }) => {
  const [text, setText] = useState('');
  const [strategy, setStrategy] = useState<Strategy>('adaptive');
  const [mode, setMode] = useState<'standard' | 'ultra'>('standard');
  const [charCount, setCharCount] = useState(0);

  const handleSubmit = () => {
    if (text.trim().length >= 10 && !isProcessing) {
      onHumanize(text, strategy, mode);
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newText = e.target.value;
    setText(newText);
    setCharCount(newText.length);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Mode Selection */}
      <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-black text-gray-900 mb-4 flex items-center gap-2">
          <i className="fas fa-sliders text-indigo-600"></i>
          Processing Mode
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {PROCESS_MODES.map((processMode) => (
            <button
              key={processMode.value}
              onClick={() => setMode(processMode.value)}
              className={`p-4 rounded-2xl border-2 transition-all text-left ${
                mode === processMode.value
                  ? 'border-indigo-600 bg-indigo-50'
                  : 'border-gray-200 hover:border-indigo-300'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <span className="font-bold text-gray-900">{processMode.label}</span>
                {processMode.recommended && (
                  <span className="text-xs font-black text-emerald-600 bg-emerald-100 px-2 py-1 rounded-full">
                    RECOMMENDED
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-600 mb-2">{processMode.description}</p>
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <i className="fas fa-clock"></i>
                <span>{processMode.processingTime}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Strategy Selection */}
      <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-black text-gray-900 mb-4 flex items-center gap-2">
          <i className="fas fa-wand-magic-sparkles text-indigo-600"></i>
          Strategy Selection
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {(['adaptive', 'cascade', 'style_transfer', 'mixed', 'weighted', 'diverse', 'best'] as Strategy[]).map((strat) => (
            <button
              key={strat}
              onClick={() => setStrategy(strat)}
              className={`p-4 rounded-xl border-2 transition-all text-left ${
                strategy === strat
                  ? 'border-indigo-600 bg-indigo-50'
                  : 'border-gray-200 hover:border-indigo-300'
              }`}
            >
              <span className="block font-bold text-gray-900 mb-1 capitalize">
                {strat.replace('_', ' ')}
              </span>
              <span className="text-xs text-gray-500 line-clamp-2">
                {STRATEGY_DESCRIPTIONS[strat]}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Text Input */}
      <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-black text-gray-900 flex items-center gap-2">
            <i className="fas fa-pen-to-square text-indigo-600"></i>
            Input Text
          </h3>
          <div className="flex items-center gap-4 text-sm">
            <span className={`font-bold ${
              charCount < 10 ? 'text-red-500' :
              charCount > 10000 ? 'text-amber-500' :
              'text-gray-600'
            }`}>
              {charCount.toLocaleString()} / 10,000
            </span>
            <button
              onClick={() => { setText(''); setCharCount(0); }}
              className="text-gray-400 hover:text-gray-600 transition-colors"
              disabled={!text}
            >
              <i className="fas fa-trash"></i>
            </button>
          </div>
        </div>

        <textarea
          value={text}
          onChange={handleTextChange}
          placeholder="Paste your AI-generated text here to humanize it..."
          className={`w-full h-64 p-4 rounded-2xl border-2 resize-none transition-all text-gray-800 font-serif leading-relaxed ${
            text.length > 10000 ? 'border-red-300 focus:border-red-500' :
            text.length >= 10 ? 'border-gray-300 focus:border-indigo-500' :
            'border-gray-200 focus:border-gray-300'
          }`}
          disabled={isProcessing}
        />

        {charCount > 10000 && (
          <p className="mt-3 text-sm text-amber-600 flex items-center gap-2">
            <i className="fas fa-exclamation-triangle"></i>
            Text exceeds maximum length. Please shorten your text.
          </p>
        )}

        <button
          onClick={handleSubmit}
          disabled={text.trim().length < 10 || text.length > 10000 || isProcessing}
          className={`w-full mt-6 py-5 rounded-2xl font-black text-lg transition-all shadow-xl ${
            isProcessing
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 hover:scale-[1.02] active:scale-[0.98]'
          }`}
        >
          {isProcessing ? (
            <div className="flex items-center justify-center gap-3">
              <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              <span>{mode === 'ultra' ? 'Processing (Ultra Mode)...' : 'Processing...'}</span>
            </div>
          ) : (
            <div className="flex items-center justify-center gap-3">
              <i className="fas fa-wand-magic-sparkles"></i>
              <span>{mode === 'ultra' ? 'Humanize with Ultra Mode' : 'Humanize Text'}</span>
              {mode === 'ultra' && (
                <span className="text-xs bg-white/20 px-3 py-1 rounded-full">
                  MAXIMUM EVASION
                </span>
              )}
            </div>
          )}
        </button>
      </div>

      {/* Info Card */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-3xl p-6 border border-indigo-100">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 bg-indigo-100 rounded-2xl flex items-center justify-center">
            <i className="fas fa-lightbulb text-indigo-600 text-xl"></i>
          </div>
          <div>
            <h4 className="font-bold text-gray-900 mb-2">Detection Evasion Tips</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>• <strong>Adaptive</strong> strategy automatically selects optimal approach</li>
              <li>• <strong>Ultra Mode</strong> provides maximum evasion but takes longer</li>
              <li>• <strong>Cascade</strong> strategy passes text through multiple models</li>
              <li>• Text with higher vocabulary diversity shows better results</li>
              <li>• Varying sentence lengths improves burstiness scores</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedTextInput;
