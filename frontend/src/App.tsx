import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { AuthView } from './pages/AuthView';
import { ResumeLab } from './pages/ResumeLab';
import { SkillGapView } from './pages/SkillGapView';
import { InterviewArena } from './pages/InterviewArena';
import { CodeArena } from './pages/CodeArena';
import { QuestionBankView } from './pages/QuestionBankView';
import { CompanyPrepView } from './pages/CompanyPrepView';
import { 
  FileText, 
  Mic, 
  Code, 
  Sparkles, 
  ArrowRight, 
  Compass, 
  BookOpen, 
  Building2 
} from 'lucide-react';

const MainShell: React.FC = () => {
  const { user, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0b0f19] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin" />
          <span className="text-sm font-medium text-slate-400">Loading PrepPilot...</span>
        </div>
      </div>
    );
  }

  if (!user && activeTab !== 'auth') {
    return (
      <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col">
        <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="flex-1">
          <AuthView onSuccess={() => setActiveTab('dashboard')} />
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col selection:bg-blue-500/30">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'resume_lab' ? (
          <ResumeLab />
        ) : activeTab === 'skill_gap' ? (
          <SkillGapView />
        ) : activeTab === 'interview' ? (
          <InterviewArena onNavigateToPlan={() => setActiveTab('skill_gap')} />
        ) : activeTab === 'coding' ? (
          <CodeArena />
        ) : activeTab === 'questions' ? (
          <QuestionBankView onPracticeQuestion={() => setActiveTab('interview')} />
        ) : activeTab === 'company_prep' ? (
          <CompanyPrepView onStartSimulation={() => setActiveTab('interview')} />
        ) : (
          <div className="space-y-6">
          {/* Welcome Banner */}
          <div className="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden">
            <div className="absolute right-0 top-0 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold mb-3">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Target Role: {user?.target_role || 'Software Engineer'}</span>
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
                  Welcome, {user?.full_name || 'Trainee'}!
                </h2>
                <p className="mt-1 text-slate-400 text-sm max-w-2xl">
                  PrepPilot has initialized your candidate profile and seed datasets. You're set up for end-to-end interview prep. Proceed to upload your resume or simulate a mock interview round.
                </p>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Readiness Score</div>
                  <div className="text-3xl font-black text-blue-400">{Math.round(user?.readiness_score || 0)}%</div>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Start Module Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <div 
              onClick={() => setActiveTab('resume_lab')}
              className="glass-panel glass-panel-hover rounded-2xl p-5 cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mb-3 group-hover:scale-110 transition-transform">
                  <FileText className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-1">Resume Lab</h3>
                <p className="text-slate-400 text-xs mb-4">
                  Parse candidate profile, get ATS rubrics, and match against job descriptions.
                </p>
              </div>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-blue-400 group-hover:gap-2.5 transition-all">
                <span>Open Resume Lab</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>

            <div 
              onClick={() => setActiveTab('skill_gap')}
              className="glass-panel glass-panel-hover rounded-2xl p-5 cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-3 group-hover:scale-110 transition-transform">
                  <Compass className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-1">Skill Gap & Plan</h3>
                <p className="text-slate-400 text-xs mb-4">
                  Identify competency deltas and execute a tiered 4-week structured preparation syllabus.
                </p>
              </div>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-400 group-hover:gap-2.5 transition-all">
                <span>View Roadmap</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>

            <div 
              onClick={() => setActiveTab('interview')}
              className="glass-panel glass-panel-hover rounded-2xl p-5 cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-3 group-hover:scale-110 transition-transform">
                  <Mic className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-1">Mock Interview</h3>
                <p className="text-slate-400 text-xs mb-4">
                  Adaptive speech and text simulations with real-time STAR rubric scoring and debrief.
                </p>
              </div>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-purple-400 group-hover:gap-2.5 transition-all">
                <span>Start Simulation</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>

            <div 
              onClick={() => setActiveTab('coding')}
              className="glass-panel glass-panel-hover rounded-2xl p-5 cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-3 group-hover:scale-110 transition-transform">
                  <Code className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-1">Code Arena</h3>
                <p className="text-slate-400 text-xs mb-4">
                  In-browser code editor with sandboxed test execution and AI hints.
                </p>
              </div>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-400 group-hover:gap-2.5 transition-all">
                <span>Open Arena</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>

            <div 
              onClick={() => setActiveTab('questions')}
              className="glass-panel glass-panel-hover rounded-2xl p-5 cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-3 group-hover:scale-110 transition-transform">
                  <BookOpen className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-1">Question Bank</h3>
                <p className="text-slate-400 text-xs mb-4">
                  Hundreds of categorized prompts with ideal STAR answer breakdowns and rubric hints.
                </p>
              </div>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-amber-400 group-hover:gap-2.5 transition-all">
                <span>Browse Questions</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>

            <div 
              onClick={() => setActiveTab('company_prep')}
              className="glass-panel glass-panel-hover rounded-2xl p-5 cursor-pointer group flex flex-col justify-between"
            >
              <div>
                <div className="w-11 h-11 rounded-xl bg-pink-500/10 border border-pink-500/20 flex items-center justify-center text-pink-400 mb-3 group-hover:scale-110 transition-transform">
                  <Building2 className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold text-white mb-1">Company Prep</h3>
                <p className="text-slate-400 text-xs mb-4">
                  Playbooks and round sequences for Google, Amazon, Meta, Microsoft, and Stripe.
                </p>
              </div>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-pink-400 group-hover:gap-2.5 transition-all">
                <span>Explore Playbooks</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          </div>
        </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-auto py-6 border-t border-slate-800/80 text-center text-xs text-slate-500">
        <p>PrepPilot v1.0 • AI-Powered Resume & Interview Preparation Assistant</p>
        <p className="mt-1 text-[11px] text-slate-600">Disclaimer: AI feedback is guidance, not a guarantee of hiring outcomes.</p>
      </footer>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <MainShell />
    </AuthProvider>
  );
}
