
import React, { useCallback, useState } from 'react';
// @ts-ignore
import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://esm.sh/pdfjs-dist@4.10.38/build/pdf.worker.mjs';

interface Props {
  onUpload: (text: string, fileName: string, fileBlob?: Blob) => void;
  isLoading: boolean;
}

const FileUpload: React.FC<Props> = ({ onUpload, isLoading }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [pastedText, setPastedText] = useState('');
  const [error, setError] = useState<string | null>(null);

  const cleanExtractedText = (text: string): string => {
    return text
      .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]/g, '') // Remove non-printable control characters
      .replace(/\r\n/g, '\n')
      .replace(/[ \t]+/g, ' ') // Collapse multiple spaces/tabs
      .replace(/\n\s*\n/g, '\n\n') // Normalize paragraph breaks
      .trim();
  };

  const getWordCount = (text: string): number => {
    return text.trim().split(/\s+/).filter(word => word.length > 0).length;
  };

  const extractTextFromPdf = async (arrayBuffer: ArrayBuffer): Promise<string> => {
    try {
      const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
      const pdf = await loadingTask.promise;
      let fullText = '';
      
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        
        const lines: { [key: number]: string[] } = {};
        textContent.items.forEach((item: any) => {
          const y = Math.round(item.transform[5]);
          if (!lines[y]) lines[y] = [];
          lines[y].push(item.str);
        });

        const sortedY = Object.keys(lines).map(Number).sort((a, b) => b - a);
        const pageText = sortedY.map(y => lines[y].join(' ')).join('\n');
        
        fullText += pageText + '\n';
      }
      return cleanExtractedText(fullText);
    } catch (err) {
      console.error('PDF extraction error:', err);
      throw new Error('Could not read PDF content. Please check if the file is readable.');
    }
  };

  const handleFile = async (file: File) => {
    setError(null);
    if (!file) return;

    try {
      if (file.type === 'application/pdf') {
        const arrayBuffer = await file.arrayBuffer();
        const text = await extractTextFromPdf(arrayBuffer);
        if (!text || text.length < 10) throw new Error("Document is too short for a valid scan.");
        onUpload(text, file.name, file);
      } else if (file.type === 'text/plain' || file.name.endsWith('.txt') || file.name.endsWith('.md')) {
        const text = await file.text();
        onUpload(cleanExtractedText(text), file.name, file);
      } else {
        throw new Error('Please upload a PDF or TXT file.');
      }
    } catch (err: any) {
      setError(err.message || 'Error processing file.');
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  }, []);

  const wordCount = getWordCount(pastedText);

  return (
    <div className="max-w-5xl mx-auto space-y-12 animate-in slide-in-from-bottom-6 duration-700">
      <div className="text-center space-y-4">
        <h1 className="text-5xl font-black text-gray-900 tracking-tight sm:text-6xl">
          Universal <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500">Integrity</span> Scan
        </h1>
        <p className="mt-6 text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed">
          Verify original authorship and refine content with high-precision AI detection and humanization.
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 p-4 rounded-2xl flex items-center gap-3 text-red-600 font-medium animate-pulse">
          <i className="fas fa-exclamation-triangle"></i>
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div 
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
          className={`relative group bg-white border-2 border-dashed rounded-3xl p-16 transition-all flex flex-col items-center justify-center text-center cursor-pointer
            ${isDragging ? 'border-indigo-500 bg-indigo-50 shadow-2xl scale-[1.02]' : 'border-gray-300 hover:border-indigo-400 hover:bg-white hover:shadow-xl'}
            ${isLoading ? 'opacity-50 pointer-events-none' : ''}
          `}
        >
          <input 
            type="file" 
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleFileChange}
            accept=".pdf,.txt,.md"
          />
          <div className={`w-24 h-24 rounded-3xl flex items-center justify-center mb-8 transition-all transform ${isDragging ? 'bg-indigo-600 text-white rotate-12' : 'bg-slate-100 text-slate-500 group-hover:bg-indigo-600 group-hover:text-white'}`}>
            <i className={`fas ${isLoading ? 'fa-spinner fa-spin' : 'fa-file-pdf'} text-4xl`}></i>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Upload Original PDF</h3>
          <p className="text-gray-500 mb-8 max-w-[250px] mx-auto">Cross-checks archives, Reddit, and Wikipedia.</p>
          <button className="px-10 py-4 bg-indigo-600 text-white font-black rounded-2xl shadow-lg hover:bg-indigo-700 transition-all">
            Select File
          </button>
        </div>

        <div className="bg-white border border-gray-100 rounded-3xl p-10 shadow-xl flex flex-col h-full min-h-[450px]">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-gray-900 flex items-center gap-3">
              <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><i className="fas fa-paste"></i></div>
              Paste Content
            </h3>
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{wordCount} Words</span>
          </div>
          <textarea
            placeholder="Paste your content here for deep analysis..."
            className="flex-grow w-full p-6 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-indigo-10 focus:border-indigo-500 outline-none transition-all resize-none bg-slate-50 text-slate-800 font-serif leading-relaxed text-lg"
            value={pastedText}
            onChange={(e) => setPastedText(e.target.value)}
          ></textarea>
          <button 
            disabled={!pastedText.trim() || isLoading}
            onClick={() => onUpload(cleanExtractedText(pastedText), "Manual Entry Submission")}
            className="mt-8 w-full py-5 bg-slate-900 text-white font-black rounded-2xl hover:bg-slate-800 transition-all shadow-xl active:scale-[0.98] disabled:bg-slate-200 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Scanning Universally...' : 'Run Analysis'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
