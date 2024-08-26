chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
	if (changeInfo.status == 'loading' && tab.url.indexOf(tab.index > -1)) {
		const origin = (new URL(tab.url)).origin;
		registerRules(origin);
	}
});

const registerRules = (url) => {
	chrome.storage.local.get(url).then((data) => {
		const arr = data[url];
		if (arr != null) {
			for (let i = 0; i < arr.length; i++) {
				const rule = arr[i];
				rule['id'] = i+1;
				chrome.declarativeNetRequest.updateDynamicRules({
					addRules: [
						rule
					],
					removeRuleIds: [i+1]
				});
			}
		}
	});
};

// rules for corctf-challenge-dev.be.ax
const rules = [
{
	"action": { // fizzbuzz hates microsoft!
		"type": "block",
		"redirect": {},
		"responseHeaders": [],
		"requestHeaders": []
	},
	"condition": {
		"initiatorDomains": ["corctf-challenge-dev.be.ax"],
		"resourceTypes": ['image', 'media', 'script'],
		"urlFilter": "https://microsoft.com*"
	}
},
{
	"action": { // block subdomains too
		"type": "block",
		"redirect": {},
		"responseHeaders": [],
		"requestHeaders": []
	},
	"condition": {
		"initiatorDomains": ["corctf-challenge-dev.be.ax"],
		"resourceTypes": ['image', 'media', 'script'],
		"urlFilter": "https://*.microsoft.com*"
	}
},
{
	"action": { // fizzbuzz hates systemd!
		"type": "block",
		"redirect": {},
		"responseHeaders": [],
		"requestHeaders": []
	},
	"condition": {
		"initiatorDomains": ["corctf-challenge-dev.be.ax"],
		"resourceTypes": ['image', 'media', 'script'],
		"urlFilter": "https://systemd.io*"
	}
}
];

chrome.storage.local.set({"https://corctf-challenge-dev.be.ax": rules});