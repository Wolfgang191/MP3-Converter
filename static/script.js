document.getElementById("downloadBtn").addEventListener("click", startDownload);

function startDownload() {
  const status = document.getElementById("status");
  const input = document.getElementById("youtube_link").value.trim();

  // Check if input is empty
  if (!input) {
    status.style.display = "block";
    status.style.color = "red"; // show in red for errors
    status.textContent = "Please enter a valid YouTube link!";
    return; // stop further execution
  }

  // Optional: basic validation for YouTube URL
  const ytPattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\//;
  if (!ytPattern.test(input)) {
    status.style.display = "block";
    status.style.color = "red";
    status.textContent = "This doesn’t look like a YouTube link!";
    return;
  }

  // If valid, start downloading animation
  status.style.display = "block";
  status.style.color = "white"; // downloading color

  const states = ["Downloading", "Downloading.", "Downloading..", "Downloading...", "Downloading..", "Downloading."];

  let i = 0;

  const interval = setInterval(() => {
    status.textContent = states[i];
    i = (i + 1) % states.length;
  }, 400);

  setTimeout(() => {
    clearInterval(interval);
    status.textContent = "Download complete!";
    status.style.color = "lime"; // finished color
  }, 4000);
}
