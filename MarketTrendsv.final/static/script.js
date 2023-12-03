// JavaScript function to switch data using the button
function switchData(company) {
    var iframe = document.getElementById('chart-iframe');
    iframe.src = '/switch_data/' + company;  // Set to the new URL
}

function switchDataLinePlot(company) {
    var iframe = document.getElementById('line-chart-iframe');
    iframe.src = '/switch_data_line_chart/' + company;  // Set to the new URL
}