import React, { useState } from 'react';
import { Send, GitCommit, Info, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react';

const CommitClassifierApp = () => {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const API_URL = 'http://localhost:8000';

  const commitTypeColors = {
    feat: 'bg-blue-100 text-blue-800 border-blue-300',
    fix: 'bg-red-100 text-red-800 border-red-300',
    docs: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    style: 'bg-purple-100 text-purple-800 border-purple-300',
    refactor: 'bg-green-100 text-green-800 border-green-300',
    perf: 'bg-orange-100 text-orange-800 border-orange-300',
    test: 'bg-pink-100 text-pink-800 border-pink-300',
    build: 'bg-indigo-100 text-indigo-800 border-indigo-300',
    ci: 'bg-teal-100 text-teal-800 border-teal-300',
    chore: 'bg-gray-100 text-gray-800 border-gray-300',
    revert: 'bg-rose-100 text-rose-800 border-rose-300',
  };

  const classifyMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/classify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message.trim() })
      });

      const data = await response.json();
      setResult(data);
      setHistory([data, ...history.slice(0, 4)]);
    } catch (error) {
      alert('Error: Make sure the backend is running on http://localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  const exampleMessages = [
    'feat: add user authentication',
    'fix: resolve login bug',
    'docs: update API documentation',
    'added new feature for dashboard',
    'fixed the payment gateway issue',
    'refactor: optimize database queries'
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6 border border-slate-200">
          <div className="flex items-center gap-4 mb-4">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-xl">
              <GitCommit className="text-white" size={32} />
            </div>
            <div>
              <h1 className="text-4xl font-bold text-slate-800">Commit Message Classifier</h1>
              <p className="text-slate-600 mt-1">Analyze and improve your git commit messages with AI</p>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Input */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-slate-200">
              <h2 className="text-xl font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <Send size={20} />
                Classify Commit Message
              </h2>

              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Enter your commit message here..."
                className="w-full h-32 p-4 border-2 border-slate-300 rounded-xl focus:border-blue-500 focus:outline-none transition-colors resize-none text-slate-700"
              />

              <button
                onClick={classifyMessage}
                disabled={loading || !message.trim()}
                className="mt-4 w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-xl font-semibold hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
              >
                {loading ? 'Analyzing...' : 'Classify Message'}
                <Send size={18} />
              </button>

              {/* Example Messages */}
              <div className="mt-6">
                <p className="text-sm text-slate-600 mb-3 font-medium">Try these examples:</p>
                <div className="flex flex-wrap gap-2">
                  {exampleMessages.map((ex, idx) => (
                    <button
                      key={idx}
                      onClick={() => setMessage(ex)}
                      className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-2 rounded-lg transition-colors border border-slate-300"
                    >
                      {ex}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Results */}
            {result && (
              <div className="bg-white rounded-2xl shadow-lg p-6 border border-slate-200">
                <h3 className="text-xl font-semibold text-slate-800 mb-4 flex items-center gap-2">
                  <CheckCircle size={20} className="text-green-500" />
                  Classification Results
                </h3>

                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-slate-600 font-medium w-24">Type:</span>
                    <span className={`px-4 py-2 rounded-lg font-semibold border-2 ${commitTypeColors[result.type]}`}>
                      {result.type}
                    </span>
                  </div>

                  {result.scope && (
                    <div className="flex items-center gap-3">
                      <span className="text-sm text-slate-600 font-medium w-24">Scope:</span>
                      <span className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg font-medium border border-slate-300">
                        {result.scope}
                      </span>
                    </div>
                  )}

                  <div className="flex items-start gap-3">
                    <span className="text-sm text-slate-600 font-medium w-24 pt-2">Description:</span>
                    <p className="flex-1 p-3 bg-slate-50 rounded-lg text-slate-700 border border-slate-200">
                      {result.description}
                    </p>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className="text-sm text-slate-600 font-medium w-24">Confidence:</span>
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <div className="flex-1 bg-slate-200 rounded-full h-3 overflow-hidden">
                          <div
                            className="bg-gradient-to-r from-green-400 to-green-600 h-full rounded-full transition-all duration-500"
                            style={{ width: `${result.confidence * 100}%` }}
                          />
                        </div>
                        <span className="font-semibold text-slate-700">{(result.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  </div>

                  {/* Suggestions */}
                  {result.suggestions.length > 0 && (
                    <div className="mt-6 p-4 bg-amber-50 rounded-xl border-2 border-amber-200">
                      <h4 className="font-semibold text-amber-900 mb-3 flex items-center gap-2">
                        <AlertCircle size={18} />
                        Suggestions for Improvement
                      </h4>
                      <ul className="space-y-2">
                        {result.suggestions.map((suggestion, idx) => (
                          <li key={idx} className="text-sm text-amber-800 flex items-start gap-2">
                            <span className="text-amber-600 mt-1">•</span>
                            <span>{suggestion}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Info & History */}
          <div className="space-y-6">
            {/* Commit Types Info */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-slate-200">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <Info size={18} />
                Commit Types
              </h3>
              <div className="space-y-2">
                {Object.entries(commitTypeColors).map(([type, color]) => (
                  <div key={type} className={`px-3 py-2 rounded-lg border-2 ${color} text-sm font-medium`}>
                    {type}
                  </div>
                ))}
              </div>
            </div>

            {/* History */}
            {history.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-6 border border-slate-200">
                <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                  <TrendingUp size={18} />
                  Recent History
                </h3>
                <div className="space-y-3">
                  {history.map((item, idx) => (
                    <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                      <div className={`inline-block px-2 py-1 rounded text-xs font-semibold mb-2 ${commitTypeColors[item.type]}`}>
                        {item.type}
                      </div>
                      <p className="text-sm text-slate-700 truncate">{item.message}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CommitClassifierApp;