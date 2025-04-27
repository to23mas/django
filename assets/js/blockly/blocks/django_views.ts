import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

const ORDER_ATOMIC = 0;

Blockly.Blocks['django_views'] = {
    init: function() {
        this.appendDummyInput()
            .appendField('views.')
            .appendField(new Blockly.FieldDropdown([
                ['room', 'room'],
                ['home', 'home'],
                ['index', 'index'],
                ['login', 'login'],
                ['register', 'register'],
                ['profile', 'profile'],
                ['logout', 'logout']
            ]), 'VIEW_NAME');
        this.setOutput(true, 'Function');
        this.setColour(230);
        this.setTooltip('Select a Django view function');
        this.setHelpUrl('');
    }
};

pythonGenerator.forBlock['django_views'] = function(block) {
    const viewName = block.getFieldValue('VIEW_NAME');
    return [`views.${viewName}`, ORDER_ATOMIC];
}; 