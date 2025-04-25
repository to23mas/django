import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';
import { addBlocklyFlashMessage, clearBlocklyFlashMessage } from './flash_messages'
// import { toolbox } from './blockly/toolbox';

// Import all blocks
import './blockly/blocks';

const BLOCKLY_LOCALE_CS = {
	UNDO: 'Zpět',
	REDO: 'Znovu',
	DELETE_BLOCK: 'Smazat blok',
	DELETE_X_BLOCKS: 'Smazat %1 bloků',
	DELETE_ALL_BLOCKS: 'Smazat všechny bloky?',
	CLEAN_UP: 'Uspořádat bloky',
	DUPLICATE_BLOCK: 'Duplikovat',
	REMOVE_COMMENT: 'Odstranit komentář',
	ADD_COMMENT: 'Přidat komentář',
	EXTERNAL_INPUTS: 'Externí vstupy',
	INLINE_INPUTS: 'Vložené vstupy',
	COLLAPSE_BLOCK: 'Sbalit blok',
	EXPAND_BLOCK: 'Rozbalit blok',
	DISABLE_BLOCK: 'Zakázat blok',
	ENABLE_BLOCK: 'Povolit blok',
	HELP: 'Nápověda',
	COLLAPSE_ALL: 'Sbalit bloky',
	EXPAND_ALL: 'Rozbalit bloky',
	DELETE_VARIABLE_CONFIRMATION: 'Smazat %1 použití proměnné "%2"?',
	RENAME_VARIABLE: 'Přejmenovat proměnnou...',
	NEW_VARIABLE: 'Vytvořit proměnnou...',
	NEW_STRING_VARIABLE: 'Vytvořit textovou proměnnou...',
	NEW_NUMBER_VARIABLE: 'Vytvořit číselnou proměnnou...',
	NEW_COLOUR_VARIABLE: 'Vytvořit barevnou proměnnou...',
	NEW_VARIABLE_TYPE_TITLE: 'Nový typ proměnné:',
	NEW_VARIABLE_TITLE: 'Nové jméno proměnné:',
	VARIABLE_ALREADY_EXISTS: 'Proměnná se jménem "%1" již existuje.',
	VARIABLE_ALREADY_EXISTS_FOR_ANOTHER_TYPE: 'Proměnná se jménem "%1" již existuje pro jiný typ: "%2".',
	DELETE_VARIABLE: 'Smazat proměnnou "%1"',
};

export function initBlockly() {
	document.addEventListener('DOMContentLoaded', () => {

		const blocklyContainer = document.getElementById('blocklyDiv');
		if (!blocklyContainer) { return; }

		Blockly.setLocale(BLOCKLY_LOCALE_CS);

		const workspace = Blockly.inject('blocklyDiv', {
			toolbox: (window as any).blocklyToolboxConfig,
			// toolbox: toolbox,
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
			const pythonCode = pythonGenerator.workspaceToCode(workspace)
				.replace(/# Describe this function...\n/g, '');  // Remove the comments
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

		const validateButton = document.getElementById('validateButton');
		if (validateButton) {
			const defaultText = validateButton.querySelector('.default-text');
			const spinner = validateButton.querySelector('.spinner');
			if (defaultText && spinner) {
				defaultText.classList.add('hidden');
				spinner.classList.remove('hidden');
			}
		}

		try {
			const response = await fetch('/projects/lesson/validate-python', {
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
					const nextButtonContainer = document.getElementById('nextButtonContainer');
					if (nextButtonContainer) {
						const anchor = document.createElement('a');
						anchor.href = result.url;
						anchor.className = 'green_button';
						anchor.textContent = 'Další Kapitola';
						nextButtonContainer.innerHTML = '';
						nextButtonContainer.appendChild(anchor);
					}
					addBlocklyFlashMessage('Správně.', true);
				} else {
					addBlocklyFlashMessage('Správně.', true);
				}
			}
		} catch (e) {
			alert('Problém na straně serveru. Zkuste tuto akci prosím později.');
		} finally {
			const validateButton = document.getElementById('validateButton');
			if (validateButton) {
				const defaultText = validateButton.querySelector('.default-text');
				const spinner = validateButton.querySelector('.spinner');
				if (defaultText && spinner) {
					defaultText.classList.remove('hidden');
					spinner.classList.add('hidden');
				}
			}
		}
	}
}
