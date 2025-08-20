function refreshData() {
    fetch('/refresh')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#traffic-table tbody");
            tableBody.innerHTML = "";
            data.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${row.timestamp}</td>
                    <td>${row.src_ip}</td>
                    <td>${row.dst_ip}</td>
                    <td>${row.protocol}</td>
                    <td>${row.length}</td>
                `;
                tableBody.appendChild(tr);
            });
        })
        .catch(error => console.error("Error fetching traffic data:", error));
}

function loadChart() {
    fetch("/protocol_chart_data")
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('protocolChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Packet Count',
                        data: data.values,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error("Failed to load chart data:", error));
}

document.addEventListener("DOMContentLoaded", function () {
    refreshData();
    loadChart();
    setInterval(refreshData, 5000);  // Refresh table every 5 seconds
});
