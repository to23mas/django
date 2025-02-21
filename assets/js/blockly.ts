import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';
import { addBlocklyFlashMessage, clearBlocklyFlashMessage } from './flash_messages'

export function initBlockly() {
	document.addEventListener('DOMContentLoaded', () => {

		const blocklyContainer = document.getElementById('blocklyDiv');
		if (!blocklyContainer) { return; }

		// TODO implement
		// Blockly.Python.addReservedWords(
		// 	'eval,exec,open,subprocess,os,shutil,socket,pickle,marshal,ctypes,cffi, import'
		// );

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
				sendPythonCodeToServer(pythonCode);
			});
		}
	});

	async function sendPythonCodeToServer(code: string) {
		const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
		const course_db = (window as any).courseName;
		const blockly_id = (window as any).blocklyId;
		const chapter_id = (window as any).chapterId;
		const lesson_id = (window as any).lessonId;
		const project_id = (window as any).projectId;
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
			const response = await fetch('/lessons/lesson/validate-python', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
					'X-CSRFToken': csrfToken
				},
				body: new URLSearchParams({
					code,
					blockly_id,
					course_db,
					chapter_id,
					lesson_id,
					project_id,
				})
			});
			const result = await response.json();
			if (result.status == 'error') {
				addBlocklyFlashMessage(`${result.message}`);
			} else {
				if (result.redirect) {
					window.location.href = result.url;
				} else {
					addBlocklyFlashMessage('Správně.', true);
				}
			}
		} catch (error) {
			alert('Problém na straně serveru. Zkuste tuto akci prosím později.');
		}
	}
}
