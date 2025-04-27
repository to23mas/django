import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

// Definition of the function block with request parameter
Blockly.Blocks['django_custom_function'] = {
    init: function() {
        this.appendDummyInput()
            .appendField('def')
            .appendField(new Blockly.FieldTextInput('my_function'), 'FUNCTION_NAME');
        this.appendDummyInput()
            .appendField('(request):');
        this.appendStatementInput('FUNCTION_BODY')
            .setCheck(null);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(230);
        this.setTooltip('Vytvoří funkci s parametrem request');
        this.setHelpUrl('');
    }
};

// Python code generator for the function block
pythonGenerator.forBlock['django_custom_function'] = function(block) {
    const functionName = block.getFieldValue('FUNCTION_NAME');
    const functionBody = pythonGenerator.statementToCode(block, 'FUNCTION_BODY') || '    pass\n';
    
    const code = `def ${functionName}(request):\n${functionBody}`;
    return code;
};
