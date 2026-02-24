function extractArticle() {
  const documentClone = document.cloneNode(true);
  const article = new Readability(documentClone).parse();

  if (!article) {
    return { error: "Readability failed to parse article" };
  }

  const cleanText = article.textContent
    .trim()
    .replace(/[ \t]+/g, ' '); // preserve newlines

  const wordCount = cleanText.split(/\s+/).length;

  return {
    url: window.location.href,
    title: article.title,
    byline: article.byline,
    content: cleanText,
    excerpt: article.excerpt,
    length: cleanText.length,
    word_count: wordCount,
    captured_at: new Date().toISOString()
  };
}

function isValidArticle(article) {
  if (!article || article.error) return false;

  // Smarter V1: semantic volume threshold
  if (article.word_count < 300) {
    console.warn("Rejected: Too few words (" + article.word_count + ")");
    return false;
  }

  return true;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "capture") {
    const article = extractArticle();

    if (!isValidArticle(article)) {
      sendResponse({
        success: false,
        reason: "Low quality extraction",
        word_count: article.word_count,
        preview: article.content.slice(0, 200)
      });
      return;
    }

    sendResponse({
      success: true,
      data: article
    });
  }
});

chrome.commands.onCommand.addListener((command) => {
  if (command === "capture-full-page") {
    chrome.tabs.query({ active: true, currentWindow: true })
      .then(([tab]) => {
        chrome.tabs.sendMessage(tab.id, { action: "capture" });
      });
  }
});