'use client';

import { useState } from 'react';

const defaultInput = {
  team_size: 5,
  duration_months: 6,
  complexity: 'Medium',
  budget: 50000,
  requirement_changes: 'Sometimes',
  developer_experience: 'Mid',
};

export default function Home() {
  const [input, setInput] = useState(defaultInput);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const val = e.target.type === 'number' ? parseFloat(e.target.value) || 0 : e.target.value;
    setInput({ ...input, [e.target.name]: val });
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const getRiskConfig = (level: string) => {
    if (level === 'High') return {
      color: '#ff4d6d', glow: 'rgba(255,77,109,0.3)',
      bg: 'rgba(255,77,109,0.08)', border: 'rgba(255,77,109,0.25)',
      bar: 'linear-gradient(90deg, #ff4d6d, #ff0a54)', label: '🔴 High Risk',
    };
    if (level === 'Medium') return {
      color: '#f4a261', glow: 'rgba(244,162,97,0.3)',
      bg: 'rgba(244,162,97,0.08)', border: 'rgba(244,162,97,0.25)',
      bar: 'linear-gradient(90deg, #f4a261, #e76f51)', label: '🟡 Medium Risk',
    };
    return {
      color: '#52b788', glow: 'rgba(82,183,136,0.3)',
      bg: 'rgba(82,183,136,0.08)', border: 'rgba(82,183,136,0.25)',
      bar: 'linear-gradient(90deg, #52b788, #2d6a4f)', label: '🟢 Low Risk',
    };
  };

  const selectStyle = {
    width: '100%', marginTop: 4, padding: '9px 12px',
    borderRadius: 8, border: '1px solid rgba(255,255,255,0.08)',
    background: 'rgba(255,255,255,0.05)', color: '#e2e8f0',
    fontSize: 13, outline: 'none', boxSizing: 'border-box' as const,
  };

  const inputStyle = {
    ...selectStyle,
  };

  const labelStyle = {
    fontSize: 10, fontWeight: 500, color: '#475569',
    textTransform: 'uppercase' as const, letterSpacing: 0.5,
  };

  return (
    <main style={{ minHeight: '100vh', background: '#080c14', color: '#e2e8f0', fontFamily: 'Inter, sans-serif' }}>

      {/* Navbar */}
      <nav style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', padding: '16px 40px', display: 'flex', alignItems: 'center', gap: 12, background: 'rgba(255,255,255,0.02)' }}>
        <div style={{ width: 36, height: 36, borderRadius: 10, background: 'linear-gradient(135deg, #00b4d8, #0077b6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 18 }}>◈</div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 16 }}>RiskIQ Platform</div>
          <div style={{ fontSize: 11, color: '#475569' }}>Software Project Intelligence</div>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
          <span style={{ fontSize: 11, padding: '4px 12px', borderRadius: 20, background: 'rgba(0,180,216,0.12)', color: '#00b4d8', border: '1px solid rgba(0,180,216,0.25)' }}>LightGBM</span>
          <span style={{ fontSize: 11, padding: '4px 12px', borderRadius: 20, background: 'rgba(139,92,246,0.12)', color: '#a78bfa', border: '1px solid rgba(139,92,246,0.25)' }}>Groq AI</span>
        </div>
      </nav>

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '32px 40px', display: 'grid', gridTemplateColumns: '1fr 1.6fr', gap: 24 }}>

        {/* LEFT — Input */}
        <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.07)', borderRadius: 20, padding: 28 }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#64748b', letterSpacing: 1, textTransform: 'uppercase', marginBottom: 24 }}>◈ Project Details</div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

            {/* Team Size */}
            <div>
              <label style={labelStyle}>Team Size (developers)</label>
              <input type="number" name="team_size" value={input.team_size} onChange={handleChange} style={inputStyle} min={1} />
            </div>

            {/* Duration */}
            <div>
              <label style={labelStyle}>Duration (months)</label>
              <input type="number" name="duration_months" value={input.duration_months} onChange={handleChange} style={inputStyle} min={1} />
            </div>

            {/* Budget */}
            <div>
              <label style={labelStyle}>Budget ($)</label>
              <input type="number" name="budget" value={input.budget} onChange={handleChange} style={inputStyle} min={0} />
            </div>

            {/* Complexity */}
            <div>
              <label style={labelStyle}>Project Complexity</label>
              <select name="complexity" value={input.complexity} onChange={handleChange} style={selectStyle}>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>

            {/* Requirement Changes */}
            <div>
              <label style={labelStyle}>Requirement Changes</label>
              <select name="requirement_changes" value={input.requirement_changes} onChange={handleChange} style={selectStyle}>
                <option value="Rare">Rare</option>
                <option value="Sometimes">Sometimes</option>
                <option value="Frequent">Frequent</option>
              </select>
            </div>

            {/* Developer Experience */}
            <div>
              <label style={labelStyle}>Developer Experience</label>
              <select name="developer_experience" value={input.developer_experience} onChange={handleChange} style={selectStyle}>
                <option value="Junior">Junior</option>
                <option value="Mid">Mid-level</option>
                <option value="Senior">Senior</option>
              </select>
            </div>

          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            style={{
              width: '100%', marginTop: 28, padding: '14px',
              borderRadius: 12, border: 'none',
              background: loading ? 'rgba(0,180,216,0.3)' : 'linear-gradient(135deg, #00b4d8, #0077b6)',
              color: '#fff', fontWeight: 700, fontSize: 14,
              cursor: loading ? 'not-allowed' : 'pointer',
              boxShadow: loading ? 'none' : '0 0 24px rgba(0,180,216,0.35)',
              transition: 'all 0.2s',
            }}
          >
            {loading ? '⏳  Analyzing...' : '▶  Analyze Risk'}
          </button>
        </div>

        {/* RIGHT — Results */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {result ? (() => {
            const cfg = getRiskConfig(result.risk_level);
            return (
              <>
                {/* Score */}
                <div style={{ background: cfg.bg, border: `1px solid ${cfg.border}`, borderRadius: 20, padding: 28, boxShadow: `0 0 40px ${cfg.glow}` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20 }}>
                    <div>
                      <div style={{ fontSize: 11, color: '#64748b', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6 }}>Risk Score</div>
                      <div style={{ fontSize: 64, fontWeight: 900, lineHeight: 1, color: cfg.color }}>
                        {result.risk_score}<span style={{ fontSize: 28, fontWeight: 400, color: '#475569' }}>%</span>
                      </div>
                    </div>
                    <div style={{ padding: '8px 18px', borderRadius: 30, background: cfg.bg, border: `1px solid ${cfg.border}`, fontSize: 13, fontWeight: 700, color: cfg.color }}>
                      {cfg.label}
                    </div>
                  </div>
                  <div style={{ height: 8, borderRadius: 99, background: 'rgba(255,255,255,0.07)', overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${result.risk_score}%`, background: cfg.bar, borderRadius: 99, transition: 'width 1s ease' }} />
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10, color: '#334155', marginTop: 6 }}>
                    <span>0% · Safe</span><span>50% · Moderate</span><span>100% · Critical</span>
                  </div>
                </div>

                {/* Top Factors */}
                <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.07)', borderRadius: 20, padding: 24 }}>
                  <div style={{ fontSize: 11, fontWeight: 600, color: '#64748b', letterSpacing: 1, textTransform: 'uppercase', marginBottom: 16 }}>Top Risk Factors</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {result.top_risk_factors.map((factor: string, i: number) => (
                      <div key={factor} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 14px', borderRadius: 10, background: 'rgba(255,255,255,0.04)' }}>
                        <span style={{ fontSize: 11, fontWeight: 800, width: 22, height: 22, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,180,216,0.2)', color: '#00b4d8', flexShrink: 0 }}>
                          {i + 1}
                        </span>
                        <span style={{ fontSize: 13, color: '#cbd5e1', textTransform: 'capitalize', flex: 1 }}>
                          {factor.replace(/_/g, ' ')}
                        </span>
                        <div style={{ height: 4, borderRadius: 99, background: `rgba(0,180,216,${0.85 - i * 0.13})`, width: `${(5 - i) * 14}%` }} />
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Explanation */}
                <div style={{ background: 'rgba(139,92,246,0.07)', border: '1px solid rgba(139,92,246,0.2)', borderRadius: 20, padding: 24 }}>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: 14 }}>
                    <div style={{ fontSize: 11, fontWeight: 600, color: '#a78bfa', letterSpacing: 1, textTransform: 'uppercase' }}>AI Analysis</div>
                    <span style={{ marginLeft: 'auto', fontSize: 10, padding: '3px 10px', borderRadius: 99, background: 'rgba(139,92,246,0.15)', color: '#c4b5fd', border: '1px solid rgba(139,92,246,0.25)' }}>
                      Groq · LLaMA
                    </span>
                  </div>
                  <p style={{ fontSize: 13, lineHeight: 1.8, color: '#94a3b8', margin: 0 }}>
                    {result.ai_explanation}
                  </p>
                </div>
              </>
            );
          })() : (
            <div style={{ minHeight: 400, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 16, background: 'rgba(255,255,255,0.02)', border: '1px dashed rgba(255,255,255,0.08)', borderRadius: 20 }}>
              <div style={{ fontSize: 48, opacity: 0.3 }}>◈</div>
              <p style={{ fontSize: 13, color: '#334155' }}>Enter project details and click Analyze Risk</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}