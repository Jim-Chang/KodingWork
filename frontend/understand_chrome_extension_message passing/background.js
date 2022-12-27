async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  return tab;
}

// ===================================================================================

// declare message listener from content script or popup script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (sender.tab) {
    console.log(`[Demo] receive from content script ${sender.tab.url}`, request);
    sendResponse({response: "pong from background"});
    sendMsgToContentScript();

  } else {
    console.log('[Demo] receive from popup script', request);
    sendResponse({response: "pong from background"});
  }
});

// send msg: background -> content script
async function sendMsgToContentScript() {
  console.log('[Demo] ==============================================');
  console.log('[Demo] Test send message from background to content script');
  const tab = await getActiveTab();
  const ret = await chrome.tabs.sendMessage(tab.id, {msg: 'ping-ping from background'});
  console.log('[Demo] receive', ret);
}

// ===================================================================================

// declare message listener from other extension or inject script
chrome.runtime.onMessageExternal.addListener((request, sender, sendResponse) => {
  console.log('[Demo] receive from other extension or inject script', request);
  sendResponse({response: "pong from background"});
});
