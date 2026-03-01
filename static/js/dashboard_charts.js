// dashboard_charts.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("Charts JS Loaded ✅");

    loadSalesChart();
    loadFilteredChart();
});

// ✅ SALES CHART
function loadSalesChart() {
    const canvas = document.getElementById('salesChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: sales_dates,
            datasets: [{
                label: 'Revenue (₹)',
                data: sales_revenues,
                borderColor: '#28a745',
                backgroundColor: 'rgba(40,167,69,0.1)',
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#28a745'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// ✅ FILTERED CHART
function loadFilteredChart() {
    const canvas = document.getElementById('filteredSalesChart');
    if (!canvas) return;

    if (!filtered_dates || filtered_dates.length === 0) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: filtered_dates,
            datasets: [{
                label: 'Revenue',
                data: filtered_revenues,
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true
        }
    });
}