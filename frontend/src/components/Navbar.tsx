import React from 'react';
import { 
  FileText, 
  Compass, 
  Mic, 
  Code, 
  BookOpen, 
  Building2, 
  LayoutDashboard, 
  LogOut, 
  Flame,
  Award
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const { user, logout } = useAuth();

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'resume_lab', label: 'Resume Lab', icon: FileText },
    { id: 'skill_gap', label: 'Skill Gap & Plan', icon: Compass },
    { id: 'interview', label: 'Mock Interview', icon: Mic },
    { id: 'coding', label: 'Code Arena', icon: Code },
    { id: 'questions', label: 'Question Bank', icon: BookOpen },
    { id: 'company_prep', label: 'Company Prep', icon: Building2 },
  ];

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Compass className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-100 to-blue-400 bg-clip-text text-transparent">
                PrepPilot
              </div>
              <div className="text-[10px] text-blue-400 tracking-wider font-semibold uppercase">
                AI Career Co-Pilot
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-inner'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* User Metrics & Quick Actions */}
          <div className="flex items-center gap-3">
            {user ? (
              <>
                {/* Streak Badge */}
                <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold" title="Current Daily Streak">
                  <Flame className="w-4 h-4 fill-amber-400 text-amber-500" />
                  <span>{user.current_streak}d</span>
                </div>

                {/* Readiness Score Badge */}
                <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold">
                  <Award className="w-4 h-4 text-blue-400" />
                  <span>{Math.round(user.readiness_score)}% Ready</span>
                </div>

                {/* Profile Pill */}
                <div 
                  className="cursor-pointer flex items-center gap-2 pl-2 pr-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 hover:border-slate-600 transition-colors"
                  onClick={() => setActiveTab('settings')}
                >
                  <div className="w-6 h-6 rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 flex items-center justify-center text-[11px] font-bold text-white">
                    {user.full_name.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-xs font-medium text-slate-200 max-w-[90px] truncate">
                    {user.full_name}
                  </span>
                </div>

                {/* Logout Button */}
                <button
                  onClick={logout}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                  title="Log out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </>
            ) : (
              <button
                onClick={() => setActiveTab('auth')}
                className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold transition-all shadow-md shadow-blue-600/30"
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
