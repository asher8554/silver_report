"use client";

import { createChart, ColorType, IChartApi, ISeriesApi, CandlestickData, Time, CandlestickSeries } from 'lightweight-charts';
import React, { useEffect, useRef } from 'react';

/**
 * 차트 컴포넌트의 Props 인터페이스입니다.
 */
export interface ChartProps {
  /** 
   * 차트에 표시할 데이터 배열입니다.
   * 시간(time)과 시가(open), 고가(high), 저가(low), 종가(close)를 포함해야 합니다.
   */
  data: {
    time: string | number; // YYYY-MM-DD 또는 Unix 타임스탬프
    open: number;
    high: number;
    low: number;
    close: number;
  }[];
  /**
   * 차트의 색상 설정 옵션입니다.
   */
  colors?: {
    backgroundColor?: string;
    lineColor?: string;
    textColor?: string;
    areaTopColor?: string;
    areaBottomColor?: string;
  };
}

/**
 * Lightweight Charts를 사용하여 캔들스틱 차트를 렌더링하는 컴포넌트입니다.
 * 
 * @param props {@link ChartProps} 차트 데이터 및 색상 설정
 * @returns 캔들스틱 차트 요소를 포함하는 div
 */
export const CandlestickChart = (props: ChartProps) => {
  const {
    data,
    colors: {
      backgroundColor = 'white',
      lineColor = '#2962FF',
      textColor = 'black',
      areaTopColor = '#2962FF',
      areaBottomColor = 'rgba(41, 98, 255, 0.28)',
    } = {},
  } = props;

  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: backgroundColor },
        textColor,
      },
      width: chartContainerRef.current.clientWidth,
      height: 300,
      grid: {
        vertLines: { color: '#f0f3fa' },
        horzLines: { color: '#f0f3fa' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
      crosshair: {
        mode: 1, // 자석 모드 (Magnet mode)
      }
    });

    chartRef.current = chart;

    const candlestickSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#26a69a', 
      downColor: '#ef5350', 
      borderVisible: false, 
      wickUpColor: '#26a69a', 
      wickDownColor: '#ef5350',
    });

    // 데이터 유효성 검사 및 정제
    const validData = data
      .map(item => {
        const timeVal = typeof item.time === 'string' 
          ? new Date(item.time).getTime() / 1000 // Unix 타임스탬프(초)로 변환
          : item.time;
        
        return {
          ...item,
          time: timeVal as Time,
          // 가격 데이터가 유효한 숫자인지 확인
          open: Number(item.open),
          high: Number(item.high),
          low: Number(item.low),
          close: Number(item.close),
        };
      })
      .filter(item => 
        !isNaN(Number(item.time)) && 
        !isNaN(item.open) && 
        !isNaN(item.high) && 
        !isNaN(item.low) && 
        !isNaN(item.close)
      )
      .sort((a, b) => (a.time as number) - (b.time as number));

    // 시간 기준 중복 제거
    const uniqueData: CandlestickData<Time>[] = [];
    const seenTimes = new Set<number>();

    for (const item of validData) {
      const timeNum = item.time as number;
      if (!seenTimes.has(timeNum)) {
        seenTimes.add(timeNum);
        uniqueData.push(item);
      }
    }

    if (uniqueData.length === 0) {
      console.warn('Chart data is empty after validation');
      return;
    }

    try {
      candlestickSeries.setData(uniqueData);
    } catch (err) {
      console.error('Error setting chart data:', err);
    }

    window.addEventListener('resize', handleResize);

    // 초기 차트 범위 설정
    chart.timeScale().fitContent();

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, backgroundColor, textColor]);

  return (
    <div ref={chartContainerRef} className="w-full h-full" />
  );
};
