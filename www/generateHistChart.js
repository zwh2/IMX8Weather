export const generateHistChart = (title, temperature, pressure, humidity, light) => ({
    theme: "light2",
    title: {
        text: title
    },
    axisY:[{
        title: "Temperature",
        lineColor: "#C24642",
        tickColor: "#C24642",
        labelFontColor: "#C24642",
        titleFontColor: "#C24642",
        suffix: "c"
    },
    {
        title: "Pressure",
        lineColor: "#369EAD",
        tickColor: "#369EAD",
        labelFontColor: "#369EAD",
        titleFontColor: "#369EAD",
        suffix: "mbar"
    }],
    axisY2: [{
        title: "Humidity",
        lineColor: "#7F6084",
        tickColor: "#7F6084",
        labelFontColor: "#7F6084",
        titleFontColor: "#7F6084",
        minimum: 0,
        maximum: 100,
        suffix: "%"
    },
    {
        title: "Light Level",
        lineColor: "#fcba03",
        tickColor: "#fcba03",
        labelFontColor: "#fcba03",
        titleFontColor: "#fcba03",
        suffix: "lx"
    }],
    toolTip: {
        shared: true
    },
    zoomEnabled: true,
    legend: {
        cursor: "pointer",
        itemclick: toggleDataSeries
    },
    data: [{
        type: "line",
        name: "Temperature",
        color: "#C24642",
        showInLegend: true,
        dataPoints: temperature,
        axisYType: "primary",
        markerType: "none"
    },
    {
        type: "line",
        name: "Pressure",
        color: "#369EAD",
        showInLegend: true,
        dataPoints: pressure,
        axisYIndex: 1,
        axisYType: "primary",
        markerType: "none"
    },
    {
        type: "line",
        name: "Humidity",
        color: "#7F6084",
        showInLegend: true,
        dataPoints: humidity,
        axisYType: "secondary",
        markerType: "none"
    },
    {
        type: "line",
        name: "Light Level",
        color: "#fcba03",
        showInLegend: true,
        dataPoints: light,
        axisYIndex: 1,
        axisYType: "secondary",
        markerType: "none"
    }]
})

const toggleDataSeries = (e) => {
    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    } else {
        e.dataSeries.visible = true;
    }
    e.chart.render();
}