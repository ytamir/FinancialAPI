import React from 'react'
import HighchartsReact from 'highcharts-react-official'
import { withTheme } from '@material-ui/styles';

const StockChart = ({ options, highcharts }) => <HighchartsReact
  highcharts={highcharts}
  constructorType={'stockChart'}
  options={options}
/>


export default withTheme(StockChart);