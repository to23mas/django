import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

// Definice bloku pro porovnání User vlastností
Blockly.Blocks['django_user_compare'] = {
    init: function() {
        this.appendDummyInput()
            .appendField('user.')
            .appendField(new Blockly.FieldDropdown([
                ['username', 'username'],
                ['email', 'email'],
                ['first_name', 'first_name'],
                ['last_name', 'last_name']
            ]), 'PROPERTY')
            .appendField(' == ')
            .appendField(new Blockly.FieldTextInput(''), 'VALUE');

        this.setOutput(true, 'Boolean');
        this.setColour(230);
        this.setTooltip('Porovná vlastnost uživatele s hodnotou');
        this.setHelpUrl('');
    }
};

// Generator pro Python kód pro porovnání User vlastností
pythonGenerator.forBlock['django_user_compare'] = function(block) {
    const property = block.getFieldValue('PROPERTY');
    const value = block.getFieldValue('VALUE');
    return [`user.${property} == "${value}"`, 0];
};