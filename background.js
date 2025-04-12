/*! InstantDataScraperNext - 2025-01-29 */

// Store extension state
let extensionState = {
  activeTabId: null,
  parentWindowId: null,
  connections: new Set()
};

// Handle extension icon click
chrome.action.onClicked.addListener(function(tab) {
  extensionState.activeTabId = tab.id;
  chrome.windows.getCurrent(function(window) {
    extensionState.parentWindowId = window.id;
    chrome.windows.create({
      url: chrome.runtime.getURL(`popup.html?tabid=${encodeURIComponent(tab.id)}&url=${encodeURIComponent(tab.url)}`),
      type: "popup",
      width: 720,
      height: 650
    });
  });
});

// Handle connection errors
chrome.runtime.onConnect.addListener(function(port) {
  extensionState.connections.add(port);
  port.onDisconnect.addListener(function() {
    extensionState.connections.delete(port);
  });
});

// Set up message listener
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Handle messages from popup or content scripts
  if (message.type) {
    switch (message.type) {
      case 'getTabInfo':
        sendResponse({ 
          success: true, 
          tabId: extensionState.activeTabId,
          parentWindowId: extensionState.parentWindowId 
        });
        break;
      case 'findTables':
        // Forward the message to the content script
        if (extensionState.activeTabId) {
          chrome.tabs.sendMessage(extensionState.activeTabId, message, response => {
            if (chrome.runtime.lastError) {
              sendResponse({ error: chrome.runtime.lastError.message });
            } else {
              sendResponse(response);
            }
          });
        } else {
          sendResponse({ error: 'No active tab' });
        }
        break;
      case 'getTableData':
        // Forward the message to the content script
        if (extensionState.activeTabId) {
          chrome.tabs.sendMessage(extensionState.activeTabId, message, response => {
            if (chrome.runtime.lastError) {
              sendResponse({ error: chrome.runtime.lastError.message });
            } else {
              sendResponse(response);
            }
          });
        } else {
          sendResponse({ error: 'No active tab' });
        }
        break;
      default:
        sendResponse({ success: false, error: 'Unknown message type' });
    }
  }
  // Return true to indicate we'll respond asynchronously
  return true;
});