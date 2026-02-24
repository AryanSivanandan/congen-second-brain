chrome.commands.onCommand.addListener(function (command) {
  if (command === "capture-full-page") {

    chrome.tabs.query(
      { active: true, currentWindow: true },
      function (tabs) {

        if (!tabs || !tabs.length) return;

        chrome.tabs.sendMessage(
          tabs[0].id,
          { action: "capture" },
          function (response) {

            if (!response) {
              console.error("No response from content script");
              return;
            }

            if (!response.success) {
              console.warn("Capture rejected:", response.reason);
              return;
            }

            console.log("Captured article:", response.data);

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
});