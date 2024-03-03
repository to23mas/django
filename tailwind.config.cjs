/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');
module.exports = {
	content: [
		"./src/**/*.{html,js}",
		"./assets/**/*.css"
	],
	theme: {
		colors: {
			...colors,
			...{
				main:colors.sky,
				secondary: colors.black,
			}
		},
		extend: {},
	},
	plugins: [],
}

