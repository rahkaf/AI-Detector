
import React from 'react';
import { AppState } from '../types';

interface Props {
  currentState: AppState;
  onNavigate: (state: AppState) => void;
}

const Header: React.FC<Props> = ({ currentState, onNavigate }) => {
  const getLinkClass = (state: AppState) => {
    const isActive = currentState === state || 
      (state === AppState.IDLE && (currentState === AppState.ANALYZING || currentState === AppState.COMPLETED || currentState === AppState.REFining));
    
    return isActive 
      ? "text-indigo-600 font-bold border-b-2 border-indigo-600 pb-1" 
      : "text-gray-500 hover:text-gray-900 transition-colors pb-1";
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-2 cursor-pointer" onClick={() => onNavigate(AppState.IDLE)}>
            <div className="bg-indigo-600 p-2 rounded-lg shadow-lg shadow-indigo-100">
              <i className="fas fa-shield-halved text-white text-xl"></i>
            </div>
            <span className="text-2xl font-black text-gray-900 tracking-tight">VeriScript</span>
          </div>
          <nav className="hidden md:flex space-x-8">
            <button 
              onClick={() => onNavigate(AppState.IDLE)} 
              className={getLinkClass(AppState.IDLE)}
            >
              Dashboard
            </button>
            <button 
              onClick={() => onNavigate(AppState.HISTORY)} 
              className={getLinkClass(AppState.HISTORY)}
            >
              History
            </button>
            <button 
              onClick={() => onNavigate(AppState.SETTINGS)} 
              className={getLinkClass(AppState.SETTINGS)}
            >
              Settings
            </button>
          </nav>
          <div className="flex items-center gap-4">
            <button className="text-gray-400 hover:text-indigo-600 transition-colors">
              <i className="fas fa-bell"></i>
            </button>
            <div 
              className="h-9 w-9 rounded-xl bg-gradient-to-br from-indigo-500 to-blue-600 flex items-center justify-center text-white font-bold border-2 border-white shadow-md cursor-pointer hover:scale-105 transition-transform"
              onClick={() => onNavigate(AppState.SETTINGS)}
            >
              JS
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
