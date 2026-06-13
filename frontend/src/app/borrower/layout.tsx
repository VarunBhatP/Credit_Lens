'use client';

import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, UserPlus, Upload, ShieldAlert, TrendingUp, Calculator, Activity, LogOut, ChevronRight } from 'lucide-react';

export default function BorrowerLayout({ children }: { children: React.ReactNode }) {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!loading && (!user || user.role !== 'borrower')) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F7F8FC]">
        <div className="w-8 h-8 border-2 border-[#E2E8F0] border-t-[#00B4D8] rounded-full animate-spin" />
      </div>
    );
  }

  const navItems = [
    { href: '/borrower/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/borrower/onboarding', label: 'Onboarding', icon: UserPlus, step: 1 },
    { href: '/borrower/upload', label: 'Upload Docs', icon: Upload, step: 2 },
    { href: '/borrower/score', label: 'Credit Score', icon: ShieldAlert, step: 3 },
    { href: '/borrower/roadmap', label: 'Roadmap', icon: TrendingUp, step: 4 },
    
    { href: '/borrower/monitor', label: 'Health Monitor', icon: Activity, step: 5 },
    { href: '/borrower/applications', label: 'Applications', icon: Activity, step: 6 },
    { href: '/borrower/simulator', label: 'Loan Simulator', icon: Calculator, step: 7 },
  ];

  return (
    <div className="min-h-screen bg-[#f8f7f5] flex">
      {/* ─── Sidebar ─── */}
      <aside className="w-[260px] bg-[#320070] hidden md:flex flex-col shrink-0 border-r-2 border-[#7100eb]">
        {/* Logo */}
        <div className="px-6 py-6 border-b border-[#7100eb]">
          <Link href="/borrower/dashboard" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded bg-[#95f4a0] border border-[#320070] text-[#320070] flex items-center justify-center font-black text-sm">C</div>
            <span className="text-white font-extrabold text-lg uppercase tracking-wider">CreditLens</span>
          </Link>
        </div>
        
        {/* Nav */}
        <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-sm text-xs font-bold uppercase tracking-wider transition-all border-l-4 ${
                  isActive 
                    ? 'bg-[#7100eb] text-white border-l-[#95f4a0] shadow-sm' 
                    : 'text-white/60 border-l-transparent hover:bg-white/5 hover:text-white/90'
                }`}
              >
                <Icon size={16} className={isActive ? 'text-[#95f4a0]' : ''} />
                {item.step ? `${item.step}. ${item.label}` : item.label}
                {isActive && <ChevronRight size={14} className="ml-auto text-white/50" />}
              </Link>
            );
          })}
        </nav>
        
        {/* User / Logout */}
        <div className="p-4 border-t border-[#7100eb]">
          <div className="flex items-center gap-3 px-2 mb-3">
            <div className="w-9 h-9 rounded bg-white/10 flex items-center justify-center text-white font-bold text-sm border border-white/20">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-bold text-white truncate uppercase tracking-wider">{user?.name || 'User'}</p>
              <p className="text-[10px] text-white/50 truncate font-semibold">{user?.email}</p>
            </div>
          </div>
          <button 
            onClick={logout}
            className="flex items-center gap-2 w-full px-3 py-2.5 text-xs font-bold uppercase tracking-wider text-white/50 hover:text-[#EF476F] hover:bg-white/5 rounded transition-colors"
          >
            <LogOut size={16} />
            Sign Out
          </button>
        </div>
      </aside>

      {/* ─── Main ─── */}
      <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
        {/* Mobile Header */}
        <header className="md:hidden bg-[#320070] px-4 py-3 flex justify-between items-center border-b border-[#7100eb]">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded bg-[#95f4a0] text-[#320070] flex items-center justify-center font-black text-xs">C</div>
            <span className="text-white font-extrabold text-sm uppercase tracking-wider">CreditLens</span>
          </div>
          <button onClick={logout} className="text-white/60 hover:text-white">
            <LogOut size={18} />
          </button>
        </header>

        <main className="flex-1 overflow-y-auto">
          <div className="max-w-5xl mx-auto px-4 md:px-8 py-6 md:py-10">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
