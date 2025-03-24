import { initBlockly } from './blockly';
import { initVisNetwork } from './vis';
import { initCli } from './cli';
import { initTimeout } from './timeout';
import 'flowbite'

// Initialize Blockly
initBlockly();

// Initialize Vis.js Network
initVisNetwork();

// Initialize CLI
initCli();

// Initialize Test Timeout
initTimeout();

