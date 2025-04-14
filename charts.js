function drawCustomGraph(canvasID) {
  const id = canvasID;
  const ctx = document.getElementById(canvasID).getContext('2d');

  let titleText;
  if (id === 'co2-graph') {
    titleText = 'CO2 Sensor Graph';
  } else if (id === 'temp-graph') {
    titleText = 'Temperature Graph';
  } else if (id === 'alt-graph') {
    titleText = 'Altitude Graph';
  }

  const initialLabels = [];
  const initialData = [];

  const chartData = {
    labels: initialLabels,
    datasets: [{
      label: 'Sensor Reading',
      borderColor: 'white',
      borderWidth: 1,
      pointRadius: 6,
      fill: false,
      pointBackgroundColor: []  
    }]  
  };


  function updateSensorValue(id, value, thresholds) {
    const el = document.getElementById(id);
    el.textContent = value;
      
    if(id == 'co2'){
      if (value < thresholds.warning) {
          el.style.color = '#42a5f5';
        } else if (value <= thresholds.normal) {
          el.style.color = '#4caf50';
        } else {
          el.style.color = '#ff4c4c';
        }
    } else if (id == 'temp'){
      if (value < thresholds.warning) {
          el.style.color = '#42a5f5';
        } else if (value <= thresholds.normal) {
          el.style.color = '#4caf50';
        } else {
          el.style.color = '#ff4c4c';
        }
    } else if (id == 'alt'){
      if (value < thresholds.warning) {
          el.style.color = '#42a5f5';
        } else if (value <= thresholds.normal) {
          el.style.color = '#4caf50';
        } else {
          el.style.color = '#ff4c4c';
        }
    }
  }
  

  const config = {
    type: 'line',
    data: chartData,
    options: {
      responsive: true,
      bordercolor: 'white',
      borderwidth: 1,
      plugins: {
        title: {
          display: true,
          text: titleText
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return 'Value: ' + context.parsed.y;
          }
        }
      },
      animation: {
        duration: 300  
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 5
          }
        }
      }
    }
  };

  const myChart = new Chart(ctx, config);

  function getDataValue() {
    const dataArr = myChart.data.datasets[0].data;
    return dataArr[dataArr.length - 1];
  }

  function addData(label, data) {
    myChart.data.labels.push(label);
    const dataset = myChart.data.datasets[0];
    dataset.data.push(data);
  

    let thresholds;
    if (id === 'co2-graph') {
      thresholds = { normal: 50, warning: 20 };
    } else if (id === 'temp-graph') {
      thresholds = { normal: 80, warning: 30 };
    } else if (id === 'alt-graph') {
      thresholds = { normal: 15, warning: 5 };
    }
  

    let pointColor;
    if (data < thresholds.warning) {
      pointColor = '#42a5f5';
    } else if (data <= thresholds.normal) {
      pointColor = '#4caf50';
    } else {
      pointColor = '#ff4c4c';
    }
  
    
    dataset.pointBackgroundColor.push(pointColor);
  
  
    const maxDataPoints = 20;
    if (myChart.data.labels.length > maxDataPoints) {
      myChart.data.labels.shift();
      dataset.data.shift();
      dataset.pointBackgroundColor.shift();  // Remove old point color
    }
  
    myChart.update();
  }
  

  setInterval(() => {
    const now = new Date();
    const newLabel = now.toLocaleTimeString();
    let newValue;

    if (id === 'co2-graph') {
      newValue = Math.floor(Math.random() * 60);
      const co2Value = newValue;
      updateSensorValue('co2', co2Value, { normal: 50, warning: 20 })
      addData(newLabel, newValue);
    } else if (id === 'temp-graph') {
      newValue = Math.floor(Math.random() * 120);
      const tempValue = newValue;
      updateSensorValue('temp', tempValue, { normal: 80, warning: 30 })
      addData(newLabel, newValue);
    } else if (id === 'alt-graph') {
      newValue = Math.floor(Math.random() * 20);
      const altValue = newValue;
      updateSensorValue('alt', altValue, { normal: 15, warning: 5 })
      addData(newLabel, newValue);
    }
    
    const sensorDisplayId = id.replace('-graph', '');
    document.getElementById(sensorDisplayId).textContent = getDataValue();
  }, 1000);
}