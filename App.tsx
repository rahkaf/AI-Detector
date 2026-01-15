
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import AnalysisDashboard from './components/AnalysisDashboard';
import RefinementLab from './components/RefinementLab';
import History from './components/History';
import Settings from './components/Settings';
import { analyzeSubmission } from './geminiService';
import { AnalysisResult, AppState, HistoryItem } from './types';

const App: React.FC = () => {
  const [state, setState] = useState<AppState>(AppState.IDLE);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [fileName, setFileName] = useState<string>('');
  const [rawText, setRawText] = useState<string>('');
  const [fileBlob, setFileBlob] = useState<Blob | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  // Load history from localStorage on mount
  useEffect(() => {
    const savedHistory = localStorage.getItem('veriscript_history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (e) {
        console.error("Failed to load history", e);
      }
    }
  }, []);

  // Save history to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('veriscript_history', JSON.stringify(history));
  }, [history]);

  const handleUpload = async (text: string, name: string, blob?: Blob) => {
    if (!text.trim()) return;
    setFileName(name);
    setRawText(text);
    setFileBlob(blob);
    setState(AppState.ANALYZING);
    setError(null);
    try {
      const analysis = await analyzeSubmission(text);
      setResult(analysis);
      
      // Save to history
      const newHistoryItem: HistoryItem = {
        id: crypto.randomUUID(),
        fileName: name,
        timestamp: Date.now(),
        result: analysis,
        rawText: text
      };
      setHistory(prev => [newHistoryItem, ...prev]);
      
      setState(AppState.COMPLETED);
    } catch (err) {
      setError("Extensive scan failed. The document might be too complex or the engine hit a high-traffic limit.");
      setState(AppState.ERROR);
    }
  };

  const handleSelectHistoryItem = (item: HistoryItem) => {
    setResult(item.result);
    setRawText(item.rawText);
    setFileName(item.fileName);
    setFileBlob(undefined); // Blobs aren't persisted in localStorage easily
    setState(AppState.COMPLETED);
  };

  const clearHistory = () => {
    if (window.confirm("Are you sure you want to clear all analysis history?")) {
      setHistory([]);
    }
  };

  const reset = () => {
    setState(AppState.IDLE);
    setResult(null);
    setError(null);
    setFileBlob(undefined);
  };

  const loadingSteps = [
    { 
      label: fileBlob ? 'Normalizing PDF Formatting' : 'Sanitizing Text Input', 
      icon: fileBlob ? 'fa-file-pdf' : 'fa-font' 
    },
    { label: 'Scanning External Repositories', icon: 'fa-globe' },
    { label: 'Auditing Grammar & Syntax', icon: 'fa-spell-check' },
    { label: 'Verifying Knowledge Context', icon: 'fa-brain' }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Header currentState={state} onNavigate={setState} />
      <main className="flex-grow container mx-auto px-4 py-8 md:py-16">
        {state === AppState.IDLE && (
          <FileUpload onUpload={handleUpload} isLoading={false} />
        )}

        {state === AppState.ANALYZING && (
          <div className="flex flex-col items-center justify-center py-32 text-center space-y-10">
            <div className="relative">
              <div className="w-32 h-32 border-[6px] border-indigo-50 border-t-indigo-600 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <i className="fas fa-microscope text-3xl text-indigo-600 animate-pulse"></i>
              </div>
            </div>
            <div className="space-y-4">
              <h2 className="text-4xl font-black text-slate-900 tracking-tight">Universal Deep Scan</h2>
              <p className="text-slate-500 max-w-md mx-auto font-medium">
                Scouring Wikipedia, Reddit, academic archives, and web indexes for total integrity verification...
              </p>
            </div>
            <div className="flex flex-col gap-4 w-72 mx-auto text-left">
              {loadingSteps.map((step, i) => (
                <div key={i} className="flex items-center gap-3 text-slate-400 text-sm font-bold uppercase tracking-widest">
                  <i className={`fas ${step.icon} w-6 text-center text-indigo-200`}></i>
                  <span>{step.label}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {state === AppState.ERROR && (
          <div className="max-w-xl mx-auto bg-white p-12 rounded-3xl shadow-2xl text-center border border-red-50">
            <div className="w-20 h-20 bg-red-50 text-red-500 rounded-3xl flex items-center justify-center mx-auto mb-8 transform -rotate-6">
              <i className="fas fa-exclamation-circle text-3xl"></i>
            </div>
            <h2 className="text-3xl font-black text-slate-900 mb-4">Inspection Interrupted</h2>
            <p className="text-slate-500 mb-10 font-medium">{error}</p>
            <button onClick={reset} className="w-full py-5 bg-slate-900 text-white rounded-2xl font-black shadow-xl hover:bg-slate-800 transition-all">
              Try New Submission
            </button>
          </div>
        )}

        {state === AppState.COMPLETED && result && (
          <AnalysisDashboard 
            result={result} 
            onReset={reset} 
            onRefine={() => setState(AppState.REFining)}
            fileName={fileName} 
            rawText={rawText}
            fileBlob={fileBlob}
          />
        )}

        {state === AppState.REFining && (
          <RefinementLab initialText={rawText} onBack={() => setState(AppState.COMPLETED)} />
        )}

        {state === AppState.HISTORY && (
          <History 
            items={history} 
            onSelectItem={handleSelectHistoryItem} 
            onClear={clearHistory}
          />
        )}

        {state === AppState.SETTINGS && (
          <Settings />
        )}
      </main>
    </div>
  );
};

export default App;
