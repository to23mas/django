export function addBlocklyFlashMessage(message: string, isSuccess: boolean = false) {
	const flashContainer = document.getElementById('blockly-flash-messages');
	if (!flashContainer) return;

	clearBlocklyFlashMessage();

	const messageDiv = document.createElement('div');
	messageDiv.className = `flex items-center p-4 mb-4 rounded-lg ${
		isSuccess ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
	}`;

	const iconSvg = document.createElement('svg');
	iconSvg.className = 'flex-shrink-0 w-4 h-4';
	iconSvg.setAttribute('aria-hidden', 'true');
	iconSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
	iconSvg.setAttribute('fill', 'currentColor');
	iconSvg.setAttribute('viewBox', '0 0 20 20');
	
	if (isSuccess) {
		iconSvg.innerHTML = '<path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>';
	} else {
		iconSvg.innerHTML = '<path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>';
	}
	messageDiv.appendChild(iconSvg);

	const textSpan = document.createElement('span');
	textSpan.className = 'ml-3 flex-grow';
	textSpan.textContent = message;
	messageDiv.appendChild(textSpan);

	const closeButton = document.createElement('button');
	closeButton.className = 'ml-4 text-sm font-semibold focus:outline-none';
	closeButton.innerHTML = `
		<svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
			<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
		</svg>
	`;
	closeButton.onclick = () => {
		messageDiv.remove();
	};
	messageDiv.appendChild(closeButton);

	flashContainer.appendChild(messageDiv);
}

export function clearBlocklyFlashMessage() {
	const flashContainer = document.getElementById('blockly-flash-messages');
	if (flashContainer) {
		flashContainer.innerHTML = '';
	}
}
