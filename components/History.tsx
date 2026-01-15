
import React from 'react';
import { HistoryItem } from '../types';

interface Props {
  items: HistoryItem[];
  onSelectItem: (item: HistoryItem) => void;
  onClear: () => void;
}

const History: React.FC<Props> = ({ items, onSelectItem, onClear }) => {
  const formatDate = (timestamp: number) => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date(timestamp));
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Audit <span className="text-indigo-600">History</span></h2>
          <p className="text-slate-500 font-medium mt-1">Review your previously analyzed documents and reports.</p>
        </div>
        {items.length > 0 && (
          <button 
            onClick={onClear}
            className="text-xs font-black text-red-500 hover:text-red-700 uppercase tracking-widest transition-colors flex items-center gap-2"
          >
            <i className="fas fa-trash-can"></i> Clear All History
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <div className="bg-white border border-slate-100 rounded-[2rem] p-20 text-center shadow-sm">
          <div className="w-24 h-24 bg-slate-50 text-slate-300 rounded-3xl flex items-center justify-center mx-auto mb-6">
            <i className="fas fa-clock-rotate-left text-4xl"></i>
          </div>
          <h3 className="text-xl font-bold text-slate-900 mb-2">No History Found</h3>
          <p className="text-slate-500 max-w-xs mx-auto mb-8">You haven't performed any integrity scans yet. New analyses will appear here.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {items.sort((a, b) => b.timestamp - a.timestamp).map((item) => (
            <div 
              key={item.id}
              onClick={() => onSelectItem(item)}
              className="bg-white border border-slate-100 p-6 rounded-3xl hover:border-indigo-300 hover:shadow-xl transition-all cursor-pointer group flex items-center justify-between"
            >
              <div className="flex items-center gap-6">
                <div className="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center group-hover:bg-indigo-600 group-hover:text-white transition-all shadow-inner">
                  <i className="fas fa-file-lines text-xl"></i>
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-lg group-hover:text-indigo-600 transition-colors">{item.fileName}</h4>
                  <p className="text-sm text-slate-400 font-medium flex items-center gap-2">
                    <i className="far fa-calendar"></i> {formatDate(item.timestamp)}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-12 text-right">
                <div className="hidden sm:block">
                  <div className="text-[10px] font-black text-slate-300 uppercase tracking-widest mb-1">AI Prob.</div>
                  <div className={`font-black ${item.result.aiLikelihood > 70 ? 'text-red-500' : 'text-slate-900'}`}>
                    {item.result.aiLikelihood}%
                  </div>
                </div>
                <div className="hidden sm:block">
                  <div className="text-[10px] font-black text-slate-300 uppercase tracking-widest mb-1">Similarity</div>
                  <div className="font-black text-slate-900">{item.result.similarityScore}%</div>
                </div>
                <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-all">
                  <i className="fas fa-chevron-right"></i>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
