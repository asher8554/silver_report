"use client";

import { createChart, ColorType, IChartApi, ISeriesApi, CandlestickData, Time } from 'lightweight-charts';
import React, { useEffect, useRef } from 'react';

export interface ChartProps {
  data: {
    time: string | number; // YYYY-MM-DD or Unix Timestamp
    open: number;
    high: number;
    low: number;
    close: number;
  }[];
  colors?: {
    backgroundColor?: string;
    lineColor?: string;
    textColor?: string;
    areaTopColor?: string;
    areaBottomColor?: string;
  };
}

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
        mode: 1, // Magnet mode
      }
    });

    chartRef.current = chart;

    const candlestickSeries = (chart as any).addCandlestickSeries({
      upColor: '#26a69a', 
      downColor: '#ef5350', 
      borderVisible: false, 
      wickUpColor: '#26a69a', 
      wickDownColor: '#ef5350',
    });

    // 데이터 타입 변환 및 정렬
    // lightweight-charts는 시간순 정렬된 데이터를 요구함
    const sortedData = [...data]
      .sort((a, b) => {
        const timeA = typeof a.time === 'string' ? new Date(a.time).getTime() : a.time;
        const timeB = typeof b.time === 'string' ? new Date(b.time).getTime() : b.time;
        return timeA - timeB;
      })
      .map(item => ({
        ...item,
        time: (typeof item.time === 'string' ? item.time : item.time) as Time
      }));

    // 중복 시간 제거 (마지막 데이터 유지)
    const uniqueData = sortedData.filter((item, index, self) => 
      index === self.findIndex((t) => (
        t.time === item.time
      ))
    );

    candlestickSeries.setData(uniqueData as CandlestickData<Time>[]);

    window.addEventListener('resize', handleResize);

    // Initial fit
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
