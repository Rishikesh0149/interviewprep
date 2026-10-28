import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  FileText, 
  Sparkles, 
  CheckCircle2, 
  AlertCircle, 
  Plus, 
  Save, 
  Award,
  Layers,
  Briefcase,
  GraduationCap,
  Code2
} from 'lucide-react';
import { apiRequest } from '../services/api';
import type { CandidateProfile, ResumeData } from '../types';

export const ResumeLab: React.FC = () => {
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [uploading, setUploading] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);
  const [newSkillInput, setNewSkillInput] = useState<string>('');
  const [selectedSkillCategory, setSelectedSkillCategory] = useState<string>('languages');

  const fetchData = async () => {
    setLoading(true);
    try {
      const [profileRes, resumeRes] = await Promise.all([
        apiRequest<{ profile: CandidateProfile }>('/profile'),
        apiRequest<{ resume: ResumeData | null }>('/resumes/latest')
      ]);
      setProfile(profileRes.profile);
      setResume(resumeRes.resume);
    } catch (err: any) {
      console.error('Error fetching resume lab data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      setMessage({ text: 'File size exceeds 5MB limit.', type: 'error' });
      return;
    }

    setUploading(true);
    setMessage(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await apiRequest<{ message: string; resume: ResumeData; candidate_profile: CandidateProfile }>('/resumes/upload', {
        method: 'POST',
        body: formData
      });
      setResume(res.resume);
      setProfile(res.candidate_profile);
      setMessage({ text: 'Resume uploaded and candidate profile updated!', type: 'success' });
    } catch (err: any) {
      setMessage({ text: err.message || 'Upload failed.', type: 'error' });
    } finally {
      setUploading(false);
    }
  };

  const handleLoadSample = async () => {
    setUploading(true);
    setMessage(null);
    try {
      const res = await apiRequest<{ message: string; resume: ResumeData; candidate_profile: CandidateProfile }>('/resumes/sample-load', {
        method: 'POST'
      });
      setResume(res.resume);
      setProfile(res.candidate_profile);
      setMessage({ text: 'Sample Senior Full Stack resume loaded successfully!', type: 'success' });
    } catch (err: any) {
      setMessage({ text: err.message || 'Failed to load sample.', type: 'error' });
    } finally {
      setUploading(false);
    }
  };

  const handleSaveProfile = async () => {
    if (!profile) return;
    setSaving(true);
    setMessage(null);
    try {
      const res = await apiRequest<{ profile: CandidateProfile }>('/profile', {
        method: 'PUT',
        body: JSON.stringify({
          headline: profile.headline,
          summary: profile.summary,
          contact_info: profile.contact_info,
          skills: profile.skills,
          experience: profile.experience,
          education: profile.education,
          projects: profile.projects,
          certifications: profile.certifications
        })
      });
      setProfile(res.profile);
      setMessage({ text: 'Candidate profile changes saved successfully!', type: 'success' });
    } catch (err: any) {
      setMessage({ text: err.message || 'Save failed.', type: 'error' });
    } finally {
      setSaving(false);
    }
  };

  const addSkill = () => {
    if (!newSkillInput.trim() || !profile) return;
    const cat = selectedSkillCategory as keyof typeof profile.skills;
    const existing = profile.skills[cat] || [];
    if (!existing.includes(newSkillInput.trim())) {
      setProfile({
        ...profile,
        skills: {
          ...profile.skills,
          [cat]: [...existing, newSkillInput.trim()]
        }
      });
    }
    setNewSkillInput('');
  };

  const removeSkill = (category: string, skillName: string) => {
    if (!profile) return;
    const cat = category as keyof typeof profile.skills;
    setProfile({
      ...profile,
      skills: {
        ...profile.skills,
        [cat]: (profile.skills[cat] || []).filter(s => s !== skillName)
      }
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-3 border-blue-500/20 border-t-blue-500 rounded-full animate-spin" />
          <span className="text-xs text-slate-400">Loading Resume Lab...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel rounded-2xl p-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold mb-2">
            <FileText className="w-3.5 h-3.5" />
            <span>Core Module 1: Ingestion & Side-by-Side Verification</span>
          </div>
          <h1 className="text-2xl font-black text-white">Resume Lab & Candidate Profile</h1>
          <p className="text-xs text-slate-400 mt-1">
            Upload your resume (PDF/DOCX/TXT) to automatically extract your skills, experience, and projects.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleLoadSample}
            disabled={uploading}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-2 transition-all cursor-pointer"
          >
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span>Load Sample Resume</span>
          </button>

          <label className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center gap-2 transition-all shadow-lg shadow-blue-500/25 cursor-pointer">
            <Upload className="w-4 h-4" />
            <span>{uploading ? 'Processing...' : 'Upload Resume'}</span>
            <input 
              type="file" 
              accept=".pdf,.docx,.txt" 
              onChange={handleFileUpload} 
              disabled={uploading}
              className="hidden" 
            />
          </label>
        </div>
      </div>

      {/* Status banner */}
      {message && (
        <div className={`p-4 rounded-xl flex items-center gap-3 text-sm ${
          message.type === 'success' 
            ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300' 
            : 'bg-rose-500/10 border border-rose-500/30 text-rose-300'
        }`}>
          {message.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
          ) : (
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
          )}
          <span>{message.text}</span>
        </div>
      )}

      {/* Main Dual-Pane Side-by-Side Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Source Document / Raw Extracted Text (5 Cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="glass-panel rounded-2xl p-5 border border-slate-800">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-blue-400" />
                <h3 className="text-sm font-bold text-white">Source Document Inspector</h3>
              </div>
              {resume && (
                <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono">
                  {resume.file_name}
                </span>
              )}
            </div>

            {resume ? (
              <div className="space-y-4">
                {/* ATS Score Preview Card */}
                <div className="p-4 rounded-xl bg-gradient-to-r from-blue-950/60 to-indigo-950/60 border border-blue-500/20 flex items-center justify-between">
                  <div>
                    <div className="text-[11px] text-blue-300 uppercase tracking-wider font-semibold">ATS Compatibility</div>
                    <div className="text-2xl font-black text-white mt-0.5">{resume.ats_score}/100</div>
                  </div>
                  <div className="text-right">
                    <span className="text-[11px] text-slate-400 block">Extracted Size</span>
                    <span className="text-xs font-mono text-slate-200">{(resume.file_size_bytes / 1024).toFixed(1)} KB</span>
                  </div>
                </div>

                {/* Raw Text Pre */}
                <div>
                  <div className="text-xs font-semibold text-slate-400 mb-1.5 flex items-center justify-between">
                    <span>Parsed OCR / PDF Text Stream</span>
                    <span className="text-[11px] font-mono text-slate-500">{resume.raw_text.length} chars</span>
                  </div>
                  <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 text-xs font-mono text-slate-300 max-h-[560px] overflow-y-auto whitespace-pre-wrap leading-relaxed select-text">
                    {resume.raw_text}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 px-4">
                <FileText className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                <p className="text-sm font-semibold text-slate-300">No Resume Uploaded Yet</p>
                <p className="text-xs text-slate-500 mt-1 max-w-xs mx-auto">
                  Upload a PDF/DOCX or click 'Load Sample Resume' above to test the parsing pipeline.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Editable Candidate Profile (7 Cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="glass-panel rounded-2xl p-6 border border-slate-800">
            <div className="flex items-center justify-between mb-5 pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Award className="w-4 h-4 text-purple-400" />
                <h3 className="text-sm font-bold text-white">Extracted Candidate Profile (Editable)</h3>
              </div>
              <button
                onClick={handleSaveProfile}
                disabled={saving || !profile}
                className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center gap-2 transition-all shadow-md shadow-emerald-600/25 cursor-pointer disabled:opacity-50"
              >
                <Save className="w-3.5 h-3.5" />
                <span>{saving ? 'Saving...' : 'Save Profile'}</span>
              </button>
            </div>

            {profile ? (
              <div className="space-y-6">
                {/* Headline & Summary */}
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Professional Headline
                    </label>
                    <input
                      type="text"
                      value={profile.headline || ''}
                      onChange={(e) => setProfile({ ...profile, headline: e.target.value })}
                      placeholder="e.g. Senior Software Engineer | Distributed Systems & Cloud"
                      className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Professional Summary
                    </label>
                    <textarea
                      rows={3}
                      value={profile.summary || ''}
                      onChange={(e) => setProfile({ ...profile, summary: e.target.value })}
                      placeholder="Summary statement..."
                      className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-blue-500 leading-relaxed"
                    />
                  </div>
                </div>

                {/* Skills Taxonomy Section */}
                <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Code2 className="w-4 h-4 text-blue-400" />
                      <span className="text-xs font-bold text-white uppercase tracking-wider">Skills Taxonomy</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <select
                        value={selectedSkillCategory}
                        onChange={(e) => setSelectedSkillCategory(e.target.value)}
                        className="px-2 py-1 rounded-lg bg-slate-800 border border-slate-700 text-[11px] text-slate-200"
                      >
                        <option value="languages">Languages</option>
                        <option value="frameworks">Frameworks</option>
                        <option value="databases">Databases</option>
                        <option value="tools">DevOps & Tools</option>
                        <option value="soft_skills">Soft Skills</option>
                      </select>
                      <input
                        type="text"
                        placeholder="Add skill..."
                        value={newSkillInput}
                        onChange={(e) => setNewSkillInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && addSkill()}
                        className="px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-700 text-white text-[11px] w-28"
                      />
                      <button
                        onClick={addSkill}
                        className="p-1 rounded-lg bg-blue-600 hover:bg-blue-500 text-white cursor-pointer"
                      >
                        <Plus className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  {/* Skills Pills categorized */}
                  {Object.entries(profile.skills || {}).map(([cat, skillList]) => (
                    <div key={cat} className="space-y-1">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
                        {cat.replace('_', ' ')}
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {skillList && skillList.length > 0 ? (
                          skillList.map((s) => (
                            <span 
                              key={s} 
                              className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-slate-800 border border-slate-700 text-slate-200 text-xs"
                            >
                              <span>{s}</span>
                              <button 
                                onClick={() => removeSkill(cat, s)}
                                className="text-slate-500 hover:text-rose-400"
                              >
                                ×
                              </button>
                            </span>
                          ))
                        ) : (
                          <span className="text-[11px] text-slate-600 italic">None detected</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Work Experience Timeline */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Briefcase className="w-4 h-4 text-emerald-400" />
                    <span className="text-xs font-bold text-white uppercase tracking-wider">Work Experience</span>
                  </div>

                  <div className="space-y-3">
                    {profile.experience && profile.experience.map((exp, idx) => (
                      <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-white">{exp.role} @ {exp.company}</span>
                          <span className="text-[11px] text-slate-400 font-mono">{exp.start} - {exp.end}</span>
                        </div>
                        <ul className="space-y-1 mt-2">
                          {exp.bullets.map((b, bIdx) => (
                            <li key={bIdx} className="text-xs text-slate-300 flex items-start gap-2">
                              <span className="text-emerald-400 mt-1">•</span>
                              <span className="leading-relaxed">{b}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Education */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <GraduationCap className="w-4 h-4 text-indigo-400" />
                    <span className="text-xs font-bold text-white uppercase tracking-wider">Education</span>
                  </div>
                  {profile.education && profile.education.map((edu, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                      <div>
                        <div className="text-xs font-bold text-white">{edu.degree} in {edu.field}</div>
                        <div className="text-[11px] text-slate-400">{edu.institution}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs font-mono text-slate-300">Class of {edu.grad_year}</div>
                        {edu.gpa && <div className="text-[11px] text-slate-400">GPA: {edu.gpa}</div>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-slate-500 text-xs">
                Candidate profile is empty. Upload a resume to populate automatically.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
