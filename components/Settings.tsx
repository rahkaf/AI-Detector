
import React from 'react';

const Settings: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-4xl font-black text-slate-900 tracking-tight">Platform <span className="text-indigo-600">Settings</span></h2>
        <p className="text-slate-500 font-medium mt-1">Manage your detection preferences and account details.</p>
      </div>

      <div className="grid gap-8">
        <section className="bg-white border border-slate-100 rounded-[2rem] p-10 shadow-sm space-y-8">
          <div>
            <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-3">
              <i className="fas fa-robot text-indigo-500"></i> AI Detection Sensitivity
            </h3>
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-bold text-slate-800">Strict Enforcement Mode</p>
                  <p className="text-sm text-slate-500">Flags content with even minor AI markers. Recommended for final theses.</p>
                </div>
                <div className="w-14 h-8 bg-indigo-600 rounded-full relative p-1 cursor-pointer">
                  <div className="w-6 h-6 bg-white rounded-full shadow-md ml-auto"></div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-bold text-slate-800">Ensemble Verification</p>
                  <p className="text-sm text-slate-500">Use all available detection models for maximum accuracy.</p>
                </div>
                <div className="w-14 h-8 bg-indigo-600 rounded-full relative p-1 cursor-pointer">
                  <div className="w-6 h-6 bg-white rounded-full shadow-md ml-auto"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-8 border-t border-slate-50">
            <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-3">
              <i className="fas fa-search-location text-indigo-500"></i> Plagiarism Sources
            </h3>
            <div className="grid grid-cols-2 gap-4">
              {['Academic Journals', 'Web Archives', 'Reddit & Forums', 'Code Repositories', 'News Portals', 'Legal Documents'].map((source) => (
                <div key={source} className="flex items-center gap-3 p-4 bg-slate-50 rounded-2xl border border-transparent hover:border-indigo-100 transition-colors cursor-pointer">
                  <div className="w-5 h-5 border-2 border-indigo-200 rounded-md bg-white flex items-center justify-center">
                    <i className="fas fa-check text-[10px] text-indigo-600"></i>
                  </div>
                  <span className="text-sm font-bold text-slate-700">{source}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="bg-slate-900 rounded-[2rem] p-10 shadow-2xl text-white">
          <h3 className="text-xl font-bold mb-6">API & Integration</h3>
          <div className="p-6 bg-slate-800 rounded-2xl border border-slate-700 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center">
                <i className="fas fa-key"></i>
              </div>
              <div>
                <p className="font-bold">Gemini 3 Pro Integration</p>
                <p className="text-xs text-slate-400 uppercase font-bold tracking-widest">Active & Authenticated</p>
              </div>
            </div>
            <button className="text-xs font-black bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg transition-colors">MANAGE KEY</button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Settings;
