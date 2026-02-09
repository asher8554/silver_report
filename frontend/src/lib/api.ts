import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

/**
 * 시장 데이터 인터페이스
 */
export interface MarketData {
  Silver: any[];
  Gold: any[];
  Bitcoin: any[];
  USD_Index: any[];
}

/**
 * 리포트 데이터 인터페이스
 */
export interface ReportData {
  timestamp: string | null;
  bullish_report: string;
  bearish_report: string;
  market_data: MarketData;
  news_data: any[];
}

export const api = {
  /**
   * 최신 리포트를 조회합니다.
   */
  getLatestReport: async (): Promise<ReportData> => {
    const response = await axios.get(`${API_BASE_URL}/report/latest`);
    return response.data;
  },

  /**
   * 리포트 생성을 트리거합니다.
   */
  triggerReport: async () => {
    const response = await axios.post(`${API_BASE_URL}/trigger-report`);
    return response.data;
  },
};
