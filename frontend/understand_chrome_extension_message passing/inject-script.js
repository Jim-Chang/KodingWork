function getExtensionId() {
  return document.getElementById('msg-passing-test').getAttribute('data');
}

// prepare btn for test send message to background
const btnBg = document.createElement('button');
btnBg.style.position = 'fixed';
btnBg.style.top = '0';
btnBg.style.left = '0';
btnBg.innerText = 'send msg to background';
btnBg.addEventListener('click', sendMsgToBackgroundScript);
document.body.appendChild(btnBg);

// send msg: inject script -> background
async function sendMsgToBackgroundScript() {
  console.log('[Demo] ==============================================');
  console.log('[Demo] Test send message from inject script to background');
  const extensionId = getExtensionId();
  // 於 inject script 使用 chrome message api 時
  // 需注意這邊還沒有 promise 的寫法
  chrome.runtime.sendMessage(extensionId, {msg: 'ping from inject script'}, (ret) => {
    console.log('[Demo] receive', ret);
  });
}

// prepare btn for test send message to content script
const btnCt = document.createElement('button');
btnCt.style.position = 'fixed';
btnCt.style.top = '50px';
btnCt.style.left = '0';
btnCt.innerText = 'send msg to content script';
btnCt.addEventListener('click', sendMsgToContentScript);
document.body.appendChild(btnCt);

// ===================================================================================

// send msg: inject script -> content script
async function sendMsgToContentScript() {
  console.log('[Demo] ==============================================');
  console.log('[Demo] Test send message from inject script to content script');
  window.postMessage({msg: 'ping from inject script', from: 'inject-script'});
}

// declare message listener from content script
window.addEventListener('message', (event) => {
  if (event.source === window && event.data.from === 'content-script') {
    console.log('[Demo] receive', event.data);
  }
});


