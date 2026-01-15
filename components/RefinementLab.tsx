
import React, { useState, useEffect } from 'react';
import { humanizeContent } from '../geminiService';

interface Props {
  initialText: string;
  onBack: () => void;
}

const RefinementLab: React.FC<Props> = ({ initialText, onBack }) => {
  const [text, setText] = useState(initialText);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [history, setHistory] = useState<string[]>([initialText]);

  const countWords = (t: string) => t.trim().split(/\s+/).filter(w => w.length > 0).length;

  const originalWords = countWords(initialText);
  const currentWords = countWords(text);
  const wordDiff = currentWords - originalWords;

  const handleHumanize = async () => {
    if (isProcessing) return;
    setIsProcessing(true);
    setShowSuccess(false);
    
    try {
      const humanized = await humanizeContent(text);
      if (humanized && humanized.trim() !== "" && humanized !== text) {
        setHistory(prev => [...prev, humanized]);
        setText(humanized);
        setShowSuccess(true);
      }
    } catch (err) {
      console.error("Ghostwriter process failed:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  useEffect(() => {
    if (showSuccess) {
      const timer = setTimeout(() => setShowSuccess(false), 4000);
      return () => clearTimeout(timer);
    }
  }, [showSuccess]);

  const undo = () => {
    if (history.length > 1) {
      const newHistory = history.slice(0, -1);
      setHistory(newHistory);
      setText(newHistory[newHistory.length - 1]);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-in fade-in zoom-in-95 duration-500">
      <div className="flex justify-between items-center">
        <div>
          <button onClick={onBack} className="text-slate-400 hover:text-indigo-600 flex items-center gap-2 mb-2 transition-colors font-bold text-xs uppercase tracking-widest">
            <i className="fas fa-arrow-left"></i> Exit Ghostwriter Mode
          </button>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Elite <span className="text-indigo-600">Ghostwriter</span> Lab</h2>
          <p className="text-slate-500 font-medium">Adversarial Rewrite for 100% Detection Bypass.</p>
        </div>
        <div className="flex gap-3">
          <div className="flex items-center gap-4 bg-white border border-slate-200 px-4 py-2 rounded-xl shadow-sm mr-2">
             <div className="text-center border-r border-slate-100 pr-4">
               <div className="text-[9px] font-black text-slate-400 uppercase leading-none mb-1">Original</div>
               <div className="text-sm font-bold text-slate-700">{originalWords}</div>
             </div>
             <div className="text-center">
               <div className="text-[9px] font-black text-slate-400 uppercase leading-none mb-1">Refined</div>
               <div className="text-sm font-bold text-indigo-600">{currentWords}</div>
             </div>
             {wordDiff !== 0 && (
               <div className={`text-[10px] font-black px-1.5 py-0.5 rounded ${wordDiff > 0 ? 'bg-emerald-50 text-emerald-600' : 'bg-red-50 text-red-600'}`}>
                 {wordDiff > 0 ? '+' : ''}{wordDiff}
               </div>
             )}
          </div>
          <button 
            onClick={undo}
            disabled={history.length <= 1 || isProcessing}
            className="px-4 py-2 bg-white border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 disabled:opacity-30 transition-all shadow-sm"
            title="Undo Edit"
          >
            <i className="fas fa-rotate-left"></i>
          </button>
          <button 
            onClick={() => {
              navigator.clipboard.writeText(text);
              setShowSuccess(true);
            }}
            className="px-6 py-2 bg-indigo-50 text-indigo-700 font-bold rounded-xl hover:bg-indigo-100 transition-all border border-indigo-100"
          >
            <i className="fas fa-copy mr-2"></i> Copy Final Draft
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[750px]">
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm flex flex-col overflow-hidden relative">
          <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/80 flex justify-between items-center">
            <div className="flex items-center gap-3">
               <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Ghostwriter Workspace</span>
               <span className="px-2 py-0.5 bg-red-100 text-red-600 text-[9px] font-black rounded uppercase tracking-tighter">Bypass Active</span>
            </div>
            <div className="flex items-center gap-2">
              {isProcessing && <div className="w-2 h-2 rounded-full bg-indigo-500 animate-ping"></div>}
              <span className={`text-[10px] font-bold ${isProcessing ? 'text-indigo-600' : 'text-green-600'}`}>
                {isProcessing ? 'RE-ENGINEERING...' : 'READY'}
              </span>
            </div>
          </div>
          
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={isProcessing}
            className={`flex-grow p-12 font-serif text-lg leading-relaxed outline-none resize-none transition-all duration-300 bg-white selection:bg-indigo-100 text-slate-900 placeholder:text-slate-300 ${isProcessing ? 'opacity-40 grayscale blur-[1px]' : 'opacity-100'}`}
            placeholder="Pasting AI-generated text here for ghostwriter rewrite..."
          />

          {showSuccess && (
            <div className="absolute top-20 left-1/2 -translate-x-1/2 bg-slate-900 text-white px-8 py-3 rounded-2xl text-sm font-black shadow-2xl animate-in slide-in-from-top-4 z-20 flex items-center gap-3">
              <i className="fas fa-user-secret text-indigo-400"></i> HUMAN SIGNATURE INJECTED
            </div>
          )}
        </div>

        <div className="space-y-6 overflow-y-auto custom-scrollbar pr-2">
          <div className="bg-slate-900 p-10 rounded-3xl shadow-2xl text-white relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
              <i className="fas fa-user-secret text-9xl"></i>
            </div>
            
            <h3 className="text-2xl font-black mb-4 flex items-center gap-3">
              <i className="fas fa-mask text-indigo-400"></i> Stealth Rewrite
            </h3>
            <p className="text-slate-400 text-sm mb-8 leading-relaxed font-medium">
              Activating adversarial semantic mapping. This process shifts word probability and sentence rhythm to break statistical detection markers.
            </p>
            
            <button 
              onClick={handleHumanize}
              disabled={isProcessing}
              className="w-full py-6 bg-indigo-600 text-white font-black rounded-2xl hover:bg-indigo-500 hover:shadow-2xl hover:-translate-y-1 active:translate-y-0 transition-all shadow-xl disabled:bg-slate-700 disabled:cursor-not-allowed group/btn overflow-hidden"
            >
              {isProcessing ? (
                <span className="flex items-center justify-center gap-3">
                  <i className="fas fa-user-ninja fa-spin"></i> ADVERSARIAL MAPPING...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-3">
                   START STEALTH REWRITE <i className="fas fa-fingerprint group-hover/btn:animate-pulse"></i>
                </span>
              )}
            </button>
            <div className="mt-6 flex justify-between items-center text-[9px] font-black text-slate-500 uppercase tracking-widest border-t border-slate-800 pt-6">
              <span>Target: GPTZero / Originality</span>
              <span className="text-green-500">Protocol: High Entropy</span>
            </div>
          </div>

          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-md">
            <h3 className="font-black text-slate-900 mb-6 uppercase tracking-widest text-xs flex items-center gap-2">
              <i className="fas fa-list-check text-indigo-600"></i> Adversarial Checklist
            </h3>
            <div className="grid grid-cols-1 gap-4">
              {[
                { icon: 'fa-shuffle', title: 'Perplexity Scaling', desc: 'Chooses statistically "surprising" word alternatives.' },
                { icon: 'fa-wave-square', title: 'Burstiness Optimization', desc: 'Extreme sentence length variation (3-30+ words).' },
                { icon: 'fa-ban', title: 'Cliché Scrubbing', desc: 'Eliminates "Delve", "Tapestry", "Furthermore".' },
                { icon: 'fa-bolt', title: 'Active Voice Shift', desc: 'Converts passive robotic syntax to direct human action.' },
                { icon: 'fa-brain', title: 'Linguistic Noise', desc: 'Injects natural structural imperfections and conjunction starts.' }
              ].map((tip, i) => (
                <div key={i} className="flex gap-4 p-4 rounded-2xl hover:bg-slate-50 transition-colors border border-transparent hover:border-slate-100 group">
                  <div className="w-10 h-10 bg-slate-50 text-slate-400 rounded-xl flex items-center justify-center group-hover:bg-indigo-600 group-hover:text-white transition-all shrink-0">
                    <i className={`fas ${tip.icon} text-sm`}></i>
                  </div>
                  <div>
                    <h4 className="text-xs font-black text-slate-900 mb-0.5">{tip.title}</h4>
                    <p className="text-[10px] text-slate-500 leading-normal font-medium">{tip.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RefinementLab;
