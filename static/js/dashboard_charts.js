document.addEventListener("DOMContentLoaded", function () {
    console.log("Charts JS Loaded ✅");

    loadSalesChart();
    loadFilteredChart();
    loadDayWiseChart();
    loadCategoryChart();
    loadYearlyChart();
    loadYearMonthChart();
    loadAOVChart();
    loadRevenueOrdersChart();
    loadTopProductsChart();
    loadPriceRangeChart();
    loadCLVChart();
    loadUserChart();
});

function createChart(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, config);
}

// ✅ SALES CHART
function loadSalesChart() {

    fetch("/dashboard/api/sales-report/")
    .then(response => response.json())
    .then(data => {

        const ctx = document.getElementById('salesChart');

        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Revenue (₹)',
                    data: data.revenues,
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true
            }
        });

    })
    .catch(error => console.error("Error loading sales report:", error));

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

function loadDayWiseChart() {
    const canvas = document.getElementById('dayWiseChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // 🎨 Gradients
    const gradientBlue = ctx.createLinearGradient(0, 0, 0, 400);
    gradientBlue.addColorStop(0, 'rgba(54, 162, 235, 0.9)');
    gradientBlue.addColorStop(1, 'rgba(54, 162, 235, 0.2)');

    const gradientPink = ctx.createLinearGradient(0, 0, 0, 400);
    gradientPink.addColorStop(0, 'rgba(255, 99, 132, 0.9)');
    gradientPink.addColorStop(1, 'rgba(255, 99, 132, 0.2)');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: day_labels,
            datasets: [
                {
                    label: 'Orders',
                    data: day_orders,
                    backgroundColor: gradientBlue,
                    borderRadius: 8
                },
                {
                    label: 'Revenue',
                    data: day_revenues,
                    backgroundColor: gradientPink,
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#333',
                        font: { weight: '600' }
                    }
                }
            },
            scales: {
                x: { grid: { display: false } },
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                }
            }
        }
    });
}

// 📦 CATEGORY CHART
function loadCategoryChart() {
    const canvas = document.getElementById('categoryChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: category_labels,
            datasets: [{
                data: category_revenues,
                backgroundColor: [
                    '#ff6384',
                    '#36a2eb',
                    '#ffcd56',
                    '#4bc0c0',
                    '#9966ff',
                    '#ff9f40'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// 📆 YEARLY CHART
function loadYearlyChart() {
    createChart('yearlySalesChart', {
        type: 'bar',
        data: {
            labels: year_labels,
            datasets: [{
                label: 'Yearly Revenue',
                data: year_revenues
            }]
        }
    });
}

function loadYearMonthChart() {
    const canvas = document.getElementById('yearMonthChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: year_month_labels,
            datasets: [{
                label: 'Monthly Revenue (₹)',
                data: year_month_revenues,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: '#4bc0c0',
                borderWidth: 1
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

function loadAOVChart() {
    createChart('aovChart', {
        type: 'line',
        data: {
            labels: aov_dates,
            datasets: [{
                label: 'AOV (₹)',
                data: aov_values,
                borderColor: '#ff6384',
                backgroundColor: 'rgba(255,99,132,0.1)',
                tension: 0.3,
                fill: true
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

function loadRevenueOrdersChart() {
    const canvas = document.getElementById('revenueOrdersChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: revenue_orders_dates,
            datasets: [
                {
                    label: 'Revenue (₹)',
                    data: revenue_orders_revenue,
                    borderColor: '#28a745',
                    tension: 0.3,
                    yAxisID: 'y'
                },
                {
                    label: 'Orders',
                    data: revenue_orders_counts,
                    borderColor: '#007bff',
                    tension: 0.3,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            interaction: { mode: 'index', intersect: false },
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    grid: { drawOnChartArea: false }
                }
            }
        }
    });
}

//top selling products
function loadTopProductsChart() {
    const canvas = document.getElementById('topProductsChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top_products_labels,
            datasets: [{
                label: 'Units Sold',
                data: top_products_data,
                backgroundColor: 'rgba(255, 193, 7, 0.7)'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true
        }
    });
}

//clv
function loadCLVChart() {
    createChart('clvChart', {
        type: 'bar',
        data: {
            labels: clv_labels,
            datasets: [{
                label: 'CLV',
                data: clv_values
            }]
        }
    });
}

//user chart
function loadUserChart() {
    const canvas = document.getElementById('userChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: user_labels,
            datasets: [{
                label: 'Total Spent',
                data: user_data
            }]
        },
        options: {
            responsive: true
        }
    });
}

//PRICE RANGE
function loadPriceRangeChart() {
    createChart('priceRangeChart', {
        type: 'doughnut',
        data: {
            labels: price_range_labels,
            datasets: [{
                data: price_range_data
            }]
        }
    });
}
