interface TimeoutConfig {
	startTime: number;
	duration: number;  
	onTimeout: () => void;
}

interface TestTimeData {
	endTime: number;
	testId: number;
	courseId: string;
}

export function initTimeout() {
	document.addEventListener('DOMContentLoaded', () => {
		window.onunload = () => {};

		const testStartTime = (window as any).testStartTime;
		const testDuration = (window as any).testDuration;
		const testId = (window as any).testId;
		const courseId = (window as any).courseId;

		if (testStartTime && testDuration && window.location.pathname.includes('/tests/')) {
			const endTime = testStartTime + (testDuration * 60 * 1000);
			localStorage.setItem('testTimeData', JSON.stringify({
				endTime,
				testId,
				courseId
			}));
		}

		const testTimeData = getTestTimeData();
		if (!testTimeData) return;

		if (window.location.pathname.startsWith('/users/') || window.location.pathname.startsWith('/admin/')) {
			return;
		}

		const timerElement = createTimerElement(testTimeData);

		startTimer({
			endTime: testTimeData.endTime,
			timerElement,
			onTimeout: () => {
				window.location.href = `/tests/force-fail/${testTimeData.courseId}/${testTimeData.testId}/`;
			}
		});
	});
}

function getTestTimeData(): TestTimeData | null {
	const data = localStorage.getItem('testTimeData');
	if (!data) return null;

	const testTimeData = JSON.parse(data) as TestTimeData;

	if (Date.now() > testTimeData.endTime) {
		localStorage.removeItem('testTimeData');
		window.location.href = `/tests/force-fail/${testTimeData.courseId}/${testTimeData.testId}/`;
		return null;
	}

	return testTimeData;
}

function createTimerElement(testTimeData: TestTimeData): HTMLDivElement {
	const timer = document.createElement('div');
	timer.className = 'fixed left-1/2 top-4 transform -translate-x-1/2 bg-red-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 font-bold';
	
	const isOnTestPage = window.location.pathname.includes(`/tests/detail/c-${testTimeData.courseId}/tests-${testTimeData.testId}`);
	
	if (!isOnTestPage) {
		const link = document.createElement('a');
		const testUrl = `/tests/detail/c-${testTimeData.courseId}/tests-${testTimeData.testId}/`;
		link.href = testUrl;
		link.className = 'text-white hover:text-gray-200 underline';
		link.textContent = 'Přejít na test';
		timer.appendChild(link);
		timer.appendChild(document.createTextNode(' | '));
	}
	
	document.body.appendChild(timer);
	return timer;
}

function startTimer({
	endTime,
	timerElement,
	onTimeout
}: {
	endTime: number,
	timerElement: HTMLDivElement,
	onTimeout: () => void
}) {
	const interval = window.setInterval(() => {
		const now = Date.now();
		const timeLeft = endTime - now;

		if (timeLeft <= 0) {
			clearInterval(interval);
			localStorage.removeItem('testTimeData');
			timerElement.textContent = 'Čas vypršel - test selhal';
			onTimeout();
			return;
		}

		const minutes = Math.floor(timeLeft / (1000 * 60));
		const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

		const timeText = ` ${minutes}:${seconds.toString().padStart(2, '0')}`;
		
		if (timerElement.children.length > 0) {
			timerElement.lastChild!.textContent = timeText;
		} else {
			timerElement.textContent = timeText;
		}

		if (timeLeft < 60000) {
			timerElement.classList.add('animate-pulse');
		}
	}, 1000);

	const form = document.getElementById('test-form');
	if (form) {
		form.addEventListener('submit', () => {
			clearInterval(interval);
			localStorage.removeItem('testTimeData');
			if (timerElement) {
				timerElement.remove();
			}
		});
	}

	return () => clearInterval(interval);
}
