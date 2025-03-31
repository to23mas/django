
import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

const ORDER_ATOMIC = 0;

// Register the block
Blockly.Blocks['django_include_block'] = {
    init: function() {
        this.appendValueInput('urls')
            .setCheck('String')
            .appendField('include');
        this.setOutput(true, 'Function');  // This block returns a value
        this.setColour(230);  // Set a valid color value
        this.setTooltip('Include URL patterns from another module');
        this.setHelpUrl('');
    }
};

// Register the generator
pythonGenerator.forBlock['django_include_block'] = function(block, generator) {
    const urls = generator.valueToCode(block, 'urls', ORDER_ATOMIC) || '""';
    return [`include(${urls})`, ORDER_ATOMIC];
};