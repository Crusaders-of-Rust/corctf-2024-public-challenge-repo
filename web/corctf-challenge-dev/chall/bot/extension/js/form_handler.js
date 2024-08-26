const origin = window.location.origin;

const base_rule = {
	"action": {
		"type": "block",
		"redirect": {},
		"responseHeaders": [],
		"requestHeaders": []
	},
	"condition": {
		"initiatorDomains": [origin],
		"resourceTypes": ['image', 'media', 'script']
	}
};

function serializeForm(items) {
    const result = {};
    items.forEach(([key, value]) => {
        const keys = key.split('.');
        let current = result;
		for (let i = 0; i < keys.length - 1; i++) {
            const k = keys[i];
            if (!(k in current)) {
                current[k] = {};
            }
            current = current[k];
        }
        current[keys[keys.length - 1]] = isNaN(value) ? value : Number(value);
    });

    return result;
}

// inject modal
const modal = document.createElement('div');
modal.id = 'block-modal';
modal.classList.add('modal');

modal.innerHTML = `<div class="modal-content">
					<span class="close">&times;</span>
					<form id='block-options'>
						<fieldset>
							<legend>Block URL</legend>
							<label for='priority'>Priority:</label>
							<input type='text' id='priority' name='priority'>
							<div id='condition'>
								<label for='urlFilter'>Blocked URL:</label>
								<input type='text' id='urlFilter' name='condition.urlFilter'><br>
							</div>
							<button type='button' id='submit-btn' class='fizzblock'>Add URL!</button>
						</fieldset>
					</form>
				  </div>`;

modal.querySelector('#submit-btn').addEventListener('click', async () => {
	const obj = serializeForm(Array.from(new FormData(document.getElementById('block-options'))));
	const merged_obj = _.merge(base_rule, obj);

	chrome.storage.local.get(origin).then((data) => {
		let arr = data[origin];
		if (arr == null) {
			arr = [];
		}
		arr.push(merged_obj);
		console.log(merged_obj);
		chrome.storage.local.set(Object.fromEntries([[origin, arr]]));
	});
});

// listeners to close modal
modal.querySelector('.close').addEventListener('click', () => {modal.style.display = 'none';});
window.addEventListener('click', (event) => {
	if (event.target == modal) {
		modal.style.display = 'none';
	}
});

document.body.insertBefore(modal, document.body.childNodes[0]);

// inject modal trigger button
const modal_button = document.createElement('button');
modal_button.type = 'button';
modal_button.id = 'modal-button';
modal_button.classList.add('fizzblock');
modal_button.textContent = "Open block settings";

// modal listener
modal_button.addEventListener('click', async () => {
	const modal = document.getElementById('block-modal');
	modal.style.display = 'block';
});

document.body.insertBefore(modal_button, document.body.childNodes[0]);