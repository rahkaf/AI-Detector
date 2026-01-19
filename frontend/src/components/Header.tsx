import React from 'react';
import { AppState } from '../types';

interface Props {
  currentState: AppState;
  onNavigate: (state: AppState) => void;
}

const Header: React.FC<Props> = ({ currentState, onNavigate }) => {
  const getLinkClass = (state: AppState) => {
    const isActive = 
      state === AppState.IDLE
        ? [AppState.IDLE, AppState.PROCESSING, AppState.COMPLETED].includes(currentState)
        : currentState === state;
    
    return isActive 
      ? "text-indigo-600 font-bold border-b-2 border-indigo-600 pb-1" 
      : "text-gray-500 hover:text-gray-900 transition-colors pb-1 cursor-pointer";
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => onNavigate(AppState.IDLE)}>
            <div className="bg-gradient-to-br from-indigo-600 to-purple-600 p-2.5 rounded-xl shadow-lg shadow-indigo-200">
              <i className="fas fa-user-secret text-white text-xl"></i>
            </div>
            <div>
              <span className="text-2xl font-black text-gray-900 tracking-tight">HumanizeAI</span>
              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider -mt-1">Stealth Mode</p>
            </div>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <button 
              onClick={() => onNavigate(AppState.IDLE)} 
              className={getLinkClass(AppState.IDLE)}
            >
              <i className="fas fa-wand-magic-sparkles mr-2"></i>
              Humanizer
            </button>
            <button 
              onClick={() => onNavigate(AppState.HISTORY)} 
              className={getLinkClass(AppState.HISTORY)}
            >
              <i className="fas fa-clock-rotate-left mr-2"></i>
              History
            </button>
            <button 
              onClick={() => onNavigate(AppState.SETTINGS)} 
              className={getLinkClass(AppState.SETTINGS)}
            >
              <i className="fas fa-sliders mr-2"></i>
              Settings
            </button>
          </nav>
          
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              <span className="text-xs font-bold text-emerald-700">ACTIVE</span>
            </div>
            <div 
              className="h-9 w-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold border-2 border-white shadow-md cursor-pointer hover:scale-105 transition-transform"
              onClick={() => onNavigate(AppState.SETTINGS)}
            >
              <i className="fas fa-user text-sm"></i>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
