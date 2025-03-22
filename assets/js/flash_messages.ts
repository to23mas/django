export function addBlocklyFlashMessage(message: string, isSuccess: boolean = false) {
	const flashContainer = document.getElementById('blockly-flash-messages');
	if (!flashContainer) return;

	// Clear existing messages
	clearBlocklyFlashMessage();

	// Create message element
	const messageDiv = document.createElement('div');
	messageDiv.className = `flex items-center justify-between p-4 mb-4 rounded-lg ${
		isSuccess ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
	}`;

	// Message text
	const textSpan = document.createElement('span');
	textSpan.textContent = message;
	messageDiv.appendChild(textSpan);

	// Close button
	const closeButton = document.createElement('button');
	closeButton.className = 'ml-4 text-sm font-semibold focus:outline-none';
	closeButton.innerHTML = '❌';
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
