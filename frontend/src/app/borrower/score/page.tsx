'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function ScorePage() {
  const [score, setScore] = useState<number | null>(null);
  const [explainData, setExplainData] = useState<{helping: any[], hurting: any[]} | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchScore = async () => {
      try {
        const [scoreRes, explainRes] = await Promise.all([
          api.post('/score'),
          api.post('/explain')
        ]);

        setScore(Math.round(scoreRes.data.credit_score));
        setExplainData(explainRes.data);
      } catch (err) {
        console.error('Failed to fetch score', err);
        // Fallback for demo if backend is not reachable
        setScore(694);
        setExplainData({
          helping: [{ feature: 'UPI_CONSISTENCY', impact: -0.8 }],
          hurting: [{ feature: 'DAYS_EMPLOYED', impact: 0.5 }]
        });
      } finally {
        setLoading(false);
      }
    };

    fetchScore();
  }, []);

  const getScoreColor = (s: number) => {
    if (s >= 700) return 'text-[#320070]';
    if (s >= 500) return 'text-[#320070]';
    return 'text-[#EF476F]';
  };

  const getScoreStroke = (s: number) => {
    if (s >= 700) return '#95f4a0';
    if (s >= 500) return '#FFD166';
    return '#EF476F';
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] animate-fade-in bg-[#f8f7f5]">
        <div className="w-24 h-24 rounded-full border-4 border-[#ecebe8] border-t-[#7100eb] animate-spin mb-8"></div>
        <h2 className="text-2xl font-black uppercase tracking-tight text-[#320070]">Calculating your score...</h2>
        <p className="text-[#64748B] text-xs font-bold uppercase tracking-wider mt-2">Running our alternative data ML models</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="text-center border-b-2 border-[#320070] pb-8">
        <h1 className="text-3xl font-black uppercase tracking-tight text-[#320070] mb-8">Your CreditLens Score</h1>
        <div className="relative inline-block">
          {/* Accent block under gauge */}
          <div className="absolute -inset-2 rounded bg-[#ecebe8] border-2 border-[#320070]" />
          <div className="relative bg-white border-2 border-[#320070] p-6 rounded shadow-[4px_4px_0px_0px_#320070]">
            <svg className="w-64 h-64 transform -rotate-90">
              <circle
                cx="128"
                cy="128"
                r="116"
                stroke="#ecebe8"
                strokeWidth="16"
                fill="transparent"
              />
              <circle
                cx="128"
                cy="128"
                r="116"
                stroke={getScoreStroke(score || 300)}
                strokeWidth="16"
                fill="transparent"
                strokeLinecap="square"
                strokeDasharray={2 * Math.PI * 116}
                strokeDashoffset={2 * Math.PI * 116 * (1 - ((score || 300) - 300) / 600)}
                className="transition-all duration-1000 ease-out"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-6xl font-black tracking-tight ${getScoreColor(score || 300)}`}>
                {score}
              </span>
              <span className="text-xs font-bold uppercase tracking-wider text-[#64748B] mt-2">Out of 900</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card bg-white border-2 border-[#320070] shadow-[6px_6px_0px_0px_#320070] p-6">
          <div className="flex items-center gap-2 mb-5 text-[#06382e] border-b-2 border-[#f8f7f5] pb-2">
            <TrendingUp size={20} className="text-[#059669]" />
            <h3 className="text-sm font-black uppercase tracking-wider">What's Helping</h3>
          </div>
          <ul className="space-y-3">
            {explainData?.helping.map((item, idx) => (
              <li key={idx} className="flex items-start gap-3 p-3 rounded bg-[#f8f7f5] border border-[#320070]">
                <div className="mt-1.5 w-2.5 h-2.5 rounded-sm bg-[#95f4a0] border border-[#320070] flex-shrink-0" />
                <div>
                  <p className="text-xs font-black uppercase tracking-wider text-[#320070]">{item.feature.replace(/_/g, ' ')}</p>
                  <p className="text-[10px] font-bold uppercase tracking-wider text-[#64748B] mt-0.5">{item.message || 'Positive transactional stability'}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div className="card bg-white border-2 border-[#320070] shadow-[6px_6px_0px_0px_#320070] p-6">
          <div className="flex items-center gap-2 mb-5 text-[#EF476F] border-b-2 border-[#f8f7f5] pb-2">
            <TrendingDown size={20} className="text-[#EF476F]" />
            <h3 className="text-sm font-black uppercase tracking-wider">What's Hurting</h3>
          </div>
          <ul className="space-y-3">
            {explainData?.hurting.map((item, idx) => (
              <li key={idx} className="flex items-start gap-3 p-3 rounded bg-[#f8f7f5] border border-[#EF476F]">
                <div className="mt-1.5 w-2.5 h-2.5 rounded-sm bg-[#EF476F] border border-[#320070] flex-shrink-0" />
                <div>
                  <p className="text-xs font-black uppercase tracking-wider text-[#320070]">{item.feature.replace(/_/g, ' ')}</p>
                  <p className="text-[10px] font-bold uppercase tracking-wider text-[#64748B] mt-0.5">{item.message || 'Optimization pathway recommended'}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="flex justify-end pt-4 border-t border-[#ecebe8]">
        <Link href="/borrower/roadmap" className="btn btn-primary px-6 py-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,0.15)] flex justify-center hover:bg-[#7100eb]">
          View Improvement Roadmap <ArrowRight size={16} />
        </Link>
      </div>
    </div>
  );
}
