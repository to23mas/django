import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';
import { addBlocklyFlashMessage } from './flash_messages'

document.addEventListener('DOMContentLoaded', () => {
	const course_db  = (window as any).courseName;
	const blockly_id = (window as any).blocklyId;
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
		const divElement = document.getElementById('blocklyPythonCode');
		if (!divElement) return;
		divElement.innerHTML = '';

		if (pythonCode !== '') {
			const preElement = document.createElement('pre');
			const codeElement = document.createElement('code');
			codeElement.className = 'rounded-lg shadow language-python';
			codeElement.textContent = pythonCode;

			preElement.appendChild(codeElement);
			divElement.appendChild(preElement);
		}
	};
	workspace.addChangeListener(updateCode);

	document.getElementById('validateButton').addEventListener('click', () => {
		const pythonCode = pythonGenerator.workspaceToCode(workspace);
		sendPythonCodeToServer(pythonCode, blockly_id, course_db);
	});
});

async function sendPythonCodeToServer(code: string, blockly_id: string, course_db: string) {
	console.log(course_db);
	const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
	if (!csrfToken) {
		alert('Error csrf-forgery\n');
		return;
	}
	try {
		const response = await fetch('/projects/lesson/validate-python', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				'X-CSRFToken': csrfToken
			},
			body: new URLSearchParams({ code, blockly_id, course_db })
		});
		const result = await response.json();
		if (result.status == 'error') {
			addBlocklyFlashMessage('fudsjakl fjdskal fjdsakl');
			alert('Nesprávná opověď');
		} else {
			alert('SUCCESS')
		}
	} catch (error) {
		alert('Problém na straně serveru. zkuste tuto akci prosím později.');
	}
}
