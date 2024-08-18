import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

import 'blockly/python';

document.addEventListener('DOMContentLoaded', () => {
	const workspace = Blockly.inject('blocklyDiv', {
		toolbox: (window as any).blocklyToolboxConfig,
		grid: { spacing: 20, length: 2, snap: true },
		trashcan: true,
		move: { scrollbars: { horizontal: true, vertical: true } },
		zoom: { controls: true, startScale: 1.0, maxScale: 3, minScale: 0.3, scaleSpeed: 1.2, pinch: true },
	});

	const supportedEvents = new Set([
		Blockly.Events.BLOCK_CHANGE,
		Blockly.Events.BLOCK_CREATE,
		Blockly.Events.BLOCK_DELETE,
		Blockly.Events.BLOCK_MOVE,
	]);

	const updateCode = (event: Blockly.Events.Abstract) => {
		if (workspace.isDragging() || !supportedEvents.has(event.type)) return;

		const pythonCode = pythonGenerator.workspaceToCode(workspace);
		const preElement = document.getElementById('blocklyPythonCode');
		if (!preElement) return;
		preElement.innerHTML = '';

		if (pythonCode !== '') {
			const codeElement = document.createElement('code');
			codeElement.className = 'rounded-lg shadow language-python';
			codeElement.setAttribute('data-highlighted', 'yes');
			codeElement.textContent = pythonCode;

			preElement.appendChild(codeElement);
		}
	};

	workspace.addChangeListener(updateCode);
});
