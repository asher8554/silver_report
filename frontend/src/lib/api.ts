import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export interface MarketData {
  Silver: any[];
  Gold: any[];
  Bitcoin: any[];
  USD_Index: any[];
}

export interface ReportData {
  timestamp: string | null;
  bullish_report: string;
  bearish_report: string;
  market_data: MarketData;
  news_data: any[];
}

export const api = {
  getLatestReport: async (): Promise<ReportData> => {
    const response = await axios.get(`${API_BASE_URL}/report/latest`);
    return response.data;
  },

  triggerReport: async () => {
    const response = await axios.post(`${API_BASE_URL}/trigger-report`);
    return response.data;
  },
};
