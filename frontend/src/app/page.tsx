"use client";

import { useEffect, useState } from 'react';
import { api, ReportData, AssetData } from '@/lib/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ArrowUpCircle, ArrowDownCircle, RefreshCw, TrendingUp, TrendingDown, Clock } from 'lucide-react';
import dynamic from 'next/dynamic';

const CandlestickChart = dynamic(
  () => import('@/components/CandlestickChart').then((mod) => mod.CandlestickChart),
  { ssr: false }
);

/**
 * 실버 리포트의 메인 페이지 컴포넌트입니다.
 * 리포트 데이터를 가져와 차트와 텍스트로 보여줍니다.
 */
export default function Home() {
  const [report, setReport] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchReport();
  }, []);

  /**
   * 최신 리포트 데이터를 API로부터 가져옵니다.
   */
  const fetchReport = async () => {
    try {
      setLoading(true);
      const data = await api.getLatestReport();
      setReport(data);
    } catch (error) {
      console.error("Failed to fetch report", error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 리포트 생성을 수동으로 트리거하고, 일정 시간 후 데이터를 새로고침합니다.
   */
  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await api.triggerReport();
      // 생성 대기 (더 나은 방법은 폴링이지만, UI 피드백을 위해 단순히 지연시킴)
      setTimeout(() => {
        fetchReport();
        setRefreshing(false);
      }, 5000); 
    } catch (error) {
      setRefreshing(false);
    }
  };

  if (loading && !report) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // 차트 데이터 처리
  // 가독성을 위해 필요하다면 최근 50개 포인트로 제한
  const silverData = report?.market_data?.Silver?.slice(-50) || [];
  
  // 차트 데이터 포맷팅
  const chartData = silverData.map((item) => ({
    time: new Date(item.Datetime || item.Date || '').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    price: item.Close
  }));

  return (
    <main className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex justify-between items-center bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Silver Report AI</h1>
            <p className="text-gray-500 mt-1 flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Last Updated: {report?.timestamp ? new Date(report.timestamp).toLocaleString() : 'Never'}
            </p>
          </div>
          <button 
            onClick={handleRefresh}
            disabled={true} // 정적 사이트에서는 비활성화
            className={`flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all bg-gray-300 text-gray-500 cursor-not-allowed`}
            title="GitHub Actions에 의해 자동 업데이트됩니다."
          >
            <RefreshCw className={`w-5 h-5`} />
            Auto Update via GitHub Actions
          </button>
        </header>

        {/* Charts & Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Chart */}
          <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-gray-400" />
              Silver Price Trend (7d)
            </h2>
            <div className="h-[300px] w-full">
              {/* <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                  <XAxis dataKey="time" tick={{fontSize: 12, fill: '#9ca3af'}} axisLine={false} tickLine={false} />
                  <YAxis domain={['auto', 'auto']} tick={{fontSize: 12, fill: '#9ca3af'}} axisLine={false} tickLine={false} width={40} />
                  <Tooltip 
                    contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)'}}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#2563eb" 
                    strokeWidth={3} 
                    dot={false}
                    activeDot={{r: 6, strokeWidth: 0}}
                  />
                </LineChart>
              </ResponsiveContainer> */}
              <CandlestickChart data={silverData
                .map((d: AssetData) => {
                  const timeStr = d.Datetime || d.Date;
                  if (!timeStr) return null;
                  const time = new Date(timeStr).getTime() / 1000;
                  if (isNaN(time)) return null;
                  if (d.Open == null || d.High == null || d.Low == null || d.Close == null) return null;
                  
                  return {
                    time, // Unix timestamp (seconds)
                    open: d.Open,
                    high: d.High,
                    low: d.Low,
                    close: d.Close
                  };
                })
                .filter((item): item is NonNullable<typeof item> => item !== null)
              } />
            </div>
          </div>

          {/* Stats / Info */}
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="text-gray-500 font-medium text-sm uppercase tracking-wider mb-2">Latest Silver Price</h3>
              <div className="text-4xl font-bold text-gray-900">
                ${dataLastPrice(silverData)}
              </div>
              <div className="text-sm text-green-500 font-medium mt-1 flex items-center gap-1">
                <TrendingUp className="w-4 h-4" />
                Live Data
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
              <h3 className="text-gray-500 font-medium text-sm uppercase tracking-wider mb-4">Market Context</h3>
              <div className="space-y-3">
                 <div className="flex justify-between items-center">
                    <span className="text-gray-600">Gold</span>
                    <span className="font-semibold">${dataLastPrice(report?.market_data?.Gold)}</span>
                 </div>
                 <div className="flex justify-between items-center">
                    <span className="text-gray-600">Bitcoin</span>
                    <span className="font-semibold">${dataLastPrice(report?.market_data?.Bitcoin)}</span>
                 </div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Reports */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* Bullish Report */}
          <div className="bg-gradient-to-br from-white to-blue-50 p-8 rounded-2xl shadow-sm border border-blue-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-100 rounded-full blur-3xl -mr-16 -mt-16 opcaity-50"></div>
            <div className="relative">
              <h2 className="text-2xl font-bold text-blue-900 mb-4 flex items-center gap-3">
                <ArrowUpCircle className="w-8 h-8 text-blue-600" />
                bullish Report
                <span className="text-xs font-normal px-2 py-1 bg-blue-200 text-blue-800 rounded-full">Optimistic</span>
              </h2>
              <div className="prose prose-blue max-w-none text-gray-700 whitespace-pre-line">
                {report?.bullish_report}
              </div>
            </div>
          </div>

          {/* Bearish Report */}
          <div className="bg-gradient-to-br from-white to-red-50 p-8 rounded-2xl shadow-sm border border-red-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-100 rounded-full blur-3xl -mr-16 -mt-16 opcaity-50"></div>
            <div className="relative">
              <h2 className="text-2xl font-bold text-red-900 mb-4 flex items-center gap-3">
                <ArrowDownCircle className="w-8 h-8 text-red-600" />
                Bearish Report
                <span className="text-xs font-normal px-2 py-1 bg-red-200 text-red-800 rounded-full">Pessimistic</span>
              </h2>
              <div className="prose prose-red max-w-none text-gray-700 whitespace-pre-line">
                {report?.bearish_report}
              </div>
            </div>
          </div>

        </div>

        {/* News Feed */}
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
           <h2 className="text-xl font-bold mb-6">Latest Headlines Analyzed</h2>
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {report?.news_data?.map((news: any, idx: number) => (
                <a key={idx} href={news.url} target="_blank" rel="noopener noreferrer" className="block p-4 rounded-xl hover:bg-gray-50 transition-colors border border-transparent hover:border-gray-200 group">
                  <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2">{news.title}</h3>
                  <div className="text-sm text-gray-500 mt-2">{new Date(news.published_date).toLocaleDateString()}</div>
                </a>
              ))}
              {(!report?.news_data || report.news_data.length === 0) && (
                <p className="text-gray-500">No recent news used in this analysis.</p>
              )}
           </div>
        </div>

      </div>
    </main>
  );
}

/**
 * 배열의 마지막 데이터 포인트에서 종가(Close)를 가져와 포맷팅합니다.
 */
function dataLastPrice(data: any[] | undefined) {
    if (!data || data.length === 0) return "N/A";
    const last = data[data.length - 1];
    return typeof last.Close === 'number' ? last.Close.toFixed(2) : last.Close;
}
