import React from 'react'
import HighchartsReact from 'highcharts-react-official'
import Highcharts from 'highcharts'

export default class Container extends React.Component {
  constructor () {
    super()
    this.state = {
      chartOptions: {
        series: [{
          data: [1,2,3],
          color: '#FF0000',
        negativeColor: '#0088FF'
        }]
      }
    }
    setInterval(() => this.setState({
        chartOptions: {
          series: [{
            data: [
              Math.random()*3-3,
              Math.random()*3,
              Math.random()*3
            ]
          }]
        }}
      ), 1500)
  }

  render () {
    return (
      <div>
        <HighchartsReact
          highcharts={Highcharts}
          options={this.state.chartOptions}
        />
      </div> 
    )
  }
}