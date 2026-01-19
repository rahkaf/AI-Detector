import React, { useState } from 'react';
import { HumanizeResult } from '../types';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, RadarChart, PolarGrid, PolarAngleAxis, Radar } from 'recharts';

interface Props {
  result: HumanizeResult;
  originalText: string;
  onReset: () => void;
}

const ResultsDashboard: React.FC<Props> = ({ result, originalText, onReset }) => {
  const [activeTab, setActiveTab] = useState<'humanized' | 'original' | 'comparison'>('humanized');
  const [copied, setCopied] = useState(false);
  
  const handleCopy = () => {
    navigator.clipboard.writeText(result.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  const metrics = result.metrics;
  const compositeScore = metrics.composite_score;
  
  // Pie chart data
  const pieData = [
    { name: 'Human-like', value: compositeScore },
    { name: 'Detection Risk', value: 100 - compositeScore },
  ];
  
  // Radar chart data - now with advanced metrics
  const radarData = [
    { metric: 'Perplexity', value: metrics.perplexity },
    { metric: 'Burstiness', value: metrics.burstiness },
    { metric: 'Bigram', value: metrics.bigram_entropy },
    { metric: 'Trigram', value: metrics.trigram_entropy },
    { metric: 'POS', value: metrics.pos_entropy },
    { metric: 'Coherence', value: metrics.semantic_coherence },
  ];
  
  const getScoreColor = (score: number) => {
    if (score >= 75) return 'emerald';
    if (score >= 50) return 'amber';
    return 'red';
  };
  
  const scoreColor = getScoreColor(compositeScore);
  
  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in pb-24">
      {/* Success Banner */}
      <div className="bg-gradient-to-r from-emerald-600 to-green-600 text-white px-8 py-6 rounded-3xl flex flex-col md:flex-row items-center justify-between shadow-2xl">
        <div className="flex items-center gap-4 mb-4 md:mb-0">
          <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center">
            <i className="fas fa-check-circle text-3xl"></i>
          </div>
          <div>
            <p className="font-black uppercase tracking-wider text-sm mb-1">Humanization Complete</p>
            <p className="text-emerald-100 text-sm">Your text is now undetectable by AI detection tools</p>
          </div>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={handleCopy}
            className="px-6 py-3 bg-white text-emerald-600 font-bold rounded-xl hover:bg-emerald-50 transition-all shadow-lg"
          >
            <i className={`fas ${copied ? 'fa-check' : 'fa-copy'} mr-2`}></i>
            {copied ? 'Copied!' : 'Copy Text'}
          </button>
          <button 
            onClick={onReset}
            className="px-6 py-3 bg-white/20 text-white font-bold rounded-xl hover:bg-white/30 transition-all"
          >
            <i className="fas fa-plus mr-2"></i>
            New Text
          </button>
        </div>
      </div>
      
      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {[
          { title: 'Composite', value: compositeScore, icon: 'fa-gauge-high', color: scoreColor },
          { title: 'Perplexity', value: metrics.perplexity, icon: 'fa-shuffle', color: 'indigo' },
          { title: 'Burstiness', value: metrics.burstiness, icon: 'fa-wave-square', color: 'purple' },
          { title: 'Bigram', value: metrics.bigram_entropy, icon: 'fa-link', color: 'blue' },
          { title: 'Trigram', value: metrics.trigram_entropy, icon: 'fa-project-diagram', color: 'cyan' },
          { title: 'POS Entropy', value: metrics.pos_entropy, icon: 'fa-language', color: 'teal' },
          { title: 'Coherence', value: metrics.semantic_coherence, icon: 'fa-brain', color: 'pink' },
          { title: 'Resistance', value: metrics.detection_resistance === 'HIGH' ? 85 : metrics.detection_resistance === 'MEDIUM' ? 60 : 35, icon: 'fa-shield-halved', color: 'emerald' },
        ].map((metric, i) => (
          <div key={i} className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 hover:shadow-xl transition-all group">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-2xl bg-${metric.color}-50 text-${metric.color}-600 group-hover:scale-110 transition-transform`}>
                <i className={`fas ${metric.icon} text-xl`}></i>
              </div>
              <span className="text-xs font-black text-gray-400 uppercase tracking-widest">{metric.title}</span>
            </div>
            <div className={`text-4xl font-black mb-1 text-${metric.color}-600`}>
              {typeof metric.value === 'string' ? metric.value : Math.round(metric.value)}%
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
              <div 
                className={`bg-${metric.color}-500 h-full rounded-full transition-all duration-1000`}
                style={{ width: `${typeof metric.value === 'number' ? metric.value : 0}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Charts and Text */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Charts */}
        <div className="lg:col-span-4 space-y-6">
          {/* Pie Chart */}
          <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
            <h3 className="font-black text-gray-900 mb-6 uppercase tracking-widest text-xs flex items-center gap-2">
              <i className="fas fa-chart-pie text-indigo-600"></i>
              Human-like Score
            </h3>
            <div className="h-64 relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie 
                    data={pieData} 
                    cx="50%" 
                    cy="50%" 
                    innerRadius={75} 
                    outerRadius={95} 
                    paddingAngle={0} 
                    dataKey="value"
                    startAngle={90}
                    endAngle={-270}
                  >
                    <Cell fill={compositeScore >= 75 ? '#10b981' : compositeScore >= 50 ? '#f59e0b' : '#ef4444'} />
                    <Cell fill="#f1f5f9" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-5xl font-black text-gray-900">{Math.round(compositeScore)}%</span>
                <span className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mt-1">Human</span>
              </div>
            </div>
          </div>
          
          {/* Radar Chart */}
          <div className="bg-gradient-to-br from-indigo-600 to-purple-600 p-8 rounded-3xl shadow-2xl text-white">
            <h3 className="font-black mb-6 uppercase tracking-widest text-xs flex items-center gap-2">
              <i className="fas fa-radar"></i>
              Metric Breakdown
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#ffffff40" />
                  <PolarAngleAxis dataKey="metric" stroke="#ffffff" tick={{ fill: '#ffffff', fontSize: 12 }} />
                  <Radar dataKey="value" stroke="#ffffff" fill="#ffffff" fillOpacity={0.3} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-indigo-200">Processing Time:</span>
                <span className="font-bold">{result.processing_time?.toFixed(2)}s</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-indigo-200">Model Used:</span>
                <span className="font-bold uppercase">{result.model || 'Ensemble'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-indigo-200">Strategy:</span>
                <span className="font-bold uppercase">{result.strategy}</span>
              </div>
            </div>
          </div>
          
          {/* Advanced Metrics Details */}
          <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
            <h3 className="font-black text-gray-900 mb-4 uppercase tracking-widest text-xs flex items-center gap-2">
              <i className="fas fa-chart-line text-indigo-600"></i>
              Advanced Analysis
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Detection Resistance:</span>
                <span className={`font-bold px-3 py-1 rounded-full text-xs ${
                  metrics.detection_resistance === 'HIGH' ? 'bg-emerald-100 text-emerald-700' :
                  metrics.detection_resistance === 'MEDIUM' ? 'bg-amber-100 text-amber-700' :
                  'bg-red-100 text-red-700'
                }`}>{metrics.detection_resistance}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Avg Word Length:</span>
                <span className="font-bold text-gray-900">{metrics.stylometric_features.avg_word_length.toFixed(1)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Avg Sentence Length:</span>
                <span className="font-bold text-gray-900">{metrics.stylometric_features.avg_sentence_length.toFixed(1)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Lexical Density:</span>
                <span className="font-bold text-gray-900">{(metrics.stylometric_features.lexical_density * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Repetition Score:</span>
                <span className={`font-bold ${metrics.repetitive_patterns.repetition_score < 30 ? 'text-emerald-600' : 'text-amber-600'}`}>
                  {metrics.repetitive_patterns.repetition_score.toFixed(0)}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Text Display */}
        <div className="lg:col-span-8">
          <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden flex flex-col h-[800px]">
            <div className="px-8 py-6 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div className="flex gap-2 p-1.5 bg-gray-200 rounded-2xl">
                <button 
                  onClick={() => setActiveTab('humanized')}
                  className={`px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${
                    activeTab === 'humanized' ? 'bg-white text-indigo-600 shadow-md' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <i className="fas fa-wand-magic-sparkles mr-2"></i>
                  Humanized
                </button>
                <button 
                  onClick={() => setActiveTab('original')}
                  className={`px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${
                    activeTab === 'original' ? 'bg-white text-indigo-600 shadow-md' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <i className="fas fa-file-lines mr-2"></i>
                  Original
                </button>
                <button 
                  onClick={() => setActiveTab('comparison')}
                  className={`px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${
                    activeTab === 'comparison' ? 'bg-white text-indigo-600 shadow-md' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <i className="fas fa-code-compare mr-2"></i>
                  Compare
                </button>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-gray-500">{metrics.word_count} words</span>
                <span className="text-gray-300">•</span>
                <span className="text-gray-500">{metrics.sentence_count} sentences</span>
              </div>
            </div>
            
            <div className="flex-grow overflow-y-auto p-10 bg-white">
              {activeTab === 'humanized' && (
                <div className="prose prose-lg max-w-none text-gray-800 leading-relaxed font-serif whitespace-pre-wrap">
                  {result.text}
                </div>
              )}
              
              {activeTab === 'original' && (
                <div className="prose prose-lg max-w-none text-gray-600 leading-relaxed font-serif whitespace-pre-wrap opacity-75">
                  {originalText}
                </div>
              )}
              
              {activeTab === 'comparison' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h4 className="text-xs font-black text-gray-400 uppercase tracking-wider mb-4">Original (AI)</h4>
                    <div className="prose prose-sm max-w-none text-gray-600 leading-relaxed font-serif whitespace-pre-wrap">
                      {originalText}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-xs font-black text-emerald-600 uppercase tracking-wider mb-4">Humanized</h4>
                    <div className="prose prose-sm max-w-none text-gray-800 leading-relaxed font-serif whitespace-pre-wrap">
                      {result.text}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDashboard;
