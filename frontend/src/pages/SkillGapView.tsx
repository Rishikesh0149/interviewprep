import React, { useState, useEffect } from 'react';
import type { 
  TargetRoleData, 
  SkillGapReportData, 
  StudyPlan, 
  StudyTask 
} from '../types';
import { apiRequest } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { 
  Compass, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  Sparkles, 
  ExternalLink, 
  Calendar, 
  RefreshCw,
  BookOpen,
  Check
} from 'lucide-react';

export const SkillGapView: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [roles, setRoles] = useState<TargetRoleData[]>([]);
  const [selectedRoleKey, setSelectedRoleKey] = useState<string>('');
  const [gapReport, setGapReport] = useState<SkillGapReportData | null>(null);
  const [studyPlan, setStudyPlan] = useState<StudyPlan | null>(null);
  const [activeWeek, setActiveWeek] = useState<number>(1);
  const [loadingRoles, setLoadingRoles] = useState<boolean>(true);
  const [loadingGap, setLoadingGap] = useState<boolean>(false);
  const [loadingPlan, setLoadingPlan] = useState<boolean>(false);
  const [togglingTaskId, setTogglingTaskId] = useState<number | null>(null);

  // 1. Fetch available target roles
  useEffect(() => {
    async function loadRoles() {
      try {
        setLoadingRoles(true);
        const fetchedRoles = await apiRequest<TargetRoleData[]>('/roles');
        setRoles(fetchedRoles);
        if (fetchedRoles.length > 0) {
          const defaultRole = fetchedRoles.find(r => 
            user?.target_role && r.title.toLowerCase().includes(user.target_role.toLowerCase())
          ) || fetchedRoles[0];
          setSelectedRoleKey(defaultRole.role_key);
        }
      } catch (err) {
        console.error('Failed to load roles:', err);
      } finally {
        setLoadingRoles(false);
      }
    }
    loadRoles();
  }, [user]);

  // 2. Fetch skill gap report when selected role changes
  useEffect(() => {
    if (!selectedRoleKey) return;
    async function loadGapReport() {
      try {
        setLoadingGap(true);
        const report = await apiRequest<SkillGapReportData>(`/gap-report?role_key=${selectedRoleKey}`);
        setGapReport(report);
      } catch (err) {
        console.error('Failed to load gap report:', err);
      } finally {
        setLoadingGap(false);
      }
    }
    loadGapReport();
  }, [selectedRoleKey]);

  // 3. Fetch active study plan
  useEffect(() => {
    async function loadPlan() {
      try {
        setLoadingPlan(true);
        const plan = await apiRequest<StudyPlan>('/plans/current');
        setStudyPlan(plan);
      } catch (err) {
        console.error('Failed to load current study plan:', err);
      } finally {
        setLoadingPlan(false);
      }
    }
    loadPlan();
  }, []);

  // Handle task toggle
  const handleToggleTask = async (taskId: number) => {
    try {
      setTogglingTaskId(taskId);
      const updatedPlan = await apiRequest<StudyPlan>(`/plans/tasks/${taskId}/toggle`, {
        method: 'PATCH',
      });
      setStudyPlan(updatedPlan);
      await refreshUser();
    } catch (err) {
      console.error('Failed to toggle task:', err);
    } finally {
      setTogglingTaskId(null);
    }
  };

  // Handle plan regeneration
  const handleRegeneratePlan = async () => {
    if (!gapReport) return;
    try {
      setLoadingPlan(true);
      const newPlan = await apiRequest<StudyPlan>('/plans/generate', {
        method: 'POST',
        body: JSON.stringify({
          role_title: gapReport.role_title,
          hours_per_day: 2.0,
          total_weeks: 4
        })
      });
      setStudyPlan(newPlan);
      setActiveWeek(1);
      await refreshUser();
    } catch (err) {
      console.error('Failed to generate study plan:', err);
    } finally {
      setLoadingPlan(false);
    }
  };

  const getTierBadge = (tier: string) => {
    switch (tier) {
      case 'BASIC':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'INTERMEDIATE':
        return 'bg-purple-500/10 text-purple-400 border-purple-500/30';
      case 'ADVANCED':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      default:
        return 'bg-slate-700/20 text-slate-300 border-slate-700';
    }
  };

  const currentWeekTasks = studyPlan?.tasks.filter(t => t.week_number === activeWeek) || [];
  const completedCurrentWeek = currentWeekTasks.filter(t => t.is_completed).length;

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header Banner */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden">
        <div className="absolute right-0 top-0 w-80 h-80 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold mb-3">
              <Compass className="w-3.5 h-3.5" />
              <span>Diagnostic & Roadmap Engine</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Skill Gap & Personalized Study Plan
            </h1>
            <p className="mt-1 text-slate-400 text-sm max-w-2xl">
              Benchmark your verified skills against industry role rubrics. Bridge key gaps with an adaptive, tiered 4-week structured preparation syllabus.
            </p>
          </div>

          {/* Role Picker */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Role:</span>
            <select
              value={selectedRoleKey}
              onChange={(e) => setSelectedRoleKey(e.target.value)}
              disabled={loadingRoles}
              className="bg-slate-900/90 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm font-semibold text-white focus:outline-none focus:border-blue-500 shadow-inner"
            >
              {roles.map(r => (
                <option key={r.role_key} value={r.role_key} className="bg-slate-900 text-white">
                  {r.title}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Skill Gap Analysis Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Match Percentage Card */}
        <div className="glass-panel rounded-2xl p-6 flex flex-col items-center justify-center text-center relative overflow-hidden">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Role Alignment Score</div>
          
          <div className="relative w-36 h-36 flex items-center justify-center my-3">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="42"
                stroke="currentColor"
                strokeWidth="8"
                className="text-slate-800"
                fill="transparent"
              />
              <circle
                cx="50"
                cy="50"
                r="42"
                stroke="currentColor"
                strokeWidth="8"
                className={`${(gapReport?.match_percentage || 0) >= 75 ? 'text-emerald-500' : (gapReport?.match_percentage || 0) >= 50 ? 'text-amber-500' : 'text-blue-500'} transition-all duration-1000 ease-out`}
                strokeDasharray="264"
                strokeDashoffset={264 - (264 * (gapReport?.match_percentage || 0)) / 100}
                strokeLinecap="round"
                fill="transparent"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-black text-white">{Math.round(gapReport?.match_percentage || 0)}%</span>
              <span className="text-[11px] font-semibold text-slate-400 uppercase">Match</span>
            </div>
          </div>

          <div className="text-xs text-slate-400 mt-1 max-w-[220px]">
            Benchmark against <span className="text-slate-200 font-semibold">{gapReport?.role_title || 'Target Role'}</span> rubric
          </div>
        </div>

        {/* Skill Breakdown Clusters */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-6 space-y-5">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              Competency Categorization
            </h3>
            {loadingGap && <span className="text-xs text-slate-400 animate-pulse">Analyzing profile...</span>}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* Strong Skills */}
            <div className="bg-slate-900/50 border border-emerald-500/20 rounded-xl p-4">
              <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2.5">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Strong ({gapReport?.strong_skills.length || 0})</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {gapReport?.strong_skills && gapReport.strong_skills.length > 0 ? (
                  gapReport.strong_skills.map((s, idx) => (
                    <span key={idx} className="text-xs px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 font-medium">
                      {s}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500 italic">None detected</span>
                )}
              </div>
            </div>

            {/* Partial Skills */}
            <div className="bg-slate-900/50 border border-amber-500/20 rounded-xl p-4">
              <div className="flex items-center gap-1.5 text-xs font-bold text-amber-400 uppercase tracking-wider mb-2.5">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Partial ({gapReport?.partial_skills.length || 0})</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {gapReport?.partial_skills && gapReport.partial_skills.length > 0 ? (
                  gapReport.partial_skills.map((s, idx) => (
                    <span key={idx} className="text-xs px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/20 text-amber-300 font-medium">
                      {s}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500 italic">None detected</span>
                )}
              </div>
            </div>

            {/* Missing Skills */}
            <div className="bg-slate-900/50 border border-rose-500/20 rounded-xl p-4">
              <div className="flex items-center gap-1.5 text-xs font-bold text-rose-400 uppercase tracking-wider mb-2.5">
                <XCircle className="w-3.5 h-3.5" />
                <span>Missing ({gapReport?.missing_skills.length || 0})</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {gapReport?.missing_skills && gapReport.missing_skills.length > 0 ? (
                  gapReport.missing_skills.map((s, idx) => (
                    <span key={idx} className="text-xs px-2.5 py-1 rounded-md bg-rose-500/10 border border-rose-500/20 text-rose-300 font-medium">
                      {s}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-slate-500 italic">None detected</span>
                )}
              </div>
            </div>
          </div>

          {/* Strategic Recommendations */}
          <div className="mt-4 pt-4 border-t border-slate-800">
            <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Priority Recommendations:</div>
            <ul className="space-y-1.5">
              {gapReport?.recommendations.map((rec, idx) => (
                <li key={idx} className="text-xs text-slate-400 flex items-start gap-2">
                  <span className="text-blue-400 font-bold">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* 4-Week Structured Study Roadmap */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold mb-1">
              <Calendar className="w-3 h-3" />
              <span>4-Week Guided Syllabus</span>
            </div>
            <h2 className="text-xl font-bold text-white">Personalized Preparation Roadmap</h2>
          </div>

          <div className="flex items-center gap-4">
            {/* Progress indicator */}
            <div className="text-right">
              <div className="text-xs font-semibold text-slate-400">Total Completion</div>
              <div className="text-lg font-black text-blue-400">{Math.round(studyPlan?.progress_percentage || 0)}%</div>
            </div>

            <button
              onClick={handleRegeneratePlan}
              disabled={loadingPlan}
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition-colors"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loadingPlan ? 'animate-spin' : ''}`} />
              <span>Regenerate Roadmap</span>
            </button>
          </div>
        </div>

        {/* Global Progress Bar */}
        <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-500"
            style={{ width: `${studyPlan?.progress_percentage || 0}%` }}
          />
        </div>

        {/* Week Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800/60">
          {[1, 2, 3, 4].map(w => {
            const weekTasks = studyPlan?.tasks.filter(t => t.week_number === w) || [];
            const completed = weekTasks.filter(t => t.is_completed).length;
            const isSelected = activeWeek === w;
            const weekTitles: Record<number, string> = {
              1: 'Week 1: Foundations',
              2: 'Week 2: Architecture',
              3: 'Week 3: High Scale & Systems',
              4: 'Week 4: Capstone & Full-Round'
            };

            return (
              <button
                key={w}
                onClick={() => setActiveWeek(w)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                  isSelected
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
                    : 'bg-slate-900/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                <span>{weekTitles[w]}</span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded-full ${isSelected ? 'bg-white/20 text-white' : 'bg-slate-800 text-slate-400'}`}>
                  {completed}/{weekTasks.length}
                </span>
              </button>
            );
          })}
        </div>

        {/* Week Focus Bar */}
        <div className="flex items-center justify-between text-xs text-slate-400 px-1">
          <span>Active View: <strong className="text-white">Week {activeWeek}</strong> milestones</span>
          <span>{completedCurrentWeek} of {currentWeekTasks.length} tasks finished</span>
        </div>

        {/* Tasks List */}
        <div className="space-y-3.5">
          {currentWeekTasks.map((task: StudyTask) => (
            <div
              key={task.id}
              className={`p-4 sm:p-5 rounded-xl border transition-all ${
                task.is_completed
                  ? 'bg-slate-900/30 border-slate-800/60 opacity-80'
                  : 'glass-panel border-slate-700/60 hover:border-slate-600'
              }`}
            >
              <div className="flex items-start gap-4">
                {/* Custom Checkbox */}
                <button
                  onClick={() => handleToggleTask(task.id)}
                  disabled={togglingTaskId === task.id}
                  className={`mt-0.5 w-6 h-6 rounded-lg flex items-center justify-center border transition-all ${
                    task.is_completed
                      ? 'bg-emerald-500 border-emerald-400 text-white shadow-sm shadow-emerald-500/30'
                      : 'border-slate-600 hover:border-blue-400 bg-slate-900/80 text-transparent'
                  }`}
                  title={task.is_completed ? 'Mark incomplete' : 'Mark completed'}
                >
                  <Check className="w-3.5 h-3.5 stroke-[3]" />
                </button>

                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-2 mb-1.5">
                    <span className="text-[11px] font-bold text-slate-400">Day {task.day_number}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getTierBadge(task.tier)}`}>
                      {task.tier}
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
                      {task.topic}
                    </span>
                  </div>

                  <h4 className={`text-sm sm:text-base font-bold ${task.is_completed ? 'line-through text-slate-400' : 'text-white'}`}>
                    {task.title}
                  </h4>
                  <p className="mt-1 text-xs text-slate-400 leading-relaxed">
                    {task.description}
                  </p>

                  <div className="mt-3 flex items-center gap-3">
                    {task.resource_url && (
                      <a
                        href={task.resource_url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-400 hover:text-blue-300 hover:underline"
                      >
                        <BookOpen className="w-3.5 h-3.5" />
                        <span>Curated Reference & Practice</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
