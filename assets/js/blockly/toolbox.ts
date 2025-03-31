export const toolbox = 
{
    "kind": "categoryToolbox",
    "contents": [
      {
        "kind": "category",
        "name": "Funkce",
        "colour": "%{BKY_PROCEDURES_HUE}",
        "contents": [
          {
            "kind": "block",
            "type": "procedures_defreturn"
          }
        ]
      },
      {
        "kind": "category",
        "name": "Matematika",
        "colour": "%{BKY_MATH_HUE}",
        "contents": [
          {
            "kind": "block",
            "type": "math_arithmetic",
            "fields": {
              "OP": "ADD"
            }
          },
          {
            "kind": "block",
            "type": "math_number",
            "fields": {
              "NUM": 0
            }
          }
        ]
      },
      {
        "kind": "category",
        "name": "Proměnné",
        "colour": "%{BKY_VARIABLES_HUE}",
        "contents": [
          {
            "kind": "block",
            "type": "variables_get"
          },
          {
            "kind": "block",
            "type": "variables_set"
          }
        ]
      },
      {
        "kind": "category",
        "name": "Podmínky",
        "colour": "%{BKY_LOGIC_HUE}",
        "contents": [
          {
            "kind": "block",
            "type": "controls_if"
          }
        ]
      },
      {
        "kind": "category",
        "name": "Text",
        "colour": "%{BKY_TEXTS_HUE}",
        "contents": [
          {
            "kind": "block",
            "type": "text"
          },
          {
            "kind": "block",
            "type": "text_print"
          }
        ]
      },
      {
        "kind": "category",
        "name": "Seznamy",
        "colour": "%{BKY_LISTS_HUE}",
        "contents": [
          {
            "kind": "block",
            "type": "lists_create_with"
          }
        ]
      },
      {
        "kind": "category",
        "name": "Předdefinované funkce",
        "colour": "%{BKY_PROCEDURES_HUE}",
        "contents": [
          {
            "kind": "block",
            "type": "django_include_block"
          },
          {
            "kind": "block",
            "type": "django_path_block"
          }
        ]
      }
    ]
};