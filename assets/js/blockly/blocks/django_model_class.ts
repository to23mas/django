import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

Blockly.Blocks['django_model_class'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('class')
        .appendField(new Blockly.FieldTextInput('ModelName'), 'CLASS_NAME')
        .appendField('(models.Model)');
    this.appendStatementInput('FIELDS')
        .setCheck(null)
        .appendField('fields');
    this.setColour(230);
    this.setTooltip('Define a Django model class');
    this.setHelpUrl('');
  }
};

pythonGenerator.forBlock['django_model_class'] = function(block) {
  const className = block.getFieldValue('CLASS_NAME');
  const fields = pythonGenerator.statementToCode(block, 'FIELDS');
  return `class ${className}(models.Model):\n${fields}`;
};