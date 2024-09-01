module.exports = {
	content: [
		"./src/**/*.{html,js}",
		"./src/templates/**/*.{html,js}",
		"./src/templates/*.{html,js}",
		"./assets/styles/*.css",
		"./node_modules/flowbite/**/*.js"
	],
	theme: {
		extend: {
			colors: {
				codeColor: '#282c34',
			},
		},
	},
	plugins: [
		require('flowbite/plugin'),
	],
}
