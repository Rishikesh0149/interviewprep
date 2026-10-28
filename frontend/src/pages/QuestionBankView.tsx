import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  Search, 
  ChevronDown, 
  ChevronUp, 
  Sparkles, 
  Tag, 
  CheckCircle2, 
  Mic
} from 'lucide-react';
import { apiRequest } from '../services/api';
import type { QuestionItem, QuestionListResponse } from '../types';

interface QuestionBankProps {
  onPracticeQuestion?: (questionText: string, category: string) => void;
}

export const QuestionBankView: React.FC<QuestionBankProps> = ({ onPracticeQuestion }) => {
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('All');
  const [selectedLevel, setSelectedLevel] = useState<string>('All');

  // Expanded cards
  const [expandedCards, setExpandedCards] = useState<{ [key: number]: boolean }>({});

  const fetchQuestions = React.useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (selectedCategory !== 'All') params.append('category', selectedCategory);
      if (selectedDifficulty !== 'All') params.append('difficulty', selectedDifficulty);
      if (selectedLevel !== 'All') params.append('level', selectedLevel);
      if (search.trim()) params.append('search', search.trim());
      params.append('limit', '50');

      const data = await apiRequest<QuestionListResponse>(`/questions?${params.toString()}`);
      setQuestions(data.questions);
    } catch (err) {
      console.error('Failed to load questions:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, selectedDifficulty, selectedLevel, search]);

  useEffect(() => {
    fetchQuestions();
  }, [fetchQuestions]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchQuestions();
  };

  const toggleCard = (id: number) => {
    setExpandedCards((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case 'Easy':
        return <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">Easy</span>;
      case 'Medium':
        return <span className="px-2 py-0.5 rounded text-xs font-semibold bg-amber-500/15 text-amber-400 border border-amber-500/30">Medium</span>;
      case 'Hard':
        return <span className="px-2 py-0.5 rounded text-xs font-semibold bg-rose-500/15 text-rose-400 border border-rose-500/30">Hard</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-xs font-semibold bg-slate-800 text-slate-300">{diff}</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="absolute right-0 top-0 w-80 h-80 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold mb-3">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Curated Interview Repository</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Interview Question Bank</h1>
          <p className="text-slate-400 text-sm max-w-2xl mt-1">
            Browse hundreds of real interview prompts curated across Technical, Behavioral, System Design, and Coding rounds. Each question includes an ideal STAR answer breakdown and rubric hints.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Indexed Questions</div>
            <div className="text-3xl font-black text-blue-400">{questions.length}</div>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="glass-panel rounded-xl p-4 flex flex-col gap-4">
        {/* Search Input */}
        <form onSubmit={handleSearchSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
            <input
              type="text"
              placeholder="Search by keywords, algorithms, distributed concepts, or behavioral themes..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-slate-900/80 border border-slate-700/60 rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold transition-all shadow-md shadow-blue-600/20"
          >
            Search
          </button>
        </form>

        {/* Category Pills & Dropdowns */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800/80">
          {/* Categories */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
            {['All', 'Technical', 'Behavioral', 'System Design', 'HR', 'Coding'].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'bg-slate-900/80 text-slate-400 hover:text-slate-200 border border-slate-800'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Difficulty & Level Selectors */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5">
              <span className="text-xs text-slate-400">Difficulty:</span>
              <select
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
                className="bg-slate-900/80 border border-slate-700/60 rounded-lg px-2.5 py-1 text-xs text-slate-300 focus:outline-none focus:border-blue-500"
              >
                <option value="All">All</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5">
              <span className="text-xs text-slate-400">Level:</span>
              <select
                value={selectedLevel}
                onChange={(e) => setSelectedLevel(e.target.value)}
                className="bg-slate-900/80 border border-slate-700/60 rounded-lg px-2.5 py-1 text-xs text-slate-300 focus:outline-none focus:border-blue-500"
              >
                <option value="All">All Levels</option>
                <option value="1">L1: Junior</option>
                <option value="2">L2: Intermediate</option>
                <option value="3">L3: Senior+</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Questions List */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 gap-3">
          <div className="w-8 h-8 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin" />
          <span className="text-sm text-slate-400 font-medium">Filtering Question Repository...</span>
        </div>
      ) : questions.length === 0 ? (
        <div className="glass-panel rounded-xl p-12 text-center text-slate-400">
          <BookOpen className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-semibold text-white mb-1">No matching questions found</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Try adjusting your search keywords, difficulty tier, or selecting 'All' categories to view available questions.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {questions.map((q) => {
            const isExpanded = expandedCards[q.id];
            return (
              <div
                key={q.id}
                className="glass-panel glass-panel-hover rounded-xl p-5 border border-slate-800 transition-all"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-2 mb-2">
                      {getDifficultyBadge(q.difficulty)}
                      <span className="px-2 py-0.5 rounded text-xs font-semibold bg-indigo-500/15 text-indigo-400 border border-indigo-500/30">
                        {q.category}
                      </span>
                      <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-slate-400 border border-slate-700">
                        Level {q.level}
                      </span>
                      {q.role_title && q.role_title !== 'General' && (
                        <span className="px-2 py-0.5 rounded text-xs font-medium bg-blue-500/10 text-blue-300 border border-blue-500/20">
                          {q.role_title}
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-white leading-snug">
                      {q.question_text}
                    </h3>
                  </div>

                  <div className="flex items-center gap-2">
                    {onPracticeQuestion && (
                      <button
                        onClick={() => onPracticeQuestion(q.question_text, q.category)}
                        className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-purple-300 text-xs font-semibold transition-colors"
                        title="Simulate this in Mock Interview"
                      >
                        <Mic className="w-3.5 h-3.5" />
                        <span>Simulate</span>
                      </button>
                    )}

                    <button
                      onClick={() => toggleCard(q.id)}
                      className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 transition-colors"
                      title={isExpanded ? 'Collapse answer' : 'View ideal STAR answer'}
                    >
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Keywords Bar */}
                {q.expected_keywords && q.expected_keywords.length > 0 && (
                  <div className="flex flex-wrap items-center gap-1.5 mt-3 pt-3 border-t border-slate-800/60">
                    <span className="text-[11px] text-slate-500 flex items-center gap-1 mr-1">
                      <Tag className="w-3 h-3" /> Core Keywords:
                    </span>
                    {q.expected_keywords.map((kw, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 rounded text-[11px] bg-slate-900 text-slate-300 border border-slate-800 font-mono"
                      >
                        {kw}
                      </span>
                    ))}
                  </div>
                )}

                {/* Expanded Answer & Rubric */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-slate-800 space-y-4 animate-in fade-in duration-200">
                    {/* Ideal Answer */}
                    {q.ideal_star_answer && (
                      <div className="bg-slate-900/90 rounded-lg p-4 border border-blue-500/20 space-y-2">
                        <div className="flex items-center gap-2 text-xs font-bold text-blue-400 uppercase tracking-wider">
                          <Sparkles className="w-3.5 h-3.5" />
                          <span>Ideal STAR Exemplar Answer</span>
                        </div>
                        <p className="text-xs text-slate-300 leading-relaxed font-sans">
                          {q.ideal_star_answer}
                        </p>
                      </div>
                    )}

                    {/* Rubric Hints */}
                    {q.rubric_hints && q.rubric_hints.length > 0 && (
                      <div className="bg-slate-900/50 rounded-lg p-4 border border-slate-800 space-y-2">
                        <div className="flex items-center gap-2 text-xs font-bold text-slate-300 uppercase tracking-wider">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                          <span>Interviewer Evaluation Rubric</span>
                        </div>
                        <ul className="space-y-1.5">
                          {q.rubric_hints.map((hint, idx) => (
                            <li key={idx} className="flex items-start gap-2 text-xs text-slate-400">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0" />
                              <span>{hint}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
