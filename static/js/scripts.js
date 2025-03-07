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

// Pre-Loader Script
document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("header-image");
    const preloader = document.getElementById("preloader");
    const content = document.getElementById("content");
    // Ensure background image is also loaded
    const bgImage = new Image();
    bgImage.src = "/static/images/purple_background.png";

    let videoLoaded = false;
    let bgLoaded = false;

    function checkLoaded() {
        if (videoLoaded && bgLoaded) {
            preloader.style.display = "none";
            content.style.display = "block";
        }
    }
    // Check if video is cached and already loaded
    if (video.readyState >= 4) {
        videoLoaded = true;
    } else {
        video.oncanplaythrough = function () {
            videoLoaded = true;
            checkLoaded();
        };
    }
    // Check if background image is cached and already loaded
    if (bgImage.complete) {
        bgLoaded = true;
    } else {
        bgImage.onload = function () {
            bgLoaded = true;
            checkLoaded();
        };
    }
    checkLoaded(); // Ensure check is done on load
});

// Function to get example reviews
const getReview = (button) => {
    // Desired sentiment
    sentiment = button.innerText;
    document.getElementById("review-input").innerText =
        "🤖 Generating review...";
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
            document.getElementById("review-input").innerText = result.review;
        });
};

// Function to handle prediction
const getPrediction = () => {
    // Get text from the input box
    const reviewText = document.getElementById("review-input").value;
    const predictionSpinner = `<div id="prediction-spinner">
  <div class="spinner-grow" style="color: #6b52a7; width: 1.7em; height: 1.7em;" role="status">
    <span class="visually-hidden">Loading...</span>
  </div>
</div>`;
    document.getElementById("attention-result").innerHTML = predictionSpinner;

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
            green = normalized_att[i] - 18;
            red = normalized_att[i];
            blue = 0;
        }
        html_text += `<span style="background-color: rgb(${red}, ${green}, ${blue});">&nbsp;&nbsp;${token}&nbsp;&nbsp;</span> `;
    }

    // Update attention visualization in UI
    html_text = `<p>${html_text.trim()}</p>`;
    document.getElementById("attention-result").innerHTML = html_text;

    // Show confidence level in UI
    document.getElementById(
        "confidence"
    ).innerHTML = `Confidence Level: ${confidence.toFixed(2)}%`;
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

// Function to get top games summarization
const getSummarization = (i) => {
    // Send the POST request
    fetch("/summarization/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ topic: i }),
    })
        .then((response) => response.json())
        .then((result) => {
            const topic = i + 1;
            document.querySelector(`#summ-pro-${topic}`).innerHTML =
                result.summarization[0];
            document.querySelector(`#summ-contra-${topic}`).innerHTML =
                result.summarization[1];
        });
};
