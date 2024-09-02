import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
	base: "src/public",
	resolve: {
		alias: {
			'@': resolve(__dirname, 'assets/js'),
			'~': resolve(__dirname, 'node_modules'),
		},
	},
	build: {
		manifest: true,
		minify: 'esbuild',
		outDir: resolve("src/public/dist"),
		rollupOptions: {
			output: {
				entryFileNames: '[name].js',
				assetFileNames: '[name].css',
			},
			input: {
				app: './assets/js/app.ts',
			}
		}
	}
})
