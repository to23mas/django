import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

const ORDER_ATOMIC = 0;

Blockly.Blocks['django_path_block'] = {
    init: function() {
        this.appendValueInput('route')
            .setCheck('String')
            .appendField('path');
        this.appendValueInput('view')
            .setCheck('Function')
            .appendField('view');
        this.setOutput(true, 'Function');
        this.setColour(230);
        this.setTooltip('Define a URL pattern with path');
        this.setHelpUrl('');
    }
};

pythonGenerator.forBlock['django_path_block'] = function(block, generator) {
    const route = generator.valueToCode(block, 'route', ORDER_ATOMIC) || '""';
    const view = generator.valueToCode(block, 'view', ORDER_ATOMIC) || '""';
    return [`path(${route}, ${view})`, ORDER_ATOMIC];
}; 