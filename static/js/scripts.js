// Function to get CSRF token from the cookie
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie starts with the desired name
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
};

// Get the CSRF token
const csrftoken = getCookie("csrftoken");

// Function to get example reviews
const getReview = (button) => {
    // Desired sentiment
    sentiment = button.innerText;

    // Send the POST request
    fetch("/review/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ sentiment: sentiment }),
    })
        .then((response) => response.json())
        .then((result) => {
            // Display example review in textarea
            document.getElementById("review-input").innerText =
                result.review;
        });
};

// Function to handle prediction
const getPrediction = () => {
    // Get text from the input box
    const reviewText = document.getElementById("review-input").value;

    // Send the POST request
    fetch("/predict/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ review: reviewText }),
    })
        .then((response) => response.json())
        .then((result) => {
            // Process the prediction result
            setupAttention(
                result.data.token_scores,
                result.data.confidence,
                result.data.sentiment
            );

            // Display sentiment and confidence in the UI
            document.getElementById("sentiment-result").innerText =
                result.data.sentiment;
            document.getElementById("confidence-result").innerText = Number(
                result.data.confidence.toFixed(2)
            );
        });
};

// Function to visualize attention scores
const setupAttention = (scores, confidence, sentiment) => {
    let att_array = [];

    // Extract attention scores
    scores.forEach((item) => {
        att_array.push(item.attention);
    });

    // Remove special tokens (e.g., [CLS], [SEP])
    att_array = att_array.slice(1, -1);

    // Normalize attention scores
    att_array = att_array.map((value) => Math.log(value + 1)); // Add 1 to avoid log(0)
    let att_min = Math.min(...att_array) + 0.000000001;
    let att_max = Math.max(...att_array);
    let normalized_att = att_array.map((value) =>
        Math.round(Math.min((value - att_min) * 255) / (att_max - att_min) + 40)
    );

    // Ensure values are within bounds
    normalized_att = normalized_att.map((value) =>
        Math.max(0, Math.min(value, 100))
    );

    let token_array = [];
    // Extract tokens
    scores.forEach((item) => {
        token_array.push(item.token);
    });

    // Remove special tokens
    token_array = token_array.slice(1, -1);

    let html_text = "";
    let green, red, blue;

    // Generate HTML with color-coded tokens
    for (let i = 0; i < token_array.length; i++) {
        let token = token_array[i];
        if (sentiment === "Positive") {
            green = normalized_att[i];
            red = 0;
            blue = 0;
        } else if (sentiment === "Negative") {
            green = 0;
            blue = 0;
            red = normalized_att[i];
        } else {
            // Neutral sentiment
            green = 0;
            red = 0;
            blue = normalized_att[i];
        }
        html_text += `<span style="background-color: rgb(${red}, ${green}, ${blue});">&nbsp;&nbsp;${token}&nbsp;&nbsp;</span> `;
    }

    // Update attention visualization in the UI
    html_text = `<p>${html_text.trim()}</p>`;
    document.getElementById("attention-result").innerHTML = html_text;
};

// Function to collapse all other accordions when one is opened
function collapseTopPicks() {
    // Attach event listeners to all accordion buttons
    document.querySelectorAll(".accordion-button").forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-bs-target");
            const targetElement = document.querySelector(targetId);

            // Close all other accordions
            document
                .querySelectorAll(".accordion-collapse.show")
                .forEach((openAccordion) => {
                    if (openAccordion !== targetElement) {
                        const collapseInstance =
                            bootstrap.Collapse.getInstance(openAccordion) ||
                            new bootstrap.Collapse(openAccordion, {
                                toggle: false,
                            });
                        collapseInstance.hide(); // Triggers the smooth closing animation
                    }
                });

            // The clicked accordion opens automatically via Bootstrap's default behavior
        });
    });
}
