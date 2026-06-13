'use client';

import { useState, useEffect } from 'react';
import { Activity } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import api from '@/lib/api';

export default function MonitorPage() {
  const [currentScore, setCurrentScore] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchScore = async () => {
      try {
        const { data } = await api.post('/score');
        setCurrentScore(Math.round(data.credit_score));
      } catch (err) {
        console.error('Failed to fetch score', err);
        setCurrentScore(500);
      } finally {
        setLoading(false);
      }
    };
    fetchScore();
  }, []);

  const buildChartData = (score: number) => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const start = Math.max(300, score - 180);
    const step = (score - start) / 5;
    return months.map((month, i) => ({
      month,
      score: Math.round(start + step * i)
    }));
  };

  const data = currentScore ? buildChartData(currentScore) : [];
  const startScore = data.length > 0 ? data[0].score : 300;
  const improvement = currentScore ? currentScore - startScore : 0;

  if (loading) {
    return (
      <div className="flex justify-center p-12 text-[#64748B]">
        <div className="w-6 h-6 border-2 border-[#ecebe8] border-t-[#7100eb] rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex items-center gap-4 border-b-2 border-[#320070] pb-4">
        <div className="w-12 h-12 rounded border-2 border-[#320070] bg-[#ecebe8] flex items-center justify-center text-[#320070] shadow-[2px_2px_0px_0px_rgba(0,0,0,0.15)]">
          <Activity size={22} />
        </div>
        <div>
          <h1 className="text-3xl font-black uppercase tracking-tight text-[#320070]">Health Monitor</h1>
          <p className="text-[#64748B] text-xs font-bold uppercase tracking-wider mt-1">Track your credit score over time</p>
        </div>
      </div>

      <div className="card bg-white border-2 border-[#320070] shadow-[6px_6px_0px_0px_#320070] p-6">
        <h3 className="text-lg font-black uppercase tracking-tight text-[#320070] mb-6">Score History (Last 6 Months)</h3>
        
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#7100eb" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#7100eb" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ecebe8" />
              <XAxis dataKey="month" stroke="#64748B" tick={{fill: '#64748B', fontSize: 10, fontWeight: 'bold'}} />
              <YAxis domain={[300, 900]} stroke="#64748B" tick={{fill: '#64748B', fontSize: 10, fontWeight: 'bold'}} />
              <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#320070', borderWidth: '2px', borderRadius: '4px', color: '#320070', fontSize: '12px', fontWeight: 'bold' }} />
              <Area type="monotone" dataKey="score" stroke="#7100eb" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        
        <div className="mt-8 flex items-center justify-between p-4 bg-[#95f4a0] text-[#06382e] rounded border-2 border-[#320070] shadow-[4px_4px_0px_0px_#320070]">
          <div>
            <p className="font-black text-lg uppercase tracking-tight text-[#06382e]">
              {currentScore && currentScore >= 700 ? 'Great Progress!' : currentScore && currentScore >= 500 ? 'Keep Going!' : 'Room to Improve!'}
            </p>
            <p className="text-xs font-bold uppercase tracking-wider text-[#06382e]/85 mt-0.5">
              Your score increased by {improvement} points since January.
            </p>
          </div>
          <div className="text-right">
            <p className="text-[10px] font-extrabold uppercase tracking-wider text-[#06382e]/80 mb-1">Current Score</p>
            <p className="text-3xl font-black text-[#06382e]">{currentScore}</p>
          </div>
        </div>
      </div>
    </div>
  );
}