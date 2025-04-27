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

pythonGenerator.forBlock['django_path_block'] = function(block) {
    const route = pythonGenerator.valueToCode(block, 'route', ORDER_ATOMIC) || '""';
    const view = pythonGenerator.valueToCode(block, 'view', ORDER_ATOMIC) || '""';
    return [`path(${route}, ${view})`, ORDER_ATOMIC];
};

Blockly.Blocks['django_path_named_block'] = {
    init: function() {
        this.appendValueInput('route')
            .setCheck('String')
            .appendField('path');
        this.appendValueInput('view')
            .setCheck('Function')
            .appendField('view');
        this.appendValueInput('name')
            .setCheck('String')
            .appendField('name');
        this.setOutput(true, 'Function');
        this.setColour(230);
        this.setTooltip('Define a URL pattern with path and name');
        this.setHelpUrl('');
    }
};

pythonGenerator.forBlock['django_path_named_block'] = function(block) {
    const route = pythonGenerator.valueToCode(block, 'route', ORDER_ATOMIC) || '""';
    const view = pythonGenerator.valueToCode(block, 'view', ORDER_ATOMIC) || '""';
    const name = pythonGenerator.valueToCode(block, 'name', ORDER_ATOMIC) || '""';
    return [`path(${route}, ${view}, name=${name})`, ORDER_ATOMIC];
}; 