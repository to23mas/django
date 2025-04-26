import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

Blockly.Blocks['django_model_field_param'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([
          ['max_length', 'max_length'],
          ['null', 'null'],
          ['blank', 'blank'],
          ['default', 'default'],
          ['unique', 'unique']
        ]), 'PARAM_TYPE');
    this.appendDummyInput()
        .appendField('=')
        .appendField(new Blockly.FieldTextInput('value'), 'PARAM_VALUE');
    this.setOutput(true, 'String');
    this.setColour(230);
    this.setTooltip('Define parameter for Django model field');
    this.setHelpUrl('');
  }
};

pythonGenerator.forBlock['django_model_field_param'] = function(block) {
  const paramType = block.getFieldValue('PARAM_TYPE');
  const paramValue = block.getFieldValue('PARAM_VALUE');
  return [`${paramType}=${paramValue}`, pythonGenerator.ORDER_NONE];
}; 