import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

Blockly.Blocks['django_model_field'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([
          ['CharField', 'CharField'],
          ['TextField', 'TextField'],
          ['IntegerField', 'IntegerField'],
          ['FloatField', 'FloatField'],
          ['BooleanField', 'BooleanField'],
          ['DateField', 'DateField'],
          ['EmailField', 'EmailField'],
          ['URLField', 'URLField'],
          ['ForeignKey', 'ForeignKey']
        ]), 'FIELD_TYPE');
    this.appendDummyInput()
        .appendField('name =')
        .appendField(new Blockly.FieldTextInput('field_name'), 'FIELD_NAME');
    this.appendValueInput('PARAMS')
        .setCheck('String')
        .appendField('params');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('Define a Django model field');
    this.setHelpUrl('');
  }
};

pythonGenerator.forBlock['django_model_field'] = function(block) {
  const fieldType = block.getFieldValue('FIELD_TYPE');
  const fieldName = block.getFieldValue('FIELD_NAME');
  const params = pythonGenerator.valueToCode(block, 'PARAMS', pythonGenerator.ORDER_NONE) || '';
  
  return `${fieldName} = models.${fieldType}(${params})\n`;
}; 