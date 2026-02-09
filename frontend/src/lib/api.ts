import axios from "axios";

// GitHub Pages 배포 시 basePath를 고려해야 함
const BASE_PATH = "/silver_report";
const DATA_URL = `${BASE_PATH}/data.json`;

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
    // 정적 JSON 파일에서 데이터를 가져옵니다.
    const response = await axios.get(DATA_URL);
    return response.data;
  },

  /**
   * 리포트 생성을 트리거합니다.
   */
  triggerReport: async () => {
    // 정적 사이트에서는 백엔드 트리거가 불가능하므로 에러를 반환하거나 기능을 비활성화합니다.
    console.warn("Static site: Trigger report not available via frontend.");
    throw new Error("정적 사이트에서는 리포트 생성을 지원하지 않습니다 (GitHub Actions에서 자동 수행).");
  },
};
