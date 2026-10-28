import React, { useState, useEffect, useRef } from 'react';
import type { 
  InterviewSession, 
  InterviewTurn, 
  TargetRoleData 
} from '../types';
import { apiRequest } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { 
  Mic, 
  MicOff, 
  Play, 
  Award, 
  CheckCircle2, 
  AlertCircle, 
  Volume2, 
  RotateCcw, 
  Send, 
  ChevronRight, 
  FileText,
  BarChart3,
  Bot
} from 'lucide-react';

interface SpeechRecognitionEvent {
  results: ArrayLike<ArrayLike<{ transcript: string }>>;
}

interface IWindow extends Window {
  webkitSpeechRecognition?: any;
  SpeechRecognition?: any;
}

export const InterviewArena: React.FC<{ onNavigateToPlan?: () => void }> = ({ onNavigateToPlan }) => {
  const { user, refreshUser } = useAuth();

  // Mode: 'setup' | 'active' | 'debrief'
  const [viewState, setViewState] = useState<'setup' | 'active' | 'debrief'>('setup');
  
  // Setup options
  const [roles, setRoles] = useState<TargetRoleData[]>([]);
  const [selectedRole, setSelectedRole] = useState<string>('Software Engineer');
  const [selectedLevel, setSelectedLevel] = useState<number>(2);
  const [selectedPersona, setSelectedPersona] = useState<string>('Technical Lead');
  const [selectedRoundType, setSelectedRoundType] = useState<string>('Technical');
  const [selectedMode, setSelectedMode] = useState<'text' | 'voice'>('text');

  // Active Session State
  const [session, setSession] = useState<InterviewSession | null>(null);
  const [currentTurnIndex, setCurrentTurnIndex] = useState<number>(0);
  const [answerText, setAnswerText] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isFinishing, setIsFinishing] = useState<boolean>(false);

  // Audio / Speech Recognition
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [recordingSeconds, setRecordingSeconds] = useState<number>(0);
  const [speechSupported, setSpeechSupported] = useState<boolean>(false);
  const recognitionRef = useRef<any>(null);
  const timerIntervalRef = useRef<any>(null);

  // Filler words list
  const FILLER_WORDS = ['um', 'uh', 'like', 'basically', 'actually', 'you know', 'sort of', 'kind of'];

  // Load roles on mount
  useEffect(() => {
    async function loadRoles() {
      try {
        const fetched = await apiRequest<TargetRoleData[]>('/roles');
        setRoles(fetched);
        if (fetched.length > 0 && user?.target_role) {
          const match = fetched.find(r => r.title.toLowerCase().includes(user.target_role.toLowerCase()));
          if (match) setSelectedRole(match.title);
        }
      } catch (err) {
        console.error('Failed to load roles for interview setup:', err);
      }
    }
    loadRoles();

    // Check SpeechRecognition support
    const win = window as unknown as IWindow;
    if (win.SpeechRecognition || win.webkitSpeechRecognition) {
      setSpeechSupported(true);
    }
  }, [user]);

  // Voice recording timer
  useEffect(() => {
    if (isRecording) {
      timerIntervalRef.current = setInterval(() => {
        setRecordingSeconds(prev => prev + 1);
      }, 1000);
    } else {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
    }
    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
    };
  }, [isRecording]);

  // Start Interview
  const handleStartInterview = async () => {
    try {
      setIsSubmitting(true);
      const newSession = await apiRequest<InterviewSession>('/interviews/start', {
        method: 'POST',
        body: JSON.stringify({
          role_title: selectedRole,
          level: selectedLevel,
          persona: selectedPersona,
          mode: selectedMode,
          round_type: selectedRoundType,
        }),
      });
      setSession(newSession);
      setCurrentTurnIndex(0);
      setAnswerText('');
      setViewState('active');
    } catch (err) {
      console.error('Failed to start interview:', err);
      alert('Unable to initialize simulation. Please ensure the backend is running.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Toggle Speech Recognition
  const handleToggleRecording = () => {
    const win = window as unknown as IWindow;
    const SpeechRec = win.SpeechRecognition || win.webkitSpeechRecognition;

    if (!SpeechRec) {
      alert('Speech recognition is not supported in this browser. Please use Google Chrome or type your answer.');
      return;
    }

    if (isRecording) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsRecording(false);
    } else {
      try {
        const recognition = new SpeechRec();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event: SpeechRecognitionEvent) => {
          let fullTranscript = '';
          for (let i = 0; i < event.results.length; ++i) {
            fullTranscript += event.results[i][0].transcript + ' ';
          }
          setAnswerText(fullTranscript.trim());
        };

        recognition.onerror = (e: any) => {
          console.error('Speech recognition error:', e);
          setIsRecording(false);
        };

        recognition.onend = () => {
          setIsRecording(false);
        };

        recognition.start();
        recognitionRef.current = recognition;
        setIsRecording(true);
      } catch (e) {
        console.error('Failed to start speech recognition:', e);
        setIsRecording(false);
      }
    }
  };

  // Play question with speech synthesis
  const handleSpeakQuestion = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      window.speechSynthesis.speak(utterance);
    }
  };

  // Calculate Speech Stats
  const calculateSpeechMetrics = () => {
    const words = answerText.trim() ? answerText.trim().split(/\s+/) : [];
    const wordCount = words.length;

    // Detect filler words
    let fillerCount = 0;
    const lowerText = answerText.toLowerCase();
    FILLER_WORDS.forEach(fw => {
      const regex = new RegExp(`\\b${fw}\\b`, 'gi');
      const matches = lowerText.match(regex);
      if (matches) fillerCount += matches.length;
    });

    // Speaking WPM
    const minutes = Math.max(recordingSeconds / 60, 0.2);
    const wpm = Math.round(wordCount / minutes);

    return {
      wordCount,
      fillerCount,
      wpm: isNaN(wpm) ? 0 : wpm,
      duration: recordingSeconds,
    };
  };

  // Submit Answer for Current Turn
  const handleSubmitAnswer = async () => {
    if (!session || !currentTurn) return;
    if (!answerText.trim()) {
      alert('Please enter or dictate an answer before submitting for evaluation.');
      return;
    }

    if (isRecording && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
    }

    const { fillerCount, wpm, duration } = calculateSpeechMetrics();

    try {
      setIsSubmitting(true);
      const updatedSession = await apiRequest<InterviewSession>('/interviews/turn/answer', {
        method: 'POST',
        body: JSON.stringify({
          turn_id: currentTurn.id,
          answer_text: answerText,
          audio_duration_sec: duration,
          filler_word_count: fillerCount,
          speaking_wpm: wpm,
        }),
      });

      setSession(updatedSession);
      setRecordingSeconds(0);
      await refreshUser();
    } catch (err) {
      console.error('Failed to submit answer:', err);
      alert('Error submitting answer. Please retry.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Move to next turn
  const handleNextTurn = () => {
    if (!session) return;
    if (currentTurnIndex < session.turns.length - 1) {
      setCurrentTurnIndex(prev => prev + 1);
      setAnswerText('');
      setRecordingSeconds(0);
    }
  };

  // Finish Interview
  const handleCompleteInterview = async () => {
    if (!session) return;
    try {
      setIsFinishing(true);
      const finalized = await apiRequest<InterviewSession>(`/interviews/${session.id}/complete`, {
        method: 'POST',
      });
      setSession(finalized);
      setViewState('debrief');
      await refreshUser();
    } catch (err) {
      console.error('Failed to finalize interview:', err);
      alert('Failed to generate final debrief report.');
    } finally {
      setIsFinishing(false);
    }
  };

  const currentTurn: InterviewTurn | undefined = session?.turns[currentTurnIndex];
  const speechMetrics = calculateSpeechMetrics();

  return (
    <div className="space-y-8 animate-fadeIn max-w-5xl mx-auto">
      {/* View 1: Setup Configuration */}
      {viewState === 'setup' && (
        <div className="space-y-6">
          <div className="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden">
            <div className="absolute right-0 top-0 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />
            <div className="relative z-10">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-semibold mb-3">
                <Mic className="w-3.5 h-3.5" />
                <span>AI Simulation Chamber</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                Mock Interview Simulator
              </h1>
              <p className="mt-1 text-slate-400 text-sm max-w-2xl">
                Practice high-stakes technical, behavioral (STAR), and system design simulations. Receive rigorous grading across relevance, technical depth, and delivery clarity.
              </p>
            </div>
          </div>

          {/* Configuration Form */}
          <div className="glass-panel rounded-2xl p-6 sm:p-8 space-y-6">
            <h2 className="text-lg font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
              <Bot className="w-5 h-5 text-purple-400" />
              Configure Interview Parameters
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Target Role */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">Target Job Role</label>
                <select
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value)}
                  className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm font-semibold text-white focus:outline-none focus:border-purple-500"
                >
                  {roles.map(r => (
                    <option key={r.role_key} value={r.title} className="bg-slate-900 text-white">
                      {r.title}
                    </option>
                  ))}
                </select>
              </div>

              {/* Round Type */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">Interview Round Type</label>
                <select
                  value={selectedRoundType}
                  onChange={(e) => setSelectedRoundType(e.target.value)}
                  className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm font-semibold text-white focus:outline-none focus:border-purple-500"
                >
                  <option value="Technical">Technical Deep Dive</option>
                  <option value="Behavioral">Behavioral (STAR Method)</option>
                  <option value="System Design">System Design & Architecture</option>
                  <option value="HR">Recruiter / HR Screen</option>
                </select>
              </div>

              {/* Interviewer Persona */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">Interviewer Persona</label>
                <div className="grid grid-cols-2 gap-2">
                  {['Technical Lead', 'Strict Architect', 'Friendly Mentor', 'Panel'].map(p => (
                    <button
                      key={p}
                      type="button"
                      onClick={() => setSelectedPersona(p)}
                      className={`px-3 py-2.5 rounded-xl text-xs font-semibold border transition-all ${
                        selectedPersona === p
                          ? 'bg-purple-600/20 border-purple-500 text-purple-300 shadow-sm'
                          : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                      }`}
                    >
                      {p}
                    </button>
                  ))}
                </div>
              </div>

              {/* Seniority / Level */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">Seniority Benchmark</label>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { lvl: 1, label: 'Level 1: Foundation' },
                    { lvl: 2, label: 'Level 2: Mid-Level' },
                    { lvl: 3, label: 'Level 3: Senior/Staff' }
                  ].map(item => (
                    <button
                      key={item.lvl}
                      type="button"
                      onClick={() => setSelectedLevel(item.lvl)}
                      className={`px-3 py-2.5 rounded-xl text-xs font-semibold border transition-all text-center ${
                        selectedLevel === item.lvl
                          ? 'bg-blue-600/20 border-blue-500 text-blue-300 shadow-sm'
                          : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                      }`}
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Input Simulation Mode */}
              <div className="sm:col-span-2 space-y-2">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">Simulation Mode</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div 
                    onClick={() => setSelectedMode('text')}
                    className={`cursor-pointer p-4 rounded-xl border transition-all flex items-start gap-3 ${
                      selectedMode === 'text'
                        ? 'bg-purple-600/15 border-purple-500/50 shadow-inner'
                        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <FileText className={`w-5 h-5 mt-0.5 ${selectedMode === 'text' ? 'text-purple-400' : 'text-slate-500'}`} />
                    <div>
                      <div className="text-sm font-bold text-white">Text Simulation</div>
                      <div className="text-xs text-slate-400 mt-0.5">Focus on structured written synthesis and STAR formulation.</div>
                    </div>
                  </div>

                  <div 
                    onClick={() => setSelectedMode('voice')}
                    className={`cursor-pointer p-4 rounded-xl border transition-all flex items-start gap-3 ${
                      selectedMode === 'voice'
                        ? 'bg-purple-600/15 border-purple-500/50 shadow-inner'
                        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <Mic className={`w-5 h-5 mt-0.5 ${selectedMode === 'voice' ? 'text-purple-400' : 'text-slate-500'}`} />
                    <div>
                      <div className="text-sm font-bold text-white">Voice & Speech Simulation</div>
                      <div className="text-xs text-slate-400 mt-0.5">Dictate live via microphone with cadence, WPM, and filler-word detection.</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Launch Button */}
            <div className="pt-4 flex justify-end">
              <button
                onClick={handleStartInterview}
                disabled={isSubmitting}
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-bold text-sm shadow-lg shadow-purple-600/25 transition-all flex items-center justify-center gap-2"
              >
                {isSubmitting ? (
                  <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-white" />
                    <span>Launch AI Simulation</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* View 2: Active Simulation */}
      {viewState === 'active' && session && currentTurn && (
        <div className="space-y-6">
          {/* Top Status Bar */}
          <div className="glass-panel rounded-2xl p-4 sm:p-5 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <span className="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 font-bold flex items-center justify-center text-xs">
                {currentTurn.turn_index}
              </span>
              <div>
                <span className="text-xs font-semibold text-slate-400">
                  Question {currentTurnIndex + 1} of {session.turns.length}
                </span>
                <div className="text-sm font-bold text-white">
                  {session.role_title} • {session.round_type} Round
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                Persona: {session.persona}
              </span>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                Level {session.level}
              </span>
            </div>
          </div>

          {/* Question Display Card */}
          <div className="glass-panel rounded-2xl p-6 sm:p-8 relative border-purple-500/30">
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-4">
                <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white shrink-0 shadow-md shadow-purple-600/30">
                  <Bot className="w-6 h-6" />
                </div>
                <div>
                  <div className="text-[11px] font-bold text-purple-400 uppercase tracking-wider mb-1">
                    Interviewer Prompt ({currentTurn.question_category})
                  </div>
                  <h3 className="text-lg sm:text-xl font-bold text-white leading-relaxed">
                    "{currentTurn.question_text}"
                  </h3>
                </div>
              </div>

              {/* Text-to-speech replay button */}
              <button
                onClick={() => handleSpeakQuestion(currentTurn.question_text)}
                className="p-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
                title="Hear question read aloud"
              >
                <Volume2 className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Answer Area */}
          <div className="glass-panel rounded-2xl p-6 sm:p-8 space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Candidate Response
              </label>

              {/* Voice toggle button */}
              {speechSupported && (
                <button
                  onClick={handleToggleRecording}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold transition-all ${
                    isRecording
                      ? 'bg-rose-500/20 border border-rose-500 text-rose-400 animate-pulse'
                      : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
                  }`}
                >
                  {isRecording ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5" />}
                  <span>{isRecording ? `Recording (${recordingSeconds}s)...` : 'Dictate with Mic'}</span>
                </button>
              )}
            </div>

            {/* Large Textarea */}
            <div className="relative">
              <textarea
                value={answerText}
                onChange={(e) => setAnswerText(e.target.value)}
                placeholder="Formulate your response using the STAR method: Situation, Task, Action taken, and measurable Result..."
                rows={6}
                disabled={Boolean(currentTurn.feedback)}
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-purple-500 transition-colors leading-relaxed"
              />

              {/* Live Audio Metrics Overlay */}
              <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-400 mt-2 px-1">
                <div className="flex items-center gap-3">
                  <span>Words: <strong className="text-slate-200">{speechMetrics.wordCount}</strong></span>
                  {speechMetrics.duration > 0 && (
                    <>
                      <span>Duration: <strong className="text-slate-200">{speechMetrics.duration}s</strong></span>
                      <span>Cadence: <strong className="text-slate-200">{speechMetrics.wpm} WPM</strong></span>
                    </>
                  )}
                  {speechMetrics.fillerCount > 0 && (
                    <span className="text-amber-400 font-semibold">
                      Fillers detected: {speechMetrics.fillerCount}
                    </span>
                  )}
                </div>

                <span>STAR Framework: Be specific & quantify impact</span>
              </div>
            </div>

            {/* Submit Answer Action */}
            {!currentTurn.feedback && (
              <div className="flex justify-end pt-2">
                <button
                  onClick={handleSubmitAnswer}
                  disabled={isSubmitting || !answerText.trim()}
                  className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 disabled:opacity-50 text-white font-bold text-xs uppercase tracking-wider flex items-center gap-2 shadow-md shadow-purple-600/30 transition-all"
                >
                  {isSubmitting ? (
                    <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                  ) : (
                    <>
                      <Send className="w-3.5 h-3.5" />
                      <span>Evaluate with STAR Rubric</span>
                    </>
                  )}
                </button>
              </div>
            )}
          </div>

          {/* Evaluated Turn Feedback Card */}
          {currentTurn.feedback && (
            <div className="glass-panel rounded-2xl p-6 sm:p-8 space-y-6 border-indigo-500/40 bg-gradient-to-b from-indigo-950/20 to-slate-900/40 animate-fadeIn">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center font-black text-lg">
                    {currentTurn.feedback.score_overall}
                  </div>
                  <div>
                    <div className="text-sm font-bold text-white">AI Turn Evaluation</div>
                    <div className="text-xs text-slate-400">Scored against Senior {session.role_title} benchmark</div>
                  </div>
                </div>

                {/* STAR Metric Chips */}
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">
                    Relevance: <strong>{currentTurn.feedback.score_relevance}/10</strong>
                  </span>
                  <span className="text-xs px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">
                    STAR Structure: <strong>{currentTurn.feedback.score_star_structure}/10</strong>
                  </span>
                  <span className="text-xs px-2.5 py-1 rounded-md bg-slate-800 text-slate-300">
                    Tech Depth: <strong>{currentTurn.feedback.score_technical_accuracy}/10</strong>
                  </span>
                </div>
              </div>

              {/* Constructive Critique */}
              <div className="space-y-1.5">
                <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">Coach Critique:</div>
                <p className="text-xs sm:text-sm text-slate-300 leading-relaxed bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                  {currentTurn.feedback.critique}
                </p>
              </div>

              {/* Sample Ideal Senior Answer */}
              <div className="space-y-1.5">
                <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Award className="w-3.5 h-3.5" />
                  <span>Senior Caliber Exemplar Answer:</span>
                </div>
                <p className="text-xs sm:text-sm text-indigo-200/90 leading-relaxed bg-indigo-950/30 p-4 rounded-xl border border-indigo-500/20 italic">
                  "{currentTurn.feedback.sample_ideal_answer}"
                </p>
              </div>

              {/* Action Buttons for Next Turn or Finish */}
              <div className="flex items-center justify-between pt-2">
                <div className="text-xs text-slate-400">
                  {currentTurnIndex < session.turns.length - 1 ? 'Next question ready.' : 'All turns recorded.'}
                </div>

                <div className="flex items-center gap-3">
                  {currentTurnIndex < session.turns.length - 1 ? (
                    <button
                      onClick={handleNextTurn}
                      className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs uppercase tracking-wider flex items-center gap-1.5 shadow-md shadow-blue-600/30 transition-all"
                    >
                      <span>Next Question</span>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={handleCompleteInterview}
                      disabled={isFinishing}
                      className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs uppercase tracking-wider flex items-center gap-2 shadow-md shadow-emerald-600/30 transition-all"
                    >
                      {isFinishing ? (
                        <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                      ) : (
                        <>
                          <CheckCircle2 className="w-4 h-4" />
                          <span>Generate Debrief Report</span>
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* View 3: Complete Debrief Report */}
      {viewState === 'debrief' && session && (
        <div className="space-y-6 animate-fadeIn">
          {/* Header Trophy Banner */}
          <div className="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden text-center sm:text-left">
            <div className="absolute right-0 top-0 w-80 h-80 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none" />
            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold mb-3">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Session Completed</span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                  Interview Simulation Debrief
                </h1>
                <p className="mt-1 text-slate-400 text-sm max-w-xl">
                  {session.summary_feedback}
                </p>
              </div>

              {/* Overall Score Circle */}
              <div className="flex flex-col items-center sm:items-end">
                <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Final Rating</div>
                <div className="text-4xl font-black text-emerald-400 mt-1">{session.overall_score} / 10</div>
                <div className="text-[11px] text-slate-500 mt-1">Readiness boost applied</div>
              </div>
            </div>
          </div>

          {/* Strengths & Improvement Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {/* Key Strengths */}
            <div className="glass-panel rounded-2xl p-6 space-y-4">
              <h3 className="text-sm font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Demonstrated Strengths
              </h3>
              <ul className="space-y-2">
                {session.strengths.map((str, idx) => (
                  <li key={idx} className="text-xs text-slate-300 flex items-start gap-2 bg-emerald-500/5 p-3 rounded-lg border border-emerald-500/15">
                    <span className="text-emerald-400 font-bold">•</span>
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Areas for Improvement */}
            <div className="glass-panel rounded-2xl p-6 space-y-4">
              <h3 className="text-sm font-bold text-amber-400 uppercase tracking-wider flex items-center gap-2">
                <AlertCircle className="w-4 h-4" />
                High-Yield Focus Areas
              </h3>
              <ul className="space-y-2">
                {session.weaknesses.map((w, idx) => (
                  <li key={idx} className="text-xs text-slate-300 flex items-start gap-2 bg-amber-500/5 p-3 rounded-lg border border-amber-500/15">
                    <span className="text-amber-400 font-bold">•</span>
                    <span>{w}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Suggested Practice Topics */}
          <div className="glass-panel rounded-2xl p-6 space-y-3">
            <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-blue-400" />
              Recommended Modules to Review Before Real Interviews:
            </h3>
            <div className="flex flex-wrap gap-2">
              {session.suggested_topics_to_improve.map((topic, idx) => (
                <span key={idx} className="text-xs px-3 py-1.5 rounded-lg bg-slate-800 text-slate-200 border border-slate-700 font-medium">
                  {topic}
                </span>
              ))}
            </div>
          </div>

          {/* Transcript Review */}
          <div className="glass-panel rounded-2xl p-6 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">
              Turn-by-Turn Transcript & Rubric Review
            </h3>
            <div className="space-y-4">
              {session.turns.map((turn, idx) => (
                <div key={turn.id} className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-purple-400">Question {idx + 1} ({turn.question_category})</span>
                    {turn.feedback && (
                      <span className="font-bold text-emerald-400">Score: {turn.feedback.score_overall}/10</span>
                    )}
                  </div>
                  <div className="text-xs font-semibold text-white">"{turn.question_text}"</div>
                  <div className="text-xs text-slate-300 pl-3 border-l-2 border-slate-700 italic">
                    "{turn.user_answer || '[No response recorded]'}"
                  </div>
                  {turn.feedback && (
                    <div className="text-[11px] text-slate-400 mt-2 pt-2 border-t border-slate-800/80">
                      <strong>Coach Note:</strong> {turn.feedback.critique}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Action Row */}
          <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
            <button
              onClick={() => {
                setViewState('setup');
                setSession(null);
                setCurrentTurnIndex(0);
                setAnswerText('');
              }}
              className="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs uppercase tracking-wider flex items-center gap-2 border border-slate-700 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Start Another Simulation</span>
            </button>

            {onNavigateToPlan && (
              <button
                onClick={onNavigateToPlan}
                className="px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs uppercase tracking-wider flex items-center gap-2 shadow-md shadow-blue-600/30 transition-all"
              >
                <span>Jump to Skill Gap Study Plan</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
