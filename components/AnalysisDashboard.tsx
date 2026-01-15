
import React, { useState } from 'react';
import { AnalysisResult, FlaggedSection, GrammarIssue } from '../types';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

interface Props {
  result: AnalysisResult;
  onReset: () => void;
  onRefine: () => void;
  fileName: string;
  rawText: string;
  fileBlob?: Blob;
}

const AnalysisDashboard: React.FC<Props> = ({ result, onReset, onRefine, fileName, rawText, fileBlob }) => {
  const [activeTab, setActiveTab] = useState<'annotated' | 'preview' | 'grammar'>('annotated');
  
  const originalityScore = Math.max(0, 100 - result.similarityScore);
  const COLORS = ['#10b981', '#f1f5f9']; // Green for original, Light slate for matches
  const chartData = [
    { name: 'Originality', value: originalityScore },
    { name: 'Matches', value: result.similarityScore },
  ];

  const highlightText = (text: string, flagged: FlaggedSection[]) => {
    if (!flagged || flagged.length === 0) return text;
    const sortedFlagged = [...flagged].sort((a, b) => b.text.length - a.text.length);
    let highlighted = text;
    sortedFlagged.forEach((section) => {
      const colorClass = section.type === 'plagiarism' ? 'bg-red-100 border-b-2 border-red-400' : 'bg-orange-100 border-b-2 border-orange-400';
      const escapedText = section.text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`(${escapedText})`, 'gi');
      highlighted = highlighted.replace(regex, `<span class="${colorClass} cursor-help px-0.5" title="${section.reason}">$1</span>`);
    });
    return highlighted;
  };

  const getMetricColor = (title: string, value: number) => {
    if (title === 'AI Prob.') return value >= 85 ? 'red' : value > 50 ? 'amber' : 'green';
    if (title === 'Plagiarism') return value > 30 ? 'red' : value > 15 ? 'amber' : 'green';
    return 'indigo';
  };

  const metrics = [
    { title: 'AI Prob.', value: result.aiLikelihood, icon: 'fa-robot', desc: 'GPTZero Calibration' },
    { title: 'Plagiarism', value: result.similarityScore, icon: 'fa-copy', desc: 'Universal Match' },
    { title: 'Words', value: result.wordCount, icon: 'fa-file-word', desc: 'Submission Size', noPercent: true },
    { title: 'Grammar', value: result.grammarScore, icon: 'fa-spell-check', desc: 'Accuracy Check' },
    { title: 'Clarity', value: result.clarityScore, icon: 'fa-feather', desc: 'Flow & Tone' }
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-700 pb-24">
      {/* Risk Alert Banner for High AI Probability */}
      {result.aiLikelihood >= 85 && (
        <div className="bg-red-600 text-white px-6 py-4 rounded-3xl flex items-center justify-between shadow-2xl animate-pulse">
          <div className="flex items-center gap-4">
            <i className="fas fa-triangle-exclamation text-2xl"></i>
            <div>
              <p className="font-black uppercase tracking-tighter">Critical AI Detection Alert</p>
              <p className="text-sm opacity-90">This document shows heavy markers of LLM generation (90%+ confidence).</p>
            </div>
          </div>
          <button onClick={onRefine} className="bg-white text-red-600 px-6 py-2 rounded-xl font-black text-sm hover:bg-slate-100 transition-all">
            FIX NOW
          </button>
        </div>
      )}

      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
        <div>
          <div className="flex items-center gap-2 text-indigo-600 font-black mb-2 uppercase tracking-tighter text-sm">
            <span className="bg-indigo-600 text-white px-2 py-0.5 rounded text-[10px]">SUPREME SCAN</span>
            Analysis Complete
          </div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Integrity Audit <span className="text-indigo-600">Report</span></h2>
          <p className="text-slate-500 font-medium">Document: <span className="text-slate-900 font-bold">{fileName}</span></p>
        </div>
        <div className="flex gap-4 w-full lg:w-auto">
          <button onClick={onReset} className="flex-1 lg:flex-none px-6 py-3 bg-white border border-slate-200 rounded-2xl text-slate-700 font-bold hover:bg-slate-50 transition-all shadow-sm">
            <i className="fas fa-plus mr-2"></i> New Analysis
          </button>
          <button onClick={onRefine} className="flex-1 lg:flex-none px-10 py-3 bg-indigo-600 text-white font-bold rounded-2xl hover:bg-indigo-700 transition-all shadow-xl hover:-translate-y-0.5">
            <i className="fas fa-wand-magic-sparkles mr-2"></i> Humanize Draft
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {metrics.map((card, idx) => {
          const color = getMetricColor(card.title, card.value);
          const isHighRisk = card.title === 'AI Prob.' && card.value >= 85;
          return (
            <div key={idx} className={`bg-white p-6 rounded-3xl shadow-sm border ${isHighRisk ? 'border-red-500 shadow-red-100' : 'border-slate-100'} group hover:shadow-xl transition-all relative overflow-hidden`}>
              <div className="flex items-center justify-between mb-4 relative z-10">
                <div className={`p-3 rounded-2xl ${isHighRisk ? 'bg-red-600 text-white' : `bg-${color}-50 text-${color}-600`} group-hover:scale-110 transition-transform`}>
                  <i className={`fas ${card.icon} text-xl`}></i>
                </div>
                <span className="text-xs font-black text-slate-400 uppercase tracking-widest">{card.title}</span>
              </div>
              <div className={`text-4xl font-black mb-1 relative z-10 ${isHighRisk ? 'text-red-600' : 'text-slate-900'}`}>
                {card.value}{!card.noPercent && '%'}
              </div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider relative z-10">{card.desc}</p>
              {isHighRisk && <div className="absolute -bottom-4 -right-4 w-20 h-20 bg-red-600 opacity-5 rotate-12"></div>}
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 relative">
            <h3 className="font-black text-slate-900 mb-8 uppercase tracking-widest text-xs flex items-center gap-2">
              <i className="fas fa-chart-pie text-indigo-600"></i> Originality Score
            </h3>
            <div className="h-64 relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie 
                    data={chartData} 
                    cx="50%" 
                    cy="50%" 
                    innerRadius={75} 
                    outerRadius={95} 
                    paddingAngle={0} 
                    dataKey="value"
                    startAngle={90}
                    endAngle={-270}
                  >
                    {chartData.map((e, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} stroke="none" />)}
                  </Pie>
                  <Tooltip cursor={false} content={() => null} />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-5xl font-black text-slate-900">{originalityScore}%</span>
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mt-1">Unique</span>
              </div>
            </div>
            <div className="mt-4 flex justify-center gap-6">
               <div className="flex items-center gap-2">
                 <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                 <span className="text-[10px] font-black text-slate-500 uppercase">Original Content</span>
               </div>
               <div className="flex items-center gap-2">
                 <div className="w-3 h-3 rounded-full bg-slate-200"></div>
                 <span className="text-[10px] font-black text-slate-500 uppercase">Matched Data</span>
               </div>
            </div>
          </div>

          <div className="bg-slate-900 p-8 rounded-3xl shadow-2xl text-white">
            <h3 className="font-black text-indigo-300 mb-6 uppercase tracking-widest text-xs">Knowledge Matches</h3>
            <div className="space-y-6">
              {result.sources.length > 0 ? result.sources.map((s, i) => (
                <div key={i} className="group">
                  <div className="flex justify-between items-center mb-2">
                    <div className="flex flex-col">
                      <span className="text-[10px] font-black text-indigo-400 uppercase mb-0.5">{s.sourceType}</span>
                      <a href={s.url} target="_blank" className="text-sm font-bold text-slate-100 hover:text-indigo-300 truncate max-w-[180px]">{s.title}</a>
                    </div>
                    <span className="text-xs font-black text-red-400">{s.matchPercentage}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div className="bg-red-500 h-full rounded-full transition-all duration-1000" style={{ width: `${s.matchPercentage}%` }}></div>
                  </div>
                </div>
              )) : (
                <div className="text-center py-4 text-slate-500 text-xs italic">
                  No public knowledge matches found.
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="lg:col-span-8 space-y-6">
          <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden flex flex-col h-[800px]">
            <div className="px-8 py-6 border-b border-slate-50 flex flex-wrap justify-between items-center bg-slate-50/50 gap-4">
              <div className="flex gap-2 p-1.5 bg-slate-200 rounded-2xl shrink-0">
                <button 
                  onClick={() => setActiveTab('annotated')}
                  className={`px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${activeTab === 'annotated' ? 'bg-white text-indigo-600 shadow-md' : 'text-slate-500 hover:text-slate-700'}`}
                >
                  Document Scan
                </button>
                <button 
                  onClick={() => setActiveTab('grammar')}
                  className={`px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${activeTab === 'grammar' ? 'bg-white text-indigo-600 shadow-md' : 'text-slate-500 hover:text-slate-700'}`}
                >
                  Grammar ({result.grammarIssues.length})
                </button>
                {fileBlob && (
                  <button 
                    onClick={() => setActiveTab('preview')}
                    className={`px-6 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${activeTab === 'preview' ? 'bg-white text-indigo-600 shadow-md' : 'text-slate-500 hover:text-slate-700'}`}
                  >
                    PDF Viewer
                  </button>
                )}
              </div>
            </div>
            
            <div className="flex-grow overflow-y-auto p-10 bg-white custom-scrollbar">
              {activeTab === 'annotated' && (
                <div 
                  className="prose prose-slate max-w-none text-slate-800 leading-relaxed font-serif text-xl whitespace-pre-wrap selection:bg-indigo-100"
                  dangerouslySetInnerHTML={{ __html: highlightText(rawText, result.flaggedSections) }}
                />
              )}
              
              {activeTab === 'grammar' && (
                <div className="space-y-6">
                  {result.grammarIssues.length > 0 ? result.grammarIssues.map((issue, i) => (
                    <div key={i} className="p-6 bg-slate-50 border border-slate-100 rounded-2xl flex gap-6 hover:border-indigo-200 transition-colors">
                      <div className="shrink-0 w-12 h-12 bg-white rounded-xl shadow-sm flex items-center justify-center text-indigo-600">
                        <i className={`fas ${issue.type === 'spelling' ? 'fa-spell-check' : 'fa-pen-nib'}`}></i>
                      </div>
                      <div className="space-y-3">
                        <div className="flex items-center gap-3">
                          <span className="line-through text-red-400 font-medium italic">{issue.original}</span>
                          <i className="fas fa-arrow-right text-slate-300 text-xs"></i>
                          <span className="text-green-600 font-black">{issue.correction}</span>
                        </div>
                        <p className="text-sm text-slate-600 leading-relaxed font-medium">{issue.explanation}</p>
                        <span className="text-[10px] font-black uppercase text-slate-400 tracking-widest bg-white px-2 py-1 rounded-md border border-slate-100">{issue.type} issue</span>
                      </div>
                    </div>
                  )) : (
                    <div className="text-center py-24 text-slate-300">
                      <i className="fas fa-check-circle text-6xl mb-4 opacity-10"></i>
                      <p className="font-black uppercase tracking-widest text-sm">Perfect Grammatical Accuracy</p>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'preview' && fileBlob && (
                <iframe 
                  src={URL.createObjectURL(fileBlob)} 
                  className="w-full h-full rounded-2xl border border-slate-100 shadow-inner min-h-[600px]"
                  title="PDF Original Preview"
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisDashboard;
