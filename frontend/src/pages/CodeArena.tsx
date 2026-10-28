import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import confetti from 'canvas-confetti';
import { 
  Play, 
  Send, 
  CheckCircle2, 
  XCircle, 
  AlertCircle, 
  Clock, 
  Sparkles, 
  Lightbulb, 
  Search,
  Code2,
  Cpu,
  ChevronDown,
  ChevronUp,
  RefreshCw
} from 'lucide-react';
import { apiRequest } from '../services/api';
import type { CodingProblem, CodeRunResponse } from '../types';
import { useAuth } from '../context/AuthContext';

export const CodeArena: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [problems, setProblems] = useState<CodingProblem[]>([]);
  const [selectedProblem, setSelectedProblem] = useState<CodingProblem | null>(null);
  const [language, setLanguage] = useState<'python' | 'javascript'>('python');
  const [code, setCode] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('All');
  
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [executionResult, setExecutionResult] = useState<CodeRunResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'description' | 'hints' | 'history'>('description');
  const [expandedHints, setExpandedHints] = useState<{ [key: number]: boolean }>({});

  const selectProblem = (problem: CodingProblem, lang: 'python' | 'javascript') => {
    setSelectedProblem(problem);
    setCode(problem.starter_code[lang] || '');
    setExecutionResult(null);
    setExpandedHints({});
  };

  const loadProblems = async () => {
    try {
      const data = await apiRequest<CodingProblem[]>('/coding/problems');
      setProblems(data);
      if (data.length > 0) {
        selectProblem(data[0], 'python');
      }
    } catch (err) {
      console.error('Failed to load coding problems:', err);
    }
  };

  useEffect(() => {
    loadProblems();
  }, []);

  const handleLanguageChange = (newLang: 'python' | 'javascript') => {
    setLanguage(newLang);
    if (selectedProblem) {
      setCode(selectedProblem.starter_code[newLang] || '');
    }
  };

  const resetStarterCode = () => {
    if (selectedProblem) {
      setCode(selectedProblem.starter_code[language] || '');
      setExecutionResult(null);
    }
  };

  const handleRun = async () => {
    if (!selectedProblem) return;
    setIsRunning(true);
    try {
      const res = await apiRequest<CodeRunResponse>('/coding/run', {
        method: 'POST',
        body: JSON.stringify({
          problem_id: selectedProblem.id,
          language,
          code
        })
      });
      setExecutionResult(res);
    } catch (err: any) {
      setExecutionResult({
        status: 'Error',
        passed_cases: 0,
        total_cases: 0,
        runtime_ms: 0,
        test_results: [{
          input_str: '',
          expected_output: '',
          actual_output: '',
          passed: false,
          error: err.message || 'Execution failed'
        }],
        ai_feedback: 'Server execution timed out or threw an error.'
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handleSubmit = async () => {
    if (!selectedProblem) return;
    setIsSubmitting(true);
    try {
      const res = await apiRequest<CodeRunResponse>('/coding/submit', {
        method: 'POST',
        body: JSON.stringify({
          problem_id: selectedProblem.id,
          language,
          code
        })
      });
      setExecutionResult(res);

      if (res.status === 'Passed') {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
        refreshUser();
      }
    } catch (err: any) {
      setExecutionResult({
        status: 'Error',
        passed_cases: 0,
        total_cases: 0,
        runtime_ms: 0,
        test_results: [{
          input_str: '',
          expected_output: '',
          actual_output: '',
          passed: false,
          error: err.message || 'Submission failed'
        }],
        ai_feedback: 'Submission could not be evaluated.'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const filteredProblems = problems.filter((p) => {
    const matchesSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          p.category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDiff = difficultyFilter === 'All' || p.difficulty === difficultyFilter;
    return matchesSearch && matchesDiff;
  });

  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case 'Easy':
        return <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">Easy</span>;
      case 'Medium':
        return <span className="px-2 py-0.5 rounded text-xs font-semibold bg-amber-500/15 text-amber-400 border border-amber-500/30">Medium</span>;
      case 'Hard':
        return <span className="px-2 py-0.5 rounded text-xs font-semibold bg-rose-500/15 text-rose-400 border border-rose-500/30">Hard</span>;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-panel rounded-2xl p-6 relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="absolute right-0 top-0 w-80 h-80 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none" />
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold mb-2">
            <Code2 className="w-3.5 h-3.5" />
            <span>Interactive Code Sandbox</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Code Arena</h1>
          <p className="text-slate-400 text-sm max-w-2xl mt-1">
            Solve algorithmic problems in a secure local execution sandbox. Benchmark runtime, receive automated STAR complexity analysis, and level up your engineering readiness.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Candidate Score</div>
            <div className="text-2xl font-black text-emerald-400">{Math.round(user?.readiness_score || 0)}%</div>
          </div>
        </div>
      </div>

      {/* Main Arena Grid: Left Problem List & Details, Right Monaco Editor & Console */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[750px]">
        {/* Left Column: Problem Browser & Spec (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          {/* Problem Selector Bar */}
          <div className="glass-panel rounded-xl p-4 flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <div className="relative flex-1">
                <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search challenges or tags..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-900/80 border border-slate-700/60 rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors"
                />
              </div>

              <select
                value={difficultyFilter}
                onChange={(e) => setDifficultyFilter(e.target.value)}
                className="bg-slate-900/80 border border-slate-700/60 rounded-lg px-2.5 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-emerald-500"
              >
                <option value="All">All Tiers</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>

            {/* Quick Challenge Pills */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
              {filteredProblems.map((prob) => {
                const isSelected = selectedProblem?.id === prob.id;
                return (
                  <button
                    key={prob.id}
                    onClick={() => selectProblem(prob, language)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                      isSelected
                        ? 'bg-emerald-600/20 text-emerald-300 border border-emerald-500/40 shadow-sm'
                        : 'bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800'
                    }`}
                  >
                    {prob.title}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Problem Detail Card */}
          {selectedProblem && (
            <div className="glass-panel rounded-xl p-5 flex-1 flex flex-col overflow-y-auto max-h-[640px]">
              <div className="flex items-start justify-between gap-3 mb-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    {getDifficultyBadge(selectedProblem.difficulty)}
                    <span className="text-xs text-slate-400 font-medium px-2 py-0.5 rounded bg-slate-800/80 border border-slate-700">
                      {selectedProblem.category}
                    </span>
                  </div>
                  <h2 className="text-xl font-bold text-white">{selectedProblem.title}</h2>
                </div>

                <div className="text-right">
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">Target Complexity</div>
                  <div className="text-xs font-mono text-emerald-400 font-medium">{selectedProblem.optimal_complexity}</div>
                </div>
              </div>

              {/* Sub-tabs */}
              <div className="flex border-b border-slate-800 mb-4 text-xs font-medium">
                <button
                  onClick={() => setActiveTab('description')}
                  className={`pb-2 px-3 border-b-2 transition-colors ${
                    activeTab === 'description'
                      ? 'border-emerald-500 text-emerald-400 font-semibold'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Description
                </button>
                <button
                  onClick={() => setActiveTab('hints')}
                  className={`pb-2 px-3 border-b-2 transition-colors flex items-center gap-1 ${
                    activeTab === 'hints'
                      ? 'border-emerald-500 text-emerald-400 font-semibold'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <Lightbulb className="w-3.5 h-3.5" />
                  Hints ({selectedProblem.hints.length})
                </button>
              </div>

              {activeTab === 'description' ? (
                <div className="space-y-4 text-xs text-slate-300 leading-relaxed">
                  <div className="whitespace-pre-line">{selectedProblem.description}</div>

                  {/* Examples */}
                  <div className="space-y-3 pt-2">
                    <div className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Examples</div>
                    {selectedProblem.examples.map((ex, idx) => (
                      <div key={idx} className="bg-slate-900/90 rounded-lg p-3 border border-slate-800 font-mono text-[11px] space-y-1">
                        <div><span className="text-slate-400">Input:</span> <span className="text-emerald-300">{ex.input}</span></div>
                        <div><span className="text-slate-400">Output:</span> <span className="text-blue-300">{ex.output}</span></div>
                        {ex.explanation && (
                          <div className="text-slate-400 font-sans text-xs pt-1 border-t border-slate-800 mt-1">
                            {ex.explanation}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  {/* Constraints */}
                  {selectedProblem.constraints && selectedProblem.constraints.length > 0 && (
                    <div className="pt-2">
                      <div className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-2">Constraints</div>
                      <ul className="list-disc list-inside space-y-1 text-slate-400 font-mono text-[11px]">
                        {selectedProblem.constraints.map((c, i) => (
                          <li key={i}>{c}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                /* Hints tab */
                <div className="space-y-3">
                  {selectedProblem.hints.map((hint, idx) => {
                    const isExpanded = expandedHints[idx];
                    return (
                      <div key={idx} className="rounded-lg border border-slate-800 bg-slate-900/60 p-3">
                        <button
                          onClick={() => setExpandedHints({ ...expandedHints, [idx]: !isExpanded })}
                          className="w-full flex items-center justify-between text-xs font-semibold text-emerald-400 hover:text-emerald-300 text-left"
                        >
                          <span className="flex items-center gap-1.5">
                            <Sparkles className="w-3.5 h-3.5" />
                            Hint {idx + 1}
                          </span>
                          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                        </button>
                        {isExpanded && (
                          <p className="mt-2 text-xs text-slate-300 leading-relaxed font-sans border-t border-slate-800/80 pt-2">
                            {hint}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Code Editor & Execution Console (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-4">
          {/* Editor Header Bar */}
          <div className="glass-panel rounded-xl px-4 py-2.5 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-xs font-semibold text-slate-300">Language:</span>
              <div className="inline-flex rounded-lg bg-slate-900/80 p-0.5 border border-slate-800">
                <button
                  onClick={() => handleLanguageChange('python')}
                  className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
                    language === 'python'
                      ? 'bg-blue-600 text-white shadow'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Python 3.12
                </button>
                <button
                  onClick={() => handleLanguageChange('javascript')}
                  className={`px-3 py-1 rounded-md text-xs font-semibold transition-all ${
                    language === 'javascript'
                      ? 'bg-amber-600 text-white shadow'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  JavaScript
                </button>
              </div>

              <button
                onClick={resetStarterCode}
                title="Reset to starter template"
                className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800/80 rounded-md transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleRun}
                disabled={isRunning || isSubmitting}
                className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold transition-all disabled:opacity-50"
              >
                <Play className="w-3.5 h-3.5 text-emerald-400 fill-emerald-400" />
                <span>{isRunning ? 'Running...' : 'Run Code'}</span>
              </button>

              <button
                onClick={handleSubmit}
                disabled={isRunning || isSubmitting}
                className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-md shadow-emerald-600/30 transition-all disabled:opacity-50"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{isSubmitting ? 'Evaluating...' : 'Submit'}</span>
              </button>
            </div>
          </div>

          {/* Monaco Editor Container */}
          <div className="glass-panel rounded-xl overflow-hidden border border-slate-800 flex-1 min-h-[420px] relative">
            <Editor
              height="420px"
              language={language === 'python' ? 'python' : 'javascript'}
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 13,
                fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 4,
                padding: { top: 12, bottom: 12 }
              }}
            />
          </div>

          {/* Output & Test Console */}
          <div className="glass-panel rounded-xl p-4 flex flex-col gap-3 min-h-[220px]">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <div className="flex items-center gap-2">
                <Cpu className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-bold text-white uppercase tracking-wider">Execution Console</span>
              </div>

              {executionResult && (
                <div className="flex items-center gap-3">
                  <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                    executionResult.status === 'Passed'
                      ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                      : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
                  }`}>
                    {executionResult.status === 'Passed' ? (
                      <CheckCircle2 className="w-3.5 h-3.5" />
                    ) : (
                      <XCircle className="w-3.5 h-3.5" />
                    )}
                    {executionResult.status} ({executionResult.passed_cases}/{executionResult.total_cases})
                  </span>

                  <span className="inline-flex items-center gap-1 text-[11px] text-slate-400 font-mono">
                    <Clock className="w-3 h-3 text-slate-500" />
                    {executionResult.runtime_ms} ms
                  </span>
                </div>
              )}
            </div>

            {/* Test Results Output */}
            {executionResult ? (
              <div className="space-y-3 overflow-y-auto max-h-[160px]">
                {/* AI Complexity Coach Note */}
                {executionResult.ai_feedback && (
                  <div className="p-2.5 rounded-lg bg-blue-500/10 border border-blue-500/20 text-xs text-blue-300 flex items-start gap-2">
                    <Sparkles className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-semibold text-blue-200">Coach Feedback:</span> {executionResult.ai_feedback}
                      {executionResult.time_complexity && (
                        <span className="ml-2 font-mono text-[11px] text-slate-400">
                          (Time: {executionResult.time_complexity}, Space: {executionResult.space_complexity})
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {/* Test Cases */}
                <div className="space-y-2">
                  {executionResult.test_results.map((tr, index) => (
                    <div
                      key={index}
                      className={`p-2.5 rounded-lg border text-xs font-mono flex flex-col gap-1 ${
                        tr.passed
                          ? 'bg-emerald-500/5 border-emerald-500/20 text-slate-300'
                          : 'bg-rose-500/5 border-rose-500/20 text-slate-300'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-200">Test Case #{index + 1}</span>
                        <span className={`text-[11px] font-bold ${tr.passed ? 'text-emerald-400' : 'text-rose-400'}`}>
                          {tr.passed ? 'PASSED' : 'FAILED'}
                        </span>
                      </div>
                      {tr.input_str && (
                        <div><span className="text-slate-500">Input:</span> {tr.input_str}</div>
                      )}
                      <div><span className="text-slate-500">Expected:</span> <span className="text-emerald-400">{tr.expected_output}</span></div>
                      <div><span className="text-slate-500">Actual:</span> <span className={tr.passed ? 'text-emerald-400' : 'text-rose-400'}>{tr.actual_output}</span></div>
                      {tr.error && (
                        <div className="text-rose-400 font-sans text-xs mt-1 pt-1 border-t border-rose-500/20 flex items-center gap-1.5">
                          <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                          <span>{tr.error}</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-500 py-6 text-xs">
                <Code2 className="w-8 h-8 text-slate-600 mb-2" />
                <p>Run your code or submit to inspect test execution results and time complexity benchmarking.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
