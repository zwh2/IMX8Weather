import { generateChart } from './generateChart.js';
import { generateHistChart } from './generateHistChart.js';

window.onload = () => {

    let temperature = [];
    let pressure = [];
    let humidity = [];
    let light = [];

    let htemperature = [];
    let hpressure = [];
    let hhumidity = [];
    let hlight = [];
    
    const chart = new CanvasJS.Chart("chartContainer1", generateChart("Live Data",temperature, pressure, humidity, light));
    const histChart = new CanvasJS.Chart("chartContainer2", generateHistChart("History",htemperature, hpressure, hhumidity, hlight));
    const addData = (data) => {
        const time = Object.keys(data)[0]
        temperature.push({x:new Date(time), y:data[time].temp})
        pressure.push({x:new Date(time), y:data[time].pressure})
        humidity.push({x:new Date(time), y:data[time].humidity})
        light.push({x:new Date(time), y:data[time].light})
        chart.render();
        //setTimeout(updateData, 1500);
    }

    const addHistory = (data) => {
        htemperature.length = 0;
        hpressure.length = 0;
        hhumidity.length = 0;
        hlight.length = 0;
        for(const point of Object.entries(data)) {
            const time = point[0]
            htemperature.push({x:new Date(time), y:point[1].temp})
            hpressure.push({x:new Date(time), y:point[1].pressure})
            hhumidity.push({x:new Date(time), y:point[1].humidity})
            hlight.push({x:new Date(time), y:point[1].light})
        }
        histChart.render();
    }
    
    const updateLiveData = () => {
        try{
            fetch("/live.json")
                .then(response => response.json())
                .then(addData)
        } catch(error){
            console.error("live data error")
            console.error(error);
        }
    }

    const updateHistory = () => {
        try{
            fetch("/history.json")
                .then(response => response.json())
                .then(addHistory)
        }catch(error){
            console.error("history data error")
            console.error(error);
        }
    }
    updateLiveData();
    updateHistory();
    setInterval(updateLiveData,1000);
    setInterval(updateHistory,60000);
    
    }