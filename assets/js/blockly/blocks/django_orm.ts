import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

// Definice bloku pro Post.objects.get()
Blockly.Blocks['django_post_get'] = {
    init: function() {
        this.appendDummyInput()
            .appendField('Post')
            .appendField(new Blockly.FieldDropdown([
                ['objects', 'objects'],
                ['DoesNotExist', 'DoesNotExist'],
                ['MultipleObjectsReturned', 'MultipleObjectsReturned']
            ]), 'PROPERTY')
            .appendField(new Blockly.FieldDropdown([
                ['filter', 'filter'],
                ['get', 'get'],
                ['all', 'all']
            ]), 'METHOD');
        this.appendValueInput('VALUE')
            .setCheck('Number')
            .appendField(new Blockly.FieldDropdown([
                ['title', 'title'],
                ['content', 'content'],
                ['id', 'id'],
                ['author', 'author'],
                ['created_at', 'created_at']
            ]), 'FIELD')
            .appendField('=');
        this.setOutput(true, null);
        this.setColour(230);
        this.setTooltip('Získá Post objekt podle zvoleného pole');
        this.setHelpUrl('');
    }
};

// Generator pro Python kód
pythonGenerator.forBlock['django_post_get'] = function(block: any) {
    const property = block.getFieldValue('PROPERTY');
    const method = block.getFieldValue('METHOD');
    const field = block.getFieldValue('FIELD');
    const value = pythonGenerator.valueToCode(block, 'VALUE', 0) || '0';
    
    if (property === 'objects') {
        if (method === 'get') {
            return [`Post.objects.get(${field}=${value})`, 0];
        } else if (method === 'filter') {
            return [`Post.objects.filter(${field}=${value})`, 0];
        } else {
            return ['Post.objects.all()', 0];
        }
    } else {
        return [`Post.${property}`, 0];
    }
};

// Blok pro číslo (ID)
Blockly.Blocks['number_input'] = {
    init: function() {
        this.appendDummyInput()
            .appendField(new Blockly.FieldNumber(0), 'NUMBER');
        this.setOutput(true, 'Number');
        this.setColour(230);
        this.setTooltip('Číslo pro ID');
        this.setHelpUrl('');
    }
};

pythonGenerator.forBlock['number_input'] = function(block: any) {
    const number = block.getFieldValue('NUMBER');
    return [number.toString(), 0];
}; 