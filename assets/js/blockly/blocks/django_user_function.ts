import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

// Definice bloku pro funkci s user parametrem
Blockly.Blocks['django_user_function'] = {
    init: function() {
        this.appendDummyInput()
            .appendField('def')
            .appendField(new Blockly.FieldTextInput('my_function'), 'FUNCTION_NAME');
        this.appendDummyInput()
            .appendField('(user):');
        this.appendValueInput('RETURN')
            .setCheck(null)
            .appendField('return');
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip('Vytvoří funkci s parametrem user');
        this.setHelpUrl('');
    }
};

// Generator pro Python kód pro funkci s user parametrem
pythonGenerator.forBlock['django_user_function'] = function(block) {
    const functionName = block.getFieldValue('FUNCTION_NAME');
    const returnValue = pythonGenerator.valueToCode(block, 'RETURN', 0) || 'None';
    
    const code = `def ${functionName}(user):\n    return ${returnValue}\n`;
    return code;
};