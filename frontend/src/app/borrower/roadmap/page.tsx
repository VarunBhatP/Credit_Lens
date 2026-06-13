'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { CheckCircle2, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function RoadmapPage() {
  const [roadmap, setRoadmap] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRoadmap = async () => {
      try {
        // Fetch explain data to get actual hurting features
        const explainRes = await api.post('/explain');
        const hurtingFeatures = explainRes.data.hurting.map((h: any) => h.feature);
        
        const { data } = await api.post('/roadmap', { hurting: hurtingFeatures });
        setRoadmap(data);
      } catch (err) {
        console.error('Failed to fetch roadmap', err);
        // Mock data for demo
        setRoadmap({
          '3_months': ['Clear any outstanding utility bills', 'Maintain minimum balance of ₹2,000'],
          '6_months': ['Stay at current job for 6+ months', 'Increase UPI transaction frequency'],
          '12_months': ['Apply for a micro-loan and repay on time to build formal credit']
        });
      } finally {
        setLoading(false);
      }
    };

    fetchRoadmap();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] bg-[#f8f7f5]">
        <div className="w-16 h-16 border-4 border-[#ecebe8] border-t-[#7100eb] rounded-full animate-spin mb-4"></div>
        <p className="text-[#64748B] text-xs font-bold uppercase tracking-wider">Generating your personalized roadmap...</p>
      </div>
    );
  }

  const timelines = [
    { key: '3_months', title: '3-Month Plan', color: '#320070', text: '#ffffff' },
    { key: '6_months', title: '6-Month Plan', color: '#7100eb', text: '#ffffff' },
    { key: '12_months', title: '12-Month Plan', color: '#95f4a0', text: '#06382e' }
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      <header className="border-b-2 border-[#320070] pb-4">
        <h1 className="text-3xl font-black uppercase tracking-tight text-[#320070]">Improvement Roadmap</h1>
        <p className="text-[#64748B] text-xs font-bold uppercase tracking-wider mt-1">Actionable steps to boost your score</p>
      </header>

      <div className="space-y-6">
        {timelines.map((timeline, index) => {
          const items = roadmap?.[timeline.key] || [];
          return (
            <div
              key={timeline.key}
              className="card bg-white border-2 border-[#320070] shadow-[6px_6px_0px_0px_#320070] p-6 animate-fade-in"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div
                  className="w-9 h-9 rounded border-2 border-[#320070] flex items-center justify-center font-black text-xs shrink-0 shadow-[2px_2px_0px_0px_rgba(0,0,0,0.15)]"
                  style={{ backgroundColor: timeline.color, color: timeline.text }}
                >
                  {index + 1}
                </div>
                <h3 className="font-black text-lg text-[#320070] uppercase tracking-tight">{timeline.title}</h3>
              </div>
              <ul className="space-y-3 ml-[48px]">
                {items.map((item: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-3 text-xs font-semibold text-[#64748B] leading-relaxed">
                    <CheckCircle2 size={16} className="shrink-0 mt-0.5" style={{ color: timeline.color === '#95f4a0' ? '#7100eb' : timeline.color }} />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>

      <div className="flex justify-center pt-4 border-t border-[#ecebe8]">
        <Link href="/borrower/monitor" className="btn btn-primary px-8 py-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,0.15)] flex justify-center hover:bg-[#7100eb]">
          Try Health Monitor<ArrowRight size={16} />
        </Link>
      </div>
    </div>
  );
}
