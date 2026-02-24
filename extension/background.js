chrome.commands.onCommand.addListener(function(command) {
  if (command === "capture-full-page") {

    chrome.tabs.query(
      { active: true, currentWindow: true },
      function(tabs) {
        if (!tabs || !tabs.length) return;

        chrome.tabs.sendMessage(
          tabs[0].id,
          { action: "capture" },
          function(response) {
            console.log("Shortcut capture response:", response);
          }
        );
      }
    );

  }
});