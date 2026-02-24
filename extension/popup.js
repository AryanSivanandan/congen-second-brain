function capturePage() {
  chrome.tabs.query(
    { active: true, currentWindow: true },
    function(tabs) {
      if (!tabs || !tabs.length) {
        console.error("No active tab found");
        return;
      }

      chrome.tabs.sendMessage(
        tabs[0].id,
        { action: "capture" },
        function(response) {

          if (!response) {
            console.error("No response received");
            return;
          }

          if (!response.success) {
            console.warn("Capture rejected:", response.reason);
            alert("Page does not appear to be a full article.");
            return;
          }

          console.log("Valid capture:", response.data);

          fetch("http://127.0.0.1:8000/capture", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(response.data)
          })
            .then(res => res.json())
            .then(data => {
              console.log("Backend response:", data);
            })
            .catch(err => {
              console.error("Backend error:", err);
            });

        }
      );
    }
  );
}

document
  .getElementById("captureBtn")
  .addEventListener("click", capturePage);