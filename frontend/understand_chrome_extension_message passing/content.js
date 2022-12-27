// declare message listener from background or popup script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Demo] ==============================================');
  console.log('[Demo] receive', request);
  sendResponse({response: '[Demo] pone-pone from content script'});
});

// send msg: content script ->  background
async function sendMsgToBackground() {
  console.log('[Demo] ==============================================');
  console.log('[Demo] Test send message from content script to background');
  const ret = await chrome.runtime.sendMessage({msg: '[Demo] ping from content script'});
  console.log('[Demo] receive', ret);
}

// ===================================================================================

// declare message listener from inject script
window.addEventListener('message', (event) => {
  if (event.source === window && event.data.from === 'inject-script') {
    console.log('[Demo] receive', event.data);

    sendMsgToInjectScript();
  }
});

// send msg:  content script -> inject script
async function sendMsgToInjectScript() {
  console.log('[Demo] ==============================================');
  console.log('[Demo] Test send message from content script to inject script');
  window.postMessage({msg: 'ping from content script', from: 'content-script'});
}

// ===================================================================================

function injectScriptToPage() {
  const idTag = document.createElement('div');
  idTag.setAttribute('id', 'msg-passing-test');
  idTag.setAttribute('data', chrome.runtime.id);
  document.body.appendChild(idTag);

  const script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = chrome.runtime.getURL('inject-script.js');
  document.head.appendChild(script);
}


sendMsgToBackground();
injectScriptToPage();

