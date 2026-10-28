import React, { useState } from 'react';
import { 
  Building2, 
  Target, 
  CheckCircle, 
  ArrowRight, 
  Layers, 
  Award,
  BookOpen
} from 'lucide-react';

interface CompanyGuide {
  id: string;
  name: string;
  category: string;
  color: string;
  badgeColor: string;
  tagline: string;
  culturePillars: string[];
  rounds: Array<{
    title: string;
    duration: string;
    focus: string;
  }>;
  keyAdvice: string[];
  sampleQuestions: string[];
}

const COMPANIES: CompanyGuide[] = [
  {
    id: 'google',
    name: 'Google',
    category: 'Big Tech',
    color: 'from-blue-500 to-emerald-500',
    badgeColor: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    tagline: 'Focus on general cognitive ability, scalable system design, and Googliness.',
    culturePillars: [
      'Googliness & Navigation of Ambiguity',
      'Data-Driven Decision Making',
      'Large-scale Distributed Thinking',
      'Intellectual Humility & Collaboration'
    ],
    rounds: [
      { title: 'Recruiter & Technical Phone Screen', duration: '45 mins', focus: '1-2 LeetCode Medium data structures problems (Trees, Graphs, DP)' },
      { title: 'Coding Round 1: Algorithms', duration: '45 mins', focus: 'Clean bug-free code, edge cases, time/space complexity optimization' },
      { title: 'Coding Round 2: Data Structures', duration: '45 mins', focus: 'Custom data structure design (LRU, Trie, Heaps)' },
      { title: 'System Design Round', duration: '45 mins', focus: 'Global scalable architecture, API contracts, consistency, latency budgets' },
      { title: 'Googliness & Leadership', duration: '45 mins', focus: 'Ethics, managing conflict, teamwork, diversity, navigating ambiguity' }
    ],
    keyAdvice: [
      'Think out loud continuously. Google evaluators grade your thought process as heavily as your final answer.',
      'Always start by clarifying ambiguous constraints before writing code.',
      'Address scale: ask yourself how your solution behaves when handling billions of queries.'
    ],
    sampleQuestions: [
      'Design a distributed rate limiter that handles 100,000 requests per second across 5 continents.',
      'Given a stream of words, find the top 10 most frequent words in real-time.',
      'Tell me about a time you worked on a project with vague requirements and how you brought alignment.'
    ]
  },
  {
    id: 'amazon',
    name: 'Amazon',
    category: 'Big Tech / Cloud',
    color: 'from-amber-500 to-orange-500',
    badgeColor: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    tagline: 'Customer Obsession, Ownership, and the legendary Bar Raiser behavioral evaluation.',
    culturePillars: [
      'Customer Obsession',
      'Ownership & Long-Term Value',
      'Bias for Action',
      'Have Backbone; Disagree and Commit'
    ],
    rounds: [
      { title: 'Online Assessment (OA)', duration: '90 mins', focus: '2 algorithmic coding problems + Work Simulation & Leadership Survey' },
      { title: 'Onsite: Technical & Data Structures', duration: '60 mins', focus: 'Practical coding + 20 mins of Leadership Principle STAR stories' },
      { title: 'Onsite: System Design / OOD', duration: '60 mins', focus: 'Designing microservices, data modeling, AWS paradigms' },
      { title: 'Onsite: Bar Raiser Round', duration: '60 mins', focus: 'Deep behavioral interview measuring highest company standards and culture fit' }
    ],
    keyAdvice: [
      'Every interview round includes 15-20 minutes of Leadership Principle questions. Have 8-10 distinct STAR stories ready.',
      'Quantify your results strictly. Use metrics (e.g., "saved 22% AWS compute cost", "boosted throughput by 35%").',
      'Avoid using "we" in behavioral answers—explain exactly what YOU personally did and decided.'
    ],
    sampleQuestions: [
      'Describe a time you took calculated risk with incomplete information. What was the outcome?',
      'Design Amazon Locker delivery and reservation microservice architecture.',
      'Tell me about a time you strongly disagreed with your team lead or manager. How did you handle it?'
    ]
  },
  {
    id: 'meta',
    name: 'Meta',
    category: 'Social / AI',
    color: 'from-blue-600 to-indigo-600',
    badgeColor: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30',
    tagline: 'Move Fast, solve 2 LeetCode mediums in 45 minutes, and master production systems.',
    culturePillars: [
      'Move Fast & Bold Execution',
      'Focus on Long-Term Impact',
      'Live in the Future & Openness',
      'Directness & Peer Accountability'
    ],
    rounds: [
      { title: 'Initial Technical Screen', duration: '45 mins', focus: '2 LeetCode Medium coding problems in 40 minutes' },
      { title: 'Ninja Coding Round 1', duration: '45 mins', focus: 'High-speed algorithmic implementation, trees, graphs, strings' },
      { title: 'Ninja Coding Round 2', duration: '45 mins', focus: 'Fast recursion, dynamic programming, arrays, and two-pointer paradigms' },
      { title: 'Pirate System Design Round', duration: '45 mins', focus: 'Feed generation, messaging, live notifications, CDN caching' },
      { title: 'Jedi Behavioral Round', duration: '45 mins', focus: 'Fast-paced execution, managing cross-functional relationships and retrospectives' }
    ],
    keyAdvice: [
      'Coding speed is paramount. Meta candidates typically need to complete 2 problems in 45 minutes.',
      'Test your code manually on the whiteboard or editor with a test case before claiming it works.',
      'In system design, dive deep into the data model and API payload early.'
    ],
    sampleQuestions: [
      'Design Facebook Live Comments streaming system with millions of concurrent viewers.',
      'Find the shortest distance from all buildings in a 2D grid.',
      'Tell me about a time you identified an operational failure before anyone else and fixed it fast.'
    ]
  },
  {
    id: 'microsoft',
    name: 'Microsoft',
    category: 'Enterprise / Cloud',
    color: 'from-cyan-500 to-blue-500',
    badgeColor: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    tagline: 'Growth Mindset, customer empathy, maintainable architecture, and collaborative impact.',
    culturePillars: [
      'Growth Mindset & Curiosity',
      'Customer Empathy & Inclusion',
      'Enterprise Stability & Reliability',
      'Cross-Team Trust & Stewardship'
    ],
    rounds: [
      { title: 'Technical Phone Screen', duration: '45 mins', focus: 'Foundational coding problem and resume deep-dive' },
      { title: 'Onsite Coding Round 1', duration: '45 mins', focus: 'Clean object-oriented code, error handling, maintainability' },
      { title: 'Onsite Coding Round 2', duration: '45 mins', focus: 'Data structures, string parsing, matrix traversal' },
      { title: 'Onsite System Architecture', duration: '45 mins', focus: 'Azure-scale cloud design, disaster recovery, tenant isolation' },
      { title: 'As-Appropriate (AA) Round', duration: '45 mins', focus: 'Senior leadership interview assessing executive presence and growth mindset' }
    ],
    keyAdvice: [
      'Show eagerness to learn when you make an error or receive a hint from the interviewer.',
      'Emphasize code readability, naming conventions, and modular separation of concerns.',
      'Demonstrate how you collaborate across product, design, and QA partners.'
    ],
    sampleQuestions: [
      'Design Microsoft Teams collaborative presence and status sync service.',
      'Implement an in-memory file system with directory creation and path search.',
      'Tell me about a time you took critical feedback from a peer or user and evolved your solution.'
    ]
  },
  {
    id: 'stripe',
    name: 'Stripe',
    category: 'Fintech / APIs',
    color: 'from-violet-500 to-purple-600',
    badgeColor: 'bg-violet-500/10 text-violet-400 border-violet-500/30',
    tagline: 'Practical software engineering, real API debugging, integration tests, and pristine code.',
    culturePillars: [
      'Users First & Developer Craft',
      'Rigorous Precision & Idempotency',
      'Micro-optimization of User Experience',
      'High-Output Writing Culture'
    ],
    rounds: [
      { title: 'CoderPad Technical Screen', duration: '60 mins', focus: 'Practical parsing or data aggregation in your local dev environment' },
      { title: 'Onsite: Practical Coding', duration: '60 mins', focus: 'Build a working API client or multi-step rate limiter with test cases' },
      { title: 'Onsite: Bug Squash / Debugging', duration: '60 mins', focus: 'Clone an open-source codebase, replicate a failing bug, fix it, and verify tests' },
      { title: 'Onsite: System Design', duration: '60 mins', focus: 'Financial ledger, payment processing idempotency, multi-region database failover' },
      { title: 'Onsite: Integration / Architecture', duration: '60 mins', focus: 'Evaluating trade-offs between third-party systems and custom engines' }
    ],
    keyAdvice: [
      'Stripe does not use puzzle-based LeetCode; they test practical engineering with real IDEs, internet documentation, and unit tests.',
      'Write clean, modular code with descriptive variable names and automated unit assertions.',
      'Idempotency is paramount in fintech: know how to handle retry storms and duplicate HTTP requests.'
    ],
    sampleQuestions: [
      'Design an immutable double-entry accounting ledger system with atomic transfers.',
      'Implement a credit card charging retry mechanism with exponential backoff and idempotency keys.',
      'Given an unfamiliar codebase with 3 failing integration tests, identify the concurrency bug and fix it.'
    ]
  }
];

