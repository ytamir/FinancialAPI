import React from 'react'
import HighchartsReact from 'highcharts-react-official'
import Highcharts from 'highcharts'

export default class Container extends React.Component {
  constructor () {
    super()
    this.state = { // TODO remove chart title
      chartOptions: {
        title: {text: null},
        exporting: {
            buttons: {
                contextButton: {
                    enabled: false
                }    
            }
        },
        credits: {
            enabled: false
          },
          legend: {
            enabled: false
        },
        chart: {
            height: 200,
            type: 'area'
        },
        plotOptions: {
            series: {
                fillOpacity: 0.1
            }
        },   
        series: [{
          data: [],
          color: '#34d965',
        negativeColor: '#0088FF',
        threshold: 2
        }],
        xAxis:{
            visible: false
        },
        yAxis:{
            visible: false
        },
        title:{
            visible: false
        }
      }
    }
    this.timer();
    // setInterval(function(){
    //     console.log(this);
    //     const { chartOptions } = this.state;
    //     console.log(chartOptions);
    
    //     this.setState({
    //     chartOptions: {
    //       series: [{
    //         data: this.state.chartOptions.series[0].data.push(Math.random()*3 -1),
    //         color: '#FF0000',
    //         negativeColor: '#0088FF'          
    //       }]
    //     }}
    //   )}, 1500);
    
  }
  
  getData(){
    
    setInterval(() => {
        const axios = require('axios');
        //var a = this.state;
        let cur = this;
        


        let url = "https://financialmodelingprep.com/api/v3/majors-indexes/.DJI";
        axios.get(url).then(function (response) {
            // handle success
           
            console.log(response.data.price);
            console.log("this.state");
        console.log(cur.state);
        let old_data = cur.state.chartOptions.series[0].data;
        old_data.push(response.data.price);
    
        console.log('Our data is fetched');
        cur.setState({
            chartOptions: {
                
            chart: {
                height: 200,
                type: 'area'
            },
            exporting: {
                buttons: {
                    contextButton: {
                        enabled: false
                    }    
                }
            },
            legend: {
                enabled: false
            },
            series: [{
                data: old_data,//[0].data.push(Math.random()*3 -1),
                color: '#FF0000',
                negativeColor: '#0088FF' ,
                threshold: 2
            }],
            title: {text: null},
            xAxis:{
                visible: false
            },
            yAxis:{
                visible: false
            },
            title:{
                visible: false
            }
            }});
          })
          .catch(function (error) {
            // handle error
            console.log(error);
          })
          .finally(function () {
            // always executed
          });
        
    }, 5000);
  }

  componentDidMount(){
    this.getData();
  }

  componentWillUnmount() {
    clearInterval(this.countdown);
  }

  timer() {
    //this.setState({ currentCount: 10 });
    var a = this.state;
    console.log("a");
    console.log(a);

    this.setState({
        chartOptions: {
          series: [{
            //data: this.state.chartOptions.series[0].data.push(Math.random()*3 -1),
            color: '#FF0000',
            negativeColor: '#0088FF'          
          }]
        }});
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