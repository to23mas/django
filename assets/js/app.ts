import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';
import { addBlocklyFlashMessage, clearBlocklyFlashMessage } from './flash_messages'

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
		Blockly.Events.CLICK,
	]);

	const updateCode = (event: Blockly.Events.Abstract) => {
		if (workspace.isDragging() || !supportedEvents.has(event.type)) return;

		clearBlocklyFlashMessage();
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

	const sendCodeButton = document.getElementById('validateButton');
	if (sendCodeButton) {
		sendCodeButton.addEventListener('click', () => {
			const pythonCode = pythonGenerator.workspaceToCode(workspace);
			sendPythonCodeToServer(pythonCode, blockly_id, course_db);
		});
	}
});

async function sendPythonCodeToServer(code: string, blockly_id: string, course_db: string) {
	const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
	if (!csrfTokenElement) {
		alert('Error csrf-forgery\n');
		return;
	}
	const csrfToken = csrfTokenElement.getAttribute('content');
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
			addBlocklyFlashMessage('Nesprávná odpověď.');
		} else {
			addBlocklyFlashMessage('Správně.', true);

			const chapterFinished = (window as any).chapterFinished;
			console.log('chapter finished: ', chapterFinished);
			if (chapterFinished === "False") {
				const chapter_id = (window as any).chapterId;
				const lesson_id = (window as any).lessonId;
				const project_id = (window as any).projectId;
				const course = (window as any).courseName;
				const response = await fetch('/projects/lesson/unlock-chapter', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/x-www-form-urlencoded',
						'X-CSRFToken': csrfToken
					},
					body: new URLSearchParams({ chapter_id, lesson_id, project_id, course })
				});

				if (response.redirected) {
					window.location.href = response.url;
				}
			}
		}
	} catch (error) {
		alert('Problém na straně serveru. zkuste tuto akci prosím později.');
	}
}
