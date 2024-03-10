/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors');
module.exports = {
    content: [
        "./src/**/*.{html,js}",
        "./assets/**/*.css",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {},
    plugins: [
        require('flowbite/plugin'),
    ],
}

    // theme: {
    //     colors: {
    //         ...colors,
    //         ...{
    //             main:colors.sky,
    //             secondary: colors.black,
    //         }
    //     },
    //     extend: {},
    // },
