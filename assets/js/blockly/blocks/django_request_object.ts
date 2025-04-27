import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

Blockly.Blocks['django_request_object'] = {
    init: function() {
        this.appendDummyInput()
            .appendField('request.')
            .appendField(new Blockly.FieldDropdown([
                ['user', 'user'],
                ['method', 'method'],
                ['session', 'session'],
                ['FILES', 'FILES'],
                ['COOKIES', 'COOKIES'],
                ['path', 'path'],
                ['headers', 'headers']
            ]), 'PROPERTY');
        
        this.setOutput(true, null);
        this.setColour(230);
        this.setTooltip('Django request object properties');
    }
};

pythonGenerator.forBlock['django_request_object'] = function(block) {
    const property = block.getFieldValue('PROPERTY');
    const code = `request.${property}`;
    return [code, pythonGenerator.ORDER_MEMBER];
};
