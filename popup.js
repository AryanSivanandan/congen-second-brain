async function capturePage() {
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  const response = await chrome.tabs.sendMessage(tab.id, {
    action: "capture"
  });

  console.log("Captured:", response);

  // Later: send to backend
}

document.getElementById("captureBtn")
  .addEventListener("click", capturePage);
