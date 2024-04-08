module.exports = {
    content: [
        "./src/**/*.{html,js}",
        "./src/templates/**/*.{html,js}",
        "./assets/styles/*.css",
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
