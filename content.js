function extractArticle() {
  const documentClone = document.cloneNode(true);
  const article = new Readability(documentClone).parse();

  if (!article) {
    return {
      error: "Unable to parse article"
    };
  }

  return {
    url: window.location.href,
    title: article.title,
    byline: article.byline,
    content: article.textContent,
    excerpt: article.excerpt,
    length: article.length,
    captured_at: new Date().toISOString()
  };
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "capture") {
    const data = extractArticle();
    sendResponse(data);
  }
});
