
cd "$(dirname "$0")"

# python src/rule_generator.py src/input.json

python wfc_multishot_control.py wfc_multishot.lp simple_rules.lp