interface CompanyPrepProps {
  onStartSimulation?: (companyName: string) => void;
}

export const CompanyPrepView: React.FC<CompanyPrepProps> = ({ onStartSimulation }) => {
  const [selectedCompany, setSelectedCompany] = useState<CompanyGuide>(COMPANIES[0]);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="absolute right-0 top-0 w-80 h-80 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold mb-3">
            <Building2 className="w-3.5 h-3.5" />
            <span>Target Company Playbooks</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Company-Specific Prep</h1>
          <p className="text-slate-400 text-sm max-w-2xl mt-1">
            Tailor your preparation for specific tech giants and high-growth innovators. Review verified round sequences, culture principles, and high-frequency technical questions.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Playbooks Available</div>
            <div className="text-3xl font-black text-indigo-400">{COMPANIES.length}</div>
          </div>
        </div>
      </div>

      {/* Company Selector Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {COMPANIES.map((company) => {
          const isSelected = selectedCompany.id === company.id;
          return (
            <button
              key={company.id}
              onClick={() => setSelectedCompany(company)}
              className={`p-4 rounded-xl text-left transition-all flex flex-col justify-between border ${
                isSelected
                  ? 'glass-panel border-indigo-500/50 shadow-md shadow-indigo-500/10 scale-[1.02]'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className={`w-8 h-8 rounded-lg bg-gradient-to-tr ${company.color} flex items-center justify-center text-white font-bold text-sm shadow-sm`}>
                    {company.name.charAt(0)}
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${company.badgeColor}`}>
                    {company.category}
                  </span>
                </div>
                <div className="text-sm font-bold text-white">{company.name}</div>
              </div>

              <div className="mt-2 text-[11px] text-slate-500 line-clamp-1">
                {company.rounds.length} Interview Rounds
              </div>
            </button>
          );
        })}
      </div>

      {/* Selected Company Detailed Dossier */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Dossier (8 cols): Rounds & Advice */}
        <div className="lg:col-span-8 space-y-6">
          {/* Company Hero Card */}
          <div className="glass-panel rounded-2xl p-6 border border-slate-800">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
              <div className="flex items-center gap-3">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${selectedCompany.color} flex items-center justify-center text-white font-black text-xl shadow-lg`}>
                  {selectedCompany.name.charAt(0)}
                </div>
                <div>
                  <h2 className="text-xl font-extrabold text-white">{selectedCompany.name} Interview Playbook</h2>
                  <p className="text-xs text-slate-400 mt-0.5">{selectedCompany.tagline}</p>
                </div>
              </div>

              {onStartSimulation && (
                <button
                  onClick={() => onStartSimulation(selectedCompany.name)}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 transition-all self-start sm:self-auto"
                >
                  <span>Practice {selectedCompany.name} Simulation</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            {/* Cultural Pillars */}
            <div className="pt-4 border-t border-slate-800/80">
              <div className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Target className="w-3.5 h-3.5 text-indigo-400" />
                Core Cultural Dimensions Evaluated
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {selectedCompany.culturePillars.map((pillar, idx) => (
                  <div key={idx} className="flex items-center gap-2 p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    <span>{pillar}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Round-by-Round Sequence */}
          <div className="glass-panel rounded-2xl p-6 border border-slate-800">
            <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
              <Layers className="w-4 h-4 text-indigo-400" />
              Verified Interview Stages & Focus
            </h3>

            <div className="space-y-3">
              {selectedCompany.rounds.map((round, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="flex items-start gap-3">
                    <div className="w-7 h-7 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">
                      {idx + 1}
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-white">{round.title}</div>
                      <div className="text-xs text-slate-400 mt-0.5">{round.focus}</div>
                    </div>
                  </div>

                  <span className="px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 text-[11px] font-mono shrink-0 self-start sm:self-auto">
                    {round.duration}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* High-Yield Evaluator Advice */}
          <div className="glass-panel rounded-2xl p-6 border border-slate-800">
            <h3 className="text-base font-bold text-white mb-3 flex items-center gap-2">
              <Award className="w-4 h-4 text-amber-400" />
              Key Strategy & Insider Advice
            </h3>
            <ul className="space-y-2.5">
              {selectedCompany.keyAdvice.map((advice, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-300 leading-relaxed">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                  <span>{advice}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Right Column (4 cols): Curated Company Questions */}
        <div className="lg:col-span-4 space-y-6">
          <div className="glass-panel rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center gap-2 mb-4">
              <BookOpen className="w-4 h-4 text-indigo-400" />
              <h3 className="text-base font-bold text-white">High-Frequency Questions</h3>
            </div>

            <p className="text-xs text-slate-400 mb-4 leading-relaxed">
              These prompts have been reported with highest recurrence by candidates interviewing for {selectedCompany.name}:
            </p>

            <div className="space-y-3">
              {selectedCompany.sampleQuestions.map((q, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed flex flex-col gap-2">
                  <div className="flex items-center justify-between text-[11px] text-indigo-400 font-semibold">
                    <span>Question #{idx + 1}</span>
                    <span className="text-slate-500 font-normal">Real Interview</span>
                  </div>
                  <div>"{q}"</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
