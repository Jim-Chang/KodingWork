async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
  return tab;
}

// ===================================================================================

document.getElementById('send-bg-btn').addEventListener('click', sendMsgToBackground);

// send msg: popup script -> background
async function sendMsgToBackground() {
  console.log('[Demo] ==============================================');
  console.log('[Demo] Test send message from popup script to background');
  const ret = await chrome.runtime.sendMessage({msg: 'ping from popup script'});
  console.log('[Demo] receive', ret);
}

// ===================================================================================

document.getElementById('send-content-btn').addEventListener('click', sendMsgToContentScript);

// send msg: popup script -> content script
async function sendMsgToContentScript() {
  console.log('[Demo] ==============================================');
  console.log('[Demo] Test send message from popup script to content script');
  const tab = await getActiveTab();
  const ret = await chrome.tabs.sendMessage(tab.id, {msg: 'ping from popup script'});
  console.log('[Demo] receive', ret);
}
