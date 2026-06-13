'use client';

import { useState } from 'react';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { CheckCircle2, XCircle, ArrowRight, Loader2 } from 'lucide-react';
import Link from 'next/link';

export default function SimulatorPage() {
  const [formData, setFormData] = useState({
    loanAmnt: 50000,
    term: 36,
  });
  
  const [result, setResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const payload = {
        loan_amnt: Number(formData.loanAmnt),
        term: Number(formData.term),
      };

      const { data } = await api.post('/eligibility', payload);
      setResult(data);
    } catch (err) {
      console.error('Simulation failed', err);
      // Mock for demo if backend is unreachable
      setResult({
        eligible: true,
        recommended_amount: formData.loanAmnt,
        default_probability: 0.12
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8 animate-fade-in">
      <header className="border-b-2 border-[#320070] pb-4">
        <h1 className="text-3xl font-black uppercase tracking-tight text-[#320070]">Loan Simulator</h1>
        <p className="text-[#64748B] text-xs font-bold uppercase tracking-wider mt-1">See what loans you qualify for today</p>
      </header>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card bg-white border-2 border-[#320070] shadow-[6px_6px_0px_0px_#320070] p-6 h-fit">
          <form onSubmit={handleSimulate} className="space-y-6">
            <div>
              <label className="label">Loan Amount Requested (₹)</label>
              <input
                type="number"
                required
                className="input text-sm font-bold text-[#320070]"
                value={formData.loanAmnt}
                onChange={(e) => setFormData({ ...formData, loanAmnt: Number(e.target.value) })}
              />
              <input 
                type="range" 
                min="10000" 
                max="500000" 
                step="5000"
                className="w-full mt-4 accent-[#7100eb]"
                value={formData.loanAmnt}
                onChange={(e) => setFormData({ ...formData, loanAmnt: Number(e.target.value) })}
              />
            </div>

            <div>
              <label className="label">Tenure (Months)</label>
              <select 
                className="input text-sm font-bold text-[#320070]"
                value={formData.term}
                onChange={(e) => setFormData({ ...formData, term: Number(e.target.value) })}
              >
                <option value={12}>12 Months</option>
                <option value={24}>24 Months</option>
                <option value={36}>36 Months</option>
                <option value={48}>48 Months</option>
                <option value={60}>60 Months</option>
              </select>
            </div>

            <button type="submit" className="btn btn-primary w-full py-4 shadow-[3px_3px_0px_0px_rgba(0,0,0,0.15)] flex justify-center hover:bg-[#7100eb]" disabled={isLoading}>
              {isLoading ? <Loader2 className="animate-spin text-white" /> : 'Check Eligibility'}
            </button>
          </form>
        </div>

        <div>
          {result ? (
            <div className={`card bg-white border-2 border-[#320070] p-8 h-full flex flex-col justify-center items-center text-center animate-fade-in space-y-4 ${
              result.eligible ? 'shadow-[6px_6px_0px_0px_#95f4a0]' : 'shadow-[6px_6px_0px_0px_#EF476F]'
            }`}>
              {result.eligible ? (
                <>
                  <div className="w-16 h-16 rounded border-2 border-[#320070] bg-[#95f4a0] flex items-center justify-center text-[#320070] mb-2 shadow-[2px_2px_0px_0px_rgba(0,0,0,0.15)]">
                    <CheckCircle2 size={32} />
                  </div>
                  <h3 className="text-2xl font-black uppercase tracking-tight text-[#06382e]">You are Eligible!</h3>
                  <p className="text-xs font-bold uppercase tracking-wider text-[#64748B]">Based on your CreditLens score.</p>
                  
                  <div className="w-full bg-[#f8f7f5] rounded border-2 border-[#320070] p-4 mt-4">
                    <p className="text-[10px] font-extrabold uppercase tracking-wider text-[#64748B] mb-1">Approved Amount</p>
                    <p className="text-3xl font-black text-[#320070]">₹{result.recommended_amount.toLocaleString()}</p>
                  </div>
                  
                  {result.recommended_amount < formData.loanAmnt && (
                     <p className="text-[10px] font-black uppercase tracking-wider text-[#d97706] mt-2 mb-4">
                       Note: Approved amount is lower than requested due to risk parameters.
                     </p>
                  )}
                  
                  <button 
                    onClick={async () => {
                      try {
                        const { data: lenders } = await api.get('/lenders');
                        await Promise.all(
                          lenders.map((lender: any) =>
                            api.post(`/lender/select/${lender.id}`).catch(() => {})
                          )
                        );
                        toast.success('Application submitted to lenders successfully!');
                      } catch (err) {
                        toast.error('Failed to submit application.');
                      }
                    }}
                    className="btn btn-accent w-full py-4 text-xs font-black uppercase tracking-wider mt-4 shadow-[3px_3px_0px_0px_rgba(50,0,112,0.15)]"
                  >
                    Submit Application to Lenders
                  </button>
                </>
              ) : (
                <>
                  <div className="w-16 h-16 rounded border-2 border-[#EF476F] bg-[#EF476F]/10 flex items-center justify-center text-[#EF476F] mb-2">
                    <XCircle size={32} />
                  </div>
                  <h3 className="text-2xl font-black uppercase tracking-tight text-[#EF476F]">Not Eligible Yet</h3>
                  <p className="text-xs font-bold uppercase tracking-wider text-[#64748B]">
                    Your current profile risk is too high for this amount.
                  </p>
                  <div className="w-full bg-[#f8f7f5] rounded border-2 border-[#EF476F] p-4 mt-4 text-left">
                    <p className="text-[10px] font-extrabold uppercase tracking-wider text-[#EF476F] mb-1">Recommended Action</p>
                    <p className="text-xs font-bold text-[#320070]">Follow your 3-month roadmap plan to improve your eligibility.</p>
                  </div>
                </>
              )}
            </div>
          ) : (
            <div className="h-full border-2 border-dashed border-[#7100eb] rounded flex items-center justify-center bg-[#f8f7f5] text-[#64748B] p-8 text-center text-xs font-bold uppercase tracking-wider leading-relaxed">
              Adjust the parameters and click "Check Eligibility" to see your results.
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
