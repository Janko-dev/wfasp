
cd "$(dirname "$0")"

# python src/rule_generator.py src/input.json

python wfc_singleshot_control.py wfc_singleshot.lp simple_rules.lp
