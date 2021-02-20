import { generateChart } from './generateChart.js';

window.onload = () => {

    let temperature = [];
    let pressure = [];
    let humidity = [];
    let light = [];
    let time;
    
    const chart = new CanvasJS.Chart("chartContainer", generateChart(temperature, pressure, humidity, light));

    const addData = (data) => {
        time = Object.keys(data)[0]
        temperature.push({x:new Date(time), y:data[time].temp})
        pressure.push({x:new Date(time), y:data[time].pressure})
        humidity.push({x:new Date(time), y:data[time].humidity})
        light.push({x:new Date(time), y:data[time].light})
        chart.render();
        //setTimeout(updateData, 1500);
    }
    
    const updateData = () => {
        try{
            fetch("/live.json")
                .then(response => response.json())
                .then(addData)
        } catch(error){
            console.log(error);
        }
    }

    setInterval(updateData,1000);
    
    }