const ctx = document.getElementById('light-sensor-chart').getContext('2d');
const maxDataPoints = 50; // Maximální počet bodů v grafu
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Uin [V]',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            pointRadius: 0
        }, {
            label: 'Uout [V]',
            data: [],
            borderColor: 'rgba(192, 75, 75, 1)',
            borderWidth: 1,
            pointRadius: 0
        }, {
            label: 'Proud 1 [A]',
            data: [],
            borderColor: 'rgba(75, 75, 192, 1)',
            borderWidth: 1,
            pointRadius: 0
        }, {
            label: 'Proud 2 [A]',
            data: [],
            borderColor: 'rgba(192, 192, 75, 1)',
            borderWidth: 1,
            pointRadius: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second'
                },
                ticks: {
                    maxTicksLimit: 10
                }
            },
            y: {
                beginAtZero: true
            }
        },
        animation: false
    }
});

const socket = io('http://127.0.0.1:5000');

socket.on('connect', function() {
    console.log('Connected to server');
});

let startTime = Date.now();

socket.on('data', function(data) {

    const now = Date.now();
    const elapsedTime = (now - startTime) / 1000; // Čas v sekundách

    myChart.data.labels.push(now);
    myChart.data.datasets[0].data.push({x: now, y: data.Uin});
    myChart.data.datasets[1].data.push({x: now, y: data.Uout});
    myChart.data.datasets[2].data.push({x: now, y: data.proud1});
    myChart.data.datasets[3].data.push({x: now, y: data.proud2});

    // Omezení počtu bodů v grafu
    if (myChart.data.labels.length > maxDataPoints) {
        myChart.data.labels.shift();
        myChart.data.datasets.forEach(dataset => dataset.data.shift());
    }

    // Nastavení rozsahu osy x
    const oldestDataPoint = myChart.data.labels[0];
    myChart.options.scales.x.min = oldestDataPoint;
    myChart.options.scales.x.max = now;

    myChart.update();

    // Aktualizace aktuálních hodnot
    document.getElementById('uin-value').textContent = data.Uin.toFixed(2);
    document.getElementById('uout-value').textContent = data.Uout.toFixed(2);
    document.getElementById('proud1-value').textContent = data.proud1.toFixed(2);
    document.getElementById('proud2-value').textContent = data.proud2.toFixed(2);
});

const switchButtons = document.querySelectorAll('.switch-btn');
switchButtons.forEach(button => {
    button.addEventListener('click', function() {
        const switchNumber = this.getAttribute('data-switch');
        console.log('Sending switch command:', switchNumber);
        socket.emit('switch', switchNumber);
    });
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
});