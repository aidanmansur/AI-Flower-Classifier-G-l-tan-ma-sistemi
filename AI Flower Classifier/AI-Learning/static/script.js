
// Dashboard məlumatlarını backend-dən alırıq
async function loadDashboard() {

    const response = await fetch("/api/dashboard");

    const data = await response.json();

    // Accuracy göstəririk
    document.getElementById("accuracy").textContent =
        data.accuracy + "%";

    // Gül növlərini qruplaşdırırıq
    const colors = {
        setosa: "#8b5cf6",
        versicolor: "#06b6d4",
        virginica: "#f59e0b"
    };

    const datasets = data.classes.map(flower => {

        const points = data.flowers
            .filter(item => item.class === flower)
            .map(item => ({
                x: item.petal_length,
                y: item.petal_width
            }));

        return {
            label: flower,
            data: points,
            backgroundColor: colors[flower]
        };
    });

    // Scatter Chart
    new Chart(
        document.getElementById("flowerChart"),
        {
            type: "scatter",

            data: {
                datasets: datasets
            },

            options: {
                responsive: true,

                plugins: {
                    legend: {
                        labels: {
                            color: "#ffffff"
                        }
                    }
                },

                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Petal Length",
                            color: "#ffffff"
                        },
                        ticks: {
                            color: "#9aa5bd"
                        }
                    },

                    y: {
                        title: {
                            display: true,
                            text: "Petal Width",
                            color: "#ffffff"
                        },
                        ticks: {
                            color: "#9aa5bd"
                        }
                    }
                }
            }
        }
    );

    // Confusion Matrix
    let table = `
        <table>
            <tr>
                <th>Actual / Predicted</th>
                ${data.classes.map(name =>
                    `<th>${name}</th>`
                ).join("")}
            </tr>
    `;

    data.matrix.forEach((row, index) => {

        table += `
            <tr>
                <th>${data.classes[index]}</th>
                ${row.map(value =>
                    `<td>${value}</td>`
                ).join("")}
            </tr>
        `;
    });

    table += "</table>";

    document.getElementById("matrix").innerHTML = table;
}


// Prediction form

document.getElementById("predictionForm")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const resultBox = document.getElementById("result");

        resultBox.innerHTML = "AI internetdə şəkil axtarır... 🔍";

        const formData = new FormData(this);

        const flowerData = Object.fromEntries(
            formData.entries()
        );

        try {

            const response = await fetch("/api/predict", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(flowerData)
            });

            if (!response.ok) {
                throw new Error("Prediction failed");
            }

            const result = await response.json();

            // Şəkil tapılıbsa göstər
            const imageHTML = result.image
                ? `
                    <img
                        src="${result.image.image_url}"
                        alt="${result.flower}"
                        class="flower-image"
                    >

                    <a
                        href="${result.image.source_url}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Image source
                    </a>
                `
                : `
                    <p>Bu gül üçün şəkil tapılmadı.</p>
                `;

            resultBox.innerHTML = `

                <div class="result-card">

                    ${imageHTML}

                    <div class="result-info">

                        <span class="result-label">
                            AI PREDICTION SUCCESSFUL
                        </span>

                        <h2>${result.flower}</h2>

                        <h3>${result.confidence}%</h3>

                        <p>Prediction confidence</p>

                    </div>

                </div>

            `;

        } catch (error) {

            resultBox.innerHTML =
                "Xəta baş verdi. Yenidən yoxla.";

            console.error(error);
        }
    });


// Səhifə açıldıqda dashboard yüklənir
loadDashboard();
