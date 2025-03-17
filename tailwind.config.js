/** @type {import('tailwindcss').Config} */
export default {
	content: [
		"./app/**/templates/**/*.html",
	],
	theme: {
		extend: {},
	},
	safelist: [
		'habit_tracker_input_field',
		'errorlist',
	],
	plugins: [],
};
