import * as Blockly from 'blockly';
import { pythonGenerator } from 'blockly/python';

Blockly.Blocks['django_os_environ_get'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('os.environ.get(');
    this.appendValueInput('KEY')
        .setCheck('String')
        .appendField('key');
    this.appendDummyInput()
        .appendField(',');
    this.appendValueInput('DEFAULT')
        .setCheck(['String', 'Number'])
        .appendField('default');
    this.appendDummyInput()
        .appendField(')');
    this.setOutput(true, 'String');
    this.setColour(230);
    this.setTooltip('Get environment variable with default value');
    this.setHelpUrl('');
  }
};

pythonGenerator.forBlock['django_os_environ_get'] = function(block) {
  const key = pythonGenerator.valueToCode(block, 'KEY', pythonGenerator.ORDER_NONE) || '""';
  const defaultValue = pythonGenerator.valueToCode(block, 'DEFAULT', pythonGenerator.ORDER_NONE) || '""';
  return [`os.environ.get(${key}, ${defaultValue})`, pythonGenerator.ORDER_FUNCTION_CALL];
}; 