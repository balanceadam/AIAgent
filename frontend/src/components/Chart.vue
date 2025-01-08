<template>
  <div ref="chartContainer" class="chart-container"></div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { createChart, CrosshairMode, LineStyle } from 'lightweight-charts'
import { useAssetsStore } from '@/stores/assets'

const { getMinuteMarketData } = useAssetsStore()

export default {
  name: 'Chart',
  props: ['id'],
  setup(props) {
    // 创建对 chartContainer 的引用
    const chartContainer = ref(null)
    let chart = null
    let candlestickSeries = null
    const { id } = props
    // 获取比特币的 K 线数据
    const fetchMinuteMarketData = async () => {
      try {
        let data = []
        try {
          data = await getMinuteMarketData(id)
        } catch (error) {
          console.error(error)
        }
        // 转换数据格式为 lightweight-charts 需要的格式
        const klineData = data.map((item) => ({
          time: item[0] / 1000, // 将时间戳转换为秒
          open: parseFloat(item[1]),
          high: parseFloat(item[2]),
          low: parseFloat(item[3]),
          close: parseFloat(item[4])
        }))

        // 设置蜡烛图数据
        candlestickSeries.setData(klineData)
      } catch (error) {
        console.error('Error fetching Kline data:', error)
      }
    }

    // 在组件挂载时初始化图表
    onMounted(() => {
      // 创建图表
      chart = createChart(chartContainer.value, {
        width: chartContainer.value.clientWidth,
        layout: {
          background: {
            color: '#0d0d0d'
          },
          textColor: '#efefe2'
        },
        grid: {
          vertLines: {
            visible: false
          },
          horzLines: {
            visible: false
          }
        },
        timeScale: {
          timeVisible: true, // 显示具体时间
          secondsVisible: false // 显示秒，如果需要分钟级，可以关闭
        },
      })
      candlestickSeries = chart.addCandlestickSeries({
        upColor: '#4caf50',       // 上涨柱子颜色
        downColor: '#e91e63',     // 下跌柱子颜色
        borderUpColor: '#4caf50', // 上涨边框颜色
        borderDownColor: '#e91e63', // 下跌边框颜色
        wickUpColor: '#4caf50',   // 上涨影线颜色
        wickDownColor: '#e91e63', // 下跌影线颜色
        priceFormat: {
          type: 'price',
          minMove: 0.00000000000001,
        }
      });
      chart.subscribeCrosshairMove((param) => {
        if (!param || !param.seriesData) {
          return;
        }

        // 获取当前悬停的柱子数据
        const bar = param.seriesData.get(candlestickSeries);
        if (!bar) {
          return;
        }

        const isUp = bar.close > bar.open; // 判断涨跌
        const color = isUp ? '#4caf50' : '#e91e63'; // 根据涨跌设置颜色

        // 动态修改 crosshair 标签背景颜色
        chart.applyOptions({
          crosshair: {
            vertLine: { labelBackgroundColor: color }, // 时间标签背景颜色
            horzLine: { labelBackgroundColor: color }, // 价格标签背景颜色
          },
        });
      });
      // 获取并展示比特币 K 线数据
      fetchMinuteMarketData()
    })

    // 在组件卸载时移除图表
    onBeforeUnmount(() => {
      if (chart) {
        chart.remove()
      }
    })

    return {
      chartContainer
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  margin: 0 auto;
}
</style>
