"use client";

import { useEffect, useState } from 'react';
import { useInterviewSocket } from '@/hooks/useInterviewSocket'; 
import { Send, Mic, FileText } from 'lucide-react';

export default function Home() {
  // NOTE: We assume the backend is running on localhost:8000
  // If you are accessing this remotely (not on the same machine), 
  // you must replace 'localhost' with your server's IP address.
  const { messages, isConnected, sendMessage, uploadResume, connect } = useInterviewSocket(
    "ws://localhost:8000/api/v1/ws/interview/web_user_1"
  );
  
  const [input, setInput] = useState("");
  const [hasStarted, setHasStarted] = useState(false);

  useEffect(() => {
    connect();
  }, [connect]);

  const handleStart = () => {
    uploadResume("sample_resume.pdf");
    setHasStarted(true);
  };

  return (
    <main className="flex min-h-screen flex-col bg-slate-950 text-slate-100 font-sans">
      {/* Header */}
      <header className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900 sticky top-0 z-10">
        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          AI Interviewer <span className="text-xs text-slate-500 border border-slate-700 px-2 py-0.5 rounded ml-2">BETA</span>
        </h1>
        <div className="flex items-center gap-2">
           <span className="text-xs text-slate-400">{isConnected ? 'Online' : 'Offline'}</span>
           <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-4xl mx-auto w-full scroll-smooth">
        {!hasStarted ? (
          <div className="flex flex-col items-center justify-center h-[60vh] space-y-4">
            <div className="p-8 bg-slate-900/50 rounded-2xl border border-slate-800 text-center max-w-md shadow-2xl backdrop-blur-sm">
              <div className="w-16 h-16 bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileText className="w-8 h-8 text-blue-400" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Ready for your interview?</h2>
              <p className="text-slate-400 mb-8 leading-relaxed">
                The AI has analyzed your resume. Expect questions on 
                <span className="text-blue-300"> Python, System Design, and Algorithms.</span>
              </p>
              <button 
                onClick={handleStart}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-500 active:scale-95 text-white rounded-xl font-semibold transition-all shadow-lg shadow-blue-900/20"
              >
                Start Session
              </button>
            </div>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div 
              key={i} 
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}
            >
              <div 
                className={`max-w-[85%] p-4 sm:p-5 rounded-2xl shadow-md leading-relaxed ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white rounded-tr-none' 
                    : 'bg-slate-800 text-slate-200 rounded-tl-none border border-slate-700'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Input Area */}
      {hasStarted && (
        <div className="p-4 bg-slate-900 border-t border-slate-800 sticky bottom-0">
          <div className="max-w-4xl mx-auto flex gap-3">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (sendMessage(input), setInput(""))}
              placeholder="Type your answer..."
              className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-slate-100 placeholder-slate-500"
            />
            <button 
              onClick={() => { sendMessage(input); setInput(""); }}
              className="p-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white transition-all shadow-lg active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={!input.trim()}
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </main>
  );
}