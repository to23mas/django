import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

Blockly.Blocks['django_return'] = {
    init: function() {
        this.appendValueInput('VALUE')
            .setCheck(null)
            .appendField('return');
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip('Return statement for Django functions');
        this.setHelpUrl('');
    }
};

pythonGenerator.forBlock['django_return'] = function(block) {
    const value = pythonGenerator.valueToCode(block, 'VALUE', pythonGenerator.ORDER_NONE) || 'None';
    return `return ${value}\n`;
};