import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

// Definice bloku pro User vlastnosti
Blockly.Blocks['django_user_property'] = {
    init: function() {
        this.appendDummyInput()
            .appendField('user.')
            .appendField(new Blockly.FieldDropdown([
                ['id', 'id'],
                ['username', 'username'],
                ['email', 'email'],
                ['is_active', 'is_active'],
                ['is_staff', 'is_staff'],
                ['is_superuser', 'is_superuser'],
                ['date_joined', 'date_joined'],
                ['first_name', 'first_name'],
                ['last_name', 'last_name']
            ]), 'PROPERTY');
        this.setOutput(true, null);
        this.setColour(230);
        this.setTooltip('Získá vlastnost uživatele');
        this.setHelpUrl('');
    }
};

// Generator pro Python kód pro User vlastnosti
pythonGenerator.forBlock['django_user_property'] = function(block) {
    const property = block.getFieldValue('PROPERTY');
    return [`user.${property}`, 0];
};