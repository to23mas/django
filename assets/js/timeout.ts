interface TimeoutConfig {
	startTime: number;
	duration: number;  // in minutes
	onTimeout: () => void;
}

interface TestTimeData {
	endTime: number;
	testId: number;
	courseId: string;
}

export function initTimeout() {
	// Force reload on back/forward navigation
	window.addEventListener('pageshow', (event) => {
		if (event.persisted) {
			window.location.reload();
		}
	});

	document.addEventListener('DOMContentLoaded', () => {
		// Prevent caching
		window.onunload = () => {};

		// If we're on the test page, store the test time
		const testStartTime = (window as any).testStartTime;
		const testDuration = (window as any).testDuration;
		const testId = (window as any).testId;
		const courseId = (window as any).courseId;

		if (testStartTime && testDuration) {
			const endTime = testStartTime + (testDuration * 60 * 1000);
			// Store test time data
			localStorage.setItem('testTimeData', JSON.stringify({
				endTime,
				testId,
				courseId
			}));
		}

		// Check if there's an active test
		const testTimeData = getTestTimeData();
		if (!testTimeData) return;

		const timerElement = createTimerElement();

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

	// Clear data if test has expired
	if (Date.now() > testTimeData.endTime) {
		localStorage.removeItem('testTimeData');
		return null;
	}

	return testTimeData;
}

function createTimerElement(): HTMLDivElement {
	console.log('createTimerElement');
	const timer = document.createElement('div');
	timer.className = 'fixed left-1/2 top-4 transform -translate-x-1/2 bg-red-600 text-white px-4 py-2 rounded-lg shadow-lg z-50 font-bold';
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
	console.log('startTimer');
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

		timerElement.textContent = `Zbývající čas: ${minutes}:${seconds.toString().padStart(2, '0')}`;

		// Add warning class when less than 1 minute remains
		if (timeLeft < 60000) {
			timerElement.classList.add('animate-pulse');
		}
	}, 1000);

	// Add form submit listener to clear timer
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

// Add this function to handle navigation
function handleNavigation() {
	window.addEventListener('popstate', () => {
		window.location.reload();
	});

	// Disable browser's back/forward cache
	if (window.history && window.history.pushState) {
		window.addEventListener('load', () => {
			window.history.pushState('forward', null, window.location.href);
		}, false);

		window.addEventListener('popstate', () => {
			window.history.pushState('forward', null, window.location.href);
			window.location.reload();
		});
	}
}
